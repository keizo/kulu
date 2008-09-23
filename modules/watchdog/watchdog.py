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
import loader
inc = loader.import_('includes')

urls = (
    '/admin/logs','watchdog_overview',
    '/admin/logs/recent', 'watchdog_recent',
#    '/admin/logs/hits','hits',
#    '/admin/logs/access-denied','access_denied',
#    '/admin/logs/page-not-found','pagenotfound',
#    '/admin/logs/referrers','referrers',
#    '/admin/logs/status','status'
    )

class watchdog_overview(page):
    def GET(self):
        page = self.page
        form = form_overview()
        content = form.render()
        content += 'watchdog overview goes here'
        web.render('generic.html')

        
class watchdog_recent(page):
    def GET(self):
        page = self.page
        
        sortable_headers = ['timestamp', 'type', 'message', 'name']
        order_sql = inc.tablesort.sql(sortable_headers)
        
        iter_entries, page_nums = inc.pager.query('''SELECT w.wid, \
        w.uid, w.severity, w.type, w.timestamp, w.message, w.link, \
        u.name FROM watchdog w INNER JOIN users u \
        ON w.uid = u.uid'''+order_sql, limit=100)
        
        headers = [ {'title':'Type', 'name':'type'},
                    {'title':'Date', 'name':'timestamp', 'sort':'desc'}, 
                    {'title':'Message', 'name':'message'}, 
                    {'title':'User', 'name':'name'} ]
        rows = []
        for entry in iter_entries:
            rows.append( (str(entry.type),
                          str(inc.common.format_date(entry.timestamp)),
                          str(entry.message),
                          str(entry.name),
                          'put operation here') )

        table = str(web.render('table.html', terms={'rows':rows, 'headers':headers}, asTemplate=True))

        content = table
        # i'm so fucking lazy, figure out the right way to do this.  
        # ie a template, or theme function call like drupal
        '''
        content = '<table><tr><th>type</th><th>date</th><th>message</th><th>user</th><th>operations</th>'
        for entry in iter_entries:
            content += '<tr>'
            content += ''.join(('<td>', str(entry.type), '</td>'))
            content += ''.join(('<td>', str(inc.common.format_date(entry.timestamp)), '</td>'))
            content += ''.join(('<td>', str(entry.message), '</td>'))
            content += ''.join(('<td>', str(entry.name), '</td>'))
            content += ''.join(('<td>','put operation here', '</td>'))
            content += '</tr>'
        content += '</table>'
         '''
            
        content += page_nums.render()
        web.render('generic.html')
        
        
def drupy_cron():
    """clean out old stuff in the watchdog table"""
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



