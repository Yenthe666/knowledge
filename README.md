# knowledge
Apps related to Odoo it's knowledge features:
- [knowledge_share_with_token](#knowledge_share_with_token): allow sharing knowledge articles with tokens

## knowledge_share_with_token
This app adds support to share knowledge articles in a semi-public way.<br/>
Default Odoo only has two options. You either share an article with the world and it is completely public (and since the URL is based on a database ID people can guess/try all your articles) or you have to share with specific portal users.<br/>
This app adds an in-between option so you can share articles with anyone, not needing any portal user, but having it secured with tokens.<br/>
This option is ideal to share articles with multiple people where you do not want to manually configure who should have access person by person.<br/>
For example: you write a knowledge article for your customer who has 100 employees. In this case you can share a link with token and the people internally can forward the knowledge article.<br/>
This option is an easy toggle on the knowledge "Share" block:<br/>
<img width="1275" alt="image" src="https://github.com/Yenthe666/knowledge/assets/6352350/7f0d7e1d-b848-4734-abda-905961424fb8">
