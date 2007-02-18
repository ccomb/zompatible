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
    name=u""
    subdevices=PersistentList()
    # IDevice fournit IContained donc il faut mettre ces attributs :
    __name__=__parent__=None


device_widget = CustomWidgetFactory(ObjectWidget, Device)
subdevices_widget = CustomWidgetFactory(ListSequenceWidget, subwidget=device_widget)


# Autre méthode pour créer un objectwidget ? (pas encore testé)
#class DeviceWidget(ObjectWidget):
#    __used_for__ = IDevice
#    subdevices_widget = CustomWidgetFactory(ObjectWidget, Device)


class DeviceAdd(AddForm):
  "La vue (classe) de formulaire pour l'ajout"
  form_fields=Fields(IDevice, ISubDevices)
  form_fields['subdevices'].custom_widget=subdevices_widget
  form_fields=form_fields.omit('__name__', '__parent__')
  label=u"Ajout d'un matériel"
  #####template=ViewPageTemplateFile("device_form.pt")
  def create(self, data):
    "on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
    device=Device()
    "puis on applique les données du formulaire à l'objet"
    applyChanges(device, self.form_fields, data)
    "puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
    self.context.contentName=device.names[0]
    return device


class DeviceEdit(EditForm):
  label=u"Modification d'un matériel"
  form_fields=Fields(IDevice, ISubDevices, render_context=True)
  form_fields['subdevices'].custom_widget=subdevices_widget
  form_fields=form_fields.omit('__name__', '__parent__')
  ## template désactivé
  ######template=ViewPageTemplateFile("device_form.pt")


class DeviceView(BrowserPage):
    "la vue qui permet d'afficher un device"
    label=u"Visualisation d'un matériel"
    __call__=ViewPageTemplateFile("device.pt")
    def getmainname(self):
        return self.context.__name__
    def getothernames(self):
        return self.context.names


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
    

class SearchDevice(BrowserPage):
    u"""
    la méthode lancée depuis le template pour effectuer la recherche
    """
    def update(self, query):
        catalog=getUtility(ICatalog)
        self.results=catalog.searchResults(device_names=query)

    render = ViewPageTemplateFile('search.pt')
    
    def __call__(self, query):
        self.update(query)
        return self.render()
    
    def getResults(self):
        print len(self.results)
        for item in self.results:
            names=""
            for name in item.names:
                names += name + " "
            yield names




