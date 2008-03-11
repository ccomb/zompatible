# -*- coding: utf-8 -*-
from zope.interface import implements, Interface
from zope.component import adapts
from zope.location import Location
from zope.annotation.interfaces import IAnnotations
from persistent.list import PersistentList
from interfaces import ICharacteristic, ICharacterizable, ICharacteristics

__characteristics_key__ = 'zompatible.characteristics'

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
            return IAnnotations(self.context)[__characteristics_key__]
        except KeyError:
            characteristics = PersistentList()
            IAnnotations(self.context)[__characteristics_key__] = characteristics
            return characteristics

    def _set_characteristics(self, characteristics):
        IAnnotations(self.context)[__characteristics_key__] = PersistentList(characteristics)

    characteristics = property(_get_characteristics, _set_characteristics)


class Characteristic(object):
    implements(ICharacteristic)
    adapts(Interface)
    def __init__(self, name, value, unit=None):
        self.name, self.value, self.unit = name, value, unit
    

