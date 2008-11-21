# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains
from zope.schema import Choice, List

class ISupported(Interface):
    u"""
    Interface added to products to let them have a compatibility list
    """
    supports = Attribute("Compatibility List")

class ISupportContainer(IContainer, IContained):
    u"""
    The main container that stores Support object
    """
    contains("zompatible.support.interfaces.ISupport")

class ISupport(IContainer):
    u"""
    object that links a list of products
    It contains references to products
    and a list of Report objects
    """
    products = List(title = u'compatible products', 
                    description = u'compatible products',
                    value_type = Choice( title=u'product',
                                         description=u'product',
                                         source="productsource"))
    
