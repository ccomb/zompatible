# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContainer
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine, URI
from zope.index.text.interfaces import ISearchableText


class IManufacturer(IContainer):
    u"""
    a manufacturer may contain devices so be a device container??
    """
    containers('zompatible.manufacturer.interfaces.IManufacturerContainer')
    names=List(title=u'names', description=u'possible names of the manufacturer', value_type=TextLine(title=u'name', description=u'a name for the manufacturer'))
    url = URI(title=u'web site', description=u'main web site of the manufacturer', max_length=50)
    def get_devices():
        pass

class IManufacturerContainer(IContainer):
  u"""
  a container for the manufacturers should only contain manufacturers
  """
  contains(IManufacturer)
  
  
class ISearchableTextOfManufacturer(ISearchableText):
    u"""
    on déclare un index juste pour cette interface de façon à indexer juste les fabricants
    """