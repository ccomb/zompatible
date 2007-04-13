# -*- coding: utf-8 -*-
from zope.viewlet.interfaces import IViewletManager
from zope.app.container.interfaces import IContainer
from zope.app.component.interfaces import IPossibleSite
from zope.component.interfaces import IObjectEvent

sitename="Zompatible"


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

class IMainAreaManager(IViewletManager):
    u"""
    This is the viewlet manager for the central area in the homepage.
    It should at least contain the main search viewlet
    """

class IAdminAreaManager(IViewletManager):
    u"""
    The viewlet manager for the admin viewlets
    """

class IToolboxManager(IViewletManager):
    u"""
    The viewlet manager for a side toolbox
    """



# définir une interface IVersionned pour dire qu'un truc est versionné ?

# reste des définitions initiales non déplacées dans des packages séparés.
# voir au début du memo.txt  IOsSupport et IAction
