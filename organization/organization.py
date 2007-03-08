# -*- coding: utf-8 -*-
from interfaces import *
from zope.interface import implements
from persistent import Persistent  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.app.container.browser.contents import Contents
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder
from zope.index.text.interfaces import ISearchableText
from zope.component import adapts, adapter
from zope.app.folder.interfaces import IFolder
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.keyreference.persistent import connectionOfPersistent
from zope.schema.interfaces import ISource, IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized
from zope.component.interface import nameToInterface, interfaceToName
from ZODB.interfaces import IConnection
from zope.schema.vocabulary import SimpleTerm
from zope.app.content import ContentTypesVocabulary
from zope.component import adapter, getAllUtilitiesRegisteredFor
from zope.interface.declarations import alsoProvides, noLongerProvides

from zompatible.device.device import DeviceContainer
from zompatible.software.software import OperatingSystemContainer
from interfaces import IOrganization, IOrganizationType


class OrganizationContainer(Folder):
  "a organization container"
  implements(IOrganizationContainer)
  __name__=__parent__=None



@adapter(IOrganization, IObjectAddedEvent)
def createOrganizationSubfolders(organization, event):
    u"Create the device container"
    devices=DeviceContainer()
    organization['devices']=devices 
    u"then create the operating system container"
    operatingsystems=OperatingSystemContainer()
    organization['operating-systems']=operatingsystems


class Organization(Folder):
    implements(IOrganization,IFolder)
    names=[]
    url=""
    __name__=__parent__=None
    def __init__(self):
        self.availabletypes = list(getAllUtilitiesRegisteredFor(IOrganizationType))
        super(Organization, self).__init__()
    def get_devices(self):
        return self['devices'].items()
    def __getattr__(self, name):
        if name=='types':
            u"When accessing manufacturer.types, return the provided interfaces of type IOrganizationType)" 
            return [ interface for interface in self.availabletypes if interface.providedBy(self) ]
        else:
            return super(Organization, self).__getattr__(name)
    def __setattr__(self, name, value):
        u"Same as getitem, but we tell the object to provide the wanted interfaces when we write manufacturer.types"
        if name=='types':
            for i in self.availabletypes:
                noLongerProvides(self, i)
                if i in value:
                    alsoProvides(self, i)
        else:
            return super(Organization, self).__setattr__(name,value)
            
  

class SearchableTextOfOrganization(object):
    u"""
    l'adapter qui permet d'indexer les organizations
    """
    implements(ISearchableTextOfOrganization)
    adapts(IOrganization)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        u"peut surement être optimisé avec une seule ligne de return..."
        text = u""
        for t in self.context.names:
            text += " " + t
        return text
    

class SearchOrganization(object):
    u"""
    une classe qui effectue la recherche de organization
    """
    def update(self, query):
        catalog=getUtility(ICatalog)
        del self.results
        self.results=[]
        if query!="":
            self.results=catalog.searchResults(organization_names=query)
    def __init__(self, query):
        self.results=[]
        self.update(query)
    def getResults(self):
        return self.results

class OrganizationTypeVocabulary2(object):
    implements(IVocabularyTokenized)
    interface = IOrganization

class OrganizationTypeVocabulary(object):
    """
    This is the vocabulary that provides the different types of Organization types (as interfaces!) to choose from.
    """
    implements(IVocabularyTokenized)
    adapts('zompatible.organization.interfaces.IOrganization')
    index=0
    def __init__(self, context):
        "here the context is the Organization"
        self.context=context
        self.index=0
        #self.types = IOrganization.dependents.keys()
        self.types = list(getAllUtilitiesRegisteredFor(IOrganizationType))
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
        if self.index>=len(self.types):
            raise StopIteration
        self.index=self.index+1
        return self.getTerm(self.types[self.index-1])
    def __len__(self):
        return len(self.types)
    def __contains__(self, value):
        return value in self.types

class OrganizationInterfacesVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return OrganizationTypeVocabulary(context)



