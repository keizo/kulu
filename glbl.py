"""global variables always kept in memory
module is named glbl since global is reserved."""

__all__ = ["constant","variable","perm","role","url_dst","url_src"]

import loader
inc = loader.import_('includes')

from web.utils import storage

constant = storage({
    'anonymous_role_id':1,
    'authenticated_role_id':2,
    'remember_me_length':2592000, #30 days
    'watchdog_notice':0,
    'watchdog_warning':1,
    'watchdog_error':2,
    })

#
## Database tables kept in memory
#
variable = inc.util.Variable('variable', key_field='name', value_field='value')

# Keeping permissions and roles in memory probably isn't a great idea if
# there's going to be lots and lots of roles.  Ok since I only have a few.
perm = inc.util.Variable('permission', key_field='rid', value_field='perm')
role = inc.util.Variable('role', key_field='rid', value_field='name')

# src is the place the actual page is. 
# e.g. 'node/186' is the src, 'about' is the dst
url_dst = inc.util.Variable('url_alias', key_field='src', value_field='dst')
url_src = inc.util.Variable('url_alias', key_field='dst', value_field='src')

# filters 
filter = inc.util.VariableList('filter', key_field='format', value_field='modules')
filter_roles = inc.util.VariableList('filter', key_field='format', value_field='roles')
# using the word 'filter' overrides the function filter, 
# but I guess we won't ever use it here...

def load():
    # Load into memory from database
    variable.load()
    perm.load()
    role.load()
    url_dst.load()
    url_src.load()
    filter.load()
    filter_roles.load()
    
    # TODO: set defaults
    # check to see if this works:
    # variable.setdefault('site_name','drupy website')
    # variable.setdefault('','')
    # variable.setdefault('recaptcha_public_key', 
    #    '6Lf4MwAAAAAAAOlBfZz1o7kYrUBVUk8bJ8XQ1IKH')
    # variable.setdefault('recaptcha_private_key', 
    #    '6Lf4MwAAAAAAACa4W-4akk6je10IBNFkFOxL3iIL')
    # variable.setdefault('email_admin','')