import copy
import json
import unittest

from scripts.prepare_attribute_audit import prepare, select_expansion


def fixture():
    return ([{'image_id':'1', 'sha256':'a'*64}],
            [{'image_id':'1', 'name':'Blue Skinny Jeans'}],
            {'examples':[{'id':'glami:1', 'sha256':'a'*64, 'usage_scope':'private_research_reviewed'}]},
            [{'id':'glami:1', 'image_sha256':'a'*64, 'schema_valid':False,
              'raw_response':json.dumps({'target_ambiguous':False, 'color_family':'black',
                                        'lightness':'dark', 'observed_tone':'neutral',
                                        'front_hip_whiskers':'invalid wash assertion'})}])


class AttributeAuditTests(unittest.TestCase):
    def test_expansion_excludes_transitive_metadata_bridges_and_seen_pixels(self):
        examples=[{'image_id':str(i),'sha256':str(i)*64,'pixel_sha256':
                   'shared' if i in (4,5) else str(i)} for i in range(1,7)]
        rows=[{'image_id':str(i),'item_id':str(i),'name':f'Brand{i} jeans'} for i in range(1,7)]
        rows[0].update(item_id='a',name='Brand Straight Jeans - Blue')
        rows[1].update(item_id='b',name='Brand Straight Jeans - Black')
        rows[2].update(item_id='c')
        rows.extend([{'image_id':'9','item_id':'b','name':'Bridge Slim'},
                     {'image_id':'10','item_id':'c','name':'Bridge Slim'}])
        result=select_expansion(examples,rows,{'glami:1'},{'glami:4'},count=1)
        self.assertEqual([r['id'] for r in result['examples']],['glami:6'])
        self.assertEqual(result['summary']['excluded_reviewed_images'],5)
        self.assertFalse(result['summary']['training_eligible'])
        with self.assertRaisesRegex(ValueError,'Insufficient'):
            select_expansion(examples,rows,{'glami:1'},{'glami:4'},count=2)

    def test_expansion_is_deterministic_unique_and_does_not_invent_attributes(self):
        examples=[{'image_id':str(i),'sha256':'a'*64,'pixel_sha256':str(i)} for i in range(20)]
        rows=[{'image_id':str(i),'item_id':str(i),
               'name':f'Brand{i} '+('slim' if i%2 else 'straight')+' jeans'} for i in range(20)]
        a=select_expansion(examples,rows,set(),set(),count=8)
        self.assertEqual(a,select_expansion(list(reversed(examples)),list(reversed(rows)),set(),set(),count=8))
        self.assertEqual(len({r['source_group'] for r in a['examples']}),8)
        self.assertTrue(all('attributes' not in r for r in a['examples']))

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
