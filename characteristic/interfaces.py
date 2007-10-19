from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.schema import Choice, TextLine, Int, List, Iterable
from zope.component.interface import  provideInterface

class ICharacterizable(Interface):
    u""" Marker interface to be able to provide ICharactericManager on any object.
    """

class ICharacteristicManager(Interface):
    u""" This interface manages characteristic interfaces that can be provided by a
         ICharacterizable object
    """
    characteristicInterfaces = List(title=u"Characteristics", 
                                    description=u"Characteristics that can be provided by a ICharacterizable", 
                                    value_type=Choice(
                                                      title=u'Name', 
                                                      description=u'Characteristic Names', 
                                                      vocabulary="Characteristic Names"
                                                      )
                                    )

    def Add(self, iface):
        u""" Add the characteristic "iface"
        """

    def Remove(self, iface):
        u""" Remove the characteristic interface "iface"
             TODO: Should it also remove the values stored in the object ?
        """
    def Provides(self, ifaceList):
        u""" Replace characteristics by those provided in ifaceList (list of interfaces NAMES). 
        """
    def CurrentList(self):
        u""" Return all the characteristic interfaces NAMES provided by an object
        """
    def AvailableList(self):
        u""" Return all the characteristic available as a list of tuples:
            - name of the characteristic,
            - characteristic description (__doc__ of the Interface),
            - marker interface NAME (needs a queryInterface() call to be used),
            - interface NAME (needs a queryInterface())
        """

class ICharacteristic(Interface):
    u""" Base interface for characteristitics
    """

    def Name(self):
        u""" Return the characteristic name.
        """
    
    def __str__(self,context):
        u"""
        """

provideInterface('', ICharacteristic)


class IPhysInterface(ICharacteristic):
    u""" Describe a physical interface (USB, PCI, ...)
    """
    interface = Choice (
                        title = u"Physical interface",
                        description = u"Link interface",
                        values=[u'USB', u'PCI'],
                        required = True
                        )
    
class IHasPhysInterface(Interface):
    u""" Marker interface
    """
    pass

provideInterface('', IPhysInterface)
provideInterface('', IHasPhysInterface)

class IResolution(ICharacteristic):
    u""" Resolution parameter.
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
    u""" Marker interface
    """
    pass

provideInterface('', IResolution)
provideInterface('', IHasResolution)

class IFlashCardSlots(ICharacteristic):
    u""" Flash card reader characteristics.
    """
    type = List(
                  title = u"Flash cards slot",
                  description = u"flash card slot",
                  value_type = Choice(
                                      values=[u'CF', u'Memory Stick', u'SD']
                                      ),
                  required = True
                  )

class IHasFlashCardSlots(Interface):
    u""" Marker interface
    """
    pass

provideInterface('', IFlashCardSlots)
provideInterface('', IHasFlashCardSlots)

class IPaperFormat(ICharacteristic):
    u""" Describe the paper formats supported.
    """
    paperType = List (
                      title = u"Paper format",
                      description = u"Paper format",
                      value_type = Choice(
                                          values=[u'A3', u'A4', u'A6', u'A7']
                                          ),
                      required = True
                      )

class IHasPaperFormat(Interface):
    u""" Marker interface
    """
    pass

provideInterface('', IPaperFormat)
provideInterface('', IHasPaperFormat)

