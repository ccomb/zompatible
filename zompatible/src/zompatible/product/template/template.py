import copy

from zompatible.product.product import Product
from zope.interface import alsoProvides, directlyProvidedBy, directlyProvides

from interfaces import *

class Category(Product):
    
    def __init__(self, name):
        Product.__init__(self, name)
        alsoProvides(self, ICategory)

    def NewProduct(self):
        prod = copy.deepcopy(self)
        directlyProvides(prod, directlyProvidedBy(prod) - ICategory)
        prod.categories.append(self)
        return prod
        
from zope.interface import providedBy

def getCategoryInterfaces(obj):
    l = list(providedBy(obj))
    l = [str(e) for e in l]
    l = [e for e in l if e.find('zompatible.categorynew.interfaces.IIs') >= 0]
    
    return l
