# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component.factory import Factory
from zope.component import getUtility
from zope.app.catalog.interfaces import ICatalog, ICatalogIndex
from zope.app.catalog.text import ITextIndex
from zope.app.intid.interfaces import IIntIds
from zope.app.catalog.attribute import AttributeIndex
from zope.index.interfaces import IInjection, IIndexSearch
from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree
from BTrees.IFBTree import IFTreeSet
from zope.app.container.contained import Contained
from persistent import Persistent

from interfaces import *

class BaseIndex(Persistent, Contained):
    u"""
    A custom index that is used to index object attributes
    when these attributes are objects.
    (copied from zope.app.catalog.README.txt)
    (TextIndex is not a good choice, and FieldIndex require that
    the object attribute be orderable).
    The first use is to index the 'organization' attribute of devices
    """
    implements(IBaseIndex, IInjection, IIndexSearch)
    __name__ = __parent__ = None
    def clear(self):
        u"we store the association the two ways"
        self.forward = OOBTree() # value → set with all docids
        self.backward = IOBTree() # docid → value
    def __init__(self, *args, **kwargs):
        Persistent.__init__(self, *args, **kwargs)
        Contained.__init__(self, *args, **kwargs)
        self.clear()
    def index_doc(self, docid, value):
        u"This method is called with super from AttributeIndex, at the end of its index_doc method"
        if docid in self.backward:
            self.unindex_doc(docid)
        self.backward[docid] = value
        set = self.forward.get(value)
        if set is None:
            set = IFTreeSet()
            self.forward[value] = set
        set.insert(docid)
        self._p_changed=True # because set.insert does not modify the index itself, but just the set (see philipp's book p91)
    def unindex_doc(self, docid):
        if self.interface is not None and not self.interface.providedBy(getUtility(IIntIds).getObject(docid)):
            return
        value = self.backward.get(docid)
        if value is None:
            return
        self.forward[value].remove(docid)
        del self.backward[docid]
    def apply(self, value):
        set = self.forward.get(value)
        if set is None:
            set = IFTreeSet()
        return set

class ObjectIndex(AttributeIndex, BaseIndex):
    implements(IObjectIndex)

class SearchObject(object):
    implements(ISearchObject)
    def update(self, **query):
        catalog=getUtility(ICatalog, u"zompatible.catalog")
        del self._results
        self._results=[]
        for q in query:
            if q not in catalog:
                raise "the key %s does not exist in the catalog"
            if query[q]=="":
                return
            if ITextIndex.providedBy(catalog[q]):
                query[q]+="*"
        self._results=catalog.searchResults(**query)
    def __init__(self, **query):
        self._results=[]
        self.update(**query)
    def getResults(self):
        return self._results

SearchObjectFactory = Factory(
    SearchObject,
    title=u"SearchObject factory",
    description = u"This factory instantiates a new SearchObject"
    )


    