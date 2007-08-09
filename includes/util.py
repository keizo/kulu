

#todo - reduce this, we don't need all of webpy here
import web

class Variable(dict):
    """
    A Variable object is like a dictionary, but writes 
    and deletes to the database in addition to the normal 
    in-memory operations.  It is only good for a db table
    that has two columns. e.g. key,value
    
    Does not work with auto-incrementing fields.
    """
    def __init__(self,table,key_field='name',value_field='value'):
        self.table = table
        self.key_field = key_field
        self.value_field = value_field
        
    def load(self):
        self.clear()
        try:
            table_iter = web.select(self.table) #returns iterbetter
            for row in table_iter: #where variable is a storage object
                key = row[self.key_field]
                value = row[self.value_field]
                dict.__setitem__(self,key,value)
            print 'Variable object loaded for', self.table
        except:
            raise

    def __setitem__(self, key, value):
        if self.has_key(key):
            web.update(self.table,where=self.key_field+'=$key',vars=locals(),**{self.value_field:value})
        else:
            web.insert(self.table,**{self.key_field:key,self.value_field:value})
        dict.__setitem__(self,key,value)
    
    def __getitem__(self,key):
        if self.has_key(key):
            return dict.__getitem__(self,key)
        else:
            return '*<!-- missing variable '+key+'-->'

    def __delitem__(self, key):
        if self.has_key(key):
            try:
                web.delete(self.table,where=self.key_field+'=$key',vars=locals())
            except:
                raise
            dict.__delitem__(self,key)
        # Do nothing if there is no key.  TODO: file an error?

    def __repr__(self):
        return '<Variable ' + dict.__repr__(self) + '>'

class VariableList(Variable):
    """
    Just like the class Variable, except each dictionary value is a list.
    
    The lists are stored as comma seperated text in the database.
    """
    def load(self):
        super(VariableList,self).load()
        for key in self:
            self[key] = self[key].split(', ')
            
    def __setitem__(self, key, value):
        super(VariableList,self).__setitem__(key,', '.join(value))
        dict.__setitem__(self,key,value)
        
    def __repr__(self):
        return '<VariableList ' + dict.__repr__(self) + '>'
    
class Bin(dict):
    """
    A Bin object is like a dictionary with web.Storage objects as values.
    It makes writes and deletes to the database in addition to the normal in-memory operations.  
    It also has a sort function.
    
    Does not work with auto-incrementing fields.
    """
    def __init__(self,table,index='id'):
        self.table = table
        self.index = index
        
    def load(self):
        self.clear()
        try:
            table_iter = web.select(self.table) #returns iterbetter
            for row in table_iter: #where variable is a storage object
                index = row[self.index]
                #print index, row
                dict.__setitem__(self,index,row)
        except:
            raise
        print 'bin load function run for', self.table

    def __setitem__(self, key, values):
        #make values a storage object if it's not...
        #there is probably a cleaner way to do this
        if issubclass(values,dict) is not True:
            values = web.storify({key:values})
            
        if self.has_key(key):
            web.update(self.table,where=self.index+'=$key',vars=locals(),**web.storify(values,**self[key]))
        else:
            web.insert(self.table,**web.storify({self.index:key},**values))
        dict.__setitem__(self,key,values)

    #def __getitem__(self,key):
    #    print 'getting item'
    #    try:
    #        return dict.__getitem__(self,key)
    #    except KeyError:
    #        self.__setitem__(key,web.storify({self.index:key}))
    #        return dict.__getitem__(self,key)

    def __delitem__(self, key):
        try:
            web.delete(self.table,where=self.index+'=$key',vars=locals())
        except KeyError, k:
            raise AttributeError, k
        dict.__delitem__(self,key)

    def __repr__(self):
        return '<Bin ' + dict.__repr__(self) + '>'

    def sort(self,by='id',reverse=False):
        return sorted(self.values(),key=lambda i:(i[by]),reverse=reverse)

