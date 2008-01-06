# -*- coding: utf-8 -*-
import unittest
import doctest
from interfaces import *
from zope.app.testing import placelesssetup

def test_suite( ):
    # we create a testsuite
    suite = unittest.TestSuite()

    # we add the doctests contained in the docfile
    suite.addTest(doctest.DocFileSuite(
            'report.txt',
             setUp = placelesssetup.setUp,
             tearDown = placelesssetup.tearDown,
             optionflags = doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS))
    
    return suite

if __name__ == '__main__':
    unittest.main()