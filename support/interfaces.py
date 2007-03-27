# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.app.container.interfaces import IContainer
from zope.schema import Choice

class ISupported(Interface):
    u"""
    Interface added to software and devices to let them have a compatibility list
    """
    supports = Attribute("Compatibility List")


class ISupport(IContainer):
    u"""
    objet qui fait le lien entre un Device et un Software.
    Il pointe vers un Device et un Software,
    et contient des UserReports
    """
    software = Choice(title=u'software', description=u'software', source="softwaresource")
    device = Choice(title=u'device', description=u'a device', source="devicesource")
    
