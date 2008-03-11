# -*- coding: utf-8 -*-
from zope.interface import Interface

class IProductTemplate(Interface):
    """
    interface added to a product to make it a template usable
    to create other products.
    """
    def create_product( ):
        u"create a product from the template"

