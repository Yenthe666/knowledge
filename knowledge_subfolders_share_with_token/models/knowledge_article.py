import uuid
from werkzeug.urls import url_join
from odoo import fields, models, api, _
from odoo.tools import consteq


class KnowledgeArticle(models.Model):
    _inherit = 'knowledge.article'

    is_token_shared = fields.Boolean(string='Is Token Shared?',
        compute="_compute_token_shared", compute_sudo=True,
        store=True, recursive=True)

    @api.depends('share_with_token', 'parent_id', 'root_article_id', 'child_ids', \
                        'parent_id.share_with_token', 'root_article_id.share_with_token', 'child_ids.share_with_token')
    def _compute_token_shared(self):
        for article in self:
            article.is_token_shared = article.share_with_token
            article.child_ids.share_with_token = article.share_with_token
