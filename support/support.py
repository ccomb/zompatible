# -*- coding: utf-8 -*-
from zope.app.folder import Folder
from zope.interface import implements
from zope.app.folder.interfaces import IFolder
from zope.component import adapts, adapter
from zope.app.container.interfaces import IObjectRemovedEvent


from interfaces import *

class SupportContainer(Folder):
    u"support container for all Support objects"

class Support(Folder):
    implements(ISupport)
    device = software = __name__ = __parent__ = None


@adapter(ISupport, IObjectRemovedEvent)
def SupportDeletion(support, event):
    u"remove the two other symetric support objects remaining"
    del support.device.supports[support.software], support.software.supports[support.device]