# -*- coding: utf-8 -*-
from zope.interface import implements
from persistent import Persistent
from zope.app.folder.folder import Folder
from zope.component import adapts, adapter
from zope.schema.interfaces import ISource, IVocabularyFactory
from zope.app.component.hooks import getSite
from zope.app.container.interfaces import INameChooser, IObjectRemovedEvent
from zope.app.container.contained import NameChooser
from zope.component.factory import Factory
from zope.copypastemove import ObjectMover
import string
from BTrees.OOBTree import OOBTree
from zope.app.folder.interfaces import IFolder
from zope.app.container.contained import Contained
from zope.app.container.interfaces import IContained, IContainer
from zope.component.interface import queryInterface
from zompatible.characteristic.interfaces import ICharacteristicManager
from interfaces import *

class Product(Persistent):
    implements(IProduct, ISubProducts)
    names=[]
    subdevices=[]
    description = u""
    pciid=""
    usbid=""
    # IDevice fournit IContained donc il faut mettre ces attributs :
    __name__=__parent__= None
    def __init__(self, names=None, description=None):
        self.names = names
        self.description = description
        self.supports = OOBTree() #the list of supported software that lead to the Support objects
        super(Device, self).__init__()
    def __get_organization(self): # used in the property
        if self.__parent__ is not None:
            return self.__parent__.__parent__
        return None
    def __set_organization(self, orga): # used in the property
        if orga is not self.__parent__ and orga is not None and self.__parent__ is not None:
            mover = ObjectMover(self)
            if not mover.moveableTo(orga['products']):
                raise "Impossible action" # FIXME set a correct derived exception
            else:
                mover.moveTo(value['products'])
    def __del_organization(self):
        raise NotImplementedError # FIXME → move the product in a noname area
    organization = property(__get_organization, __set_organization, __del_organization)
        
deviceFactory = Factory( Device,
                         title = u"Product factory",
                         description = u"This factory instantiates a new Product.")

class Device(Product):
    u"FIXME: should probably be removed since a device is a product category"
    implements(IDevice)
    pciid=""
    usbid=""

class Software(Product):
    u"FIXME: should probably be removed since a software is a product category"
    implements(ISoftware)
    builtVersion = u""
    architectures = []
    version = codename = u""
    url=""
    #architectures = List(title=u'architectures', description=u'architectures that software applies to', value_type=Object(title=u'architecture',description=u'list of architectures', schema=IArchitecture))


@adapter(IProduct, IObjectRemovedEvent)
def ProductRemovedEvent(product, event):
    u"a subscriber that throws the product into the trash if it contains support objects, instead of deleting it"
    if event.newParent is None and len(product.supports) != 0 :
        trash = getSite()['trash']
        device_name = INameChooser(trash).chooseName(u"",product)
        trash[device_name]=product

        
class ProductContainer(Folder):
    """
    a folder that contains devices
    """
    __name__=__parent__= None
    implements(IProductContainer)


class ProductNameChooser(NameChooser):
    u"""
    adapter that allows to choose the name of the Product from the container point of view
    The real name is stored in an attribute, but this name is important
    as it appears in the URL and is used for traversing    """
    implements(INameChooser)
    adapts(IProduct)
    def chooseName(self, name, product):
        if not name and product is None:
            raise "ProductNameChooser Error"
        rawname = name
        if product is not None and len(product.names)>0:
            rawname = product.names[0]
        return string.lower(rawname).strip().replace(' ','-').replace(u'/',u'-').lstrip('+@') # FIXME: UTILISER PEUT-ÊTRE UNICODE.LOWER
    def checkName(self, name, product): # FIXME: **************************utiliser le super.checkName ) la place
        if name in product.__parent__ and product is not product.__parent__['name']:
            return False
        else :
            return True

class SoftwareNameChooser(ProductNameChooser): # FIXME: should be remove if software is turned into a category
    u"slightly modified name chooser derived from the product name chooser"
    implements(INameChooser)
    adapts(ISoftware)
    def chooseName(self, name, software):
        if not name and software is None:
            raise "SoftwareNameChooser Error"
        rawname = name
        if software is not None and len(software.names)>0:
            rawname = software.names[0]
        codename = version = u""
        if software.codename:
            codename="-" + software.codename
        if software.version:
            version = software.version
        return string.lower(rawname + "-" + version + codename).strip().replace(' ','-').replace(u'/',u'-').lstrip('+@')


# Autre méthode pour créer un objectwidget ? (pas encore testé)
#class DeviceWidget(ObjectWidget):
#    __used_for__ = IDevice
#    subdevices_widget = CustomWidgetFactory(ObjectWidget, Device)

class SearchableTextOfProduct(object):
    u"""
    l'adapter qui permet d'indexer les devices. Il fournit le texte à indexer depuis le contenu d'un objet product.
    Il est possible d'indexer n'importe quels attributs,
    et même les traductions qui se trouvent dans des fichiers .po externes !!
    """
    implements(ISearchableTextOfProduct)
    adapts(IProduct)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        u"FIXME: peut probablement être optimisé"
        sourcetext = texttoindex = u''
        u"on commence par créer un texte depuis tous les noms"
        for word in self.context.names:
            sourcetext += word + " "
        u"""puis on génère les sous-mots pour pouvoir rechercher les parties des noms
        par exemple, foobar donnera : foobar oobar obar bar ar r"""
        for word in sourcetext.split():        
            for subword in [ word[i:] for i in xrange(len(word)) if len(word)>=1 ]:
                texttoindex += subword + " "
        return texttoindex


class SearchableTextOfSoftware(object):
    u"""
    The adapter that allows to index software objects
    """
    implements(ISearchableTextOfSoftware)
    adapts(ISoftware)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        sourcetext = texttoindex = u''
        u"First, gather all interesting text"
        for word in self.context.names + [ self.context.version, self.context.codename ] :
            sourcetext += word + " "
        u"then split all words into subwords"
        for word in sourcetext.split():        
            for subword in [ word[i:] for i in xrange(len(word)) if len(word)>=1 ]:
                texttoindex += subword + " "
        return texttoindex

class ProductSource(object):
    """
    implémentation de la Source de Products utilisée dans le schema de sub_products.
    Il s'agit juste d'implémenter ISource
    Cette source est censée représenter l'ensemble de tous les products.
    Elle parcourt toutes les organizations et recherche le product voulu.
    *********
    FIXME: ATTENTION, dans l'implémentation ci-dessous, si deux orga ont
    FIXME: des products avec le même nom, seul le 1er est retourné.
    """
    implements(ISource)
    def __contains__(self, value):
        root = getSite()
        for orga in root['organizations']:
            if 'product' in root['organizations'][orga] and value.__name__ in root['organizations'][orga]['product'].keys():
                return True
        return False

class ProductVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return ProductSource()
 
#class FuzzyDevice(Device):
    #u"""
    #A class that represents a device or another, for people that don't
    #really know which one to choose. This just a container for a series of
    #devices that are the same, or in which people don't really see the difference
    #or that are managed by the same driver
    #"""
    #implements(IDevice, ISupported)
    #names = []
    ##organization = None
    #description = u""
    #devices = []
    #supports
    
#class FuzzySoftware(Software):
#    u"""
#    a software representing several softwares
#    For ex : ubuntu representing all variants (kubuntu, ubuntu server, etc.)
#    It contains the union of all support objects an can have its own supports.
#    """
#    implements(IFuzzy)
#    group = []
    





