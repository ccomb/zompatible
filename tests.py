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

# We launch the tests with bin/test -s zompatible -pvv
# The script looks for all the 'tests*' and get the test suite by executing test_suite of each tests module. 

# This module should test only global stuffs
# component specific tests must go into their respective package

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

    def test_example2(self):
        pass # here we do the tests

    def tearDown(self):
        # we clean the setup

        # ...
        
        placelesssetup.tearDown()

class CheckNoSelfInInterfaces(unittest.TestCase):
    u"This tests checks there is no 'self' in every method definitions of interfaces"
    def test(self):
        import zompatible
        zompatible_folder_name = os.path.dirname(zompatible.__file__)
        for currentwalk in os.walk(zompatible_folder_name):
            currentdir = currentwalk[0]
            currentdir_content = os.listdir(currentdir)
            if '__init__.py' in currentdir_content and 'interfaces.py' in currentdir_content:
                interface_file_name = os.path.join(currentdir, 'interfaces.py')
                try:
                    f = open(interface_file_name)
                    for line in [line.decode('utf-8') for line in f.readlines()]:
                        self.failIf(re.compile(u'^ *def .*( *self *)').match(line), 
                                    u"A method definition in an interface cannot have 'self':\nline: %sin file: %s" % (line, interface_file_name))
                                    
                finally:
                    f.close()


def test_suite( ):
    # we create a testsuite
    suite = unittest.TestSuite()
    # we add the current unit test
    suite.addTest(unittest.makeSuite(CheckNoSelfInInterfaces))

    # we add the doctests contained in the zompatible.txt text file
    suite.addTest(doctest.DocFileSuite('zompatible.txt', setUp=placelesssetup.setUp, tearDown=placelesssetup.tearDown))
    
    # we add the inline doctests contained in the different modules
    #suite.addTest(doctest.DocTestSuite('zompatible.organization'))

    
    return suite

if __name__ == '__main__':
    unittest.main()