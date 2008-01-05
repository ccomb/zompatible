# -*- coding: utf-8 -*-
from zope.app.folder.folder import Folder
from zope.interface import implements
from zope.component import adapts, getUtility, adapter, getSiteManager, queryUtility
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized
from zope.component.factory import Factory
from zope.proxy import removeAllProxies
from zompatible.skin.navigation.browser import PrettyName
from zope.location import Location
from zope.annotation.interfaces import IAnnotations
from persistent.list import PersistentList

from interfaces import *

class Category(Folder):
    implements(ICategory)
    name = []
    description = u""
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        super(Category, self).__init__()

categoryFactory = Factory(
    Category,
    title=u"Category factory",
    description = u"This factory instantiates a new category."
    )
    
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
        self.availablecategories = IAvailableCategories(self.context.context)
        self._cur = self._current = self._parent = self.availablecategories # store the current categorie to be able to iterate in its subcategories
        self.parent_iterators = [ ] # list of iterators of the current category and its parents: [ iter(toplevel), iter(subcategory), iter(subsubcategory, etc... ]
    def getTerm(self, value):
        "here, value is a a category"
        token = self._intid.getId(value)
        title = (len(self.parent_iterators)-1)*u'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + PrettyName(value, None)() # TODO: remplacer les "____" par un niveau de liste
        return SimpleTerm(value, token, title)
    def getTermByToken(self, token):
        value=self._intid.getObject(int(token))
        title=(len(self.parent_iterators)-1)*u'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + PrettyName(value, None)() # TODO: remplacer les "____" par un niveau de liste
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

CATEGORIES_KEY = 'zompatible.category'

class Categories(Location):
    u"""
    The adapter that writes and retrieves the categories put on any object
    """
    adapts(ICategorizable)
    implements(ICategories)

    def __init__(self, context):
        self.context = context

    def _get_categories(self):
        try:
            return IAnnotations(self.context)[CATEGORIES_KEY]
        except KeyError:
            categories = PersistentList()
            IAnnotations(self.context)[CATEGORIES_KEY] = categories
            return categories

    def _set_categories(self, categories):
        for cat in categories: # for each category, add every upper category
            parent = cat.__parent__
            while not IAvailableCategoriesContainer.providedBy(parent):
                if parent not in categories:
                    categories.append(parent)
                parent = parent.__parent__
        IAnnotations(self.context)[CATEGORIES_KEY] = PersistentList(categories)

    categories = property(_get_categories, _set_categories)
    

@adapter(ICategorizable)
def AvailableCategories(context):
    u"""
    The adapter that returns the container (folder)
    where reside all the available categories for a particular object type.
    This allows to have a different category container for each content type
    """
    utilityname = type(removeAllProxies(context)).__name__ + u'_categories'
    try: # the category container should be registered in the sitemanager for ICategories
        return getUtility(IAvailableCategories, utilityname)
    except: # we create and register a new category container for the object type"
        sm = getSiteManager(context)
        sm[utilityname] = AvailableCategoriesContainer()
        sm.registerUtility(sm[utilityname], IAvailableCategories, utilityname)
        return sm[utilityname]

@adapter(ICategories)
def CategoriesAvailableCategories(categories):
    u"I was obliged to add this adapter from ICategories because the Vocabulary needs it"
    return AvailableCategories(categories.context)

class SearchableTextOfCategorizable(object):
    u"""
    adapter that allows to index categories of Categorizable objects
    """
    implements(ISearchableTextOfCategorizable)
    adapts(ICategorizable)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        sourcetext = texttoindex = u''
        # First, gather all interesting text
        for category in ICategories(self.context).categories: # Peut-être déporter ça dans la gestion des categories
            sourcetext += category.description + " " + reduce(lambda x,y: x+" "+y, category.names)
        # then split all words into subwords
        for word in sourcetext.split():        
            for subword in [ word[i:] for i in xrange(len(word)) if len(word)>=1 ]:
                texttoindex += subword + " "
        return texttoindex


