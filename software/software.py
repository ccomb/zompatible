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
from zope.copypastemove import ObjectMover
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
    builtVersion=u""
    description=u""
    subsoftware = []
    names=architectures=[]
    version=codename=u""
    link=u""
    url=""
    __name__=__parent__=None
    def __init__(self):
        u"a list of support devices, that lead to the Support objects"
        self.supports = OOBTree()
    def __getattr__(self, name):
        if name == 'organization':
            if self.__parent__ is not None:
                return self.__parent__.__parent__
            return None
        return super(Software, self).__getattr__(name)
    def __setattr__(self, name, value):
        if name == 'organization':
            if value is not self.__parent__ and value is not None and self.__parent__ is not None:
                mover = ObjectMover(self)
                if not mover.moveableTo(value['software']):
                    raise "Impossible action"
                else:
                    mover.moveTo(value['software'])
        else:
            super(Software, self).__setattr__(name, value)

class SoftwareNameChooser(NameChooser):
    u"""
    adapter that allows to choose the name of the Software from the container point of view
    The real name is stored in an attribute, but this name is important
    as it appears in the URL and is used for traversing
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
    The adapter that allows to index software objects
    """
    implements(ISearchableTextOfSoftware)
    adapts(ISoftware)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        sourcetext = texttoindex = u''
        u"First, gather all interesting text"
        for word in self.context.names:
            sourcetext += word + " "
        u"then split all words into subwords"
        for word in sourcetext.split():        
            for subword in [ word[i:] for i in xrange(len(word)) if len(word)>=1 ]:
                texttoindex += subword + " "
        return texttoindex

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
        for orga in root['organizations']:
            if 'software' in root['organizations'][orga] and value.__name__ in root['organizations'][orga]['software'].keys():
                return True
        return False

class SoftwareVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return SoftwareSource()


