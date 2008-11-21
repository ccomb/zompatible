# -*- coding: utf-8 -*-
import unittest
import doctest
from interfaces import *

def test_suite( ):
    # we create a testsuite
    suite = unittest.TestSuite()       
    suite.addTest(doctest.DocTestSuite('zompatible.skin.browser'))
    return suite

if __name__ == '__main__':
    unittest.main()