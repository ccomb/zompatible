# -*- coding: utf-8 -*-
"""
This is an example of a module source code that belongs to the skeleton package.
Doctests are inline.
Calling the file from the command line run all the doctests in this module.

This example is also a reference concerning the typography of the source code.
"""
from zope.interface import implements
from interfaces import *

ELEVEN_NUMBER = 11

class MyFirstClass(object):
    implements(IMyFirstInterface)
    
    def displayText(self, text):
        """ Display the text "text".
        
        Example:
            
            >>> text = "coucou"
            >>> c = MyFirstClass()
            >>> c.displayText(text)
            coucou
            
        """
        is_displayed = True
        if is_displayed:
            print text
        
def _test():
    import doctest
    doctest.testmod()
    
if __name__ == "__main__":
    _test()

