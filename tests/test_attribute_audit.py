import copy
import json
import unittest

from scripts.prepare_attribute_audit import prepare


def fixture():
    return ([{'image_id':'1', 'sha256':'a'*64}],
            [{'image_id':'1', 'name':'Blue Skinny Jeans'}],
            {'examples':[{'id':'glami:1', 'sha256':'a'*64, 'usage_scope':'private_research_reviewed'}]},
            [{'id':'glami:1', 'image_sha256':'a'*64, 'schema_valid':False,
              'raw_response':json.dumps({'target_ambiguous':False, 'color_family':'black',
                                        'lightness':'dark', 'observed_tone':'neutral',
                                        'front_hip_whiskers':'invalid wash assertion'})}])


class AttributeAuditTests(unittest.TestCase):
    def test_coarse_drafts_survive_unrelated_wash_failure_without_becoming_truth(self):
        result=prepare(*fixture())
        row=result['observations'][0]
        self.assertFalse(row['original_full_schema_valid'])
        self.assertEqual(row['proposals']['retail_fit']['value'],'skinny')
        self.assertEqual(row['proposals']['color_family']['value'],'neutral')
        self.assertEqual(row['proposals']['color_family']['raw_value'],'black')
        self.assertNotIn('front_hip_whiskers',row['proposals'])
        self.assertFalse(row['human_verified'])
        self.assertFalse(row['training_eligible'])

    def test_ambiguous_or_unknown_never_becomes_absent_or_negative(self):
        args=fixture()
        for ambiguity in (True,False):
            value=json.loads(args[3][0]['raw_response'])
            value.update(target_ambiguous=ambiguity,color_family='unknown')
            args[3][0]['raw_response']=json.dumps(value)
            fields=prepare(*args)['observations'][0]['proposals']
            self.assertIsNone(fields['color_family']['value'])
            self.assertEqual(fields['lightness']['value'],None if ambiguity else 'dark')

    def test_conflicting_source_tags_do_not_become_observed_attributes(self):
        args=fixture();args[1].append({'image_id':'1','name':'Slim black jeans'})
        fields=prepare(*args)['observations'][0]['proposals']
        self.assertNotIn('retail_fit',fields)
        self.assertEqual(fields['color_family']['raw_value'],'black')
        self.assertNotIn('volume',fields)

    def test_rejects_broken_provenance_and_missing_descriptions(self):
        for mutation in ('wrong_hash','duplicate','missing','invalid_enum'):
            args=copy.deepcopy(fixture())
            if mutation=='wrong_hash':args[3][0]['image_sha256']='b'*64
            elif mutation=='duplicate':args[3].append(copy.deepcopy(args[3][0]))
            elif mutation=='missing':args[3].clear()
            else:
                value=json.loads(args[3][0]['raw_response']);value['lightness']='perfect'
                args[3][0]['raw_response']=json.dumps(value)
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):prepare(*args)
