# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine, URI
from zope.index.text.interfaces import ISearchableText
from zope.interface import Attribute, Interface, implements
from zope.interface.interfaces import IInterface
from zope.component import adapts
from zope.schema import Text, Choice, InterfaceField, List, Set

class IOrganizationType(IInterface):
    u"""
    The interface type for organizations (IManufacturer,...)
    On the model of ContentType
    """

class IOrganization(IContainer, IContained):
    u"""
    an organization of any kind.
    """
    containers('zompatible.organization.interfaces.IOrganizationContainer')
    names=List(title=u'names', description=u'possible names of the organization', value_type=TextLine(title=u'name', description=u'a name for the organization'))
    url = URI(title=u'web site', description=u'main web site of the organization', max_length=50)
    products = Attribute(u"products of the organization")

class IOrganizationInterfaces(Interface):
    u"""
    The class which manages additional interfaces for organizations
    """
    interfaces = List(title=u"Products", description=u"The kind of products the organization releases", value_type=Choice(title=u'product type', description=u'the type of the product', vocabulary="organization_type"))
    
class IOrganizationContainer(IContainer, IContained):
  u"""
  a container for the organizations should only contain organizations
  """
  contains(IOrganization)
  
  
class ISearchableTextOfOrganization(ISearchableText):
    u"""
    on déclare un index juste pour cette interface de façon à indexer juste les organisations
    """



class IManufacturer(Interface):
    pciids=List(title=u'PCI IDs', description=u'list of pci ids for the manufacturer', value_type=TextLine(title=u'PCI ID', description=u'a PCI ID given to the manufacturer'))
IManufacturer.setTaggedValue('name','Devices')
IManufacturer.setTaggedValue('description','The organization manufactures or assembles computer devices')


class IOsEditor(Interface):
    pass
IOsEditor.setTaggedValue('name','Operating Systems')
IOsEditor.setTaggedValue('description','The organization produces or transforms Operating Systems')

