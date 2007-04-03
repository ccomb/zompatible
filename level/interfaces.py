# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.schema import TextLine, Int, List, Object


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
    levels = List(title=u"available level", description=u"Avalailable levels", value_type=Object(ILevel, title=u"level"))


