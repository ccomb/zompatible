# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine, Object
from zope.interface import Interface



class IDevice(IContainer):
    u"""
    IDevice offers basic attributes of a device
    So a Device would be a container that can contain Features, Chips, PhysicalInterfaces and Driver
    Un device pourrait être une implémentation fournissant IDevice, IPhysicalInterface, IChiped, etc... ?
    Pour un contenu potentiellement infini (ex: devices pour un manufacturer), faire un folder
    Pour un contenu limité (ex: chip dans un device), mettre en attributs.
    """
    containers('zompatible.device.interfaces.IDeviceContainer')
    #contains('zompatible.driver.interfaces.IDriver')
    names = List(title=u'names', description=u'possible names of the device', value_type=TextLine(title=u'name', description=u'a name for the device (commercial name, code name, etc.)'))
#    physicalinterfaces = List(title=u'physical interfaces', description=u'list of physical interfaces on the device', value_type=Object(title=u'physical interface', description=u'a physical interface on the device', schema=IPhysicalInterface))
#    existingdrivers = List(title=u'existing drivers', description=u'list of supported OS', value_type=Object(title=u'supported OS', description=u'OS on which the device works', schema=IDriver))

class IDeviceContainer(IContainer):
    u"""
    a toplevel device container. This is a base storage for devices.
    """
    contains(IDevice)

class ISubDevices(Interface):
    u"""
    Must be implemented by a device that is made of other devices
    """
    subdevices = List(title=u'subdevices', description=u'subdevices', value_type=Object(title=u'subdevice', description=u'a subdevice (chip, component)', schema=IDevice))
