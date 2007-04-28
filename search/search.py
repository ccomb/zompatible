# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component.factory import Factory
from zope.component import getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.catalog.text import ITextIndex
from zope.app.catalog.attribute import AttributeIndex
from zope.index.interfaces import IInjection, IIndexSearch
from BTrees.OOBTree import OOBTree
from BTrees.IOBTree import IOBTree
from BTrees.IFBTree import IFTreeSet
from zope.app.container.contained import Contained
from persistent import Persistent
from zope.app.keyreference.persistent import KeyReferenceToPersistent
from zope.proxy import removeAllProxies
from interfaces import *

class BaseIndex(Persistent):
    u"""
    A custom index that is used to index object attributes
    when these attributes are objects.
    (copied from zope.app.catalog.README.txt)
    (TextIndex is not a good choice, and FieldIndex require that
    the object attribute be orderable).
    The first use is to index the 'organization' attribute of devices
    """
    implements(IBaseIndex, IInjection, IIndexSearch)
    __name__ = __parent__ = forward = backward = None
    def clear(self):
            u"we store the association the two ways"
            self.forward = OOBTree() # value → set with all docids
            self.backward = IOBTree() # docid → value
    def __init__(self, *args, **kwargs):
        if self.forward is None or self.backward is None:
            self.clear()
    def index_doc(self, docid, value):
        u"This method is called with super from AttributeIndex, at the end of its index_doc method"
        if docid in self.backward:
            self.unindex_doc(docid)
        valuekey = KeyReferenceToPersistent(removeAllProxies(value))
        self.backward[docid] = valuekey
        set = self.forward.get(valuekey)
        if set is None:
            set = IFTreeSet()
            self.forward[valuekey] = set
        set.insert(docid)
    def unindex_doc(self, docid):
        valuekey = self.backward.get(docid)
        if valuekey is None:
            return
        self.forward[valuekey].remove(docid)
        del self.backward[docid]
    def apply(self, value):
        set = self.forward.get(KeyReferenceToPersistent(removeAllProxies(value)))
        if set is None:
            set = IFTreeSet()
        return set

class ObjectIndex(AttributeIndex, BaseIndex, Contained):
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


    