"""a node module creates a content type 'link' 
The node type contains a single link and description"""

import web
from drupy import *

drupy_node_module = True

urls = ('/links','links')

class links:
    def GET(self):
        path = web.ctx.path
        variable = glbl.variable
        user = web.storage({'uid':0})
        limit = int(variable['default_nodes_main'])
        nodes = mod.node.node_load_many(limit)
        content = mod.node.node_render_many(nodes)
        web.render('index.html')


def node_load(nid, vid, **args):
    #todo - rewrite query as web.select()
    try:
        node = web.query('''SELECT l.field_link_value, l.field_description_value,
            l.field_description_format 
            FROM content_type_link l 
            WHERE l.vid = $vid AND l.nid = $nid''', vars=locals())[0]
    except IndexError:
        return None
        #file a watchdog error here?

    return node
    
def node_load_many(limit=10):
    """returns a list of node web.storage objects"""
    # this function is not used yet
    nodes = []
    iter_nodes = web.query('''SELECT n.nid, l.field_link_value, l.field_description_value,
        l.field_description_format FROM node n INNER JOIN content_type_link l 
        ON n.nid = l.nid AND n.vid = l.vid WHERE n.promote = 1 AND n.status = 1 \
        ORDER BY n.sticky DESC, n.created DESC LIMIT $limit''', vars=locals())
    for node in iter_nodes:
        #todo - piggy back and info from other modules depending on the node type
        nodes.append(node)
    return nodes