#!/usr/bin/env python
"""
a webpy cms
"""
__revision__ = "9"
__license__ = "MIT License"
__author__ = "Keizo Gates <kzo@kzo.net>"

#webpy imports
import web, db_params

#drupy imports
import loader
inc = loader.import_('includes')

from PHPUnserialize import *



def convert_variable_table():
    """this unserializes (a php thing) the variable table so that python can understand it"""
    variable = inc.util.Variable('variable', key_field='name', value_field='value')
    variable.load()
    #web.transact()
    u = PHPUnserialize()
    for v in variable.iteritems():
        try:
            unserialized = u.unserialize(v[1])
            variable[v[0]] = unserialized
            print 'converted',v[0]
        except:
            print v[0],'skipped',v[1]
    #web.commit()
    
if __name__ == "__main__": 
    web.config.db_parameters = dict(dbn='mysql', user=db_params.user, pw=db_params.password, db=db_params.database)
    web.load()
    convert_variable_table()