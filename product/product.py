from zope.interface import implements

from interfaces import IProduct
from zompatible.characteristic.characteristic import getCharacteristicInterfaces

class Product(object):
    implements(IProduct)
    
    name = u""
    subProducts = []
 
    def __init__(self, name=None):
        self.name = name
        self.subProducts = []
        
    def Display(self):
        # Display the product name
        s = u'Name: %s' % self.name
        print s
        self.DisplayCharacteristics()
        self.DisplayProducts()
    
    def DisplayCharacteristics(self):
        l = getCharacteristicInterfaces(self)
        if len(l) > 0:
            print u'Characteristics:'
            for e in l:
#                s = u'\n'.join([s, e(self).Display()])
                e(self).Display()
            
    def DisplayProducts(self):
        for e in self.subProducts:
            print u'-----'
            e.Display()

    def AddProduct(self, product):
        self.subProducts.append(product) 
