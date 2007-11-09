# -*- coding: utf-8 -*-
import unittest
import doctest
from interfaces import *
from zope.component import provideUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.catalog.catalog import Catalog
from zope.app.testing import placelesssetup
from zope.app.folder.folder import Folder
import os
import re


def test_suite( ):
    # we create a testsuite
    suite = unittest.TestSuite()

    # we add the doctests contained in the zompatible.txt text file
    suite.addTest(doctest.DocFileSuite('product.txt', setUp=placelesssetup.setUp, tearDown=placelesssetup.tearDown))
    
    return suite

if __name__ == '__main__':
    unittest.main()