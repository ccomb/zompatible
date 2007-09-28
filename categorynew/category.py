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
        return prod
