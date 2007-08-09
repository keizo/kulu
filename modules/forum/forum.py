
import web

from drupy import *

urls = (
    '/forum()','forum',
    '/forum/(.+)','forum',
    )
perms = (
    'create forum topics', 
    'edit own forum topics', 
    'administer forums',
    )
    
class forum(page):
    GET = web.autodelegate('GET_')
    def GET_(self):
        page = self.page
        content = 'forum index'
        web.render('generic.html')

    def GET_test(self):
        print 'test'
