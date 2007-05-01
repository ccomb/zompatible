# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.app.folder.folder import Folder
from zope.component import adapts, getAllUtilitiesRegisteredFor
from zope.app.folder.interfaces import IFolder
from zope.app.container.interfaces import INameChooser
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized, ISource
from zope.component.interface import nameToInterface, interfaceToName
from zope.schema.vocabulary import SimpleTerm
from zope.interface.declarations import alsoProvides, noLongerProvides
from zope.proxy import removeAllProxies
from zope.app.container.contained import NameChooser
from zope.component.factory import Factory
from zope.app.component.hooks import getSite

import string

from interfaces import *
from zompatible.device.device import DeviceContainer
from zompatible.software.software import SoftwareContainer
from interfaces import IOrganization, IOrganizationType


class OrganizationContainer(Folder):
  "a organization container"
  implements(IOrganizationContainer)
  __name__=__parent__=None

OrganizationContainerFactory = Factory(OrganizationContainer)
    
class Organization(Folder):
    implements(IOrganization,IFolder)
    names=[]
    url=""
    description=u""
    pciids=[] # une Organization peut fournir IManufacturer !!
    usbids=[] # idem
    __name__=__parent__=None

from zope.component.factory import Factory

organizationFactory = Factory(
    Organization,
    title=u"Organization factory",
    description = u"This factory instantiates new Organization."
    )

class OrganizationNameChooser(NameChooser):
    u"""
    adapter that allow to choose the __name__ of an organization
    The real pretty name is stored in an attribute, but this name is also important
    as it appears in the URL ans is used for traversing.
    """
    implements(INameChooser)
    adapts(IOrganization)
    def chooseName(self, name, organization):
        if not name and organization is None:
            raise "OrganizationNameChooser Error"
        if name:
            rawname = name
        if organization is not None and len(organization.names)>0:
            rawname = organization.names[0]
        return string.lower(rawname).strip().replace(' ','-').replace(u'/',u'-').lstrip('+@')
    def checkName(self, name, organization):
        if name in organization.__parent__ and organization is not organization.__parent__['name']:
            return False
        else :
            return true

class OrganizationInterfaces(object):
    u"""
    An adapter that allows to get and set additional interfaces on Organizations.
    """
    implements(IOrganizationInterfaces)
    adapts(IOrganization)
    def __init__(self, orga):
        self.orga = orga
        self.availableinterfaces = list(getAllUtilitiesRegisteredFor(IOrganizationType))
        self.__parent__ = self.orga.__parent__
    def __getattr__(self, name):
            if name=='interfaces':
                u"When accessing orga.interfaces, return the provided interfaces of type IOrganizationType)" 
                return [ interface for interface in self.availableinterfaces if interface.providedBy(self.orga) ]
            else :
                return self.__dict__[name]

    def __setattr__(self, name, value):
        u"Same as getitem, but we tell the object to provide the wanted interfaces when we write orga.interfaces"
        if name=='interfaces':
            for i in self.availableinterfaces:
                noLongerProvides(removeAllProxies(self.orga), i)
                if i in value:
                    u"on crée le DeviceContainer ou SoftwareContainer si absent"
                    if i.getTaggedValue('containername') not in self.orga:
                        self.orga[i.getTaggedValue('containername')] = InternalContainerFactory(i)
                    alsoProvides(removeAllProxies(self.orga), i)
        else :
            self.__dict__[name]=value

class Manufacturer(object):
    implements(IManufacturer)
    adapts(IOrganization)
    def __init__(self, context):
        self.context=context
    def __getattr__(self, name):
        if name == "products":
            return self.context['devices']
        else:
            try :
                return self.__dict__[name]
            except :
                return None

class SoftwareEditor(object):
    implements(ISoftwareEditor)
    adapts(IOrganization)
    def __init__(self, context):
        self.context=context
    def __getattr__(self, name):
        if name == "products":
            return self.context['software']
        else:
            return self.__dict__[name]

def InternalContainerFactory(i):
    u"fonction qui crée le bon container en fonction de l'interface"
    if (i is IManufacturer):
        return DeviceContainer()
    if (i is ISoftwareEditor):
        return SoftwareContainer()

        
class SearchableTextOfOrganization(object):
    u"""
    l'adapter qui permet d'indexer les organizations
    """
    implements(ISearchableTextOfOrganization)
    adapts(IOrganization)
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

class OrganizationTypeVocabulary(object):
    """
    This is the vocabulary that provides the different interfaces of Organization to choose from. (ISoftwareEditor and IManufacturer)
    """
    implements(IVocabularyTokenized)
    adapts('zompatible.organization.interfaces.IOrganization')
    index=0
    def __init__(self, context):
        "here the context is the Organization"
        self.context=context
        self.index=0
        self.interfaces = list(getAllUtilitiesRegisteredFor(IOrganizationType))
    def getTerm(self, value):
        "here, value is a an organization interface, such as IManufacturer"
        token = interfaceToName(self.context, value).encode('base64')
        title = value.getTaggedValue('name')
        return SimpleTerm(value, token, title)
    def getTermByToken(self, token):
        value=nameToInterface(self.context, token.decode('base64'))
        title=value.getTaggedValue('name')
        return SimpleTerm(value, token, title)
    def __iter__(self):
        "we decide the iterator is the object itself. So we need to implement next() and have our own internal index"
        self.index=0
        return self
    def next(self):
        if self.index>=len(self.interfaces):
            raise StopIteration
        self.index=self.index+1
        return self.getTerm(self.interfaces[self.index-1])
    def __len__(self):
        return len(self.interfaces)
    def __contains__(self, value):
        return value in self.interfaces

class OrganizationInterfacesVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return OrganizationTypeVocabulary(context)

class OrgaSource(object):
    implements(ISource)
    def __contains__(self, value):
        root = getSite()
        if value.__name__ in root['organizations']:
            return True
        return False

class OrganizationVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return OrgaSource()



