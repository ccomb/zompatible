# -*- coding: utf-8 -*-
"""
Objective:
    Run doctests located in ../doc. Any file inside ../doc that ends with .txt
will be considered as a doctest.

Command line to run from the root directory to execute all the module doctests:
    bin/test -u test_docs -vv

Dependencies: 
    gettests.py in the current directory.

Source: 
    Python - Petit guide à l'usage du développeur agile - Tarek Ziadé
"""
import unittest
import os

from gettests import doc_suite

tests_dir = os.path.dirname(__file__)
package_dir = os.path.split(tests_dir)[0]
doc_dir = os.path.join(package_dir, 'doc')

globs = {}
globs["path"] = doc_dir

def setUp(test):
    pass

def tearDown(test):
    pass

def test_suite():
    # renvoi tous les doctsts contenus dans
    # le sous répertoire 'doc' du paquet
    return doc_suite(doc_dir, setUp, tearDown, globs)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
