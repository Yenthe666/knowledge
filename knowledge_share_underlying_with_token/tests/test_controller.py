# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common, tagged
from odoo.addons.knowledge_share_underlying_with_token.tests.test_share_underlying_with_token import \
    TestShareUnderlyingWith_token
from http import HTTPStatus


@tagged('post_install', 'knowledge')
class TestShareUnderlyingWithTokenController(TestShareUnderlyingWith_token, common.HttpCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()

    def test_can_access_underlying_with_token(self):
        self.article_A.write({'share_underlying': True})

        resultA = self.url_open(f'/knowledge/article/{str(self.article_A.id)}/{self.article_A.access_token}')
        self.assertTrue("This is the Article A" in resultA.text)

        resultB = self.url_open(f'/knowledge/article/{str(self.article_B.id)}/{self.article_A.access_token}')
        self.assertTrue("This is the Article B" in resultB.text)

        resultC = self.url_open(f'/knowledge/article/{str(self.article_C.id)}/{self.article_A.access_token}')
        self.assertTrue("This is the Article C" in resultC.text)

        self.article_A.write({'share_underlying': False})
        resultB = self.url_open(f'/knowledge/article/{str(self.article_B.id)}/{self.article_A.access_token}')
        self.assertEqual(resultB.status_code, HTTPStatus.NOT_FOUND.value)
