import time
import cPickle as pickle
from web import form
import web

import glbl
from drupy import *
import loader
inc = loader.import_('includes')
mod = loader.import_('modules')

urls = (
    '/node/(\d+)','node',
    '/node/(\d+)/edit','node_edit',
    '/node/add/(.+)','node_add',
    )
perms = ('most modules can set perms here as a tuple, but not this one',)

class node(page):
    def GET(self,nid):
        page = self.page
        node = mod.node.load(nid)
        if node is None:
            pagenotfound()
        else:
            links = ''
            page.title = node.title
            try:
                web.render(''.join(('node-',node.type,'.html')))
            except:
                web.render('node.html')

class node_add(page):
    def GET(self, node_type):
        page = self.page
        f = _form_node(node_type, page.user.roles.keys())
        if not f: pagenotfound()
        else:
            checkaccess(page.user, ''.join(('create ',node_type,' content')))
            content = '<form method="post" name="new_node">'
            content += f.render()
            content += '<input type="submit" /></form>'
                        
            web.render('generic.html')
        
    def POST(self, node_type):
        page = self.page
        form = _form_node(node_type, 
                page.user.roles.keys())  # checks if this node_type exists too
        checkaccess(page.user, ''.join(('create ',node_type,' content')))
        
        if form.validates():
            node = form.d
            node.time_now = int(time.time())
            node.uid = page.user.uid
            
            # Get publishing settings.
            options = mod[node_type].defaults
            
            # Insert main entry in 'node' table
            node.nid = web.insert('node',uid=page.user.uid,created=node.time_now,
                             changed=node.time_now, title=node.title, type=node_type,
                             **options)
                             
            # Do module specific insertions.
            if hasattr(mod[node_type], 'node_insert'):
                mod[node_type].node_insert(node)

            web.redirect('/node/'+str(node.nid))
            
        content = '<form method="post" name="new_node">'
        content += form.render()
        content += '<input type="submit" /></form>'
        web.render('generic.html')

class node_edit(page):
    def GET(self, nid):
        page = self.page
        node = mod.node.load(nid)
        if node is None:
            pagenotfound()
        else:
            self._checkaccess(node)
            form = _form_node(node.type, page.user.roles.keys())
            form.fill(node)
            
            content = '<form method="post">'
            content += form.render()
            content += '<input type="submit" /></form>'
            web.render('generic.html')
            
    def POST(self, nid):
        page = self.page
        node = mod.node.load(nid)
        if node is None:
            pagenotfound()
        else:
            self._checkaccess(node)
            form = _form_node(node.type, page.user.roles.keys())
            
            if form.validates():
                content = form.d
                
                web.render('generic.html')
                
    def _checkaccess(self, node):
        if self.page.user.uid and self.page.user.uid == node.uid:  # user is the owner
            # CAVEAT: even if anyone can edit, the owner can edit only
            # if 'edit own' is checked too
            checkaccess(self.page.user, ''.join(('edit own ',node.type,' content')))
        else:  # anyone else
            checkaccess(self.page.user, ''.join(('edit ',node.type,' content')))
#
## FUNCTIONS
#
def _perms():
    """dynamically create permissions for all node types available"""
    perms = ['administer content types', 'administer nodes', 'access content',
            'view revisions', 'revert revisions']
    for key in mod:
        if hasattr(mod[key],'drupy_node_module'):
            perms.append(''.join(('create ',key,' content')))
            perms.append(''.join(('edit own ',key,' content')))
            perms.append(''.join(('edit ',key,' content')))
            perms.append(''.join(('delete own ',key,' content')))
            perms.append(''.join(('delete ',key,' content')))
    return tuple(perms)
perms = _perms()

def load(nid, revision = None, **args):
    try:  # TODO: put less code in this try, (pep8)
        node = web.query('''SELECT n.nid, n.vid, c.cache, \
        c.nid AS cache_nid, c.vid AS cache_vid, n.type, n.status, \
        n.created, n.changed, n.comment, n.promote, n.sticky, \
        u.uid, u.name, u.picture, u.data FROM node n INNER JOIN users u \
        ON u.uid = n.uid LEFT JOIN cache_node c ON c.nid = n.nid \
        AND c.vid = n.vid WHERE n.nid = $nid''', vars=locals())[0]
    except IndexError:
        return None
        # TODO: file a watchdog error here?
    if revision:
        node.rid = revision

    if node.nid:  # Is a valid node
        # Prepare node by adding additional data and processing filters
        node = _prepared(node)
    return node

def listing_default(limit=0):
    """Returns a list of nodes (web.storage objects) in descending order
    that have been published and promoted to the front page."""
    nodes = []
    if not limit: limit = int(glbl.variable['default_nodes_main'])
    iter_nodes, page_nums = inc.pager.query('''SELECT n.nid, c.cache, c.nid \
        AS cache_nid, c.vid as cache_vid, n.vid, n.type, \
        n.status, n.created, n.changed, n.comment, n.promote, n.sticky, \
        u.uid, u.name, u.picture, u.data FROM node n INNER JOIN \
        users u ON u.uid = n.uid LEFT JOIN cache_node c ON c.nid = n.nid \
        AND c.vid = n.vid WHERE n.promote = 1 AND n.status = 1 \
        ORDER BY n.sticky DESC, n.created DESC''',limit=limit)
    for node in iter_nodes:
        # Piggy back the data from other modules depending on the node type.
        # This uses only as many db queries as there are types.
        # The way it is now is fine, until many nodes on the default page 
        # are not default node types.
        nodes.append(_prepared(node, teaser=True))
    return nodes, page_nums
    
def render_many(nodes):
    """Returns a string containing the templated output of node teasers."""
    t = []
    for node in nodes:
        try:
            t.append(str(web.render(''.join(('node-',node.type,'_teaser.html')), asTemplate=True)))
        except:
            t.append(str(web.render('node_teaser.html', asTemplate=True)))
    return ''.join(t)

def _prepared(node, teaser=False):
    if node.cache:
        cached = pickle.loads(node.cache)
        
        # override the user info in cached, since when the user updates their
        # profile, it will not update the node cache
        cached.name = node.name
        cached.picture = node.picture
        return cached
    
    # Proceed to build the node from scratch.
    
    # Merge data created by node modules.
    node = _node_load(node)
    
    # Apply filters or other preperations.
    node = _node_prepare(node, teaser=teaser)
    
    # Cache all that work so we never have to do it until something changes.
    pickled = pickle.dumps(node)
    if node.cache_nid:
        web.update('cache_node',where='nid=$node.nid AND vid=$node.vid',
            created=time.time(), cache=pickled)
    else:
        web.insert('cache_node',nid=node.nid,vid=node.vid,
            created=time.time(),cache=pickled)
    
    return node
    
def _node_load(node):
    """Piggy back the data from node modules if available."""
    if mod.has_key(node.type) and hasattr(mod[node.type], 'node_load'):
        additions = mod[node.type].node_load(node.nid,node.vid)
        node = web.storify(additions,**node)
    return node
    
def _node_prepare(node, teaser=False):
    """Apply preperations specified in the node module's 'node_prepare'
    function.  This includes text filters and default node parameters."""
    if mod.has_key(node.type) and hasattr(mod[node.type], 'node_prepare'):
        node = mod[node.type].node_prepare(node, teaser)
    return node
        
def drupy_cron():
    """Clean the cache_node table."""
    pass
    
#
## FORMS
#

def _form_node(node_type, users_roles=[1]):
    if mod.has_key(node_type) and \
       hasattr(mod[node_type], 'drupy_node_module') and \
       hasattr(mod[node_type], 'form_node'):
        return mod[node_type].form_node(users_roles)
    else:  # non-existant node
        return False  #TODO: file watchdog error?