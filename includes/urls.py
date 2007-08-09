
import web

import glbl

def combine_urls(pre_modules, mod, bot_urls):
    """
    In webpy urls are set up in a tuple. When a request is made the tuple
    is searched linearly in order.  So we want the most common urls searched 
    first and least common or catch-all type urls last.  The tuple top_urls 
    are first.  Then urls created by modules are appended.  Finally the tuple 
    bot_urls is added last.
    
    core_mod is a tuple of ordered module names that have their urls loaded
        before the rest of the modules.
        
    mod is all the available modules imported by loader.py
    """
    url_list = []
    mod_list = mod.keys()
    mod_list.sort()
    print mod_list
    
    # TODO: there is a giant chunk of repated code here. Fix it.
    for module_name in pre_modules:
        if hasattr(mod[module_name], 'urls'):
            mod_urls = list(mod[module_name].urls)
            for i in range(len(mod_urls)):
                if i%2: mod_urls[i] = 'modules.'+module_name+'.'+mod_urls[i]
            url_list.extend(mod_urls)
            mod_list.remove(module_name)
            
    for module_name in mod_list:
        if hasattr(mod[module_name], 'urls'):
            mod_urls = list(mod[module_name].urls)
            for i in range(len(mod_urls)):
                if i%2: mod_urls[i] = 'modules.'+module_name+'.'+mod_urls[i]
            url_list.extend(mod_urls)
    
    url_list.extend(bot_urls)
    return tuple(url_list)
