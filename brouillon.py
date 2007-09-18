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
 
    def __init__(self, name=None):
        self.name = name

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

#######################################
# Classes and interfaces from modules.
#######################################

from zompatible.product.product import Product
from zope.interface import providedBy, alsoProvides

multi = Product(u'Hewlett-Packard PhotoSmart C5180')
list(providedBy(multi))
print multi.Display()
from zope.interface import alsoProvides
from zope.component import provideAdapter
from zompatible.characteristic.interfaces import IHasPhysInterface, IPhysInterface
from zompatible.characteristic.characteristic import HasPhysInterface

alsoProvides(multi,IHasPhysInterface)
provideAdapter(HasPhysInterface) # implement(IPhysInterface) adapts(IHasPhysInterface)
IPhysInterface(multi).Name()

IPhysInterface(multi).interface = u'USB'
IPhysInterface(multi).Display()

multi.Display()

from zompatible.characteristic.interfaces import IHasResolution, IResolution
from zompatible.characteristic.characteristic import HasResolution

alsoProvides(multi,IHasResolution)
provideAdapter(HasResolution)
IResolution(multi).x = 4800
IResolution(multi).y = 1200
IResolution(multi).unit = u'dpi'

IResolution(multi).Display()


