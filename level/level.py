# -*- coding: utf-8 -*-
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import alsoProvides, implements
from persistent.list import PersistentList
from persistent import Persistent

from interfaces import *

class Level(Persistent):
    u"""
    must be implemented by support, trust and stability levels
    """
    implements(ILevel)
    level = description = None
    
class Levels(Persistent):
    implements(ILevels)
    u"used only for subclasses"
    levels = PersistentList()

class EasinessLevels(Levels):
    pass

class StabilityLevels(Levels):
    pass

class EasinessLevelsVocabulary(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        levels = getUtility(ILevels, 'easiness_levels')
        return SimpleVocabulary.fromValues(levels.levels)

class StabilityLevelsVocabulary(object):
    implements(IVocabularyFactory)
    def __call_(self, context):
        levels = getUtility(ILevels, 'stability_levels')
        return SimpleVocabulary.fromValues(levels.levels)
