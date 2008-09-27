import web

class table:
    
    def __init__(self, header = web.Storage(), rows = [], default_order_by = ''):
        self.header = header
        self.rows = rows
        self.default_order_by = default_order_by
        
    def render(self):
        headers = self._header_html()
        rows = self.rows
        return str(web.render('table.html', asTemplate=True))


    def _header_html(self):
        """
        we'll make the links here, because it's too hard in the template
        """
        i = web.input()
        header_html = []
        
        for n in range(len(self.header.titles)):
            try:
                if i.has_key('order_by'):
                    if self.header.fields[n] == i.order_by:
                        if i.sort == 'asc' or i.sort == 'ASC':
                            self.header.sorts[n] = 'desc'
                        elif i.sort == 'desc' or i.sort == 'DESC':
                            self.header.sorts[n] = 'asc'
                        
                header_html.append(''.join(('<a href="?sort=',
                                        self.header.sorts[n],
                                        '&order_by=',
                                        self.header.fields[n],
                                        '">',
                                        self.header.titles[n],
                                        '</a>')))
            except IndexError:
                header_html.append(self.header.titles[n])
        return header_html

    def order_sql(self, before = ''):
        """Description
        Create an SQL sort clause.

        This function produces the ORDER BY clause to insert in your SQL queries, assuring that the returned database table rows match the sort order chosen by the user.

        header: A list containing the table headers. 
    
        Each element after the first one is a dictionary with the following keys:
            TODO: make it so you only have to put a localized string 

        "title": The localized title of the table column.
        "name": The database field represented in the table column (required if user is to be able to sort on this column).
        "sort": A default sort order for this column ("asc" or "desc").

        $before An SQL string to insert after ORDER BY and before the table sorting code. Useful for sorting by important attributes like "sticky" first.

        Return value
        An SQL string to append to the end of a query.
        """
        i = web.input()

        #decide what field to sort by
        if self.default_order_by:
            order_field = self.default_order_by
        else:
            order_field = self.header.fields[0]
        
        if i.has_key('order_by'):
            if self.header.fields.count(i['order_by']):
                order_field = i['order_by']
        
        #decide asc or desc
        if i.has_key('sort'):
            if i['sort'] == 'asc' or i['sort'] == 'ASC':
                sort = 'ASC'
            else:
                sort = 'DESC'
        else:
            for n in range(len(self.header.fields)):
                if order_field == self.header.fields[n]:
                    sort = self.header.sorts[n]
            
            
        return ' '.join((" ORDER BY",before, order_field, sort.upper()))
