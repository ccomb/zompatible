# -*- coding: utf-8 -*-
from interfaces import *
from persistent import Persistent  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.app.container.browser.contents import Contents
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder
from zompatible.device.device import DeviceContainer


class ManufacturerContainer(Folder):
  "a manufacturer container"
  implements(IManufacturerContainer)
  #def __init__():
  # créer les sous-dossiers

class Manufacturer(Folder):
  implements(IManufacturer,IFolder)
  names=[]
  
  def __init__(self):
      super(Manufacturer,self).__init__()
      "on crée les containers nécessaires"
      devices=DeviceContainer()
      #drivers=Folder()
      self['devices']=devices
      #self['drivers']=drivers


class ManufacturerAdd(AddForm):
  "La vue (classe) de formulaire pour l'ajout"
  form_fields=Fields(IManufacturer).omit('__name__', '__parent__')
  label=u"Ajout d'un fabricant"
  template=ViewPageTemplateFile("manufacturer_form.pt")
  def create(self, data):
    "on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
    manufacturer=Manufacturer()
    "puis on applique les données du formulaire à l'objet"
    applyChanges(manufacturer, self.form_fields, data)
    "puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
    self.context.contentName=manufacturer.names[0]
    return manufacturer

class ManufacturerEdit(EditForm):
  label="Modification d'un fabricant"
  form_fields=Fields(IManufacturer).omit('__name__', '__parent__')
  template=ViewPageTemplateFile("manufacturer_form.pt")

class ManufacturerView(BrowserPage):
    "la vue qui permet d'afficher un manufacturer"
    label="Visualisation d'un fabricant"
    __call__=ViewPageTemplateFile("manufacturer.pt")
    def getmainname(self):
        return self.context.__name__
    def getothernames(self):
        return self.context.names
    def getcontentinfo(self):
        return Contents(self.context, self.request).listContentInfo()
    def testannotations(self):
        IAnnotations(self.context)['zompatible.manufacturer.manufacturer.Manufacturer.category']='toto'
        return IAnnotations(self.context)['zompatible.manufacturer.manufacturer.Manufacturer.category']
        

