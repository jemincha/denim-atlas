import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.analyze_calibration import analyze
from scripts.extract_features import REVISION, WEIGHT_SHA256
from scripts.run_baselines import rank_pools
from tests.test_judgment_packet import asset
from scripts.build_judgment_packet import packet


def fixture():
    p=packet([asset('q')],[asset('a'),asset('b'),asset('c')])
    r={k:p[k] for k in ('schema_version','packet_id','packet_sha256','rater_id','purpose')}
    r['ratings']=[{'trial_id':t['trial_id'],'grade':3 if t['candidate']==0 else 0} for t in p['trials']]
    f={'schema_version':1,'provenance':{'revision':REVISION,'weights_sha256':WEIGHT_SHA256,'training_run':False},
       'assets':{a['id']:{'embedding':[1.,0.]+[0.]*766,'mean_rgb':[0.,0.,0.],
                          'crop_sha256':a['crop_sha256']} for a in p['queries']+p['candidates']}}
    return p,r,f


class CalibrationTests(unittest.TestCase):
    def test_cli_records_inputs_and_preserves_existing_output(self):
        p,r,f=fixture()
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root=Path(directory)
            for name,data in [('packet',p),('ratings',r),('features',f)]:
                (root/(name+'.json')).write_text(json.dumps(data),encoding='utf-8')
            command=[sys.executable,str(Path(__file__).resolve().parents[1]/'scripts/analyze_calibration.py')]
            for name in ('packet','ratings','features'):
                command += ['--'+name,str(root/(name+'.json'))]
            target=root/'result.json';command += ['--output',str(target)]
            result=subprocess.run(command,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            original=target.read_bytes();report=json.loads(original)
            self.assertEqual(set(report['input_sha256']),{'packet','ratings','features'})
            self.assertFalse(report['held_out_evaluation'])
            self.assertNotEqual(subprocess.run(command,capture_output=True).returncode,0)
            self.assertEqual(target.read_bytes(),original)

    def test_complete_then_uncertain_pool_has_no_metric_and_same_ranks(self):
        p,r,f=fixture();before=analyze(p,r,f)
        self.assertEqual(before['results'][0]['calibration_ndcg_at_5'],1.)
        self.assertFalse(before['held_out_evaluation'])
        for row in r['ratings']: row['grade']='U'
        after=analyze(p,r,f)
        self.assertEqual(after['usable_pairs'],0)
        self.assertIsNone(after['results'][0]['calibration_ndcg_at_5'])
        self.assertEqual(before['results'][0]['ranking'],after['results'][0]['ranking'])

    def test_conflicts_hashes_and_frozen_provenance(self):
        p,r,f=fixture()
        repeated=next(t['trial_id'] for t in p['trials'] if t['repeat'])
        next(row for row in r['ratings'] if row['trial_id']==repeated)['grade']=2
        self.assertFalse(analyze(p,r,f)['results'][0]['fully_judged_pool'])
        for path,value in [('crop_sha256','bad'),('embedding',[1.,0.])]:
            broken=copy.deepcopy(f);broken['assets']['q'][path]=value
            with self.assertRaises(ValueError):analyze(p,r,broken)
        f['provenance']['training_run']=True
        with self.assertRaises(ValueError):analyze(p,r,f)
        for pool in ({'q':['q']},{'q':['a','a']},{'q':[]}):
            with self.assertRaises(ValueError):rank_pools(pool,f,.5)
