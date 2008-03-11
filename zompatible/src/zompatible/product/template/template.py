# -*- coding: utf-8 -*-
import copy

from zompatible.product.product import Product
from zope.interface import implements, alsoProvides, directlyProvidedBy, directlyProvides

from interfaces import IProductTemplate

class ProductTemplate(Product):
    implements(IProductTemplate)

    def create_product(self, name):
        obj = copy.copy(self)
        obj.name = name
        return obj
