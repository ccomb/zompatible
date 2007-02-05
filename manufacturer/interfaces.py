# -*- coding: utf-8 -*-
from zope.app.folder.interfaces import IFolder
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine
from zope.interface import implements, Interface



class IManufacturer(IContainer):
  u"""
  a manufacturer may contain devices so be a device container??
  """
  containers('zompatible.manufacturer.interfaces.IManufacturerContainer')
  names=List(title=u'names', description=u'possible names of the manufacturer', value_type=TextLine(title=u'name', description=u'a name for the manufacturer'))


class IManufacturerContainer(IContainer):
  u"""
  a container for the manufacturers should only contain manufacturers
  """
  contains(IManufacturer)