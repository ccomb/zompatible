from persistent import Persistent

from zope.app.folder.folder import Folder
from zope.app.folder.interfaces import IFolder
from zope.app.container.contained import Contained
from zope.app.container.interfaces import IContained, IContainer
from zope.interface import implements
from zope.component.interface import queryInterface
from zope.component.factory import Factory

from zompatible.characteristic.interfaces import ICharacteristicManager

from interfaces import *

class Product(Persistent, Contained):
    implements(IProduct, IContainer, IContained)
    
    def __init__(self, name=None):
        self.__name__ = name
        self.__parent__ = None

        self.name = name
        self.categories = []
        
    def Display(self):
        # Display the product name
        print u'Name: %s' % self.name
        self.DisplayCharacteristics()
        self.DisplayProducts()
    
    def DisplayCharacteristics(self):
        l = ICharacteristicManager(self).CurrentList()
        if len(l) > 0:
            print u'Characteristics:'
            for e in l:
                iface = queryInterface(e)
                iface(self).Display()
            
    def DisplayProducts(self):
        for e in self.items():
            print u'-----'
            e[1].Display()

    def GetCategories(self):
        u""" Return the list of categories names the product belongs to. 
        """
        cat = []
        for e in self.categories:
            cat.append(e.name)
        for e in self.items():
            cat.extend(e[1].GetCategories())
        return cat
    
    def GetProduct(self, category):
        u""" Return a sub product that belongs to the category
        """
        for e in self.categories:
            if category == e.name:
                return self

        for e in self.items():
            obj = e[1].GetProduct(category)
            if obj != None:
                return obj

        return None

productFactory = Factory(
                         Product,
                         title=u"Product factory",
                         description = u"This factory instantiates a new Product."
                         )

        
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

from interfaces import *

@adapter(IDevice, IObjectRemovedEvent)
def DeviceRemovedEvent(device, event):
    u"a subscriber that put the device into trash if it contains support objects, intead of deleting it"
    if event.newParent is None and len(device.supports) != 0 :
        trash = getSite()['trash']
        device_name = INameChooser(trash).chooseName(u"",device)
        trash[device_name]=device

class DeviceContainer(Folder):
    """
    a folder that contains devices
    """
    __name__=__parent__= None
    implements(IDeviceContainer)

class Device(Persistent):
    implements(IDevice, ISubDevices)
    names=[]
    subdevices=[]
    description = u""
    pciid=""
    usbid=""
    # IDevice fournit IContained donc il faut mettre ces attributs :
    __name__=__parent__= None
    def __init__(self, names=None, description=None):
        u"the list of supported software that lead to the Support objects"
        self.names = names
        self.description = description
        self.supports = OOBTree()
        super(Device, self).__init__()
    def __getattr__(self, name):
        if name == 'organization':
            if self.__parent__ is not None:
                return self.__parent__.__parent__
            return None
        return super(Device, self).__getattr__(name)
    def __setattr__(self, name, value):
        if name == 'organization':
            if value is not self.__parent__ and value is not None and self.__parent__ is not None:
                mover = ObjectMover(self)
                if not mover.moveableTo(value['devices']):
                    raise "Impossible action"
                else:
                    mover.moveTo(value['devices'])
        else:
            super(Device, self).__setattr__(name, value)
        
deviceFactory = Factory(
    Device,
    title=u"Device factory",
    description = u"This factory instantiates new Device."
    )
    
class DeviceNameChooser(NameChooser):
    u"""
    adapter qui permet de choisir le nom du device auprès du container
    Le vrai nom est stocké dans un attribut, mais ce nom est aussi important
    car il apparaît dans l'URL, et sert pour le traversing.
    """
    implements(INameChooser)
    adapts(IDevice)
    def chooseName(self, name, device):
        if not name and device is None:
            raise "DeviceNameChooser Error"
        rawname = name
        if device is not None and len(device.names)>0:
            rawname = device.names[0]
        return string.lower(rawname).strip().replace(' ','-').replace(u'/',u'-').lstrip('+@') # UTILISER PEUT-ÊTRE UNICODE.LOWER*********************
    def checkName(self, name, device): # **************************utiliser le super.checkName ) la place
        if name in device.__parent__ and device is not device.__parent__['name']:
            return False
        else :
            return True

# Autre méthode pour créer un objectwidget ? (pas encore testé)
#class DeviceWidget(ObjectWidget):
#    __used_for__ = IDevice
#    subdevices_widget = CustomWidgetFactory(ObjectWidget, Device)

class SearchableTextOfDevice(object):
    u"""
    l'adapter qui permet d'indexer les devices. Il fournit le texte à indexer depuis le contenu d'un objet device.
    Le principe est génial car ça permet notamment d'indexer n'importe quels attributs,
    et même les traductions qui se trouvent dans des fichiers .po externes !!
    """
    implements(ISearchableTextOfDevice)
    adapts(IDevice)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        u"peut probablement être optimisé"
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

class DeviceSource(object):
    """
    implémentation de la Source de Devices utilisée dans le schema de sub_devices.
    Il s'agit juste d'implémenter ISource
    Cette source est censée représenter l'ensemble de tous les devices.
    Elle parcourt toutes les organizations et recherche le device voulu.
    *********
    ATTENTION, dans l'implémentation ci-dessous, si deux orga ont
    des devices avec le même nom, seul le 1er est retourné.
    """
    implements(ISource)
    def __contains__(self, value):
        root = getSite()
        for orga in root['organizations']:
            if 'devices' in root['organizations'][orga] and value.__name__ in root['organizations'][orga]['devices'].keys():
                return True
        return False

class DeviceVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return DeviceSource()

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
    




# -*- coding: utf-8 -*-
from persistent import Persistent
from zope.app.folder.folder import Folder
from zope.interface import implements
from zope.component import adapts, adapter
from zope.app.container.interfaces import INameChooser, IObjectRemovedEvent
from zope.app.container.contained import NameChooser
from zope.app.component.hooks import getSite
from zope.copypastemove import ObjectMover
from zope.component.factory import Factory
import string
from zope.schema.interfaces import ISource, IVocabularyFactory
from BTrees.OOBTree import OOBTree

from interfaces import *


@adapter(ISoftware, IObjectRemovedEvent)
def SoftwareRemovedEvent(software, event):
    u"a subscriber that put software to trash if it contains support objects, before deleting it"
    if event.newParent is None and len(software.supports) != 0 :
        trash = getSite()['trash']
        software_name = INameChooser(trash).chooseName(u"",software)
        trash[software_name]=software

class SoftwareContainer(Folder):
    "a container for all software"
    implements(ISoftwareContainer)
    __name__=__parent__=None
        
class Software(Persistent):
    implements(ISoftware, ISubSoftware)
    builtVersion = u""
    description = u""
    subsoftware = []
    names = architectures = []
    version = codename = u""
    link = u""
    url=""
    __name__=__parent__=None
    def __init__(self, names=None, description=None):
        u"a list of support devices, that lead to the Support objects"
        self.names = names
        self.description = description
        self.supports = OOBTree()
        super(Software, self).__init__()
    def __getattr__(self, name):
        if name == 'organization':
            if self.__parent__ is not None:
                return self.__parent__.__parent__
            return None
        return super(Software, self).__getattr__(name)
    def __setattr__(self, name, value):
        if name == 'organization':
            if value is not self.__parent__ and value is not None and self.__parent__ is not None:
                mover = ObjectMover(self)
                if not mover.moveableTo(value['software']):
                    raise "Impossible action"
                else:
                    mover.moveTo(value['software'])
        else:
            super(Software, self).__setattr__(name, value)

        
softwareFactory = Factory(
    Software,
    title=u"Software factory",
    description = u"This factory instantiates new Software."
    )
    
class SoftwareNameChooser(NameChooser):
    u"""
    adapter that allows to choose the name of the Software from the container point of view
    The real name is stored in an attribute, but this name is important
    as it appears in the URL and is used for traversing
    """
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
    def checkName(self, name, software):
        if name in software.__parent__ and software is not software.__parent__['name']:
            return False
        else :
            return true

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

class SoftwareSource(object):
    """
    implémentation de la Source de Software utilisée dans le schema de Support
    Il s'agit juste d'implémenter ISource
    Cette source est censée représenter l'ensemble de tous les softwares.
    Elle parcourt toutes les organizations et recherche le software voulu.
    *********
    ATTENTION, dans l'implémentation ci-dessous, si deux orga ont
    des softwares avec le même nom, seul le 1er est retourné.
    """
    implements(ISource)
    def __contains__(self, value):
        root = getSite()
        for orga in root['organizations']:
            if 'software' in root['organizations'][orga] and value.__name__ in root['organizations'][orga]['software'].keys():
                return True
        return False

class SoftwareVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return SoftwareSource()

class FuzzySoftware(Software):
    u"""
    a software representing several softwares
    For ex : ubuntu representing all variants (kubuntu, ubuntu server, etc.)
    It contains the union of all support objects an can have its own supports.
    """
    implements(IFuzzy)
    group = []
    





