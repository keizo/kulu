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
import includes as wd

from PHPUnserialize import *



def convert_variable_table():
    
    variable = inc.Variable('variable',key_field='name',value_field='value')
    variable.load()
    #web.transact()
    u = PHPUnserialize()
    for v in variable.iteritems():
        try:
            unserialized = u.unserialize(v[1])
            variable[v[0]] = unserialized
        except:
            print v[0],'skipped',v[1]
    #web.commit()
    
if __name__ == "__main__": 
    web.config.db_parameters = dict(dbn='mysql', user=db_params.user, pw=db_params.password, db=db_params.database)
    web.load()
    convert_variable_table()