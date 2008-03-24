# -*- coding: utf-8 -*-
from zope.app.folder import Folder
from zope.interface import implements
from zope.component import adapter
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.component.factory import Factory
from persistent.list import PersistentList

from interfaces import *

class SupportContainer(Folder):
    u"main support container for all Support objects"

SupportContainerFactory = Factory(SupportContainer)

class Support(Folder):
    implements(ISupport)
    products = PersistentList()

@adapter(ISupport, IObjectRemovedEvent)
def SupportDeletion(support, event):
    u"remove the two other symetric support objects remaining in the products"
    for product in support.products:
        del product.support



    
    