# -*- coding: utf-8 -*-
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility
from zope.schema.interfaces import IVocabulary, IVocabularyFactory
from zope.interface import alsoProvides, implements
from zope.app.container.constraints import containers
from persistent.list import PersistentList
from persistent import Persistent
from interfaces import *

class Level(Persistent):
    u"""
    must be implemented by support, trust and stability levels
    """
    implements(ILevel)
    level = description = None
    def __init__(self, level=None, description=None):
        self.level, self.description = level, description
    
_default_easiness_levels = [
Level(0, u"It worked out of the box"),
Level(1, u"Someone made it work for me"),
Level(2, u"It didn't work")
]

_default_stability_levels = [
Level(0, u"It's very stable!"),
Level(1, u"I have some problems"),
Level(2, u"it's not usable")
]


class Levels(Persistent):
    implements(ILevels)
    u"used only for subclasses"
    levels = PersistentList()

class EasinessLevels(Levels):
    def __init__(self):
        self.levels=_default_easiness_levels


class StabilityLevels(Levels):
    def __init__(self):
        self.levels=_default_stability_levels

class EasinessLevelsVocabulary(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        levels = getUtility(ILevels, 'easiness_levels')
        return SimpleVocabulary.fromItems([("%s %s"%(level.level,level.description),level) for level in levels.levels])

class StabilityLevelsVocabulary(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        levels = getUtility(ILevels, 'stability_levels')
        return SimpleVocabulary.fromItems([("%s %s"%(level.level,level.description),level) for level in levels.levels])
