


# it's like I'm retarded and have add... started and didn't finish

def tablesort_sql($header, $before = ''):
"""Description
Create an SQL sort clause.

This function produces the ORDER BY clause to insert in your SQL queries, assuring that the returned database table rows match the sort order chosen by the user.

Parameters
$header A list of column headers in the format described in theme_table().

$before An SQL string to insert after ORDER BY and before the table sorting code. Useful for sorting by important attributes like "sticky" first.

Return value
An SQL string to append to the end of a query.
"""
  $ts = tablesort_init($header);
  if ($ts['sql']):
    // Based on code from db_escape_table(), but this can also contain a dot.
    $field = preg_replace('/[^A-Za-z0-9_.]+/', '', $ts['sql']);

    // Sort order can only be ASC or DESC.
    $sort = drupal_strtoupper($ts['sort']);
    $sort = in_array($sort, array('ASC', 'DESC')) ? $sort : '';

    return " ORDER BY $before $field $sort";
