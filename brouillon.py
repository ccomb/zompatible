from zope.interface import providedBy, alsoProvides
from zope.component import provideAdapter
from zope.interface import implements
from zope.component import adapts
from zope.schema import TextLine

from zope.interface import Interface

class IProduct(Interface):
    """
    """
    name = TextLine (
                    title = u"Name",
                    description = u"Name of the product",
                    required = True
                    )

class Product(object):
    implements(IProduct)
    
    name = u""
    
    def __init__(self, context):
        self.context = context
    

class IPrinter(Interface):
    """
    """
    def Name():
        """
        """

class IHasPrinter(Interface):
    """ Marker interface
    """
    pass

class HasPrinter(object):
    implements(IPrinter)
    adapts(IHasPrinter)
    def __init__(self,context):
        self.context = context
        
    def Name(self):
        print u"Printer interface"
        return


dev = Product("multi")
list(providedBy(dev))
provideAdapter(HasPrinter)
alsoProvides(dev, IHasPrinter)
IPrinter(dev).Name()
list(providedBy(dev))
