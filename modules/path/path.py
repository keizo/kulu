
import web

from drupy import *


urls = (
    '/admin/path','path'
    )
perms = (
    'create url aliases', 
    'administer url aliases'
    )
    
class path(page):
    @access('administer url aliases')
    def GET(self):
        page = self.page
        
        content = 'path aliasing admin page goes here'
        web.render('generic.html')