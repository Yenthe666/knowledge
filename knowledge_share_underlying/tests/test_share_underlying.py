# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import common, tagged
from markupsafe import Markup


@tagged('-at_install', 'post_install', 'knowledge')
class TestShareUnderlying(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestShareUnderlying, cls).setUpClass()
        cls.article_A = cls.env['knowledge.article'].create({'name': 'A',
                            'body': Markup("""Hello World! This is the Article A"""),
                            'website_published': True, })
        cls.article_B = cls.env['knowledge.article'].create({'name': 'B',
                            'body': Markup("""Hello World! This is the Article B"""),
                            'parent_id': cls.article_A.id})
        cls.article_C = cls.env['knowledge.article'].create({'name': 'C',
                            'body': Markup("""Hello World! This is the Article C"""),
                            'parent_id': cls.article_B.id})

    def test_share_underlying(self):
        self.assertFalse(self.article_B.website_published)
        self.assertFalse(self.article_C.website_published)

        self.article_A.write({'share_underlying': True})
        # Once article A shares underlying articles, B and C are now website_published

        self.assertCountEqual(self.article_A.underlying_article_ids.ids, (self.article_B + self.article_C).ids)
        self.assertCountEqual(self.article_C.ancestor_ids.ids, (self.article_A + self.article_B).ids)

        self.assertTrue(self.article_B.shared_by_ancestors)
        self.assertTrue(self.article_C.shared_by_ancestors)

        self.article_A.write({'share_underlying': False})

        self.assertFalse(self.article_B.shared_by_ancestors)
        self.assertFalse(self.article_C.shared_by_ancestors)

    def test_share_create(self):
        self.article_A.write({'share_underlying': True})
        article_D = self.article_A.create({
            'name': 'D',
            'body': Markup("""Hello World! This is the Article D"""),
            'website_published': False,
            'parent_id': self.article_A.id
        })

        self.assertTrue(article_D.shared_by_ancestors)