# -*- coding: utf-8 -*-
import unittest
import doctest
from interfaces import *
from zope.component import provideUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.catalog.catalog import Catalog
from zope.app.testing import placelesssetup

# We launch the tests with bin/test -s zompatible -pvv
# The script looks for all the 'tests*' and get the test suite by executing test_suite of each tests module. 

class ExampleTestCase(unittest.TestCase):

    def setUp(self):
        # this brings many registrations (event handling, i18n, authentication, default namechooser for containers, etc.)
        placelesssetup.setUp()
        # we may need a catalog
        provideUtility(Catalog(), ICatalog)
        # we may need a fake root to store things
        self.root = Folder()

        # ...
              
    def test_example1(self):
        pass # here we do the tests
    
    def tearDown(self):
        # we clean the setup

        # ...
        
        placelesssetup.tearDown()




def test_suite( ):
    # we create a testsuite
    suite = unittest.TestSuite()
    # we add the doctests contained in the zompatible.txt text file
    suite.addTest(doctest.DocFileSuite('zompatible.txt', setUp=placelesssetup.setUp, tearDown=placelesssetup.tearDown))
    
    # we add the inline doctests contained in the different modules
    #suite.addTest(doctest.DocTestSuite('zompatible.organization'))

    # we add the current unit test
    suite.addTest(unittest.makeSuite(ExampleTestCase))
    
    return suite

if __name__ == '__main__':
    unittest.main()