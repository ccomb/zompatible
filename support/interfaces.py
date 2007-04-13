# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains
from zope.schema import Choice

class ISupported(Interface):
    u"""
    Interface added to software and devices to let them have a compatibility list
    """
    supports = Attribute("Compatibility List")

class ISupportContainer(IContainer, IContained):
    u"""
    The main container that stores Support object
    """
    contains("zompatible.support.interfaces.ISupport")

class ISupport(IContainer):
    u"""
    object that links a software to a device
    It contains references to the software and device objects
    and a list of Report objects
    """
    software = Choice(title=u'software', description=u'software', source="softwaresource")
    device = Choice(title=u'device', description=u'a device', source="devicesource")
    
