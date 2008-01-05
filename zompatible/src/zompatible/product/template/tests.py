# -*- coding: utf-8 -*-
import unittest
import doctest
from interfaces import *
from zope.app.testing import placelesssetup

def test_suite( ):
    # we create a testsuite
    suite = unittest.TestSuite()

    # we add the doctests contained in the zompatible.txt text file
    suite.addTest(doctest.DocFileSuite('template.txt', setUp=placelesssetup.setUp, tearDown=placelesssetup.tearDown))
    
    return suite

if __name__ == '__main__':
    unittest.main()