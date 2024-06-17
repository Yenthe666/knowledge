# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import werkzeug

from odoo import http
from odoo.http import request
from odoo.addons.knowledge.controllers.main import KnowledgeController


class CustomKnowledgeWebsiteController(KnowledgeController):

    @http.route('/knowledge/article/<int:article_id>', type='http', auth='public', website=True, sitemap=False)
    def redirect_to_article(self, **kwargs):
        if request.env.user._is_public():
            article = request.env['knowledge.article'].sudo().browse(kwargs['article_id'])
            if not article.exists():
                raise werkzeug.exceptions.NotFound()
            if article.website_published or article.shared_by_ancestors:
                if request.env.user.has_group('base.group_user'):
                    return self._redirect_to_backend_view(article)
                return self._redirect_to_portal_view(article)
        return super().redirect_to_article(**kwargs)
