/** @odoo-module */

import publicWidget from 'web.public.widget';

publicWidget.registry.KnowledgeWidget.include({

    /**
     * @override
     */
    _searchArticles: async function (ev) {
        //optimise me
        const url = new URL(window.location.href).pathname.split('/');
        const access_token = url.slice(-1)[0];
        const searchTerm = this.$('.knowledge_search_bar').val();
        if (url.length === 5 && searchTerm){
            ev.preventDefault();
            const container = this.el.querySelector('.o_knowledge_tree');
            try {
                const htmlTree = await this._rpc({
                    route: '/knowledge/tree_panel/portal/search',
                    params: {
                        search_term: searchTerm,
                        active_article_id: this.$id,
                        access_token: access_token,
                    }
                });
                container.innerHTML = htmlTree;
            } catch {
                container.innerHTML = "";
            }
        }else{
            return this._super(...arguments);
        }
    },
});