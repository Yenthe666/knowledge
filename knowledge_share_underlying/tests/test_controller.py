# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import common, tagged
from odoo.addons.knowledge_share_underlying.tests.test_share_underlying import TestShareUnderlying

@tagged('post_install', 'knowledge')
class TestShareUnderlyingController(TestShareUnderlying, common.HttpCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()

    def test_can_access_underlying(self):
        resultA = self.url_open('/knowledge/article/' + str(self.article_A.id))
        self.assertTrue("This is the Article A" in resultA.text)

        resultB = self.url_open('/knowledge/article/' + str(self.article_B.id))
        self.assertFalse("This is the Article B" in resultB.text)

        resultC = self.url_open('/knowledge/article/' + str(self.article_C.id))
        self.assertFalse("This is the Article C" in resultC.text)

        self.article_A.write({'share_underlying': True})
        # Once article A shares underlying articles, B and C are now website_published

        resultB = self.url_open('/knowledge/article/' + str(self.article_B.id))
        self.assertTrue("This is the Article B" in resultB.text)

        resultC = self.url_open('/knowledge/article/' + str(self.article_C.id))
        self.assertTrue("This is the Article C" in resultC.text)
