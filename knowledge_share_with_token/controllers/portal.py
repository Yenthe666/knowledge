import werkzeug

from odoo import http
from odoo.http import request
from odoo.addons.knowledge.controllers.main import KnowledgeController


class CustomKnowledgeWebsiteController(KnowledgeController):

    @http.route('/knowledge/article/<int:article_id>/<string:access_token>', type='http', auth='public', website=True)
    def redirect_to_article_with_token(self, **kwargs):
        """ This route will redirect internal users to the backend view of the
        article and the share users to the frontend view instead."""
        if 'access_token' in kwargs and 'article_id' in kwargs:
            article_id = kwargs['article_id']
            access_token = kwargs['access_token']
            article = request.env['knowledge.article'].sudo().search([('id', '=', article_id)])
            if article and access_token and article.share_with_token:
                available_documents = article._get_documents_and_check_access(access_token)
                if available_documents is False:
                    return request.not_found()
                if request.env.user.has_group('base.group_user'):
                    if not article:
                        return werkzeug.exceptions.Forbidden()
                    return self._redirect_to_backend_view(article)
                return self._redirect_to_portal_view(article)
            return werkzeug.exceptions.Forbidden()

