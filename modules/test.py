"""test module"""
import time
try:
    import cPickle as pickle
except ImportError:
    import pickle

from web import form
import web

import recaptcha

import glbl
from drupy import *

urls = (
    '/util','util',
    '/captcha','captcha',
    '/glbl','print_glbl',
    '/test/session','session',
    '/test/roles','roles',
    '/pickle/(.+)','pickle_speed',
    '/access','test_access',
    )

perms = ('test access',)

import loader, sys
mod = loader.import_('modules')
#inc = loader.import_('includes')

class util(page):
    """tests the classes in util.py include"""
    def GET(self):
        page = self.page
        f = form_util()
        content = '<form method="post">'
        content += f.render()
        content += '<input type="submit" /></form>'
        var = str(glbl.filter)
        var = var.replace('<', '&lt;')
        content += var
        web.render('generic.html')
        
    def POST(self):
        format = web.input().format
        values = web.input().modules
        values = values.split(',')
        values = [x.strip() for x in values]
        print int(format), values
        print 'setting glbl.filter'
        glbl.filter[int(format)] = values
    
form_util = form.Form(
    form.Textbox('format'),
    form.Textbox('modules')
    )

public_key = '6Lf4MwAAAAAAAOlBfZz1o7kYrUBVUk8bJ8XQ1IKH'
private_key = '6Lf4MwAAAAAAACa4W-4akk6je10IBNFkFOxL3iIL'
class captcha(page):
    def GET(self):
        page = self.page
        content = '<form method="post">'
        content += recaptcha.displayhtml(public_key)
        content += '<input type="submit" /></form>'
        web.render('generic.html')
    def POST(self):
        page = self.page
        i = web.input()
        captcha = recaptcha.submit(i.recaptcha_challenge_field, 
                                    i.recaptcha_response_field, 
                                    private_key, web.ctx.ip)
        content = captcha.is_valid, captcha.error_code
        web.render('generic.html')

class print_glbl(page):
    def GET(self):
        print glbl.variable
        
class roles(page):
    def GET(self):
        page = self.page
        print page.user

class session:
    def GET(self):
        page = self.page
        inc.session.regenerate(uid=11)
        print web.cookies()
        
    def POST(self):
        form = signup()
        form.validates()
        page = self.page
        web.render('test.html')
        
class pickle_speed:
    """test the speed of pickling to see if we should use it to cache nodes"""
    def GET(self,nid):
        #node = mod.node.load(nid)
        nodes, page_nums = mod.node.listing_default()
        pickled_nodes = []
        for node in nodes:
            pickled_nodes.append(pickle.dumps(node))
        unpickled = []
        start = time.time()
        for node in pickled_nodes:
            unpickled.append(pickle.loads(node))
        print time.time() - start
        print ': time to unpickle some objects'
        
        
        expanded = []
        new = {'readmore':True, 'teaser':'there is nothing to see here',
               'links':'no links to see here', 'time':time.time()}
        start = time.time()
        for node in unpickled:
            expanded = web.storify(new,**node)
        print time.time()-start
        print ': time to storify some nodes'
        
        
        
        for node in unpickled:
            print node.title + '\n'
        
    
class test_access:
    def GET(self):
        access('test access')
        print 'loaded'