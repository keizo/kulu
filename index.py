#!/usr/bin/env python
"""
a webpy cms
"""
__revision__ = "9"
__license__ = "MIT License"
__author__ = "Keizo Gates <kzo@kzo.net>"

#standard library imports

#webpy imports
import web
import db_params

#drupy imports
import glbl
from drupy import *
import loader
inc = loader.import_('includes')
mod = loader.import_('modules')

#
## URLS
#
# urls for these modules loaded before other modules, in order
pre_modules = ('home','node','user')  
#post_modules = ('path',)
bot_urls = ('/(.*)','url_handler')

# Add in module urls
urls = inc.urls.combine_urls(pre_modules, mod, bot_urls)
print urls


#
## PATH STUFF
# TODO: url_handler and aliased_url should go in the path module? or not...
class url_handler(page):
    def GET(self,url):
        if glbl.url_src.has_key(url):
            web.ctx.path = '/'+glbl.url_src[url]  # Remember to put the leading /
            web.handle(urls,globals())
        else:
            pagenotfound()
            
def aliased_url():
    """
    This function is added to webpy _loadhooks in index.py.
    It loads on every request to check if the called path has been aliased.
    If the called path has been aliased, it redirects to the alias.
    """
    path = web.ctx.path[1:]  # Remove the leading slash '/'
    if glbl.url_dst.has_key(path):
        web.redirect('/'+glbl.url_dst[path])


# Set notfound page to a function in drupy.py
web.webapi.notfound = pagenotfound

print 'starting cheetah templates'
# Load base template
web.render('page.html', asTemplate=True, base='page')

print 'setting up start up middleware'
#
## MIDDLEWARE 
#
class start_mw:
    def __init__(self,app):
        web.load()
        self.load()
        self.app = app
    def __call__(self, e, o): 
        return self.app(e, o)
        
    def load(self):
        glbl.load()

#
## RUN
#
web.webapi.internalerror = web.debugerror
if __name__ == "__main__": 
    print 'setting up db'
    web.config.db_parameters = dict(dbn='mysql', user=db_params.user, pw=db_params.password, db=db_params.database)
    print 'setting up loadhooks'
    web._loadhooks['aliased_url'] = aliased_url 
    
    mw = [start_mw, web.profiler]
    print 'starting server'
    web.run(urls, globals(), *mw)
    
