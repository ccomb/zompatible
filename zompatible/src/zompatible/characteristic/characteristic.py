# -*- coding: utf-8 -*-
from zope.interface import implements, Interface
from zope.component import adapts
from zope.location import Location
from zope.annotation.interfaces import IAnnotations
from persistent.list import PersistentList
from interfaces import ICharacteristic, ICharacterizable, ICharacteristics

CHARACTERISTICS_KEY = 'zompatible.characteristics'

class Characteristics(Location):
    u"""
    The adapter that writes and retrieves the characteristics put on any object
    """
    adapts(ICharacterizable)
    implements(ICharacteristics)

    def __init__(self, context):
        self.context = context

    def _get_characteristics(self):
        try:
            return IAnnotations(self.context)[CHARACTERISTICS_KEY]
        except KeyError:
            characteristics = PersistentList()
            IAnnotations(self.context)[CHARACTERISTICS_KEY] = characteristics
            return characteristics

    def _set_characteristics(self, characteristics):
        IAnnotations(self.context)[CHARACTERISTICS_KEY] = PersistentList(characteristics)

    characteristics = property(_get_characteristics, _set_characteristics)


class Characteristic(object):
    implements(ICharacteristic)
    adapts(Interface)
    def __init__(self, name, value, unit=None):
        self.name, self.value, self.unit = name, value, unit
    

