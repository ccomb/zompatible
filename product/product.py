from zope.interface import implements

from interfaces import IProduct
from zompatible.characteristic.characteristic import getCharacteristicInterfaces

class Product(object):
    implements(IProduct)
    
    name = u""
 
    def __init__(self, name=None):
        self.name = name
        
    def Display(self):
        # Display the product name
        s = u'Name: %s' % self.name
        print s
        self.DisplayCharacteristics()
        self.DisplayProducts()
    
    def DisplayCharacteristics(self):
        s = u''
        l = getCharacteristicInterfaces(self)
        for e in l:
            s = u'\n'.join([s, e(self).Display()])
        print s

    def DisplayProducts(self):
        return ""

