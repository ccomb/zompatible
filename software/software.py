# -*- coding: utf-8 -*-
from zope.app.folder.interfaces import IFolder
from zope.app.folder.folder import Folder
from zope.interface import implements
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.interfaces import INameChooser
from zope.app.container.contained import NameChooser
import string

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
        return string.lower(os.names[0] + "-" + os.version + codename).replace(' ','-')
    def checkName(self, name, os):
        if name in os.__parent__ and os is not os.__parent__['name']:
            return False
        else :
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
        sourcetext = texttoindex = u''
        for word in self.context.names:
            sourcetext += word + " "
        for word in sourcetext.split():        
            for subword in [ word[i:] for i in range(len(word)) ]:
                texttoindex += subword + " "
        print texttoindex
        return texttoindex
        
class SearchOperatingSystem(object):
    u"""
    une classe qui effectue la recherche d'operating system
    """
    def update(self, query, organization=None):
        catalog=getUtility(ICatalog)
        del self.results
        self.results=[]
        if query!="":
            self.results=catalog.searchResults(operatingsystem_names=query+"*")
        if organization is not None:
            self.results = ( os for os in self.results if (os.__parent__.__parent__ == organization) )
    def __init__(self, query, organization=None):
        self.results=[]
        self.update(query)
    def getResults(self):
        return self.results
        
