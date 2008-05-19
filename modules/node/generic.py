"""
This file has all the functions needed for a generic node.

To make a new generic node:

1) create a new module with the name of your node type.  e.g. story.py
2) Add the following lines to that file:

# Set up this module as a node module.
drupy_node_module = True
# Make it a generic one.
from modules.node.generic import *

3) There is no step 3!
"""
from web import form
import web

import modules.filter

# Set publishing defaults.
defaults = web.storage({})
defaults.status = 1
defaults.promote = 0
defaults.comment = 1
defaults.moderate = 0
defaults.sticky = 0

def node_load(nid, vid):
    """the node_load for story, page, or other genric node types"""
    try:
        addition = web.query('''SELECT r.vid, r.timestamp \
        AS revision_timestamp, r.title, r.body, r.teaser, r.log, r.format, \
        r.uid FROM node_revisions r WHERE r.nid = $nid AND r.vid = $vid''', 
        vars=locals())[0]
    except IndexError:
        raise "node table out of sync with revisions"
        # TODO:  Report to watchdog that node table
        # and this addition table are out of sync for some reason.
    return addition
    
def node_prepare(node):
    node.read_more = len(node.body) > len(node.teaser)
    if node.format:
        if node.teaser:
            node.teaser = modules.filter.process(node.teaser, node.format)

        # removed any <!--break--> tags
        temp = node.body.split('<!--break-->')
        node.body = ''.join(temp)
        # now apply the usual filters
        node.body = modules.filter.process(node.body, node.format)
    return node
    
def node_insert(node):
    teaser = node.body.split('<!--break-->')[0]  # Create the teaser
    web.insert('node_revisions',nid=node.nid,uid=node.uid,
               teaser=teaser, body=node.body, timestamp=node.time_now, 
               title=node.title, format=node.format)
    
def node_update(node):
   teaser = node.body.split('<!--break-->')[0]  # Create the teaser
   # TODO: add something so it doesn't have to create a new revision
   # every single time we change something.
   new_vid = node.vid + 1
   web.insert('node_revisions',nid=node.nid,vid=new_vid, uid=node.uid,
              teaser=teaser, body=node.body, timestamp=node.time_now, 
              title=node.title, format=node.format)
    
def form_node(users_roles=[1]):
    return form.Form(
        form.Textbox('title',
            size=79),
        form.Textarea('body',
            cols=79,rows=20),
        *modules.filter.form_fields_input_formats(users_roles)
        )
    