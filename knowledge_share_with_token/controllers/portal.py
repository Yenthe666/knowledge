import werkzeug

from odoo import http
from odoo.http import request
from odoo.addons.knowledge.controllers.main import KnowledgeController


class CustomKnowledgeWebsiteController(KnowledgeController):

    @http.route('/knowledge/article/<int:article_id>', type='http', auth='public', website=True, sitemap=False)
    def redirect_to_article(self, **kwargs):
        """ This route is being over-ridden to handle child article display in case of cookie stored in session.
        """
        if request.env.user._is_public():
            article = request.env['knowledge.article'].sudo().browse(kwargs['article_id'])
            if not article.exists():
                raise werkzeug.exceptions.NotFound()
            token = request.httprequest.cookies.get('k_article_token', False)
            if token:
                display_article_data = self.display_article_data_from_token(token)
                if article in display_article_data['all_visible_articles']:
                    return self._redirect_to_portal_view(article)
        return super().redirect_to_article(**kwargs)

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

                request.future_response.set_cookie('k_article_token', access_token, max_age=24 * 3600)

                if request.env.user.has_group('base.group_user'):
                    return self._redirect_to_backend_view(article)
                return self._redirect_to_portal_view(article)
            return werkzeug.exceptions.Forbidden()

    @http.route('/knowledge/tree_panel/children', type='json', auth='public', website=True, sitemap=False)
    def get_tree_panel_children(self, parent_id):
        token = request.httprequest.cookies.get('k_article_token', False)
        if token:
            display_article_data = self.display_article_data_from_token(token)
            if parent_id in display_article_data['all_visible_articles'].ids:
                parent = request.env['knowledge.article'].sudo().search([('id', '=', parent_id)])
                if parent:
                    articles = parent.child_ids.filtered(
                        lambda a: not a.is_article_item
                    ).sorted("sequence") if parent.has_article_children else request.env['knowledge.article']
                    return request.env['ir.qweb']._render('knowledge.articles_template', {
                        'articles': articles,
                        "articles_displayed_limit": self._KNOWLEDGE_TREE_ARTICLES_LIMIT,
                        "articles_displayed_offset": 0,
                        'portal_readonly_mode': not request.env.user.has_group('base.group_user'),
                        # used to bypass access check (to speed up loading)
                        "user_write_access_by_article": {
                            article.id: article.user_can_write
                            for article in articles
                        },
                        "has_parent": True
                    })
        return super().get_tree_panel_children(parent_id)

    def _prepare_articles_tree_html_values(self, active_article_id=False, unfolded_articles_ids=False, unfolded_favorite_articles_ids=False):
        """ This override add the child/related articles that need to be displayed
        in the tree panel once publish management is activated. """
        values = super()._prepare_articles_tree_html_values(
            active_article_id=active_article_id,
            unfolded_articles_ids=unfolded_articles_ids,
            unfolded_favorite_articles_ids=unfolded_favorite_articles_ids
        )
        # Fetch all required articles that need to display
        token = request.httprequest.cookies.get('k_article_token', False)
        if token:
            display_article_data = self.display_article_data_from_token(token)
            values.update({
                'shared_articles': values['shared_articles'] | display_article_data['shared_articles'],
                'all_visible_articles': values['all_visible_articles'] | display_article_data['all_visible_articles']
            })
        return values

    @staticmethod
    def display_article_data_from_token(token):
        article_data = {}
        article_sudo_model = request.env['knowledge.article'].sudo()
        article_ids = article_sudo_model.search([])
        to_show_article_ids = article_ids.filtered(
            lambda article: article._get_documents_and_check_access(token) and article.share_with_token)
        article_data['shared_articles'] = to_show_article_ids

        while True:
            res = article_sudo_model.search(
                [['parent_id', 'in', to_show_article_ids.ids], ['id', 'not in', to_show_article_ids.ids]])
            if not res:
                break
            to_show_article_ids = to_show_article_ids | res
        article_data['all_visible_articles'] = to_show_article_ids
        return article_data
