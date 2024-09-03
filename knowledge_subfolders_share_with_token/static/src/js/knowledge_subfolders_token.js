/** @odoo-module **/

import { ArticlesStructureBehavior } from "@knowledge/components/behaviors/articles_structure_behavior/articles_structure_behavior";
import { patch } from '@web/core/utils/patch';


patch(ArticlesStructureBehavior.prototype, "knowledge_subfolders_share_with_token", {

    // @override
    async _fetchAllArticles (articleId) {
        const selector = 'o_knowledge_articles_structure_children_only';
        const domain = [
            ['parent_id', this.props.anchor.classList.contains(selector) ? '=' : 'child_of', articleId],
            ['is_article_item', '=', false]
        ];
        const { records } = await this.rpc('/web/dataset/search_read', {
            model: 'knowledge.article',
            fields: ['id', 'display_name', 'parent_id', 'share_with_token', 'access_token'],
            domain,
            sort: 'sequence',
        });
        return records;
    },

    // @override
    _buildArticlesStructure (parentId, allArticles) {
        const artcls = this._super(...arguments);
        const articles = [];
        for (const article of allArticles) {
            if (article.parent_id && article.parent_id[0] === parentId) {
                articles.push({
                    id: article.id,
                    name: article.display_name,
                    child_ids: this._buildArticlesStructure(article.id, allArticles),
                    share_with_token: article.share_with_token,
                    access_token: article.access_token,
                });
            }
        }
        return articles;
    }
});
