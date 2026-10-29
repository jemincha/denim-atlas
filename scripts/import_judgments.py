"""Validate private calibration exports without promoting them to benchmark labels."""

import argparse
import hashlib
import json
from pathlib import Path


def import_ratings(packet, export):
    unsigned = {k:v for k,v in packet.items() if k != 'packet_sha256'}
    digest = hashlib.sha256(json.dumps(unsigned, sort_keys=True, ensure_ascii=False,
                                     separators=(',',':')).encode()).hexdigest()
    if packet.get('packet_sha256') != digest:
        raise ValueError('Packet checksum mismatch')
    for key in ('packet_id', 'packet_sha256', 'rater_id', 'purpose', 'schema_version'):
        if export.get(key) != packet.get(key):
            raise ValueError('Export provenance mismatch: '+key)
    if packet['purpose'] != 'calibration_only':
        raise ValueError('Only calibration packets supported')
    if packet['schema_version'] == 2:
        return import_axis_ratings(packet, export, digest)
    if packet['schema_version'] != 1:
        raise ValueError('Unsupported judgment schema')
    trials = {t['trial_id']:t for t in packet['trials']}
    answers = {}
    reasons = {'','silhouette_unobservable','occlusion_or_crop',
               'color_or_detail_uncertain','target_ambiguous'}
    for row in export['ratings']:
        tid, grade = row['trial_id'], row['grade']
        if tid not in trials or tid in answers:
            raise ValueError('Unknown or duplicate trial ID')
        if not (type(grade) is int and 0 <= grade <= 3 or grade == 'U'):
            raise ValueError('Expected integer 0..3 or U')
        if row.get('reason','') not in reasons:
            raise ValueError('Unknown observation reason')
        answers[tid] = row
    return dict(schema_version=1, purpose='calibration_only', packet_sha256=digest,
                rater_id=packet['rater_id'], research_split=None,
                **summarize_answers(packet, answers))


def summarize_answers(packet, answers):
    trials = {t['trial_id']:t for t in packet['trials']}
    pairs = {}
    for tid, row in answers.items():
        t = trials[tid]
        pairs.setdefault((t['query'],t['candidate']),[]).append(row)
    judged, conflicts, repeated = [], [], []
    for (qi,ci), rows in pairs.items():
        grades = [r['grade'] for r in rows]
        pair = {'query_id':packet['queries'][qi]['id'],
                'candidate_id':packet['candidates'][ci]['id']}
        if len(rows) > 1:
            repeated.append(dict(pair, grades=grades, exact_agreement=len(set(grades)) == 1))
        if len(set(grades)) > 1:
            conflicts.append(dict(pair, grades=grades))
        elif grades[0] != 'U':
            judged.append(dict(pair, grade=grades[0]))
    return {'answered_trials':len(answers), 'missing_trials':len(trials)-len(answers),
            'uncertain_trials':sum(r['grade']=='U' for r in answers.values()),
            'repeat_checks':repeated, 'conflicts_requiring_review':conflicts,
            'judged_unique_pairs':judged}


def import_axis_ratings(packet, export, digest):
    axes = ['silhouette', 'surface']
    if packet.get('comparison_axes') != axes or export.get('comparison_axes') != axes:
        raise ValueError('Comparison-axis provenance mismatch')
    trials = {t['trial_id'] for t in packet['trials']}
    answers = {axis:{} for axis in axes}
    seen = set()
    complete = 0
    for row in export['ratings']:
        tid, scores = row.get('trial_id'), row.get('scores')
        if tid not in trials or tid in seen:
            raise ValueError('Unknown or duplicate trial ID')
        if (set(row) != {'trial_id', 'scores'} or not isinstance(scores, dict)
                or not scores or not set(scores) <= set(axes)):
            raise ValueError('Expected separate axis scores, never a joint grade')
        seen.add(tid)
        complete += len(scores) == len(axes)
        for axis, score in scores.items():
            if not isinstance(score, dict) or not {'grade'} <= set(score) <= {'grade', 'reason'}:
                raise ValueError('Expected a grade and optional reason per axis')
            grade = score['grade']
            if not (type(grade) is int and 0 <= grade <= 3 or grade == 'U'):
                raise ValueError('Expected integer 0..3 or U per axis')
            reasons = {'', 'occlusion_or_crop', 'target_ambiguous'}
            reasons.add('silhouette_unobservable' if axis == 'silhouette' else 'color_or_detail_uncertain')
            if not isinstance(score.get('reason', ''), str) or score.get('reason', '') not in reasons:
                raise ValueError('Unknown or wrong-axis observation reason')
            answers[axis][tid] = score
    return {'schema_version':2, 'purpose':'calibration_only', 'packet_sha256':digest,
            'rater_id':packet['rater_id'], 'research_split':None, 'comparison_axes':axes,
            'answered_trials':len(seen), 'complete_trials':complete,
            'axis_results':{axis:summarize_answers(packet, answers[axis]) for axis in axes}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--ratings', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = import_ratings(json.loads(args.packet.read_text(encoding='utf-8')),
                            json.loads(args.ratings.read_text(encoding='utf-8')))
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    counts = ({axis:len(values['judged_unique_pairs']) for axis,values in result['axis_results'].items()}
              if result['schema_version'] == 2 else len(result['judged_unique_pairs']))
    print('Imported calibration judgments:',counts)
