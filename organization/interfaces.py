# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine, URI, Text, Choice, List
from zope.index.text.interfaces import ISearchableText
from zope.interface import Attribute, Interface
from zope.interface.interfaces import IInterface

class IOrganizationType(IInterface):
    u"""
    The interface type for organizations (IManufacturer, ISoftwareEditor)
    On the model of ContentType
    """

class IOrganization(IContainer, IContained):
    u"""
    an organization of any kind.
    It can be a Manufacturer or a Software Editor.
    There is an adapter from IOrganization to IOrganizationInterfaces that allow to set and get the additional
    interfaces offered by an Organization (interfaces of type IOrganizationType only)
    """
    containers('zompatible.organization.interfaces.IOrganizationContainer')
    names=List(title=u'names', description=u'possible names of the organization', min_length=1, value_type=TextLine(title=u'name', description=u'a name for the organization'))
    description = Text(title=u"description", description=u"description of the organization", required=False, max_length=1000)
    url = URI(title=u'web site', description=u'main web site of the organization', max_length=50, required=False)
    products = Attribute(u"products of the organization")

class IOrganizationInterfaces(Interface):
    u"""
    The class which manages additional interfaces for organizations
    You can get the categories of an Organization by reading orga.interfaces
    And you can change them by modifying the list. Eg: orga.interfaces = [ IManufacturer, ISoftwareEditor ]
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
    usbids=List(title=u'USB vendor IDs', description=u'list of usb ids for the manufacturer', value_type=TextLine(title=u'USB vendor ID', description=u'a USB vendor ID given to the manufacturer'))
IManufacturer.setTaggedValue('name','Devices')
IManufacturer.setTaggedValue('containername','devices')
IManufacturer.setTaggedValue('description','The organization manufactures or assembles computer devices')


class ISoftwareEditor(Interface):
    pass
ISoftwareEditor.setTaggedValue('name','Software')
ISoftwareEditor.setTaggedValue('containername','software')
ISoftwareEditor.setTaggedValue('description','The organization produces or transforms Software')

