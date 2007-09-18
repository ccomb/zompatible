from zope.interface import Interface
from zope.schema import Choice, TextLine, Int

class IPhysInterface(Interface):
    """
    """
    interface = Choice (
                        title = u"Physical interface",
                        description = u"Link interface",
                        values=[u'USB', u'PCI'],
                        required = True
                        )
    
class IHasPhysInterface(Interface):
    """ Marker interface
    """
    pass

class IResolution(Interface):
    """
    """
    x = Int (
             title = u"X",
             description = u"X resolution",
             required = True
             )
    y = Int (
             title = u"Y",
             description = u"Y resolution",
             required = True
             )
    unit = Choice(
                  title = u"unit",
                  description = u"resolution unit",
                  values=[u'dpi', u'MPixels'],
                  required = True
                  )
    
class IHasResolution(Interface):
    """ Marker interface
    """
    pass