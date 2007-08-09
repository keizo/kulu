"""
 * System monitoring and logging for administrators.
 *
 * The watchdog module monitors your site and keeps a list of
 * recorded events containing usage and performance data, errors,
 * warnings, and similar operational information.
 *
 see includes.system.log() function
"""
from web import form
import web
from drupy import *

urls = (
    '/admin/logs','overview',
#    '/admin/logs/hits','hits',
#    '/admin/logs/access-denied','access_denied',
#    '/admin/logs/page-not-found','pagenotfound',
#    '/admin/logs/referrers','referrers',
#    '/admin/logs/status','status'
    )

class overview(page):
    def GET(self):
        page = self.page
        form = form_overview()
        print form.render()
        print 'watchdog overview goes here'
        
def drupy_cron():
    time1 = time() - variable_get('watchdog_clear', 604800)
    time2 = time() - 3600
    web.transact()
    web.query('DELETE FROM watchdog WHERE timestamp < $time1', vars=locals())
    web.query('DELETE FROM flood WHERE timestamp < $time2', vars=locals())
    web.commit()


def user(op):
    """honestly, I'm not sure what this function is for"""
    if op == 'delete':
        #db_query('UPDATE {watchdog} SET uid = 0 WHERE uid = %d', $user->uid);
        pass

def form_overview():
    names = {'all':'all messages'}
    types = web.query('SELECT DISTINCT(type) FROM watchdog ORDER BY type')
    for t in types:
        names[t.values()[0]] = t.values()[0]+' messages'

    #next two lines are cool, but I'm too lazy to implement
    #if empty($_SESSION['watchdog_overview_filter']):
    #    $_SESSION['watchdog_overview_filter'] = 'all';
    f = form.Form(
        form.Dropdown('filter', [(key,names[key]) for key in names],
            description='filter by message type:'
            )
        )
    return f()



