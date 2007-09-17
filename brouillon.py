from zope.interface import providedBy, alsoProvides
from zope.component import provideAdapter
from zope.interface import implements
from zope.component import adapts
from zope.schema import TextLine

from zope.interface import Interface

###########
# PRODUCTS
###########
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

#################    
# CARACTERISTICS
#################
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
    

##############
# CATEGORIES
##############
import copy
from zope.interface import directlyProvidedBy, directlyProvides

class ICategory(IProduct):
    """
    """
    pass

class Category(Product):
#    implements(ICategory)
    
    def __init__(self, context):
        self.context = context
        alsoProvides(self, ICategory)
        
    def NewProduct(self):
        prod = copy.deepcopy(self)
        directlyProvides(prod, directlyProvidedBy(prod) - ICategory)
        return prod


dev = Product("multi")
list(providedBy(dev))
provideAdapter(HasPrinter)
alsoProvides(dev, IHasPrinter)
IPrinter(dev).Name()
list(providedBy(dev))
