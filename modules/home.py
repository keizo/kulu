"""
Module for the main index page of the website.
"""
import web

from drupy import *

import loader
mod = loader.import_('modules')

urls = ('/', 'index')

class index(page):
    def GET(self):
        page = self.page
        nodes, page_nums = mod.node.listing_default()
        #print nodes
        content = mod.node.render_many(nodes) + page_nums.render()
        web.render('index.html')