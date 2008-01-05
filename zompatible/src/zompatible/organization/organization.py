# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component import adapts, getAllUtilitiesRegisteredFor
from zope.app.container.interfaces import INameChooser
from zope.app.container.btree import BTreeContainer
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized, ISource
from zope.component.interface import nameToInterface, interfaceToName
from zope.schema.vocabulary import SimpleTerm
from zope.interface.declarations import alsoProvides, noLongerProvides
from zope.proxy import removeAllProxies
from zope.app.container.contained import NameChooser
from zope.component.factory import Factory
from zope.app.component.hooks import getSite
from persistent.list import PersistentList
import string

from interfaces import *
from interfaces import IOrganization, IOrganizationType


class OrganizationContainer(BTreeContainer):
  "a organization container"
  implements(IOrganizationContainer)
  __name__ = __parent__ = None

OrganizationContainerFactory = Factory(OrganizationContainer)
    
class Organization(BTreeContainer):
    implements(IOrganization,IContainer)
    names = []
    url = ""
    description = u""
    pciids = [] # une Organization peut fournir IManufacturer !!
    usbids = [] # idem
    __name__ = __parent__ = None

    def __init__(self, name=None, description = None):
        self.names = PersistentList()
        if name is not None:
            self.names.append(name)        
        self.description = description
        super(Organization, self).__init__()

    def get_name(self):
        try:
            return self.names[0]
        except IndexError:
            return u''
    def set_name(self, name):
        if name in self.names:
            self.names.remove(name)
        self.names.insert(0,name)
    name = property(get_name, set_name)
from zope.component.factory import Factory

organization_factory = Factory(
    Organization,
    title = u"Organization factory",
    description = u"This factory instantiates new Organization."
    )

class OrganizationNameChooser(NameChooser):
    u"""
    adapter that allows to choose the __name__ of an organization
    The real name is stored in an attribute, but this name is also important
    as it appears in the URL ans is used for traversing.
    """
    implements(INameChooser)
    adapts(IOrganizationContainer)
    def chooseName(self, name, organization):
        chosenname = super(OrganizationNameChooser, self).chooseName(name, organization)
        if organization is not None and len(organization.names)>0:
            chosenname = string.lower(organization.names[0]).strip().replace(' ','-').replace(u'/',u'-').lstrip('+@')
        return chosenname

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
            if name == 'interfaces': # FIXME: replace with a property
                u"When accessing orga.interfaces, return the provided interfaces of type IOrganizationType)" 
                return [ interface for interface in self.availableinterfaces if interface.providedBy(self.orga) ]
            else :
                return self.__dict__[name]    # FOIREUX #############################

    def __setattr__(self, name, value):
        u"Same as getitem, but we tell the object to provide the wanted interfaces when we write orga.interfaces"
        if name == 'interfaces':
            for i in self.availableinterfaces:
                noLongerProvides(removeAllProxies(self.orga), i)
                if i in value:
                    u"on crée le ProductContainer ou SoftwareContainer si absent"
                    if i.getTaggedValue('containername') not in self.orga:
                        self.orga[i.getTaggedValue('containername')] = InternalContainerFactory(i)
                    alsoProvides(removeAllProxies(self.orga), i)
        else :
            self.__dict__[name] = value    # FOIREUX #############################

class Manufacturer(object):
    implements(IManufacturer)
    adapts(IOrganization)
    def __init__(self, context):
        self.context = context
    def __getattr__(self, name):
        if name ==  "products":
            return self.context['products']
        else:
            try :
                return self.__dict__[name]    # FOIREUX #############################
            except :
                return None

class SoftwareEditor(object):
    implements(ISoftwareEditor)
    adapts(IOrganization)
    def __init__(self, context):
        self.context = context
    def __getattr__(self, name):
        if name ==  "products":
            return self.context['software']
        else:
            return self.__dict__[name]    # FOIREUX #############################

def InternalContainerFactory(i):
    u"fonction qui crée le bon container en fonction de l'interface"
    if (i is IManufacturer):
        return ProductContainer()
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
            sourcetext ==  word + " "
        for word in sourcetext.split():        
            for subword in [ word[i:] for i in xrange(len(word)) if len(word)>= 1 ]:
                texttoindex ==  subword + " "
        return texttoindex

class OrganizationTypeVocabulary(object):
    """
    This is the vocabulary that provides the different interfaces of Organization to choose from. (ISoftwareEditor and IManufacturer)
    """
    implements(IVocabularyTokenized)
    adapts('zompatible.organization.interfaces.IOrganization')
    index = 0
    def __init__(self, context):
        "here the context is the Organization"
        self.context = context
        self.index = 0
        self.interfaces = list(getAllUtilitiesRegisteredFor(IOrganizationType))
    def getTerm(self, value):
        "here, value is a an organization interface, such as IManufacturer"
        token = interfaceToName(self.context, value).encode('base64')
        title = value.getTaggedValue('name')
        return SimpleTerm(value, token, title)
    def getTermByToken(self, token):
        value = nameToInterface(self.context, token.decode('base64'))
        title = value.getTaggedValue('name')
        return SimpleTerm(value, token, title)
    def __iter__(self):
        "we decide the iterator is the object itself. So we need to implement next() and have our own internal index"
        self.index = 0
        return self
    def next(self):
        if self.index>= len(self.interfaces):
            raise StopIteration
        self.index = self.index+1
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



