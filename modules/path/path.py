
from drupy import *


urls = (
    '/admin/path','path'
    )
perms = (
    'create url aliases', 
    'administer url aliases'
    )
    
class path(page):
    def GET(self):
        print 'path aliasing admin page goes here'
        