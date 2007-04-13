# -*- coding: utf-8 -*-
from zope.app.folder import Folder
from zope.interface import implements
from zope.component import adapter
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.component.factory import Factory

from interfaces import *

class SupportContainer(Folder):
    u"main support container for all Support objects"

SupportContainerFactory = Factory(SupportContainer)

class Support(Folder):
    implements(ISupport)
    device = software = None

@adapter(ISupport, IObjectRemovedEvent)
def SupportDeletion(support, event):
    u"remove the two other symetric support objects remaining in the device and software"
    del support.device.supports[support.software], support.software.supports[support.device]



    
    