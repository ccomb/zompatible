# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains
from zope.schema import List, TextLine, Choice
from zope.interface import Interface
from zope.index.text.interfaces import ISearchableText


class IDevice(IContainer, IContained):
    u"""
    IDevice offers basic attributes of a device
    So a Device would be a container that can contain Features, Chips, PhysicalInterfaces and Driver
    Un device pourrait être une implémentation fournissant IDevice, IPhysicalInterface, IChiped, etc... ?
    Pour un contenu potentiellement infini (ex: devices pour un organization), faire un folder
    Pour un contenu limité (ex: chip dans un device), mettre en attributs.
    """
    #containers('zompatible.device.interfaces.IDeviceContainer')
    #contains('zompatible.driver.interfaces.IDriver')
    names = List(title=u'names', description=u'possible names of the device', value_type=TextLine(title=u'name', description=u'a name for the device (commercial name, code name, etc.)'))
#    physicalinterfaces = List(title=u'physical interfaces', description=u'list of physical interfaces on the device', value_type=Object(title=u'physical interface', description=u'a physical interface on the device', schema=IPhysicalInterface))
#    existingdrivers = List(title=u'existing drivers', description=u'list of supported OS', value_type=Object(title=u'supported OS', description=u'OS on which the device works', schema=IDriver))
    pciid = TextLine(title=u'pci id', description=u'PCI identifier', required=False)



class IDeviceContainer(IContainer, IContained):
    u"""
    a toplevel device container. This is a base storage for devices.
    """
    contains(IDevice)
    


class ISubDevices(Interface):
    u"""
    interface of an object that has subdevices.
    The source is called as a named utility registered for IVocabularyFactory (see in device.py)
    """
    subdevices = List(title=u'subdevices', value_type=Choice(title=u'subdevice', description=u'a subdevice (chip, component)', source="devicesource"), required=False)


class ISearchableTextOfDevice(ISearchableText):
    u"""
    l'interface marqueur qui permet d'indexer juste les devices
    """