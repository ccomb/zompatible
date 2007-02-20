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

class DeviceContainer(Folder):
    """
    a folder that contains devices
    """
    implements(IDeviceContainer)


class Device(Persistent):
    implements(IDevice, ISubDevices)
    names=PersistentList()
    #name=u""
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
    


