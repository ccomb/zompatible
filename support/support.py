from zope.app.folder import Folder
from persistent import Persistent
from zope.interface import implements 


from interfaces import *

class SupportContainer(Folder):
    implements(ISupportContainer)
    __name__ = __parent__ = None
    
class Support(Folder):
    implements(ISupport)
    __name__ = __parent__ = None
    device = software = None
    