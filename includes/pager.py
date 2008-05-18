"""
Drupal doc:
/**
 * Perform a paged database query.
 *
 * Use this function when doing select queries you wish to be able to page. The
 * pager uses LIMIT-based queries to fetch only the records required to render a
 * certain page. However, it has to learn the total number of records returned
 * by the query to compute the number of pages (the number of records / records
 * per page). This is done by inserting "COUNT(*)" in the original query. For
 * example, the query "SELECT nid, type FROM node WHERE status = '1' ORDER BY
 * sticky DESC, created DESC" would be rewritten to read "SELECT COUNT(*) FROM
 * node WHERE status = '1' ORDER BY sticky DESC, created DESC". Rewriting the
 * query is accomplished using a regular expression.
 *
 * Unfortunately, the rewrite rule does not always work as intended for queries
 * that already have a "COUNT(*)" or a "GROUP BY" clause, and possibly for
 * other complex queries. In those cases, you can optionally pass a query that
 * will be used to count the records.
 *
 * For example, if you want to page the query "SELECT COUNT(*), TYPE FROM node
 * GROUP BY TYPE", pager_query() would invoke the incorrect query "SELECT
 * COUNT(*) FROM node GROUP BY TYPE". So instead, you should pass "SELECT
 * COUNT(DISTINCT(TYPE)) FROM node" as the optional $count_query parameter.
 *
 * @param $query
 *   The SQL query that needs paging.
 * @param $limit
 *   The number of query results to display per page.
 * @param $element
 *   An optional integer to distinguish between multiple pagers on one page.
 * @param $count_query
 *   An SQL query used to count matching records.
 * @param ...
 *   A variable number of arguments which are substituted into the query (and
 *   the count query) using printf() syntax. Instead of a variable number of
 *   query arguments, you may also pass a single array containing the query
 *   arguments.
 * @return
 *   A database query result resource, or FALSE if the query was not executed
 *   correctly.
 *
 * @ingroup database
"""
import re
import web


def query(sql_query, vars={}, limit = 10, count_query = None, processed=False, _test=False):
    """Works very similar to web.query(), but it returns a tuple of the query result 
    and pager object (which just holds the page numbers links to display)
    
    Typical use:
    iter_nodes, page_nums = inc.pager.query('SELECT * FROM node WHERE uid=5 ORDER BY nid')
    for node in iter_nodes:
        print node
    print page_nums.render()
    
    DOCTEST
    >>> import pager
    >>> limit=10
    >>> iter_nodes, page_nums = pager.query('''SELECT n.nid, c.cache, c.nid \
    ...     AS cache_nid, c.vid as cache_vid, n.vid, n.type, \
    ...     n.status, n.created, n.changed, n.comment, n.promote, n.sticky, \
    ...     u.uid, u.name, u.picture, u.data FROM node n INNER JOIN \
    ...     users u ON u.uid = n.uid LEFT JOIN cache_node c ON c.nid = n.nid \
    ...     AND c.vid = n.vid WHERE n.promote = 1 AND n.status = 1 \
    ...     ORDER BY n.sticky DESC, n.created DESC''',limit=limit, _test=True)
    count_query: SELECT COUNT(*) FROM node n INNER JOIN     users u ON u.uid = n.uid LEFT JOIN cache_node c ON c.nid = n.nid     AND c.vid = n.vid WHERE n.promote = 1 AND n.status = 1    
    >>> iter_nodes
    <sql: 'SELECT n.nid, c.cache, c.nid     AS cache_nid, c.vid as cache_vid, n.vid, n.type,     n.status, n.created, n.changed, n.comment, n.promote, n.sticky,     u.uid, u.name, u.picture, u.data FROM node n INNER JOIN     users u ON u.uid = n.uid LEFT JOIN cache_node c ON c.nid = n.nid     AND c.vid = n.vid WHERE n.promote = 1 AND n.status = 1     ORDER BY n.sticky DESC, n.created DESC LIMIT 10 OFFSET 40'>
    
    NOTE: right now the regex only works when the sql is all caps.  
        i.e. inc.pager.query('select * From node WHERE uid=5 ORDER BY nid')
        would not work.  It's a good convention, but maybe should fix the regex
        to accept non caps in the future?
    """

    if not processed and not isinstance(sql_query, web.db.SQLQuery):
        sql_query = str(web.db.reparam(sql_query, vars))

    if not count_query:
        p = re.compile(r'SELECT.*?FROM (.*) ORDER BY .*')
        count_query = p.sub(lambda m: "SELECT COUNT(*) FROM %s" % m.group(1), sql_query)

    if _test:
        num_pages=10
        page = 5
        print 'count_query:', count_query
    else:
        count = web.query(count_query)[0].values()[0]
        num_pages = int(float(count) / limit + 1)
        page = _current_page()
    
    #page number validation
    #todo !!! wait a minute, maybe these two lines are no good. 
    # cause then there can be many urls for the first and last pages...
    if page < 1: page=1
    elif page > num_pages: page=num_pages
    
    p = pager(page,num_pages)
    
    offset = (page-1)*limit
    return web.query(''.join((sql_query,' LIMIT $limit OFFSET $offset')),
            vars={'limit':limit,'offset':offset},_test=_test), p

class pager:
    """ an object to keep track of page numbers. It is passed back on a pager query
        and can be rendered in the same way as webpy forms are.  i.e. page_nums.render()
        An optional argument 'show' changes how many page numbers to display at once.
    """
    def __init__(self,current,total):
        self.current = current
        self.total = total
        
    def render(self,show=7):
        page_nums = self._page_nums(self.current,self.total,show=show)
        current = self.current
        path = web.ctx.path
        if page_nums:
            return str(web.render('page_nums.html', asTemplate=True))
        return ''

    def _page_nums(self,current,total,show):
        """ returns a list of tuples like [(1,1),(2,2),(3,3),(4,Next)]
            This gets passed to the template.  In each tuple, the first
            parameter is the page number, the second is the link name used
            in the anchor tag.
        """
        p = []
        
        if current > 1:
            p.append((current-1,'&#171; previous'))
        else: p.append((None,'&#171; previous'))
        
        if current > show/2+1:
            p.append((1,1))
        if current > show/2+2:
            p.append((None,'&#0133;'))
        
        if current <= show/2:
            for i in range(1,show+1):
                p.append((i,i))
        elif current >= total-show/2:
            for i in range(total-show+1,total+1):
                p.append((i,i))
        else:
            for i in range(current-show/2,current+show/2+1):
                p.append((i,i))
        
        if current < total-show/2-1:
            p.append((None,'&#0133;'))
        if current < total-show/2:
            p.append((total,total))
        
        if current <  total:
            p.append((current+1,'next &#187;'))
        else: p.append((None,'next &#187;'))
        
        return p

def _current_page():
    """returns the 'page' number from the GET input after verifying that it's an integer."""
    if web.input().has_key('page'):
        try:
            return int(re.match(r'\d+',web.input()['page']).group(0))
        except:
            pass
    else: return 1