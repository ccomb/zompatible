# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.app.catalog.interfaces import ICatalogIndex
from zope.app.container.interfaces import IContained

class IBaseIndex(IContained):
    forward = Attribute(u"the forward association")
    backward = Attribute(u"the backward association")

class IObjectIndex(ICatalogIndex):
    pass



class ISearchObject(Interface):
    u"""
    search any object that is in the catalog.
    The **query is a non explicit argument with all the queries, for ex: ISoftware=u'debian', ICategories='kernel'
    The name of the interface is the name of the index.
    This is a 2-strikes search (not really useful for now):
      - update
      - getResults
    """
    def update(**query): # the **query can also be passed to the constructor
        pass
    def getResults():
        pass

