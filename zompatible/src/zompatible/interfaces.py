# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContainer
from zope.app.component.interfaces import IPossibleSite
from zope.component.interfaces import IObjectEvent


class IZompatibleSite(IPossibleSite, IContainer):
    u"""
    The (empty) interface of the main zompatible site container
    This interface could be used to define high-level functions
    to abstract the object hierarchy. (for ex accessing organizations).
    """

class IZompatibleSiteManagerSetEvent(IObjectEvent):
    u"""
    The event fired when a zompatible site is added.
    The subscriber must create the objects and utilities required to running the site
    in particular the IntId, the catalog and indices, the trash, etc.
    """ 

class ITrash(IContainer):
    u"""The trash that receive the deleted objects"""



# définir une interface IVersionned pour dire qu'un truc est versionné ?

# reste des définitions initiales non déplacées dans des packages séparés.
# voir au début du memo.txt  IOsSupport et IAction
