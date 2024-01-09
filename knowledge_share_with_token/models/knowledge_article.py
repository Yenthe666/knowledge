import uuid
from werkzeug.urls import url_join
from odoo import fields, models, _
from odoo.tools import consteq


class KnowledgeArticle(models.Model):
    _inherit = 'knowledge.article'

    share_with_token =  fields.Boolean(
        string="Share with token"
    )

    access_token = fields.Char(
        string='Access Token',
        default=lambda self: self._get_default_access_token(),
        copy=False
    )

    token_article_url = fields.Char(
        string='Article URL',
        compute='_compute_token_article_url',
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

    def _get_documents_and_check_access(self, access_token):
        self.ensure_one()
        if not self._check_token(access_token):
            return False
        return self

    def _compute_token_article_url(self):
        """
        Compute the article url to be shared using a unique token that will allow anyone who has this
        """
        for article in self:
            if not article.ids:
                article.token_article_url = False
            else:
                article.token_article_url = url_join(article.get_base_url(), 'knowledge/article/%s?access_token=%s' % (article.id, article.access_token))
