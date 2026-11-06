import unittest
from scripts.evaluate_frozen_human import interval, pool_scores, compare
from scripts.build_judgment_packet import packet
from scripts.extract_features import ENCODERS
from tests.test_judgment_packet import asset


class FrozenHumanTests(unittest.TestCase):
    def test_perfect_reverse_and_model_ties(self):
        best, random, correct, n = pool_scores([3,2,0],[3,2,0])
        self.assertEqual((best,correct,n),(1.,3.,3))
        self.assertLess(pool_scores([3,2,0],[0,2,3])[0],best)
        tied=pool_scores([3,2,0],[0,0,0])
        self.assertAlmostEqual(tied[0],random)
        self.assertEqual(tied[2:],(1.5,3))

    def test_human_ties_zero_gain_and_cluster_ratio(self):
        self.assertEqual(pool_scores([0,0,0],[3,2,1]),(None,None,0.,0))
        self.assertEqual(pool_scores([2,2,1],[3,2,1])[3],2)
        self.assertEqual(interval([1,1],[1,3])[0],.5)
        self.assertEqual(interval([.2]*4),[.2,.2,.2])
        self.assertIsNone(interval([]))
        self.assertIsNone(interval([0],[0]))

    def test_unknown_and_repeat_conflict_exclude_whole_axis_pool(self):
        p=packet([dict(asset('q0'),source_group='g0'),dict(asset('q1'),source_group='g1')],
                 [asset('a'),asset('b'),asset('c')],separate_axes=True,repeat_count=2,evaluation_only=True)
        e={k:p[k] for k in ('schema_version','packet_id','packet_sha256','rater_id','purpose','comparison_axes')}
        e['ratings']=[{'trial_id':t['trial_id'],'scores':{
            'silhouette':{'grade':1 if t['repeat'] and t['query']==1 else 2},
            'surface':{'grade':2}}} for t in p['trials']]
        e['ratings'][0]['scores']['silhouette']={'grade':'U'}
        profile=ENCODERS['fashion-siglip']
        f={'provenance':dict(profile,encoder=profile['model'],training_run=False,manifest_sha256='fixture',
             input_policy='EXIF RGB -> white aspect-preserving 224 square -> official model preprocessing'),
           'assets':{r['id']:{'crop_sha256':r['crop_sha256'],'embedding':[1.]+[0.]*767}
                     for r in p['queries']+p['candidates']}}
        meta={q['id']:{'source_width':'228','source_height':'298','view':'catalog_wearing'} for q in p['queries']}
        result=compare(p,e,{'fashion-siglip':f},meta,'fixture')
        self.assertEqual(result['silhouette']['excluded_anchors'],2)
        self.assertEqual(result['surface']['models']['fashion-siglip']['all']['ndcg'],[1.,1.,1.])
        self.assertFalse(result['surface']['common_gate'])
