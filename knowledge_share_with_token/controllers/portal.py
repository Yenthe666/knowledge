# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import http
from odoo.http import request
from odoo.addons.knowledge.controllers.main import KnowledgeController


class CustomKnowledgeWebsiteController(KnowledgeController):

    def _get_article_with_token(self, article_id, access_token):
        article = request.env['knowledge.article'].sudo().search([('id', '=', article_id)])
        if article and access_token and article.share_with_token:
            article = article._get_articles_and_check_access(access_token)
            return article
        return False

    @http.route('/knowledge/article/<int:article_id>/<string:access_token>', type='http', auth='public', website=True)
    def redirect_to_article_with_token(self, **kwargs):
        """ This route will redirect internal users to the backend view of the
        article and the share users to the frontend view instead."""
        if 'access_token' in kwargs and 'article_id' in kwargs:
            article_id = kwargs['article_id']
            access_token = kwargs['access_token']
            article = self._get_article_with_token(article_id, access_token)
            request.session.data = {'knowledge_access_token': access_token}
            if not article:
                return request.not_found()
            if request.env.user.has_group('base.group_user'):
                return self._redirect_to_backend_view(article)
            return self._redirect_to_portal_view(article)

