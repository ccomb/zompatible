# -*- coding: utf-8 -*-
from zope.app.folder.interfaces import IFolder
from zope.app.folder.folder import Folder
from zope.interface import implements
from zope.component import adapts
from zope.app.container.interfaces import INameChooser
from zope.app.container.contained import NameChooser

from interfaces import IOperatingSystemContainer, IOperatingSystem, ISearchableTextOfOperatingSystem



class OperatingSystemContainer(Folder):
    "a container for all operating systems"
    implements(IOperatingSystemContainer)
    __name__=__parent__=None
  
  
class OperatingSystem(Folder):
    implements(IOperatingSystem,IFolder)
    names=architectures=[]
    version=codename=u""
    link=u""
    url=""
    __name__=__parent__=None

class OperatingSystemNameChooser(NameChooser):
    u"""
    adapter qui permet de choisir le nom de l'OS auprès du container
    Le vrai nom est stocké dans un attribut, mais ce nom est aussi important
    car il apparaît dans l'URL, et sert pour le traversing.
    """
    implements(INameChooser)
    adapts(OperatingSystem)
    def chooseName(self, name, os):
        codename=u""
        if os.codename != u"":
            codename="-" + os.codename
        return os.names[0] + "-" + os.version + codename
    def checkName(self, name, os):
        return true



class SearchableTextOfOperatingSystem(object):
    u"""
    l'adapter qui permet d'indexer les OperatingSystem
    """
    implements(ISearchableTextOfOperatingSystem)
    adapts(IOperatingSystem)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        u"peut surement être optimisé avec une seule ligne de return..."
        text = u""
        for t in self.context.names:
            text += " " + t
        return text
        
class SearchOperatingSystem(object):
    u"""
    une classe qui effectue la recherche de manufacturer
    """
    def update(self, query):
        catalog=getUtility(ICatalog)
        del self.results
        self.results=[]
        if query!="":
            self.results=catalog.searchResults(operatingsystem_names=query)
    def __init__(self, query):
        self.results=[]
        self.update(query)
    def getResults(self):
        return self.results