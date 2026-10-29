"""Inventory weak source tags and machine attribute drafts; never certify training labels."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

try:
    from .annotate_denim_appearance import ENUMS
    from .evaluate import unique_object
    from .prepare_glami_fit import title_fit
except ImportError:
    from annotate_denim_appearance import ENUMS
    from evaluate import unique_object
    from prepare_glami_fit import title_fit


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
