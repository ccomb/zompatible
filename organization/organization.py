# -*- coding: utf-8 -*-
from interfaces import *
from zope.interface import implements
from zope.app.folder.folder import Folder
from zope.component import adapts, adapter
from zope.app.folder.interfaces import IFolder
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.interfaces import IObjectAddedEvent
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized
from zope.component.interface import nameToInterface, interfaceToName
from zope.schema.vocabulary import SimpleTerm
from zope.component import adapter, getAllUtilitiesRegisteredFor
from zope.interface.declarations import alsoProvides, noLongerProvides
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zope.app.container.interfaces import INameChooser
from zope.app.container.contained import NameChooser
import string

from zompatible.device.device import DeviceContainer
from zompatible.software.software import SoftwareContainer
from interfaces import IOrganization, IOrganizationType


class OrganizationContainer(Folder):
  "a organization container"
  implements(IOrganizationContainer)
  __name__=__parent__=None



@adapter(IOrganization, IObjectAddedEvent)
def createOrganizationSubfolders(organization, event):
    u"Peut-être déplacer ça dans la gestion des manufacturer et SoftwareEditor"
    u"Create the device container"
    devices=DeviceContainer()
    organization['devices']=devices 
    u"then create the software container"
    softwares=SoftwareContainer()
    organization['softwares']=softwares


class Organization(Folder):
    implements(IOrganization,IFolder)
    names=[]
    url=""
    pciids=[] # une Organization peut fournir IManufacturer !!
    __name__=__parent__=None

class OrganizationNameChooser(NameChooser):
    u"""
    adapter qui permet de choisir le nom de l'organization auprès du container
    Le vrai nom est stocké dans un attribut, mais ce nom est aussi important
    car il apparaît dans l'URL, et sert pour le traversing.
    """
    implements(INameChooser)
    adapts(IOrganization)
    def chooseName(self, name, organization):
        return string.lower(organization.names[0]).replace(' ','-')
    def checkName(self, name, organization):
        if name in organization.__parent__ and organization is not organization.__parent__['name']:
            return False
        else :
            return true

class OrganizationInterfaces(object):
    u"""
    I'm moving away orga interfaces management in an adapter
    to avoid boring issues with __getattr__
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
            return self.context['softwares']
        else:
            return self.__dict__[name]
  

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
            for subword in [ word[i:] for i in range(len(word)) ]:
                texttoindex += subword + " "
        return texttoindex
    

class SearchOrganization(object):
    u"""
    une classe qui effectue la recherche de organization
    """
    def update(self, query):
        catalog=getUtility(ICatalog)
        del self.results
        self.results=[]
        if query!="":
            self.results=catalog.searchResults(organization_names=query+"*")
    def __init__(self, query):
        self.results=[]
        self.update(query)
    def getResults(self):
        return self.results
        
class SearchProduct(object):
    u"""
    une classe qui effectue la recherche de product, c'est à dire de device puis d'software
    """
    def update(self, query, organization):
        catalog=getUtility(ICatalog)
        intids=getUtility(IIntIds)
        del self.results
        self.results={}
        if query != "" :
            self.results['devices'] = [ intids.getObject(i) for i in catalog.apply( { 'device_names': query+"*" } ) ]
            self.results['softwares'] = [ intids.getObject(i) for i in catalog.apply( { 'software_names':query+"*" } ) ]
        if organization is not None:
            self.results['devices'] = [ intids.getObject(i) for i in catalog.apply( { 'device_names': query+"*" } ) if intids.getObject(i).__parent__.__parent__ == organization ]
            self.results['softwares'] = [ intids.getObject(i) for i in catalog.apply( { 'software_names':query+"*" } ) if intids.getObject(i).__parent__.__parent__ == organization ]
    def __init__(self, query, organization):
        self.results={}
        self.update(query, organization)
    def getResults(self):
        return self.results
        
class OrganizationTypeVocabulary2(object):
    implements(IVocabularyTokenized)
    interface = IOrganization

class OrganizationTypeVocabulary(object):
    """
    This is the vocabulary that provides the different interfaces of Organization to choose from.
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




