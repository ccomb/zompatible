# -*- coding: utf-8 -*-
from zope.publisher.browser import BrowserView
from zope.interface import implements, Interface
from zope.component import adapts
from zope.publisher.interfaces.browser import IBrowserRequest
from interfaces import IPrettyName

class PrettyName(BrowserView):
    """
    Generic implementation of the prettyname view.
    This is similar to the absolute_url view and allow
    to generate a pretty name for any object that don't
    implements its own pretty name view
    
    We create an object::
    
        >>> class A(object):
        ...     pass
        ...
        >>> a=A()
    
    We register the prettyname adapter::
    
        >>> from zompatible.skin.browser import PrettyName
        >>> from zompatible.skin.interfaces import IPrettyName
        >>> from zope.app.testing import ztapi
        >>> ztapi.provideAdapter((Interface, IBrowserRequest), IPrettyName, PrettyName)
    
    We try to display the pretty name of the object::
    
        >>> from zope.publisher.browser import TestRequest
        >>> from zope.component import getMultiAdapter
        >>> getMultiAdapter((a, TestRequest()), IPrettyName)()
        u'Unnamed object'
    
    If the object has a __name__, names, or name, it is chosen::
    
        >>> a.__name__ = 'name1'
        >>> getMultiAdapter((a, TestRequest()), IPrettyName)()
        'name1'
        >>> a.names = ['name2', 'name3']
        >>> getMultiAdapter((a, TestRequest()), IPrettyName)()
        'name2'
        >>> a.name = 'name4'
        >>> getMultiAdapter((a, TestRequest()), IPrettyName)()
        'name4'
    """
    implements(IPrettyName)
    adapts(Interface, IBrowserRequest)
    def __call__(self):
        if hasattr(self.context, 'name') and self.context.name:
            return self.context.name
        if hasattr(self.context, 'names') and len(self.context.names) >=1:
            return self.context.names[0]
        if hasattr(self.context, '__name__'):
            return self.context.__name__
        return u'Unnamed object'