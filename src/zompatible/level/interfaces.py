# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.schema import TextLine, Int, List, Object
from zope.app.component.interfaces import ILocalSiteManager
from zope.app.container.constraints import containers


class ILevel(Interface):
    u"""
    must be implemented by support, trust and stability levels
    """
    level = Int(title=u'level', description=u'Level')
    description = TextLine(title=u'level description', description=u'description of the level')    

class ILevels(Interface):
    u"""
    The interface of the local utility that will store the available levels
    """
    containers(ILocalSiteManager)
    levels = List(title=u"available level", description=u"Avalailable levels", value_type=Object(ILevel, title=u"level"))


