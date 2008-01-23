# -*- coding: UTF-8 -*-
""" 
Unitary test file example. 

Command line to run it from the root directory :
bin/test -u test_module -vv
"""
import unittest
import os
import sys

dirname = os.path.dirname(__file__)
if dirname == '':
        dirname = '.'
dirname = os.path.realpath(dirname)
updir = os.path.split(dirname)[0]
if updir not in sys.path:
    sys.path.append(updir)
    
class ModuleTest(unittest.TestCase):
    def test1(self):
        print u'test 1'
        
def test_suite():
    tests = [unittest.makeSuite(ModuleTest)]
    return unittest.TestSuite(tests)

if __name__ == '__main__':
    unittest.main(defaultTest = 'test_suite')
    
    