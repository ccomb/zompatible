from zope.interface import implements

from interfaces import IProduct

class Product(object):
    implements(IProduct)
    
    name = u""
 
    def __init__(self, name=None):
        self.name = name
        
    def Display(self):
        s = u'Name: %s' % self.name
        return s
    
    


