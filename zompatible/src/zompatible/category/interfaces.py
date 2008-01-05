# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.schema import List, TextLine, Text, Choice
from zope.app.container.interfaces import IContainer
from zope.interface import Attribute
from zope.annotation.interfaces import IAttributeAnnotatable

class ICategorizable(IAttributeAnnotatable):
    u"""
    The marker interface to put (via zcml) on object that must be categorized
    """

class IAvailableCategoriesContainer(IContainer):
    u"""
    The interface of the container that stores all the available categories
    in the site manager
    """

class IAvailableCategories(Interface):
    u"""
    The interface of the registered utility that provides the available utilities
    There is no schema, just an attribute
    One can get the available categories of a categorizable object with IAvailableCategories(object)
    If object is a device, you'll get a different container than with a software, or any other categorizable object.
    If the container does not exist yet, it is created.
    """
    availablecategories = Attribute(u"all the categories that can be assigned to an object") 

class ICategory(IContainer):
    u"""
    allows to define (implement as a real object) a category of device, software, action, etc.
    A category of device (an instance) can be: laptop, server, etc.
    A category of action can be: installation, configuration, starting a program, etc. 
    """
    names = List(title=u'names', description=u'possible names of the category', value_type=TextLine(title=u'name', description=u'a category'))
    description = Text(title=u'category description', description=u'description of the category')
    #userlevel =    un niveau de complexité qui influe sur le fait que la catégorie est proposée ou non en fonction de l'utilisateur débutant ou avancé.
    # cette notion est peut-être déplaçable dans le module user, dans ce cas, une category doit être IUserLevelDependant
    # Le UserLevel doit être défini dans le module level et avoir son propre utility

class ICategories(Interface):
    u"""
    The interface through which one can access the categories of any categorizable object.
    Just call ICategories(object) then you have a sequence of categories
    """
    categories = List(title=u'categories', description=u'list of categories', value_type=Choice(title=u'category', vocabulary="categories"))

class ISearchableTextOfCategorizable(Interface):
    u"""
    Marker interface to index only categories of objects.
    """