import unittest

from scripts.build_judgment_packet import packet
from scripts.finetune_denim_pilot import training_triplets
from tests.test_judgment_packet import asset


class TrainingPairsTests(unittest.TestCase):
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
