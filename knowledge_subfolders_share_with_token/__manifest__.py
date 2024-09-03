{
    "name": "Knowledge Subfolders Share with token",
    "summary": "This modules allows token generation for knowledge in subfolders.",
    "description": "This modules allows token generation for knowledge in subfolders.",
    "category": "Productivity/Knowledge",
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "depends": [
        "knowledge_share_with_token",
    ],
    "data": [
        "views/knowledge_templates_frontend.xml",
    ],
    "assets": {
        'web.assets_backend': [
            "knowledge_subfolders_share_with_token/static/src/js/knowledge_subfolders_token.js",
            "knowledge_subfolders_share_with_token/static/src/xml/knowledge_subfolders_token.xml",
        ],
        'web.assets_frontend': [
            'knowledge_subfolders_share_with_token/static/src/js/knowledge_frontend.js',
        ],
    }
}
