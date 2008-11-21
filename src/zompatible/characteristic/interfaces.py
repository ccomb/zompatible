# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.schema import Choice, Int, List
from zope.component.interface import  provideInterface
from zope.annotation.interfaces import IAttributeAnnotatable

class ICharacterizable(IAttributeAnnotatable):
    u""" Marker interface to be able to provide ICharacteristicManager on any object.
    """

class ICharacteristics(Interface):
    """interface through which object characteristics are retrieved or set
    """
    characteristics = List(title = u"Characteristics", 
                           description = u"Characteristics provided by an object",
                           value_type = Choice(title = u"Name", 
                                               description = u"Characteristic Names", 
                                               vocabulary = 'Characteristic Names'))


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

    def Add(iface):
        u""" Add the characteristic "iface"
        """

    def Remove(iface):
        u""" Remove the characteristic interface "iface"
             TODO: Should it also remove the values stored in the object ?
        """
    def Provides(ifaceList):
        u""" Replace characteristics by those provided in ifaceList (list of interfaces NAMES). 
        """
    def CurrentList( ):
        u""" Return all the characteristic interfaces NAMES provided by an object
        """
    def AvailableList( ):
        u""" Return all the characteristic available as a list of tuples:
            - name of the characteristic,
            - characteristic description (__doc__ of the Interface),
            - marker interface NAME (needs a queryInterface() call to be used),
            - interface NAME (needs a queryInterface())
        """

class ICharacteristic(Interface):
    u""" Base interface for characteristitics
    """

    def Name( ):
        u""" Return the characteristic name.
        """
    
    def __str__(context):
        u"""
        """

provideInterface('', ICharacteristic)


class IPhysicalInterface(ICharacteristic):
    u""" Describe a physical interface (USB, PCI, ...)
    """
    interface = Choice (
                        title = u"Physical interface",
                        description = u"Link interface",
                        values=[u'USB', u'PCI'],
                        required = True
                        )
    
class IHasPhysicalInterfaces(Interface):
    u""" Marker interface
    """
    pass

provideInterface('', IPhysicalInterface)
provideInterface('', IHasPhysicalInterfaces)

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
