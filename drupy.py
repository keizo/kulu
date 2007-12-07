#!/usr/bin/env python
"""
pages.py contains stuff that gets used everywhere
from pages import *
"""
__revision__ = "9"
__license__ = "MIT License"
__author__ = "Keizo Gates <kzo@kzo.net>"

__all__ = ["page","pagenotfound","access","checkaccess","hasaccess"]

#python imports

#webpy imports
import web

#drupy imports
import glbl
import loader
inc = loader.import_('includes')

#
## base page from which other pages can inherit
#
class page:
    def __init__(self):
        print 'page init'
        self.page = web.storage()
        self.page.path = web.ctx.path
        self.page.variable = glbl.variable
        self.page.title = ''
        self.page.message = ''
        self.page.user = inc.session.read()
        print self.page.user
        #self.sess()
        
    def sess(self):
        inc.session.write(self.page.user.sid,'',user=self.page.user)

def pagenotfound():
    """the parameter page is self.page from the calling class"""
    page = web.storage()
    page.path = web.ctx.path
    page.variable = glbl.variable
    page.title = ''
    page.message = ''
    page.user = inc.session.read()
    inc.session.write(page.user.sid,'',user=page.user)
    web.render('pagenotfound.html')
    
def access(*perms):
    """
    A decorator for GET() and POST() functions that enforces user access.
    
    e.g.
    class user_profile(page):
        @access('view user profiles')
        def GET(self):
            print 'I have an awesome profile.'
    """
    def decorator(func): 
        def proxyfunc(self, *args, **kw):
            checkaccess(self.page.user, *perms)
            return func(self, *args, **kw)
        return proxyfunc
    return decorator

def checkaccess(user, *perms):
    """
    Enforces user access, but not using a decorator.  Instead the user 
    needs to be passed in.  Useful if you don't know the perms before the
    function is called -- as in node.py
    """
    # TODO: replace the next four lines with hasaccess function
    for user_rid in user.roles:
        for p in perms:
            if p in glbl.perm[int(user_rid)]:
                return True
    print 'access denied'
    web.redirect('/denied?url='+web.ctx.path)
    
def hasaccess(user, *perms):
    """Returns a bool.  True if user has the perms, false if not."""
    for user_rid in user.roles:
        for p in perms:
            if p in glbl.perm[int(user_rid)]:
                return True
    return False