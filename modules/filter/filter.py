import md5

from web import form
import web

from drupy import *
import glbl
import loader
#inc = loader.import_('includes')
mod = loader.import_('modules')

urls = (
    '/admin/filters','filter',
    #'/admin/filters/(.+)','edit_filter',
    
    )
perms = ('administer filters',)
    
class filter(page):
    @access('administer filters')
    def GET(self):
        page = self.page
        form = form_edit_filters()
        content = 'filters available:'+str(_filters_available())
        content += '<form method="post">'
        content += form.render()
        content += '<input type="submit" /></form>'
        web.render('generic.html')
        
    @access('administer filters')
    def POST(self):
        page = self.page
        form = form_edit_filters()
        
        if form.validates():
            i = form.d
            query = web.select('filter')
            for input_format in query:
                if hasattr(i,input_format.name):
                    values = i[input_format.name].split(',')
                    values = [x.strip() for x in values]
                    glbl.filter[int(input_format.format)] = values
                    
            # clear the cache on updating filters
            # TODO: make this only clear the affected nodes, instead of all
            web.query('TRUNCATE TABLE  `cache_node`')
        
        web.redirect('/admin/filters')

#
## FUNCTIONS
#

def process(text, format = 1, check = True):
    """
    * Run all the enabled filters on a piece of text.
    *
    * @param $text
    *    The text to be filtered.
    * @param $format
    *    The format of the text to be filtered. Specify FILTER_FORMAT_DEFAULT for
    *    the default format.
    * @param $check
    *    Whether to check the $format with filter_access() first. Defaults to TRUE.
    *    Note that this will check the permissions of the current user, so you
    *    should specify $check = FALSE when viewing other people's content. When
    *    showing content that is not (yet) stored in the database (eg. upon preview),
    *    set to TRUE so the user's permissions are checked.
    """
    # When check = TRUE, do an access check on format.
    #if (isset($text) && (!$check || filter_access($format))) {
    #$format = filter_resolve_format($format);

    # Check for a cached version of this piece of text.
    #cid = str(format) + ':' + md5.new(text).hexdigest()
    #query = web.select('cache_filter', where='cid=$cid',vars=locals())
    #cached_text = ''
    #try:
    #    cached_text = query[0]
    #except:
    #    pass
        
    #if cached_text:
    #    text = str(cached_text.data)
    #if ($cached = cache_get($id, 'cache_filter')) {
    #  return $cached->data;
    #}

    # See if caching is allowed for this format.
    #$cache = filter_format_allowcache($format);
    
    if not text:  # Make sure there is text to filter.
        return ''

    # Convert all Windows and Mac newlines to a single newline,
    # so filters only need to deal with one possibility.
    text = text.replace("\r\n", "\n")
    text = text.replace("\r","\n")

    # Get a complete list of filters, ordered properly.
    #filters = filter_list_format(format);

    # Give filters the chance to escape HTML-like data such as code or formulas.
    #foreach ($filters as $filter) {
    #  $text = module_invoke($filter->module, 'filter', 'prepare', $filter->delta, $format, $text);
    

    # Perform filtering.
    for module in glbl.filter[int(format)]:
        if mod.has_key(module):
            text = mod[module].drupy_filter(text) 

    # Store in cache with a minimum expiration time of 1 day.
    #if ($cache) {
    #  cache_set($id, 'cache_filter', $text, time() + (60 * 60 * 24));

    return text
    
    

def _filters_available():
    """A list of all filter modules available."""
    filters = []
    for name in mod:
        if hasattr(mod[name],'drupy_filter'):
            filters.append(name)
    return filters
    
def _make_edit_form():
    """Returns a list of textbox fields."""
    query = web.query('SELECT * FROM filter ORDER BY format ASC',vars=locals())
    fields = []
    for f in query:
        fields.append(form.Textbox(f.name,value=f.modules,size=60))
    return fields
    

#
## FORMS
#
def form_edit_filters():
    return form.Form(*tuple(_make_edit_form()))
    
def _formats_available(roles=[]):
    formats_keys = web.storage()
    formats = []
    # TODO: this is ugly and who knows if it works everytime.
    for format in glbl.filter_roles:
        for role in roles:
            #print format, role, glbl.filter_roles[format], '<br />'
            if str(role) in glbl.filter_roles[format]:
                formats_keys[format]=glbl.filter[format]
    query = web.query('SELECT * FROM filter ORDER BY format ASC')
    for fil in query:
        if formats_keys.has_key(fil.format):
            formats.append(fil)
    return formats
    
def form_fields_input_formats(users_roles=[1]):
    """Returns a form item of input formats available to roles."""
    formats = _formats_available(users_roles)
    formats_allowed = [f.format for f in formats]
    fields = []
    if len(formats) > 1:  # Multiple formats available
        a = {'desc':'Input Formats'}
        for f in formats:
            fields.append(form.Radio('format',
                [(f.format,f.name)], 
                form.Validator('No permission to use that input format.',
                    lambda x: int(x) in formats_allowed),
                description=a.pop('desc',''), value=formats[0].format,
                ))

    else:  # Only one format available: use a hidden form item and only show tips.
        f = formats[0]
        fields.append(form.Hidden('format',
            form.Validator('No permission to use that input format.',
                lambda x: int(x) in formats_allowed),
            value=f.format, post=f.tips))
    return tuple(fields)