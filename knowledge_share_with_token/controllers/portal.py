from odoo import http
from odoo.http import request
from odoo.addons.knowledge.controllers.main import KnowledgeController


class CustomKnowledgeWebsiteController(KnowledgeController):

    @http.route('/knowledge/article/<int:article_id>', type='http', auth='public', website=True)
    def redirect_to_article(self, **kwargs):
        if 'access_token' in kwargs and 'article_id' in kwargs:
            article_id = kwargs['article_id']
            access_token = kwargs['access_token']
            article = request.env['knowledge.article'].search([('id', '=', article_id)])
            if article and access_token:
                available_documents = article._get_documents_and_check_access(access_token)
                if available_documents is False:
                    return request.not_found()
                if request.env.user._is_public() and not article.website_published:
                    # public users can't access articles that are not published, let them login first
                    return request.redirect('/web/login?redirect=/knowledge/article/%s?access_token=%s' % (article.id, article.access_token))
                return self._redirect_to_portal_view(article)
        return super().redirect_to_article(**kwargs)
