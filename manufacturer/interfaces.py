from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine
from zope.interface import implements


class IManufacturer(IContained):
  "a manufacturer may contain devices so be a device container??"
  containers('goodforlinux.interfaces.IManufacturerContainer')
  names=List(title=u'names', description=u'possible names of the manufacturer', value_type=TextLine(title=u'name', description=u'a name for the manufacturer'))

class IManufacturerContainer(IContainer):
  "a container for the manufacturers should only contain manufacturers"
  contains(IManufacturer)