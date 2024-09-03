import werkzeug

from odoo import http
from odoo.http import request
from odoo.osv import expression
from odoo import http, tools, _
from odoo.exceptions import AccessError, ValidationError
from odoo.addons.knowledge.controllers.main import KnowledgeController
from odoo.addons.knowledge_share_with_token.controllers.portal import CustomKnowledgeWebsiteController


class KnowledgeTokenWebsiteController(CustomKnowledgeWebsiteController):

    def _check_sidebar_display(self):
        show_sidebar = super()._check_sidebar_display()
        if not show_sidebar:
            accessible_workspace_roots = request.env["knowledge.article"].sudo().search_count(
                [("parent_id", "=", False), ("category", "=", "workspace"), ("share_with_token", "=", True)],
                limit=1,
            )
            if accessible_workspace_roots > 0:
                return True
        return show_sidebar

    def _prepare_articles_tree_html_values(self, active_article_id=False, unfolded_articles_ids=False, unfolded_favorite_articles_ids=False):
        values = super()._prepare_articles_tree_html_values(
            active_article_id=active_article_id,
            unfolded_articles_ids=unfolded_articles_ids,
            unfolded_favorite_articles_ids=unfolded_favorite_articles_ids
        )
        #improve me
        unfolded_articles_ids = set(unfolded_articles_ids or [])
        existing_ids = self._article_ids_exists(unfolded_articles_ids)
        unfolded_articles_ids = unfolded_articles_ids & existing_ids

        active_article_ancestor_ids = []
        token_articles = request.env['knowledge.article']
        if active_article_id:
            active_article = request.env['knowledge.article'].sudo().browse(active_article_id)
            if active_article.share_with_token: #check access_token
                active_article_ancestor_ids = active_article._get_ancestor_ids()
                unfolded_articles_ids |= active_article_ancestor_ids
                root_article_ids = active_article.root_article_id.ids
                #root_article_ids = request.env["knowledge.article"].sudo().search([("parent_id", "=", False)]).ids
                all_visible_articles = request.env['knowledge.article']
                all_visible_articles_ids = unfolded_articles_ids | set(root_article_ids)
                if all_visible_articles_ids:
                    all_visible_articles = request.env['knowledge.article'].sudo().search(
                        [
                            ('id', 'child_of', all_visible_articles_ids),
                            ('is_article_item', '=', False),
                        ],
                        order='sequence, id',
                    )
                root_articles = all_visible_articles.filtered(lambda article: not article.parent_id)
                token_articles = root_articles.filtered(lambda a: a.share_with_token)
                values["all_visible_articles"] += all_visible_articles - values["all_visible_articles"]
        values.update({
            "token_articles": token_articles,
        })
        return values

    def _get_load_more_roots_domain(self, category):
        if category == "portal_token":
            return [('parent_id', '=', False), ('category', '=', 'workspace'), ('share_with_token', '=', True)]
        return super()._get_load_more_roots_domain(category)

    @http.route()
    def get_tree_panel_children(self, parent_id, access_token=False):
        try:
            return super().get_tree_panel_children(parent_id)
        except AccessError:
            parent = request.env['knowledge.article'].sudo().search([('id', '=', parent_id), ('share_with_token', '=', True)])
            if not parent:
                raise AccessError(
                    _("This Article cannot be unfolded. Either you lost access to it or it has been deleted."))
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
                "has_parent": True,
                "articles_category": 'portal_token',
            })

    @http.route()
    def get_tree_panel_portal_search(self, search_term, active_article_id=False, access_token=False):
        res = super().get_tree_panel_portal_search(search_term, active_article_id)
        article = request.env['knowledge.article'].sudo().search([('id', '=', active_article_id)])
        if article and access_token and article.share_with_token:
            available_documents = article._get_documents_and_check_access(access_token)
            if available_documents:
                all_visible_articles = request.env['knowledge.article'].sudo().search(
                    expression.AND([[('is_article_item', '=', False)], [('name', 'ilike', search_term)]]),
                    order='name',
                    limit=self._KNOWLEDGE_TREE_ARTICLES_LIMIT,
                )
                values = {
                    "search_tree": True,  # Display the flatenned tree instead of the basic tree with sections
                    "active_article_id": active_article_id,
                    'portal_readonly_mode': not request.env.user.has_group('base.group_user'),
                    'articles': all_visible_articles,
                    'articles_category': 'portal_token',
                }
                return request.env['ir.qweb']._render('knowledge.knowledge_article_tree_frontend', values)
        return res
