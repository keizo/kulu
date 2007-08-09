import web

# Set up this module as a node module.
drupy_node_module = True

# Make it a generic one.
from modules.node.generic import * 

# Set publishing defaults.
defaults.status = 1
defaults.promote = 1
defaults.comment = 1
defaults.moderate = 1
defaults.sticky = 0