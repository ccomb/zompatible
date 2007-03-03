# -*- coding: utf-8 -*-
from zope.app.folder.interfaces import IFolder
from zope.app.folder.folder import Folder
from zope.interface import implements
from zope.component import adapts

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