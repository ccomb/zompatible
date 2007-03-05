# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine, URI
from zope.index.text.interfaces import ISearchableText


class IOrganization(IContainer, IContained):
    u"""
    a organization may contain devices so be a device container??
    """
    containers('zompatible.organization.interfaces.IOrganizationContainer')
    names=List(title=u'names', description=u'possible names of the organization', value_type=TextLine(title=u'name', description=u'a name for the organization'))
    url = URI(title=u'web site', description=u'main web site of the organization', max_length=50)
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