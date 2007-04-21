# -*- coding: utf-8 -*-
from zope.app.folder.folder import Folder
from zope.interface import implements
from zope.component import adapts, getUtility, adapter, getSiteManager, queryUtility
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized
from interfaces import *

class Category(Folder):
    implements(ICategory)
    names = description = None

class AvailableCategoriesContainer(Folder):
    implements(IAvailableCategoriesContainer)


class CategoryVocabulary(object):
    """
    This is the vocabulary that provides the different available categories, depending on the context
    """
    implements(IVocabularyTokenized)
    index=0
    def __init__(self, context):
        "The context is the adapter to ICategories, because the form fields are created from ICategories"
        self.context=context
        self._intid = getUtility(IIntIds) # used to create the unique tokens
        u"""
        Here we must retrieve the list of categories, depending in the context
        We first get an adapter that will return the correct categories utility
        (the folder that contains predefined Category objects)
        """
        self.availablecategories = queryUtility(ICategories, self.context.get_utility_name(), [])
        self._cur = self._current = self._parent = self.availablecategories # store the current categorie to be able to iterate in its subcategories
        self.parent_iterators = [ ] # list of iterators of the current category and its parents: [ iter(toplevel), iter(subcategory), iter(subsubcategory, etc... ]
    def getTerm(self, value):
        "here, value is a a category"
        token = self._intid.getId(value)
        title = (len(self.parent_iterators)-1)*u'_____' + value.__name__ # TODO: remplacer les "____" par un niveau de liste
        return SimpleTerm(value, token, title)
    def getTermByToken(self, token):
        value=self._intid.getObject(int(token))
        title=(len(self.parent_iterators)-1)*u'_____' + value.__name__ # TODO: remplacer les "____" par un niveau de liste
        return SimpleTerm(value, token, title)
    def __iter__(self):
        "The class is used as its own iterator. The next() method will use the last iterator in the parent_iterators list"
        return self
    def next(self):
        if self._current is self.availablecategories and len(self._current) == 0 :
            raise StopIteration
        # if there is subcategories, we dive in it, and add a new iterator in the iterator list
        if len(self._current) != 0:
            self.parent_iterators.append(iter(self._current))
            self._parent = self._current
            self._current = self._parent[self.parent_iterators[len(self.parent_iterators)-1].next()]
            return self.getTerm(self._current)
        try: # try to return the next in the same level
            self._current = self._parent[self.parent_iterators[len(self.parent_iterators)-1].next()]
            return self.getTerm(self._current)
        except: # nothing left at the same level
            while len(self.parent_iterators) > 0: # we loop unless at the upmost level
                try: # we try to continue with the upper level, if upper level is at the end, 
                    self.parent_iterators.pop()
                    self._parent = self._parent.__parent__
                    self._current = self._parent[self.parent_iterators[len(self.parent_iterators)-1].next()]
                    return self.getTerm(self._current)
                except:
                    if len(self.parent_iterators) == 0:
                        raise StopIteration
    def __len__(self): # don't really need it for the moment
        raise NotImplementedError
    def __contains__(self, value):
        u"recursively try all items in the folder"
        if value in self._cur.values(): # first check at the current level
            self._cur = self.availablecategories # reset _cur
            return True
        for i in self._cur.values(): # otherwise parse every item in the current level
            self._cur = i
            if value in self: # make the recursion work
                self._cur = self.availablecategories # reset current
                return True
        if self._cur is not self.context:
            self._cur = self._cur.__parent__
        self._cur = self.availablecategories # reset _cur
        return False

class CategoryVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return CategoryVocabulary(context)

class Categories(object):
    u"""
    The adapter that writes and retrieves the category put on any object
    """
    adapts(ICategorizable)
    implements(ICategories)
    categories = []
    context = None
    def __init__(self, context):
        self.context = context
        try:
            self.categories = self.context.categories
        except:
            self.context.categories = [ ]
    def __setattr__(self,name,value):
        if name == 'categories':
            self.context.categories = value
        object.__setattr__(self, name, value)
    def get_utility_name(self):
        return type(self.context).__name__ + u'Categories'

@adapter(ICategorizable)
def AvailableCategories(context):
    u"""
    The adapter that returns the container (folder)
    where reside all the available categories for a particular object type.
    This allows to have a different category container for each content type
    """
    utilityname = ICategories(context).get_utility_name()
    try:
        return getUtility(ICategories, utilityname)
    except:
        u"we create and register a new category container for the object type"
        sm = getSiteManager(context)
        sm[utilityname] = AvailableCategoriesContainer()
        sm.registerUtility(sm[utilityname], ICategories, utilityname)
        return sm[utilityname]

@adapter(ICategories)
def CategoriesAvailableCategories(categories):
    u"I was obliged to add this adapter from ICategories because the Vocabulary needs it"
    return AvailableCategories(categories.context)

