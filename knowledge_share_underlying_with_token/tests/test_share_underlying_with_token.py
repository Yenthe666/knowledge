# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common, tagged
from markupsafe import Markup


@tagged('-at_install', 'post_install', 'knowledge')
class TestShareUnderlyingWith_token(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestShareUnderlyingWith_token, cls).setUpClass()
        cls.article_A = cls.env['knowledge.article'].create({'name': 'A',
                            'body': Markup("""Hello World! This is the Article A"""),
                            'share_with_token': True, })
        cls.article_B = cls.env['knowledge.article'].create({'name': 'B',
                            'body': Markup("""Hello World! This is the Article B"""),
                            'parent_id': cls.article_A.id})
        cls.article_C = cls.env['knowledge.article'].create({'name': 'C',
                            'body': Markup("""Hello World! This is the Article C"""),
                            'parent_id': cls.article_B.id})

    def test_share_underlying(self):
        self.assertFalse(self.article_B.access_token)
        self.assertFalse(self.article_C.access_token)

        self.article_A.write({'share_underlying': True})
        # Once article A shares underlying articles, B and C are now access by same token of A

        self.assertEqual(self.article_A.access_token, self.article_B.access_token, )
        self.assertEqual(self.article_A.access_token, self.article_C.access_token, )

        self.article_A.write({'share_underlying': False})

        self.assertFalse(self.article_B.share_with_token)
        self.assertFalse(self.article_B.access_token)
        self.assertFalse(self.article_C.share_with_token)
        self.assertFalse(self.article_C.access_token)

    def test_share_create(self):
        self.article_A.write({'share_with_token': True, 'share_underlying': True})
        article_D = self.article_A.create({
            'name': 'D',
            'body': Markup("""Hello World! This is the Article D"""),
            'website_published': False,
            'parent_id': self.article_A.id
        })

        self.assertEqual(self.article_A.access_token, article_D.access_token)