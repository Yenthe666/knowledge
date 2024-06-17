# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common, tagged
from markupsafe import Markup


@tagged('-at_install', 'post_install', 'knowledge')
class TestShareWithToken(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestShareWithToken, cls).setUpClass()
        cls.article_A = cls.env['knowledge.article'].create({'name': 'A',
                            'body': Markup("""Hello World! This is the Article A"""),
                            'share_with_token': True, })

    def test_share_with_token(self):
        token = self.article_A.access_token
        self.assertTrue(token)
        self.assertTrue(token in self.article_A.token_article_url)

        article_with_token = self.env['knowledge.article'].browse(self.article_A.id)
        self.assertTrue(article_with_token._get_articles_and_check_access(token))
        self.assertFalse(article_with_token._get_articles_and_check_access("fakeToken"))
