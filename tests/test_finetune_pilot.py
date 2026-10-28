import unittest
import tempfile
from pathlib import Path
import json
import hashlib

from scripts.build_judgment_packet import packet
from scripts.finetune_denim_pilot import training_triplets, initial_checkpoint
from scripts.extract_features import REVISION, WEIGHT_SHA256
from tests.test_judgment_packet import asset


class TrainingPairsTests(unittest.TestCase):
    def test_initial_checkpoint_requires_pinned_base_and_file_checksum(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root=Path(directory);raw=b'checkpoint fixture'
            (root/'last_block.pt').write_bytes(raw)
            report={'base_revision':REVISION,'base_weights_sha256':WEIGHT_SHA256,
                    'checkpoint_sha256':hashlib.sha256(raw).hexdigest()}
            (root/'training_report.json').write_text(json.dumps(report))
            path,received=initial_checkpoint(root)
            self.assertEqual(path,root/'last_block.pt');self.assertEqual(received,report)
            report['base_revision']='untrusted revision'
            (root/'training_report.json').write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError,'provenance'):initial_checkpoint(root)
            report['base_revision']=REVISION
            (root/'training_report.json').write_text(json.dumps(report))
            (root/'last_block.pt').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'provenance'):initial_checkpoint(root)

    def test_clear_pairs_only_and_conflicts_excluded(self):
        p=packet([asset('q')],[asset('a'),asset('b'),asset('c')])
        r={k:p[k] for k in ('schema_version','packet_id','packet_sha256','rater_id','purpose')}
        r['ratings']=[{'trial_id':t['trial_id'],'grade':{'a':2,'b':0,'c':1}[p['candidates'][t['candidate']]['id']]} for t in p['trials']]
        self.assertEqual(training_triplets(p,r),[('q','a','b')])
        repeated=next(t for t in p['trials'] if t['repeat'])
        next(x for x in r['ratings'] if x['trial_id']==repeated['trial_id'])['grade']='U'
        identity=p['candidates'][repeated['candidate']]['id']
        if identity in {'a','b'}:
            with self.assertRaises(ValueError):training_triplets(p,r)
        else:self.assertEqual(training_triplets(p,r),[('q','a','b')])
        r['packet_sha256']='bad'
        with self.assertRaises(ValueError):training_triplets(p,r)
