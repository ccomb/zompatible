# -*- coding: utf-8 -*-
from zope.app.folder import Folder
from zope.interface import implements 


from interfaces import *

    
class Support(Folder):
    implements(ISupport)
    device = software = None
    