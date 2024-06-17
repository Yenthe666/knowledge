# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import uuid
from werkzeug.urls import url_join
from odoo import fields, models, api, _
from odoo.tools import consteq
from odoo.http import request
from odoo.osv import expression


class KnowledgeArticle(models.Model):
    _inherit = 'knowledge.article'

    share_with_token = fields.Boolean(
        string="Share with token"
    )

    access_token = fields.Char(
        string='Access Token',
        compute='_compute_token',
        store=True,
        index=True,
        copy=False
    )

    token_article_url = fields.Char(
        string='Article URL',
        compute='_compute_token',
        store=True,
        readonly=True
    )

    def _get_default_access_token(self):
        return str(uuid.uuid4())

    def _check_token(self, access_token):
        """
        Check if the given access token is valid.
        """
        if not access_token:
            return False
        try:
            return consteq(access_token, self.access_token)
        except:
            return False

    def _get_articles_and_check_access(self, access_token):
        self.ensure_one()
        if not self._check_token(access_token):
            return False
        return self

    @api.model
    def search(self, domain, offset=0, limit=None, order=None, count=False):
        if not self.env.su and request.session and request.session.data:
            access_token = request.session.data.get("knowledge_access_token")
            if access_token:
                # providing an access_token is like giving access to articles
                domain = expression.AND([domain, [('access_token', '=', access_token)]])
                result = super(KnowledgeArticle, self).sudo().search(domain, offset, limit, order, count)
                return result
        return super(KnowledgeArticle, self).search(domain, offset, limit, order, count)

    @api.depends('share_with_token')
    def _compute_token(self):
        """
        Compute the article token and url to be shared using a unique token that will allow anyone who has link
        """
        for article in self:
            if not article.share_with_token:
                article.token_article_url = False
            else:
                if not article.access_token:  # keep for existing tokens
                    article.access_token = str(uuid.uuid4())
                article.token_article_url = url_join(article.get_base_url(), 'knowledge/article/%s/%s' % (article.id, article.access_token))

    @api.onchange('share_with_token')
    def _onchange_share_with_token(self):
        if self.share_with_token:
            self.website_published = False
