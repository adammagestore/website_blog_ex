# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Blog Ex',
    'category': 'Website',
    'sequence': 240,
    'website': 'https://www.odoobin.com',
    'summary': 'News, Blogs, Announces, Discussions',
    'version': '1.0',
    'description': """
Odoo Website Blog Extend
============

        """,
    'depends': ['website_blog'],
    'data': [
        "views/template.xml"
    ],
    'demo': [

    ],
    'test': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
