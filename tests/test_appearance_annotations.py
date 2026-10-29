import json
import unittest

from scripts.annotate_denim_appearance import parse_annotation, parse_coarse_annotation, validate_anchor_rows, ENUMS


class AppearanceAnnotationTests(unittest.TestCase):
    def test_visual_anchors_require_verified_observations_and_target_exclusion(self):
        row={'id':'reference','human_verified':True,'attributes':{
            'target_ambiguous':False,'color_family':'blue','lightness':'light'}}
        self.assertEqual(validate_anchor_rows({'examples':[row]},{'target'}),[row])
        for plan,targets in (({'examples':[row]},{'reference'}),
                             ({'examples':[dict(row,human_verified=False)]},{'target'}),
                             ({'examples':[row,row]},{'target'}),({'examples':[]},{'target'}),
                             ({'examples':[dict(row,attributes=dict(row['attributes'],lightness='unknown'))]},{'target'})):
            with self.subTest(plan=plan),self.assertRaises(ValueError):validate_anchor_rows(plan,targets)

    def test_coarse_accepts_exact_json_fence_but_not_prose_or_multiple_blocks(self):
        raw='{"target_ambiguous":false,"color_family":"neutral","lightness":"dark"}'
        self.assertEqual(parse_coarse_annotation('```json\n'+raw+'\n```'),json.loads(raw))
        for text in ('Here is the answer: '+raw,'```json\n'+raw+'\n```\nExplanation',
                     '```json\n'+raw+'\n```\n```json\n'+raw+'\n```'):
            with self.subTest(text=text),self.assertRaises(ValueError):parse_coarse_annotation(text)

    def test_coarse_mode_has_only_two_independent_attributes(self):
        row={'target_ambiguous':False,'color_family':'unknown','lightness':'light'}
        self.assertEqual(parse_coarse_annotation(json.dumps(row)),row)
        for change in (dict(row,fade_strength='strong'),dict(row,lightness='white'),
                       dict(row,target_ambiguous=1),{'target_ambiguous':False,'color_family':'blue'}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                parse_coarse_annotation(json.dumps(change))
        with self.assertRaises(ValueError):
            parse_coarse_annotation('{"target_ambiguous":false,"color_family":"blue","color_family":"neutral","lightness":"dark"}')

    def test_coarse_ambiguous_target_requires_unknown_not_dark_or_neutral(self):
        row={'target_ambiguous':True,'color_family':'unknown','lightness':'unknown'}
        self.assertEqual(parse_coarse_annotation(json.dumps(row)),row)
        with self.assertRaisesRegex(ValueError,'Ambiguous'):
            parse_coarse_annotation(json.dumps(dict(row,lightness='dark')))

    def valid(self):
        return dict(target_ambiguous=False,view='front',color_family='blue',observed_tone='cool',
            lightness='medium',fade_strength='moderate',front_hip_whiskers='visible',
            front_thigh_lightening='visible',knee_lightening='unknown',rips='absent',detail_readability='limited')

    def test_exact_schema_preserves_unknown(self):
        row=self.valid();self.assertEqual(parse_annotation(json.dumps(row)),row)
        for changed in [dict(row,color_family='navy'),dict(row,target_ambiguous=1),
                        dict(row,confidence=.99),{k:v for k,v in row.items() if k!='rips'}]:
            with self.assertRaises(ValueError):parse_annotation(json.dumps(changed))
        with self.assertRaises(ValueError):parse_annotation('{"view":"front","view":"back"}')

    def test_hidden_and_unreadable_details_rejected(self):
        row=self.valid()
        for view in ['back','side']:
            with self.assertRaisesRegex(ValueError,'Unobserved'):parse_annotation(json.dumps(dict(row,view=view)))
        with self.assertRaisesRegex(ValueError,'Unreadable'):
            parse_annotation(json.dumps(dict(row,detail_readability='insufficient')))
        row.update(view='back',front_hip_whiskers='unknown',front_thigh_lightening='unknown')
        self.assertEqual(parse_annotation(json.dumps(row))['front_hip_whiskers'],'unknown')

    def test_ambiguous_target_is_not_a_negative_label(self):
        row={k:'unknown' for k in ENUMS};row.update(target_ambiguous=True,detail_readability='insufficient')
        self.assertEqual(parse_annotation(json.dumps(row)),row)
        with self.assertRaisesRegex(ValueError,'Ambiguous'):
            parse_annotation(json.dumps(dict(row,color_family='blue')))

    def test_no_fading_conflicts_with_visible_faded_panels_but_not_rips(self):
        row=self.valid();row['fade_strength']='none'
        with self.assertRaisesRegex(ValueError,'Visible fading'):parse_annotation(json.dumps(row))
        row.update(front_hip_whiskers='absent',front_thigh_lightening='absent',knee_lightening='unknown',rips='visible')
        self.assertEqual(parse_annotation(json.dumps(row))['rips'],'visible')
        self.assertEqual(parse_annotation(json.dumps(dict(row,front_thigh_lightening='visible')))['fade_strength'],'none')
