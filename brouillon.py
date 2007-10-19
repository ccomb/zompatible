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
from zompatible.product.interfaces import IProduct
from zope.interface import providedBy, alsoProvides, directlyProvidedBy
from zope.component.interface import  provideInterface
from zope.interface import alsoProvides
from zope.component import provideAdapter

multi = Product(u'Hewlett-Packard PhotoSmart C5180')

from zompatible.characteristic.characteristic import CharacteristicManager
from zompatible.characteristic.interfaces import ICharacterizable, ICharacteristicManager

provideAdapter(CharacteristicManager)
alsoProvides(multi, ICharacterizable)

list(providedBy(multi))
multi.Display()

from zompatible.characteristic.interfaces import IHasPhysInterface, IPhysInterface, IFlashCardSlots
from zompatible.characteristic.characteristic import HasPhysInterface, HasFlashCardSlots

provideInterface('', IPhysInterface)
alsoProvides(multi,IHasPhysInterface)
provideAdapter(HasPhysInterface) # implement(IPhysInterface) adapts(IHasPhysInterface)
provideAdapter(HasFlashCardSlots)
IPhysInterface(multi).Name()

IPhysInterface(multi).interface = u'USB'
IPhysInterface(multi).Display()

multi.Display()

from zompatible.characteristic.interfaces import *
from zompatible.characteristic.characteristic import HasResolution

provideInterface('', IResolution)
alsoProvides(multi,IHasResolution)
provideAdapter(HasResolution)
IResolution(multi).x = 4800

IResolution(multi).y = 1200
IResolution(multi).unit = u'dpi'

IResolution(multi).Display()

# CHARACTERIZABLE

ICharacteristicManager(multi).AvailableList()
ICharacteristicManager(multi).CurrentList()

ICharacteristicManager(multi).Add(IFlashCardSlots)
ICharacteristicManager(multi).CurrentList()
list(directlyProvidedBy(multi))
ICharacteristicManager(multi).Remove(IFlashCardSlots)
ICharacteristicManager(multi).CurrentList()
list(directlyProvidedBy(multi))

ICharacteristicManager(multi).characteristicInterfaces
ICharacteristicManager(multi).characteristicInterfaces = [ u'Flash card slots' ]
ICharacteristicManager(multi).characteristicInterfaces
list(directlyProvidedBy(multi))

IFlashCardSlots(multi).InterfaceAttributesType


from zope.component import getUtility
from zope.schema.interfaces import  IVocabularyFactory
interfaces_factory = getUtility(IVocabularyFactory, u"Interfaces")
interfaces = interfaces_factory(multi)

#from zope.component import queryAdapter
from zope.component.interface import queryInterface
from zope.component.interface import  provideInterface

provideInterface('', IPhysInterface)
str(list(providedBy(multi))[0]).strip('><').split()[1] 
queryInterface('zompatible.characteristic.interfaces.IPhysInterface')

def getCharacteristicInterfaces(obj):
    l = list(providedBy(obj))
    l = [str(e) for e in l]
    l = [e for e in l if e.find('zompatible.characteristic.interfaces.') >= 0]
    l = [ e.replace(u'interfaces.IHas',u'interfaces.I') for e in l ]
    l = [e.strip('><').split()[1] for e in l]
    l = [ queryInterface(e) for e in l ]
    
    return l


from zompatible.categorynew.category import Category
printerCategory = Category(u'Printer')
alsoProvides(printerCategory, IHasResolution)
IResolution(printerCategory).Name()
IResolution(printerCategory).unit = 'dpi'
from zompatible.categorynew.interfaces import IIsPrinter
alsoProvides(printerCategory, IIsPrinter)
printer = printerCategory.NewProduct()

IResolution(printer).x = 4800
IResolution(printer).y = 1200
IResolution(printer).Display()

