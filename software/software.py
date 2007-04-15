# -*- coding: utf-8 -*-
from persistent import Persistent
from zope.app.folder.folder import Folder
from zope.interface import implements
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.interfaces import INameChooser
from zope.app.container.contained import NameChooser
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds
import string
from zope.schema.interfaces import ISource, IVocabularyFactory
from BTrees.OOBTree import OOBTree

from interfaces import ISoftwareContainer, ISoftware, ISearchableTextOfSoftware, ISubSoftware



class SoftwareContainer(Folder):
    "a container for all software"
    implements(ISoftwareContainer)
    __name__=__parent__=None
    def __delitem__(self,key):
        u"Move to the trash instead of deleting it"
        if len(self[key].supports) == 0:
            super(SoftwareContainer, self).__delitem__(key)
        else :
            trash = getSite()['trash']
            software = self[key]
            software_name = INameChooser(trash).chooseName(u"",software)
            trash[software_name]=software
            super(SoftwareContainer, self).__delitem__(key)
            software.__name__ = software_name
            software.__parent__ = trash
            u"then unindex the trashed object"
            getUtility(ICatalog).unindex_doc(getUtility(IIntIds).getId(software))
        
class Software(Persistent):
    implements(ISoftware, ISubSoftware)
    subsoftware = []
    names=architectures=[]
    version=codename=u""
    link=u""
    url=""
    __name__=__parent__=None
    def __init__(self):
        u"a list of support devices, that lead to the Support objects"
        self.supports = OOBTree()

class SoftwareNameChooser(NameChooser):
    u"""
    adapter qui permet de choisir le nom du software auprès du container
    Le vrai nom est stocké dans un attribut, mais ce nom est aussi important
    car il apparaît dans l'URL, et sert pour le traversing.
    """
    implements(INameChooser)
    adapts(ISoftware)
    def chooseName(self, name, software):
        codename = version = u""
        if software.codename is not None:
            codename="-" + software.codename
        if software.version is not None:
            version = software.version
        return string.lower(software.names[0] + "-" + version + codename).replace(' ','-')
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
            for subword in [ word[i:] for i in xrange(len(word)) if len(word)>=1 ]:
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

class SoftwareSource(object):
    """
    implémentation de la Source de Software utilisée dans le schema de Support
    Il s'agit juste d'implémenter ISource
    Cette source est censée représenter l'ensemble de tous les softwares.
    Elle parcourt toutes les organizations et recherche le software voulu.
    *********
    ATTENTION, dans l'implémentation ci-dessous, si deux orga ont
    des softwares avec le même nom, seul le 1er est retourné.
    """
    implements(ISource)
    def __contains__(self, value):
        root = getSite()
        for manuf in root['organizations']:
            if 'software' in root['organizations'][manuf] and value.__name__ in root['organizations'][manuf]['software'].keys():
                return True
        return False

class SoftwareVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return SoftwareSource()


