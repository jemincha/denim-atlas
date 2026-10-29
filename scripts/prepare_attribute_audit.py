"""Inventory weak source tags and machine attribute drafts; never certify training labels."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random

try:
    from .annotate_denim_appearance import ENUMS
    from .evaluate import unique_object
    from .prepare_glami_fit import title_fit, family
except ImportError:
    from annotate_denim_appearance import ENUMS
    from evaluate import unique_object
    from prepare_glami_fit import title_fit, family


def select_expansion(examples, source_rows, protected_ids, seen_ids, count=96, seed=131):
    """Select reviewed, linked-group-protected observations; strata are not target labels."""
    if type(count) is not int or count < 1:
        raise ValueError('Positive integer sample count required')
    parents, owners, names = {}, {}, defaultdict(list)
    def find(identity):
        parents.setdefault(identity, identity)
        while parents[identity] != identity:
            parents[identity] = parents[parents[identity]]
            identity = parents[identity]
        return identity
    def link(identity, key):
        current = find(identity)
        if key in owners:
            parents[current] = find(owners[key])
        else:
            owners[key] = identity
    for row in source_rows:
        identity = 'glami:' + row['image_id']
        find(identity)
        names[identity].append(row.get('name', ''))
        if row.get('item_id') not in (None, ''):
            link(identity, ('item', str(row['item_id'])))
        normalized = family(row.get('name', ''))
        if normalized:
            link(identity, ('title', normalized))
    reviewed = {}
    for row in examples:
        identity = 'glami:' + row['image_id']
        if identity in reviewed or identity not in parents or not row['image_id'].isdecimal():
            raise ValueError('Duplicate/invalid reviewed image or missing source metadata')
        reviewed[identity] = row
        link(identity, ('pixels', row['pixel_sha256']))
    blocked = {find(i) for i in set(protected_ids)|set(seen_ids) if i in parents}
    members, candidates = defaultdict(list), defaultdict(list)
    for identity in parents:
        members[find(identity)].append(identity)
    for identity,row in reviewed.items():
        group = find(identity)
        if group not in blocked:
            candidates[group].append(row)
    bins = defaultdict(list)
    for group,rows in candidates.items():
        labels = {title_fit(name) for row in rows
                  for name in names['glami:'+row['image_id']]} - {None}
        stratum = next(iter(labels)) if len(labels) == 1 else 'unclassified'
        group_hash = hashlib.sha256('|'.join(sorted(members[group])).encode()).hexdigest()
        bins[stratum].append((group_hash, sorted(rows,key=lambda r:r['image_id'])))
    if sum(map(len,bins.values())) < count:
        raise ValueError('Insufficient eligible source groups for the requested sample')
    rng = random.Random(seed)
    for stratum in sorted(bins):
        groups = bins[stratum]
        groups.sort(key=lambda x:x[0]);rng.shuffle(groups)
    selected = []
    while len(selected) < count:
        for stratum in sorted(bins):
            if not bins[stratum] or len(selected) == count:
                continue
            group_hash,rows = bins[stratum].pop()
            row = rng.choice(rows)
            selected.append({'id':'glami:'+row['image_id'],'file':row['image_id']+'.jpg',
                'sha256':row['sha256'],'usage_scope':'private_research_reviewed',
                'source_group':group_hash,'sampling_stratum':stratum})
    return {'schema_version':1,'purpose':'bounded_unverified_attribute_expansion',
            'examples':selected,'summary':{'reviewed_images':len(examples),
                'source_metadata_images':len(parents),'selected_images':len(selected),
                'eligible_source_groups':len(candidates),'excluded_reviewed_images':sum(
                    find(i) in blocked for i in reviewed),
                'stratum_counts':dict(Counter(r['sampling_stratum'] for r in selected)),
                'seed':seed,'training_eligible':False,'independent_products_verified':False,
                'limits':'Known item/title/pixel links include supplied unreviewed metadata bridges. '
                         'Strata are weak source tags, not visual labels; unknown is not a negative. '
                         'Protects supplied groups only, not proof of product independence.'}}


def prepare(examples, source_rows, manifest, descriptions):
    records, titles = {}, defaultdict(list)
    for row in source_rows:
        titles[row['image_id']].append(row.get('name', ''))
    for row in examples:
        identity = 'glami:' + row['image_id']
        if identity in records or row['image_id'] not in titles:
            raise ValueError('Duplicate reviewed image or missing source metadata')
        labels = {title_fit(title) for title in titles[row['image_id']]} - {None}
        proposals = {}
        if len(labels) == 1:
            proposals['retail_fit'] = {'value':next(iter(labels)), 'axis':'silhouette',
                                      'source':'source_title', 'status':'weak_proxy'}
        records[identity] = {'id':identity, 'image_sha256':row['sha256'],
                             'proposals':proposals, 'human_verified':False,
                             'training_eligible':False}
    known = {}
    for row in manifest['examples']:
        identity = row['id']
        if identity in known or row.get('usage_scope') != 'private_research_reviewed':
            raise ValueError('Duplicate or unreviewed pilot observation')
        known[identity] = row
        if identity not in records:
            if not identity.startswith('commons:'):
                raise ValueError('Pilot catalog image outside reviewed inventory')
            records[identity] = {'id':identity, 'image_sha256':row['sha256'],
                                 'proposals':{}, 'human_verified':False,
                                 'training_eligible':False}
        if records[identity]['image_sha256'] != row['sha256']:
            raise ValueError('Pilot manifest/image checksum mismatch')
    seen = set()
    for row in descriptions:
        identity = row['id']
        if identity in seen or identity not in known:
            raise ValueError('Duplicate or unknown machine observation')
        seen.add(identity)
        if row['image_sha256'] != known[identity]['sha256']:
            raise ValueError('Machine description/image checksum mismatch')
        value = json.loads(row['raw_response'], object_pairs_hook=unique_object)
        if not isinstance(value, dict) or type(value.get('target_ambiguous')) is not bool:
            raise ValueError('Expected explicit target ambiguity')
        record = records[identity]
        record['original_full_schema_valid'] = row['schema_valid']
        for field in ('color_family', 'lightness', 'observed_tone'):
            raw = value.get(field)
            if not isinstance(raw, str) or raw not in ENUMS[field]:
                raise ValueError('Invalid coarse attribute: ' + field)
            observed = None if value['target_ambiguous'] or raw == 'unknown' else raw
            if field == 'color_family' and observed is not None:
                observed = ('blue' if raw == 'blue' else 'neutral'
                            if raw in {'black', 'gray', 'white'} else 'other')
            record['proposals'][field] = {'value':observed, 'raw_value':raw, 'axis':'surface',
                'source':'image_only_vlm', 'status':'unverified_machine_attribute'}
    if seen != set(known):
        raise ValueError('Missing pilot descriptions')
    counts = Counter(field for r in records.values() for field in r['proposals'])
    return {'schema_version':1, 'purpose':'attribute_label_audit_only',
            'observations':list(records.values()),
            'summary':{'reviewed_catalog_images':len(examples), 'observations':len(records),
                       'proposal_counts':dict(counts), 'human_verified_observations':0,
                       'training_eligible_observations':0,
                       'limits':'Source fit remains retail terminology, not observed geometry. '
                                'Coarse fields are isolated from rejected wash assertions but remain unverified. '
                                'Unknown is not absence; titles never establish photographed color. '
                                'This inventory is not an approved training manifest.'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('examples', 'source-rows', 'manifest', 'descriptions', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    inputs = {name:getattr(args, name).read_bytes()
              for name in ('examples', 'source_rows', 'manifest', 'descriptions')}
    parsed = {name:([json.loads(line, object_pairs_hook=unique_object) for line in raw.splitlines()]
                    if name == 'source_rows' else json.loads(raw, object_pairs_hook=unique_object))
              for name,raw in inputs.items()}
    result = prepare(**parsed)
    result['input_sha256'] = {name:hashlib.sha256(raw).hexdigest() for name,raw in inputs.items()}
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'inventory.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    (args.output/'summary.json').write_text(json.dumps(result['summary'], indent=2), encoding='utf-8')
    print(json.dumps(result['summary']))
