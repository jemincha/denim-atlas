import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.audit_regional_sources import audit
from scripts.regional_supervision import checksum, import_preferences, validate_packet


def fixture():
    observations, cases = [], []
    for index in range(5):
        split = 'train' if index < 3 else 'development'
        ids = [str(index * 3 + k) for k in range(3)]
        for key in ids:
            region = {'file': key + '.png', 'sha256': key, 'box_xyxy': [0, 0, 2, 3], 'size': [2, 3]}
            observations.append({'id': key, 'split': split, 'source_group': key,
                                 'pixel_sha256': key, 'source_sha256': key,
                                 'source': {'file': key + '.png', 'sha256': key, 'size': [2, 3]},
                                 'regions': {'garment': region.copy(), 'hip_thigh': region.copy()}})
        cases.append({'id': str(index), 'split': split, 'reference': ids[0],
                      'candidates': {'A': ids[1], 'B': ids[2]}})
    packet = {'schema_version': 1, 'purpose': 'machine_axis_development',
              'reserved_ids': [], 'observations': observations, 'cases': cases,
              'rubric_version': 'fixture', 'rubric_sha256': 'fixture-hash'}
    packet['packet_sha256'] = checksum(packet)
    export = {'schema_version': 1, 'packet_sha256': packet['packet_sha256'],
              'label_source': 'machine_visual', 'teacher': {'runtime': 'engineering fixture',
              'rubric_version': 'fixture', 'rubric_sha256': 'fixture-hash',
              'exact_checkpoint': None, 'checkpoint_limit': 'Synthetic fixture'}, 'ratings': [
                  {'case_id': c['id'], 'axis': axis, 'choice': 'A', 'useful_match': True,
                   'confidence': 'medium', 'reason': 'Fixture visible evidence'}
                  for c in cases for axis in ('silhouette', 'surface')]}
    return packet, export


def resign(packet, export):
    packet.pop('packet_sha256')
    packet['packet_sha256'] = checksum(packet)
    export['packet_sha256'] = packet['packet_sha256']


class RegionalTests(unittest.TestCase):
    def test_separate_machine_constraints_and_no_quality_claim(self):
        packet, export = fixture()
        export['ratings'][1]['choice'] = 'B'
        result = import_preferences(packet, export)
        self.assertTrue(result['ready_for_pilot'])
        self.assertFalse(result['independent_quality_evidence'])
        self.assertEqual([r['target'] for r in result['constraints'][:2]], ['A', 'B'])
        self.assertNotIn('grade', result['constraints'][0])

    def test_neither_unknown_low_and_tie_have_distinct_meaning(self):
        packet, export = fixture()
        for row, choice, useful, confidence in zip(export['ratings'],
                ['neither', 'unknown', 'A', 'tie'], [False, None, True, True],
                ['high', 'low', 'low', 'medium']):
            row.update(choice=choice, useful_match=useful, confidence=confidence)
        result = import_preferences(packet, export)
        self.assertEqual(len(result['constraints']), 7)
        self.assertEqual(result['constraints'][0]['target'], 'tie')
        self.assertEqual(len(result['decisions']), 10)
        self.assertFalse(result['ready_for_pilot'])

    def test_provenance_tampering_rejected(self):
        packet, export = fixture()
        packet['reserved_ids'] = ['missing']
        with self.assertRaisesRegex(ValueError, 'checksum'):
            import_preferences(packet, export)
        packet, export = fixture()
        export['label_source'] = 'human'
        with self.assertRaisesRegex(ValueError, 'provenance'):
            import_preferences(packet, export)
        packet, export = fixture()
        export['teacher']['rubric_sha256'] = 'another rubric'
        with self.assertRaisesRegex(ValueError, 'rubric'):
            import_preferences(packet, export)

    def test_leakage_and_reserved_observations_rejected(self):
        for field in ('source_group', 'pixel_sha256', 'source_sha256'):
            packet, export = fixture()
            packet['observations'][-1][field] = packet['observations'][0][field]
            resign(packet, export)
            with self.subTest(field=field), self.assertRaises(ValueError):
                import_preferences(packet, export)
        packet, export = fixture()
        packet['reserved_ids'] = ['0']
        resign(packet, export)
        with self.assertRaisesRegex(ValueError, 'reserved'):
            import_preferences(packet, export)

    def test_case_cannot_cross_split_or_repeat_source(self):
        for candidate in ('9', '0'):
            packet, export = fixture()
            packet['cases'][0]['candidates']['A'] = candidate
            resign(packet, export)
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                import_preferences(packet, export)

    def test_malformed_missing_or_duplicate_axis_rejected(self):
        for kind in ('missing', 'duplicate', 'axis', 'choice', 'confidence', 'acceptance'):
            packet, export = fixture()
            if kind == 'missing':
                export['ratings'].pop()
            elif kind == 'duplicate':
                export['ratings'].append(copy.deepcopy(export['ratings'][0]))
            else:
                field, value = {'axis': ('axis', 'joint'), 'choice': ('choice', 3),
                                'confidence': ('confidence', .99),
                                'acceptance': ('useful_match', 1)}[kind]
                export['ratings'][0][field] = value
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                import_preferences(packet, export)

    def test_unsafe_paths_and_invalid_geometry_rejected(self):
        for kind in ('escape', 'absolute', 'box', 'size'):
            packet, export = fixture()
            region = packet['observations'][0]['regions']['garment']
            if kind in ('escape', 'absolute'):
                region['file'] = '../outside.png' if kind == 'escape' else 'C:/outside.png'
            elif kind == 'box':
                region['box_xyxy'][2] = 3
            else:
                region['size'] = [1, 3]
            resign(packet, export)
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                import_preferences(packet, export)

    def test_repeated_anchor_does_not_inflate_readiness(self):
        packet, export = fixture()
        packet['cases'][2]['reference'] = packet['cases'][0]['reference']
        resign(packet, export)
        result = import_preferences(packet, export)
        self.assertEqual(result['strict_counts']['train']['surface'], 2)
        self.assertFalse(result['ready_for_pilot'])

    def test_changed_asset_is_rejected_even_if_manifest_is_resigned(self):
        packet, export = fixture()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for row in packet['observations']:
                file = root / row['source']['file']
                Image.new('RGB', (2, 3), (int(row['id']), 0, 0)).save(file)
                digest = hashlib.sha256(file.read_bytes()).hexdigest()
                row['source_sha256'] = row['source']['sha256'] = digest
                row['pixel_sha256'] = hashlib.sha256(Image.open(file).convert('RGB').tobytes()).hexdigest()
                for region in row['regions'].values():
                    region['sha256'] = digest
            resign(packet, export)
            validate_packet(packet, root)
            wrong = root / 'wrong.png'
            Image.new('RGB', (2, 3), 'white').save(wrong)
            region = packet['observations'][0]['regions']['garment']
            original = region.copy()
            region.update(file='wrong.png', sha256=hashlib.sha256(wrong.read_bytes()).hexdigest())
            resign(packet, export)
            with self.assertRaisesRegex(ValueError, 'recorded source crop'):
                validate_packet(packet, root)
            region.update(original)
            resign(packet, export)
            (root / '0.png').write_bytes(b'corrupted')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                validate_packet(packet, root)


class SourceAuditTests(unittest.TestCase):
    def test_audit_checks_reviewed_bytes_and_resolution(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'images').mkdir()
            file = root / 'images/1.jpg'
            Image.new('RGB', (10, 8), 'blue').save(file)
            row = {'image_id': '1', 'file': 'images/1.jpg',
                   'sha256': hashlib.sha256(file.read_bytes()).hexdigest()}
            (root / 'screening_images.jsonl').write_text(json.dumps(row))
            (root / 'jeans_rows.jsonl').write_text(json.dumps({'image_id': '1'}))
            self.assertEqual(audit(root, [row])['reviewed_source_sizes'], {'10x8': 1})
            row['sha256'] = 'wrong'
            with self.assertRaisesRegex(ValueError, 'checksum'):
                audit(root, [row])


if __name__ == '__main__':
    unittest.main()
