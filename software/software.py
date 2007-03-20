# -*- coding: utf-8 -*-
from zope.app.folder.interfaces import IFolder
from zope.app.folder.folder import Folder
from zope.interface import implements
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.interfaces import INameChooser
from zope.app.container.contained import NameChooser
import string

from interfaces import ISoftwareContainer, ISoftware, ISearchableTextOfSoftware



class SoftwareContainer(Folder):
    "a container for all software"
    implements(ISoftwareContainer)
    __name__=__parent__=None

class Software(Folder):
    implements(ISoftware,IFolder)
    names=architectures=[]
    version=codename=u""
    link=u""
    url=""
    __name__=__parent__=None

class SoftwareNameChooser(NameChooser):
    u"""
    adapter qui permet de choisir le nom du software auprès du container
    Le vrai nom est stocké dans un attribut, mais ce nom est aussi important
    car il apparaît dans l'URL, et sert pour le traversing.
    """
    implements(INameChooser)
    adapts(Software)
    def chooseName(self, name, software):
        codename=u""
        if software.codename != u"":
            codename="-" + software.codename
        return string.lower(software.names[0] + "-" + software.version + codename).replace(' ','-')
    def checkName(self, name, software):
        if name in software.__parent__ and software is not software.__parent__['name']:
            return False
        else :
            return true

class SearchableTextOfSoftware(object):
    u"""
    l'adapter qui permet d'indexer les Software
    """
    implements(ISearchableTextOfSoftware)
    adapts(ISoftware)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        sourcetext = texttoindex = u''
        for word in self.context.names:
            sourcetext += word + " "
        for word in sourcetext.split():        
            for subword in [ word[i:] for i in range(len(word)) ]:
                texttoindex += subword + " "
        return texttoindex
        
class SearchSoftware(object):
    u"""
    une classe qui effectue la recherche d'software
    """
    def update(self, query, organization=None):
        catalog=getUtility(ICatalog)
        del self.results
        self.results=[]
        if query!="":
            self.results=catalog.searchResults(software_names=query+"*")
        if organization is not None:
            self.results = ( software for software in self.results if (software.__parent__.__parent__ == organization) )
    def __init__(self, query, organization=None):
        self.results=[]
        self.update(query)
    def getResults(self):
        return self.results
        
