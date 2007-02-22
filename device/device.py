# -*- coding: utf-8 -*-
from persistent import Persistent
from zope.interface import implements  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder
from interfaces import *
from zope.index.text.interfaces import ISearchableText
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.form.browser.editview import EditView
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget, ListSequenceWidget
from zope.schema.fieldproperty import FieldProperty
from persistent.list import PersistentList
from zope.schema.interfaces import ISource, IVocabularyFactory
from zope.traversing.api import getRoot

 
class DeviceContainer(Folder):
    """
    a folder that contains devices
    """
    implements(IDeviceContainer)


class Device(Persistent):
    implements(IDevice, ISubDevices)
    names=PersistentList()
    subdevices=[]
    # IDevice fournit IContained donc il faut mettre ces attributs :
    __name__=__parent__=None




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
    implements(ISearchableText)
    adapts(IDevice)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        u"peut surement être optimisé avec une seule ligne de return..."
        text = u""
        for t in self.context.names:
            text += " " + t
        return text
    

class SearchDevice(object):
    u"""
    une classe qui effectue la recherche de device
    il faudrait peut-être déporter ceci dans un module externe
    qui fournirait une interface ISearchable,
    ainsi que les fonctions de recherche.
    (voir s'il existe déjà une interface de ce type ?)
    """
    def update(self, query):
        catalog=getUtility(ICatalog)
        del self.results
        self.results=[]
        if query!="":
            self.results=catalog.searchResults(device_names=query)
    def __init__(self, query):
        self.results=[]
        self.update(query)
    def getResults(self):
        return self.results


class DeviceSource(object):
    """
    implémentation de la Source de Devices utilisée dans le schema de sub_devices.
    Il s'agit juste d'implémenter ISource
    Cette source est censée représenter l'ensemble de tous les devices.
    Elle parcourt tous les manufacturers et recherche le device voulu.
    """
    implements(ISource)
    def __contains__(self, value):
        found=0
        root = getRoot(value)
        for manuf in root['manufacturers']:
            if value.__name__ in root['manufacturers'][manuf]['devices'].keys():
                found=1
                return True
        return False


class DeviceVocabularyFactory(object):
    implements(IVocabularyFactory)
    def __call__(self, context):
        return DeviceSource()


