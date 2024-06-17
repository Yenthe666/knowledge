# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common, tagged
from odoo.addons.knowledge_share_with_token.tests.test_access_token import TestShareWithToken


@tagged('post_install', 'knowledge')
class TestShareWithTokenController(TestShareWithToken, common.HttpCase):

    @classmethod
    def setUpClass(self):
        super(TestShareWithTokenController, self).setUpClass()

    def test_can_access_underlying(self):
        resultA = self.url_open(f'/knowledge/article/{str(self.article_A.id)}/{self.article_A.access_token}')
        self.assertTrue("This is the Article A" in resultA.text)
