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
from device import Device


# choix du widget pour l'élément de la liste des subdevices
device_widget = CustomWidgetFactory(ObjectWidget, Device)
# choix du widget pour les subdevices
subdevices_widget = CustomWidgetFactory(ListSequenceWidget, subwidget=device_widget)



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


