"""Audit explicit catalog-cut proxies; no observed-color or wash labels are invented."""

import argparse
from collections import Counter, defaultdict
import hashlib
import html
import json
from pathlib import Path
import random
import re


PATTERNS = {'skinny':r'\bskinny\b', 'slim':r'\bslim\b',
            'straight':r'\bstraight\b', 'wide':r'\bwide[\s-]+(?:leg|fit)\b',
            'flared':r'\bflar(?:e|ed)\b'}


def title_fit(title):
    title = html.unescape(title).casefold()
    if re.search(r'\b(?:not|non|no)[\s-]+(?:skinny|slim|straight|wide|flared?)\b',title):
        return None
    found = [label for label,pattern in PATTERNS.items() if re.search(pattern,title)]
    return found[0] if len(found) == 1 else None


def family(title):
    title = ' '.join(html.unescape(title).casefold().split())
    # Group known color variants conservatively; this does not label photographed color.
    return re.sub(r'\s+-\s+(?:blue|black|grey|gray|white|mavi|siyah|lacivert|beyaz)$','',title)


def group_split(rows):
    """Keep known item/pixel/title-family links together; unresolved identities stay explicit."""
    parents = list(range(len(rows)))
    def find(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]; i = parents[i]
        return i
    owners = {}
    for i,row in enumerate(rows):
        keys = [('item',k) for k in row['item_ids']]
        keys += [('pixels',row['pixel_sha256']),('title',family(row['title']))]
        for key in keys:
            if key in owners: parents[find(i)] = find(owners[key])
            else: owners[key] = i
    grouped = defaultdict(list)
    for i,row in enumerate(rows): grouped[find(i)].append(row)
    by_label = defaultdict(list); conflicts = []
    for members in grouped.values():
        if len({r['source_fit'] for r in members}) != 1:
            conflicts.extend(r['image_id'] for r in members); continue
        group = hashlib.sha256('|'.join(sorted(r['image_id'] for r in members)).encode()).hexdigest()
        for row in members: row['source_group'] = group
        by_label[members[0]['source_fit']].append(members)
    rng = random.Random(17)
    selected = []
    for label,groups in sorted(by_label.items()):
        groups.sort(key=lambda g:g[0]['source_group']); rng.shuffle(groups)
        if len(groups) < 6: raise ValueError('Insufficient source groups for '+label)
        validation = max(2,round(len(groups)*0.25))
        for i,members in enumerate(groups):
            for row in members:
                row['proxy_split'] = 'validation' if i < validation else 'train'
                selected.append(row)
    return sorted(selected,key=lambda r:r['image_id']),sorted(conflicts)


def lock_validation(rows, anchor_rows):
    anchor = {r['image_id']:r['proxy_split'] for r in anchor_rows}
    if not set(anchor).issubset(r['image_id'] for r in rows):
        raise ValueError('Expansion lost a fixed anchor image')
    grouped = defaultdict(list)
    for row in rows: grouped[row['source_group']].append(row)
    selected, reserved = [], []
    for members in grouped.values():
        folds = {anchor[r['image_id']] for r in members if r['image_id'] in anchor}
        if len(folds)>1: raise ValueError('Expanded source group crosses fixed anchor folds')
        fold = 'validation' if folds=={'validation'} else 'train'
        for row in members:
            if fold=='validation' and row['image_id'] not in anchor:
                reserved.append(row['image_id']); continue
            row['proxy_split']=fold;selected.append(row)
    return sorted(selected,key=lambda r:r['image_id']),sorted(reserved)


def prepare(root, examples_path, anchor_path=None):
    examples_raw = examples_path.read_bytes()
    examples = json.loads(examples_raw)
    if not isinstance(examples,list) or len({r['image_id'] for r in examples}) != len(examples):
        raise ValueError('Expected unique previously visually screened examples')
    records = defaultdict(list)
    for line in (root/'jeans_rows.jsonl').read_text(encoding='utf-8').splitlines():
        row = json.loads(line); records[row['image_id']].append(row)
    rows, unknown = [], []
    for example in sorted(examples,key=lambda r:r['image_id']):
        identity = example['image_id']
        if not isinstance(identity,str) or not identity.isdecimal() or identity not in records:
            raise ValueError('Missing or invalid source ID')
        source = records[identity]
        labels = {title_fit(r.get('name','')) for r in source} - {None}
        if len(labels) != 1: unknown.append(identity); continue
        label = next(iter(labels))
        row = next(r for r in source if title_fit(r.get('name','')) == label)
        rows.append({'image_id':identity,'sha256':example['sha256'],
            'pixel_sha256':example['pixel_sha256'],'item_ids':example['item_ids'],
            'title':row['name'],'source_fit':label,'market_geo':row.get('geo'),
            'label_source':'explicit source title; weak catalog-cut proxy',
            'observed_color':None,'wash':None,'research_split':None})
    selected, conflicts = group_split(rows)
    reserved = []
    if anchor_path:
        selected,reserved = lock_validation(selected,json.loads(anchor_path.read_bytes())['examples'])
    summary = {'schema_version':1,'visually_screened_examples':len(examples),
        'explicit_fit_examples':len(rows),'unknown_or_ambiguous_title_examples':len(unknown),
        'group_conflict_exclusions':len(conflicts),'selected_examples':len(selected),
        'validation_linked_reserve_examples':len(reserved),
        'validation_anchor_sha256':hashlib.sha256(anchor_path.read_bytes()).hexdigest() if anchor_path else None,
        'label_counts':dict(Counter(r['source_fit'] for r in selected)),
        'split_counts':{split:dict(Counter(r['source_fit'] for r in selected if r['proxy_split']==split))
                        for split in ['train','validation']},
        'known_source_groups':len({r['source_group'] for r in selected}),
        'market_geo_counts':dict(Counter(r['market_geo'] for r in selected)),
        'structured_observed_color_labels':0,'structured_wash_labels':0,
        'seed':17,'split_unit':'linked known item, exact decoded pixels, normalized title family',
        'independent_product_groups_verified':False,
        'source_summary_sha256':hashlib.sha256((root/'summary.json').read_bytes()).hexdigest(),
        'source_examples_sha256':hashlib.sha256(examples_raw).hexdigest(),
        'limits':'Catalog words are noisy proxies, not human silhouette labels or overall relevance. Source groups are conservative metadata links, not verified product identities. No pristine test set. Color and wash remain unknown.'}
    return {'schema_version':1,'purpose':'weak_source_fit_proxy','examples':selected,
            'unknown_ids':unknown,'group_conflict_ids':conflicts,'validation_linked_reserve_ids':reserved,'summary':summary}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root',type=Path,required=True)
    parser.add_argument('--examples',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--validation-anchor',type=Path,help='Keep the exact prior validation images; reserve linked new images')
    args = parser.parse_args()
    data = prepare(args.input_root,args.examples,args.validation_anchor)
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'fit_manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (args.output/'summary.json').write_text(json.dumps(data['summary'],indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data['summary'],indent=2))
