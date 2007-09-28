from zope.interface import implements, providedBy

from zompatible.characteristic.characteristic import getCharacteristicInterfaces
from zompatible.categorynew.utilities import getCategoryInterfaces

from interfaces import *

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
                e(self).Display()
            
    def DisplayProducts(self):
        for e in self.subProducts:
            print u'-----'
            e.Display()

    def AddProduct(self, product):
        u""" Add a sub product to the product
        """
        self.subProducts.append(product) 
        
    def GetCategories(self):
        u""" Return the list of categories the product belongs to. 
        """
        cat = getCategoryInterfaces(self)
        for e in self.subProducts:
            cat.extend(getCategoryInterfaces(e))
        return cat
    
    def GetProduct(self, category):
        if category.providedBy(self):
            return self
        else:
            for e in self.subProducts:
                if category.providedBy(e):
                    return e.GetProduct(category)
            return None


    
