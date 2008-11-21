# -*- coding: utf-8 -*-
import unittest
import doctest

from zope.app.testing import placelesssetup

from zompatible.characteristic.interfaces import ICharacteristics, ICharacterizable
from zompatible.characteristic.characteristic import Characteristics
from zompatible.product.product import Product
from zope.component import provideAdapter
from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from zope.interface import classImplements

def setUp(test):
    placelesssetup.setUp(test)
    provideAdapter(Characteristics, provides=ICharacteristics)
    provideAdapter(AttributeAnnotations, provides=IAnnotations)
    classImplements(Product, ICharacterizable)

def test_suite( ):
    # we create a testsuite
    suite = unittest.TestSuite()

    # we add the doctests contained in the docfile
    suite.addTest(doctest.DocFileSuite(
            'template.txt',
             setUp = setUp,
             tearDown = placelesssetup.tearDown,
             optionflags = doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS))
    
    return suite

if __name__ == '__main__':
    unittest.main()