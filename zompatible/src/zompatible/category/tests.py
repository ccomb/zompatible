# -*- coding: utf-8 -*-
import unittest
import doctest
from category import AvailableCategories
from zope.app.testing import placelesssetup
from zope.component import provideAdapter, provideUtility, adapter
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.testing.setup import placefulSetUp, placefulTearDown
from zope.interface import Interface, implements
from zope.app.intid.interfaces import IIntIds

class DummyIntId(object):
    implements(IIntIds)
    MARKER = '__dummy_int_id__'
    def __init__(self):
        self.counter = 0
        self.data = {}
    def register(self, obj):
        intid = getattr(obj, self.MARKER, None)
        if intid is None:
            setattr(obj, self.MARKER, self.counter)
            self.data[self.counter] = obj
            intid = self.counter
            self.counter += 1
        return intid
    def getObject(self, intid):
        return self.data[intid]
    def __iter__(self):
        return iter(self.data)
    def getId(self, obj):
        for i in self.data:
            if obj is self.data[i]:
                return i


def setUp(test):
    site = placefulSetUp(True)
    provideAdapter(AvailableCategories)
    intids = IntIds()
    provideUtility(intids, IIntIds)
    intid = DummyIntId()
    provideUtility(intid, IIntIds)


def tearDown(test):
    placefulTearDown()

def test_suite( ):
    # we create a testsuite
    suite = unittest.TestSuite()

    # we add the doctests contained in the zompatible.txt text file
    suite.addTest(doctest.DocFileSuite(
        'category.txt',
         setUp = setUp,
         tearDown = placelesssetup.tearDown,
         optionflags = doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS))
    
    return suite

if __name__ == '__main__':
    unittest.main()