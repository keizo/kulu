#!/usr/bin/env python

#is this just a test file?


import os,sys
import web
import sha
from web import form

import db_params

import loader


from drupy import *

import includes.pager as pager

urls = (
    '/', 'index',
    '/test','test',
    '/pager','pager_test',
    '/checkbox','checkbox',
)
#
## pages
#

class index:
    def GET(self):
        print web.cookies()
        web.render('page.html')
        
class pager_test:
    def GET(self):
        print web.input()
        
        print pager.query('SELECT n.nid FROM node n WHERE n.nid=11 ORDER BY n.nid',_test=True)

        print pager.query('''SELECT n.nid, r.vid, n.type, n.status, n.created, \
            n.changed, n.comment, n.promote, n.sticky, r.timestamp AS revision_timestamp, \
            r.title, r.body, r.teaser, r.log, r.format, u.uid, u.name, u.picture, u.data \
            FROM node n INNER JOIN users u ON u.uid = n.uid INNER JOIN node_revisions r \
            ON r.nid = n.nid AND r.vid = n.vid WHERE n.promote = 1 AND n.status = 1 \
            ORDER BY n.sticky DESC, n.created DESC''',_test=True)

class test:
    def GET(self):
        cookie = Cookie.SimpleCookie()
        cookie.load(web.ctx.env.get('HTTP_COOKIE', ''))
        web.setcookie("cookiename", 'value',expires=4444444)
        web.setcookie("cookiename", 'no',expires=22222)
        print cookie
        print web.ctx
        print web.ctx.homedomain
        print web.ctx.fullpath
        print web.input()
myform = form.Form(form.Checkbox('mycheckbox',checked='checked',value='poo'))
class checkbox:
    def GET(self):
        print '<html><body>'
        print '<form name="blah" method="post">'
        print '<input type="checkbox" name="boo" value="hoo" />'
        print '<input type="checkbox" name="boo" value="poo" />'
        print '<input type="checkbox" name="noo" checked="false" />'
        print '<input type="checkbox" name="noo" checked="checked" />'
        print myform.render()
        print '<input type="submit" />'
        print '</form></body></html>'
    def POST(self):
        print web.input(boo=[], noo=[])
#
## MIDDLEWARE FACTORIES
#
def session_mw(app):
    sessionStore = DatabaseSessionStore(timeout=5)
    return SessionMiddleware(sessionStore, app) 


#web.webapi.internalerror = web.debugerror
if __name__ == "__main__": 
    web.config.db_parameters = dict(dbn='mysql', user=db_params.user, pw=db_params.password, db=db_params.database)
    
    #production:
    #web.run(urls, globals(), *[session_mw])
    
    #development laptop:
    web.internalerror = web.debugerror
    web.run(urls, globals(), *[web.reloader])
