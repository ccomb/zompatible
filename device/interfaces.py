# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine
from zope.interface import implements


class IDevice(IContained):
  "a device may contain devices so be a device container??"
  containers('zompatible.interfaces.IDeviceContainer')
  names=List(title=u'names', description=u'possible names of the device', value_type=TextLine(title=u'name', description=u'a name for the device'))

class IDeviceContainer(IContainer):
  """
  a container for the devices should only contain devices
  I wanted the Manufacturer to be the device container,
  but I don't want to hardcode it. This is a zcml conguration issue.
  """
  contains(IDevice)