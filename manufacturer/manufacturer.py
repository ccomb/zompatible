# -*- coding: utf-8 -*-
from interfaces import *
from zope.interface import implements
from persistent import Persistent  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.app.container.browser.contents import Contents
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder
from zompatible.device.device import DeviceContainer
from zope.index.text.interfaces import ISearchableText
from zope.component import adapts
from zope.app.folder.interfaces import IFolder

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
      #devices=DeviceContainer()  # dérange le IntId utility. Il faut faire plutôt avec des Events
      #drivers=Folder()
      #self['devices']=devices
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
    label="View of a manufacturer"
    __call__=ViewPageTemplateFile("manufacturer.pt")
    def getdevicescontentinfo(self):
        return Contents(self.context['devices'], self.request).listContentInfo()
    def testannotations(self):
        IAnnotations(self.context)['zompatible.manufacturer.manufacturer.Manufacturer.category']='toto'
        return IAnnotations(self.context)['zompatible.manufacturer.manufacturer.Manufacturer.category']
        

class SearchableTextOfManufacturer(object):
    u"""
    l'adapter qui permet d'indexer les devices. Il fournit le texte à indexer depuis le contenu d'un objet device.
    C'est génial car ça permet notamment d'indexer n'importe quels attributs,
    et même les traductions qui se trouvent dans des fichiers .po externes !!
    """
    implements(ISearchableText)
    adapts(IManufacturer)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        u"peut surement être optimisé avec une seule ligne de return..."
        text = u""
        for t in self.context.names:
            text += " " + t
        return text
    
