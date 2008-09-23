import web


def header_html(header):
    """
    $header An array containing the table headers. Each element of the array can be either a localized string or an associative array with the following keys:

    "data": The localized title of the table column.
    "field": The database field represented in the table column (required if user is to be able to sort on this column).
    "sort": A default sort order for this column ("asc" or "desc").
    """
    pass

def sql(sortable_headers, before = ''):
    """Description
    Create an SQL sort clause.

    This function produces the ORDER BY clause to insert in your SQL queries, assuring that the returned database table rows match the sort order chosen by the user.

    Parameters
    sortable_headers - is a list of the database fields which the table
    can be sorted by.  the first field listed is the default thing to
    sort by.

    $before An SQL string to insert after ORDER BY and before the table sorting code. Useful for sorting by important attributes like "sticky" first.

    Return value
    An SQL string to append to the end of a query.
    """
    sort = 'ASC'
    i = web.input()
    if i.has_key('sort'):
        if i['sort'] is 'desc' or i['sort'] is 'DESC':
            sort = 'DESC'
    else:
        #TODO: look for default sort orders passed in by header argument
        pass
    
    order_field = sortable_headers[0]
    if i.has_key('order_by'):
        if i['order_by'] in sortable_headers:
            order_field = i['order_by']
            
    return ' '.join((" ORDER BY",before, order_field, sort))
