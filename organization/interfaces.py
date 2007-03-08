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
    types = List(title=u"types", value_type=Choice(title=u'organization type', description=u'the types of the organization', vocabulary="organization_type"))
    def get_devices():
        pass

class IOrganizationContainer(IContainer, IContained):
  u"""
  a container for the organizations should only contain organizations
  """
  contains(IOrganization)
  
  
class ISearchableTextOfOrganization(ISearchableText):
    u"""
    on déclare un index juste pour cette interface de façon à indexer juste les fabricants
    """



class IManufacturer(IOrganization):
    devices = Attribute(u"devices")
    drivers = Attribute(u"drivers")
IManufacturer.setTaggedValue('name','Manufacturer')

class IEditor(IOrganization):
    operatingsystems = Attribute(u"os")
IEditor.setTaggedValue('name','Software Editor')
