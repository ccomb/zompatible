from zope.interface import Interface
from zope.schema import Choice, TextLine, Int
from zope.component.interface import  provideInterface

class ICharacteristic(Interface):
    """ Marker interface
    """
    pass

class IPhysInterface(ICharacteristic):
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

provideInterface('', IPhysInterface)

class IResolution(ICharacteristic):
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

provideInterface('', IResolution)

class IFlashCardSlots(ICharacteristic):
    """
    """
    type = Choice (
                   title = u"Flash cards slots",
                   description = u"List of all the flash cards slots available",
                   values=[u'CF', u'Merory Stick', u'SD'],
                   required = True
                   )

class IHasFlashCardSlots(Interface):
    """ Marker interface
    """
    pass

provideInterface('', IFlashCardSlots)
