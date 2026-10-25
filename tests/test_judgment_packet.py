import base64
import hashlib
import unittest

from scripts.build_judgment_packet import packet, build_html
from scripts.import_judgments import import_ratings


def asset(identity):
    raw=b'\x89PNG\r\n\x1a\nfixture'
    return {'id':identity,'data_uri':'data:image/png;base64,'+base64.b64encode(raw).decode(),
            'crop_sha256':hashlib.sha256(raw).hexdigest()}


class PacketTests(unittest.TestCase):
    def test_import_uncertain_repeat_conflict_and_provenance(self):
        data=packet([asset('q')],[asset('a'),asset('b'),asset('c')])
        export={k:data[k] for k in ('schema_version','packet_id','packet_sha256','rater_id','purpose')}
        first=data['trials'][0]
        repeat=next(t for t in data['trials'] if t['repeat'])
        export['ratings']=[{'trial_id':first['trial_id'],'grade':2},
                           {'trial_id':repeat['trial_id'],'grade':3},
                           {'trial_id':data['trials'][1]['trial_id'],'grade':'U'}]
        result=import_ratings(data,export)
        self.assertEqual(result['missing_trials'],1)
        self.assertEqual(result['uncertain_trials'],1)
        self.assertEqual(len(result['conflicts_requiring_review']),1)
        self.assertEqual(result['judged_unique_pairs'],[])
        export['ratings'][1]['grade']=2
        self.assertEqual(len(import_ratings(data,export)['judged_unique_pairs']),1)
        export['ratings'][0]['grade']=True
        with self.assertRaises(ValueError): import_ratings(data,export)
        export['packet_sha256']='wrong'
        with self.assertRaises(ValueError): import_ratings(data,export)

    def test_fixed_pools_hidden_repeats_and_no_invented_labels(self):
        queries=[asset('q1'),asset('q2')]
        gallery=[asset('a'),asset('b'),asset('c')]
        data=packet(queries,gallery)
        self.assertEqual(data,packet(queries,gallery))
        self.assertEqual(len(data['trials']),8)
        for qi in range(2):
            trials=[t for t in data['trials'] if t['query']==qi]
            self.assertEqual(sorted(t['candidate'] for t in trials if not t['repeat']),[0,1,2])
            self.assertEqual(sum(t['repeat'] for t in trials),1)
        self.assertTrue(all('grade' not in t for t in data['trials']))
        self.assertIsNone(data['research_split'])
        self.assertFalse(data['independent_product_groups_verified'])

    def test_hashes_ids_and_html_boundary(self):
        with self.assertRaises(ValueError):
            packet([asset('a')],[asset('a'),asset('b')])
        broken=asset('b');broken['crop_sha256']='0'*64
        with self.assertRaises(ValueError):
            packet([asset('q')],[asset('a'),broken])
        data=packet([dict(asset('q'),note='</script><script>alert(1)</script>')],[asset('a'),asset('b')])
        self.assertNotIn('</script><script>alert',build_html(data))
