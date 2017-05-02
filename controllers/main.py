# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import werkzeug
import itertools
import pytz
import babel.dates
from collections import OrderedDict

from odoo import http, fields, _
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.website import slug, unslug
from odoo.exceptions import UserError
from odoo.http import request
from odoo.tools import html2plaintext
from odoo.addons.website_blog.controllers.main import WebsiteBlog

class WebsiteBlogEx(WebsiteBlog):
    @http.route([
        '''/blog/<model("blog.blog"):blog>/post/<model("blog.post", "[('blog_id','=',blog[0])]"):blog_post>''',
    ], type='http', auth="public", website=True)
    def blog_post(self, blog, blog_post, tag_id=None, page=1, enable_editor=None, **post):
        BlogPost = request.env['blog.post']
        the_same_posts = None

        if blog.id:
            the_same_posts = BlogPost.search(
                [('blog_id', '=', blog.id), ("website_published", "=", True), ("id", "!=", blog_post.id)], limit=4,
                order="create_date desc")
            # for blogpost in the_same_posts:
            # blogpost.content = html2text(blogpost.content.split(".", 3)[0])

        res = super(WebsiteBlogEx, self).blog_post(blog, blog_post, tag_id=None, page=1, enable_editor=None, **post)
        res.qcontext.update({'the_same_posts': the_same_posts})
        res.qcontext.update({'the_same_number': len(the_same_posts)})
        # res.qcontext.update({'blog_dict': blog_dict})
        return res

    @http.route([
        '/blog/<model("blog.blog"):blog>',
        '/blog/<model("blog.blog"):blog>/page/<int:page>',
        '/blog/<model("blog.blog"):blog>/tag/<string:tag>',
        '/blog/<model("blog.blog"):blog>/tag/<string:tag>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def blog(self, blog=None, tag=None, page=1, **opt):
        res = super(WebsiteBlogEx, self).blog(blog, tag, page, **opt)
        BlogPost = request.env['blog.post']
        Blog = request.env['blog.blog']
        blogs = Blog.search([], order="create_date asc")
        blog_dict = {}
        for blog in blogs:
            blog_post_number = len(BlogPost.search([('blog_id', '=', blog.id), ("website_published", "=", True)]))
            blog_dict.update({
                blog.id: blog_post_number
            })
        res.qcontext.update({"blog_dict": blog_dict})
        return res