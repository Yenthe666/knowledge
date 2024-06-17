# -*- coding: utf-8 -*-
# Copyright (c) 2024 MainFrame Monkey <https://www.mainframemonkey.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models, api, _


class KnowledgeArticle(models.Model):
    _inherit = 'knowledge.article'

    def write(self, vals):
        if 'share_underlying' in vals:
            for rec in self:
                share_underlying = vals.get('share_underlying')
                if share_underlying:
                    # enable
                    rec.underlying_article_ids.write(
                        {'share_with_token': True, 'access_token': rec.access_token}
                    )
                else:
                    # disable
                    rec.underlying_article_ids.write({'share_with_token': False, 'access_token': False})
        return super(KnowledgeArticle, self).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            parent = val.get('parent_id') and self.browse(val.get('parent_id'))
            if parent and parent.share_underlying and parent.share_with_token:
                val['share_with_token'] = True
                val['access_token'] = parent.access_token
        return super(KnowledgeArticle, self).create(vals_list)

