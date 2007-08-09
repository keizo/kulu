#!/usr/bin/env python
from web import form
import web
from drupy import *
import glbl
import loader
#inc = loader.import_('includes')
mod = loader.import_('modules')

urls = (
    '/admin','admin',
    '/admin/variable','variable',
    )
perms = (
    'administer site configuration', 
    'access administration pages', 
    'select different theme',
    )   

class admin(page):
    @access('access administration pages')
    def GET(self):
        page = self.page
        content = ''
        admin_urls = []
        for key in mod:
            if hasattr(mod[key], 'urls'):
                p = web.group(mod[key].urls,2)
                for pair in p:
                    if pair[0].startswith('/admin/'):
                        admin_urls.append(pair)
                        content += '<p>'+key+' <a href="'+pair[0]+'">'+pair[1]+'</a> '
                        content += str(getattr(mod[key],pair[1]).__doc__)
                        content += '</p>'
                    
        web.render('generic.html')

            
class variable(page):
    """All variables in the system can be edited here."""
    @access('administer site configuration')
    def GET(self):
        page = self.page
        form = form_variable()
        form_new = form_new_variable()
        content = '<form method="post" name="settings">'
        content += form_new.render()
        content += form.render()
        content += '<input type="submit" /></form>'
        web.render('generic.html')
        
    @access('administer site configuration')
    def POST(self):
        page = self.page
        form = form_variable()
        form_new = form_new_variable()
        
        web.transact()
        
        # Insert new
        if form_new.validates():
            form_data = form_new.d
            name = form_data.new_variable_name
            value = form_data.new_variable_value
            if not glbl.variable.has_key(name):
                page.message += '<p>Added variable ' + name + \
                                ' = ' + value + '</p>'
                glbl.variable[name] = value
            else:
                page.message += '<p>Did not add variable ' + \
                                name + \
                                ' because it already exists. </p>' 
            
        # Do updates
        if form.validates():
            form_data = form.d
            for key in form_data:
                # Only update the variable if it changed
                if glbl.variable[key] != form_data[key]:
                    page.message += '<p>Updated ' + key + ' from "' + \
                                    glbl.variable[key] + '" to "' + \
                                    form_data[key] + '".</p>'
                    glbl.variable[key] = form_data[key]
                    
        # Do deletes
        i = web.input(new=[],delete=[])
        if hasattr(i,'delete'):
            for key in i.delete:
                page.message += '<p>Deleted ' + key + '.</p>'
                del glbl.variable[key]
        
        web.commit()
        
        # Gah, there shouldn't be html
        content = '<p><a href="/admin/variable">Refresh settings form</a></p>'
        web.render('generic.html')

def form_variable():
    fields = []
    for key in glbl.variable:
        x = form.Checkbox('delete',value=key).render()
        fields.append(form.Textbox(key,
                value=glbl.variable[key],size=60,
                post = '</td><td>'+x))  # inserting a checkbox in post 
    fields.sort(key=lambda x:x.name)    # is kind of a dirty hack
    return form.Form(*tuple(fields))
    
form_new_variable = form.Form(
    form.Textbox('new_variable_name',
        form.Validator('Cannot have a blank variable', lambda x: len(x)>0),
        size=20),
    form.Textbox('new_variable_value',
        form.Validator('Cannot have a blank variable', lambda x: len(x)>0),
        size=60)
    )