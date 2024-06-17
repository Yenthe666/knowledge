# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, api, _


class KnowledgeArticle(models.Model):
    _inherit = 'knowledge.article'

    share_underlying = fields.Boolean(
        string="Share all underlying articles",
        help="If active, gives access of underlying shared articles.",
        index=True
    )

    underlying_article_ids = fields.One2many('knowledge.article', compute='_compute_underlying_articles')

    ancestor_ids = fields.Many2many('knowledge.article', 'knowledge_article_ancestor',
                                    'article_id',
                                    'ancestor_id',
                                    compute='_compute_ancestor_ids', store=True)

    shared_by_ancestors = fields.Boolean(compute='_compute_shared_by_ancestors',
        store=True, index=True,
        help="When True, article is shared because an ancestor is set to share underlying articles"
    )

    @api.depends('parent_id',)
    def _compute_ancestor_ids(self):
        for article in self:
            article.ancestor_ids = self.sudo().browse(article.sudo()._get_ancestor_ids())

    @api.depends('ancestor_ids', 'ancestor_ids.share_underlying')
    def _compute_shared_by_ancestors(self):
        for article in self:
            article.shared_by_ancestors = any(article.mapped('ancestor_ids.share_underlying'))

    @api.depends('child_ids')
    def _compute_underlying_articles(self):
        for article in self:
            underlying_articles = self.env['knowledge.article']
            childs = article.sudo().child_ids
            while childs:
                underlying_articles |= childs
                childs = childs.mapped('child_ids')

            article.underlying_article_ids = underlying_articles

