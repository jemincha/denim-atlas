import copy
import unittest

from scripts.prepare_glami_fit import title_fit, family, group_split, lock_validation
from scripts.finetune_glami_fit import proxy_metrics


class FitProxyTests(unittest.TestCase):
    def test_expansion_keeps_exact_validation_and_reserves_related_new_images(self):
        anchor=[{'image_id':'a','proxy_split':'validation'},{'image_id':'b','proxy_split':'train'}]
        rows=[{'image_id':i,'source_group':g} for i,g in [('a','v'),('new','v'),('b','t'),('extra','x')]]
        selected,reserved=lock_validation(rows,anchor)
        self.assertEqual(reserved,['new'])
        self.assertEqual([r['image_id'] for r in selected if r['proxy_split']=='validation'],['a'])
        rows[2]['source_group']='v'
        with self.assertRaisesRegex(ValueError,'crosses'):lock_validation(rows,anchor)
        with self.assertRaisesRegex(ValueError,'lost'):lock_validation(rows[:1],anchor)

    def test_proxy_metrics_exclude_source_family_and_normalize_per_class(self):
        rows=[{'image_id':str(i),'source_group':str(i),'source_fit':'straight' if i<2 else 'wide'}
              for i in range(4)]
        scores=[[1,.9,.1,0],[.9,1,0,.1],[.1,0,1,.9],[0,.1,.9,1]]
        self.assertEqual(proxy_metrics(scores,rows)['macro_ndcg_at_5'],1.)
        rows[1]['source_group']='0'
        with self.assertRaisesRegex(ValueError,'another source group'):proxy_metrics(scores,rows)
        with self.assertRaises(ValueError):proxy_metrics([[float('nan')]],rows)
        scores[0][0]=float('nan')
        with self.assertRaisesRegex(ValueError,'Nonfinite'):proxy_metrics(scores,rows)

    def test_title_labels_are_selective_and_unknown_is_not_a_negative(self):
        for title,expected in [('Brand straight-leg jeans - Blue','straight'),
            ('WIDE LEG denim','wide'),('Flared jeans','flared'),
            ('slim straight jeans',None),('wide pockets',None),
            ('non-skinny jeans',None),('mom jeans',None),('denim',None)]:
            with self.subTest(title=title): self.assertEqual(title_fit(title),expected)

    def test_color_variants_link_without_assigning_observed_color(self):
        self.assertEqual(family('Brand Skinny Jeans - Blue'),family('Brand Skinny Jeans - Black'))
        self.assertNotEqual(family('Brand Skinny Jeans'),family('Brand Straight Jeans'))

    def test_groups_are_deterministic_and_do_not_cross_splits(self):
        rows=[{'image_id':str(i),'source_fit':'straight','title':f'Jeans model {i}',
               'item_ids':[str(i)],'pixel_sha256':str(i)} for i in range(12)]
        rows[1]['title']=rows[0]['title']+' - Blue'
        rows[3]['item_ids']=rows[2]['item_ids']
        rows[5]['pixel_sha256']=rows[4]['pixel_sha256']
        result,conflicts=group_split(copy.deepcopy(rows))
        self.assertEqual((result,conflicts),group_split(copy.deepcopy(rows)))
        groups={r['image_id']:r['source_group'] for r in result}
        for a,b in [('0','1'),('2','3'),('4','5')]:self.assertEqual(groups[a],groups[b])
        owners={}
        for row in result:
            self.assertEqual(owners.setdefault(row['source_group'],row['proxy_split']),row['proxy_split'])
        rows[1]['source_fit']='slim'
        _,conflicts=group_split(rows)
        self.assertEqual(conflicts,['0','1'])

    def test_too_few_groups_rejected(self):
        with self.assertRaisesRegex(ValueError,'Insufficient'):
            group_split([{'image_id':'1','source_fit':'wide','title':'a','item_ids':['1'],'pixel_sha256':'x'}])
