# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import unittest
import doctest
from category import AvailableCategories
from zope.app.testing import placelesssetup
from zope.component import provideAdapter

def setUp(test):
    #placelesssetup.setUp(test)
    provideAdapter(AvailableCategories)

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