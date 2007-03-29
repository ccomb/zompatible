# -*- coding: utf-8 -*-
from zope.interface import implements
from persistent import Persistent
from zope.app.folder.folder import Folder
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from persistent.list import PersistentList
from zope.schema.interfaces import ISource, IVocabularyFactory
from zope.app.component.hooks import getSite
from zope.app.container.interfaces import INameChooser
from zope.app.container.contained import NameChooser
import string
from BTrees.OOBTree import OOBTree

from interfaces import *

class DeviceContainer(Folder):
    """
    a folder that contains devices
    """
    __name__=__parent__=None
    implements(IDeviceContainer)


class Device(Persistent):
    implements(IDevice, ISubDevices)
    names=PersistentList()
    subdevices=[]
    pciid=""
    # IDevice fournit IContained donc il faut mettre ces attributs :
    __name__=__parent__=None
    def __init__(self):
        u"the list of supported software that lead to the Support objects"
        self.supports = OOBTree()
    
class DeviceNameChooser(NameChooser):
    u"""
    adapter qui permet de choisir le nom du device auprès du container
    Le vrai nom est stocké dans un attribut, mais ce nom est aussi important
    car il apparaît dans l'URL, et sert pour le traversing.
    """
    implements(INameChooser)
    adapts(IDevice)
    def chooseName(self, name, device):
        return string.lower(device.names[0]).replace(' ','-')
    def checkName(self, name, device):
        if name in device.__parent__ and device is not device.__parent__['name']:
            return False
        else :
            return true


# Autre méthode pour créer un objectwidget ? (pas encore testé)
#class DeviceWidget(ObjectWidget):
#    __used_for__ = IDevice
#    subdevices_widget = CustomWidgetFactory(ObjectWidget, Device)


# tests sur la recherche avec le catalog
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
            for subword in [ word[i:] for i in range(len(word)) ]:
                texttoindex += subword + " "
        return texttoindex


class SearchDevice(object):
    u"""
    une classe qui effectue la recherche de device
    il faudrait peut-être déporter ceci dans un module externe
    qui fournirait une interface ISearchable,
    ainsi que les fonctions de recherche.
    (voir s'il existe déjà une interface de ce type ?)
    Il faudra sûrement faire ça pour le champ de recherche principal,
    où on peut faire une recherche par device, organization, feature, etc, tout en meme temps.
    
    Un ResultSet est un objet qui implémente __iter__ mais pas __getitem__
    Donc on peut le parcourir, mais pas accéder à un élément en particulier.
    Et on ne peut pas le parcourir 2x ! Mieux vaut utiliser catalog.apply()
    """
    def update(self, query, organization=None):
        catalog=getUtility(ICatalog)
        del self.results
        self.results=[]
        if query!="":
            self.results=catalog.searchResults(device_names=query+"*")
        if organization is not None:
            # list comprehension : it creates a full list of device
            #self.results = [ device for device in self.results if (device.__parent__.__parent__ == organization) ]
            # generator expression : it creates an iterator that parse the list on demand (should save memory)
            self.results = ( device for device in self.results if (device.__parent__.__parent__ == organization) )
    def __init__(self, query, organization=None):
        self.results=[]
        self.update(query, organization)
    def getResults(self):
        return self.results


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
        found=0
        root = getSite()
        for manuf in root['organizations']:
            if 'devices' in root['organizations'][manuf] and value.__name__ in root['organizations'][manuf]['devices'].keys():
                found=1
                return True
        return False


class DeviceVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return DeviceSource()


