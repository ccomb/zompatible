# -*- coding: utf-8 -*-
from interfaces import *
from zope.interface import implements
from persistent import Persistent  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.app.container.browser.contents import Contents
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder
from zope.index.text.interfaces import ISearchableText
from zope.component import adapts
from zope.app.folder.interfaces import IFolder
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog

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
  def get_devices(self):
      return self['devices'].items()


        

class SearchableTextOfManufacturer(object):
    u"""
    l'adapter qui permet d'indexer les manufacturers
    """
    implements(ISearchableTextOfManufacturer)
    adapts(IManufacturer)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        u"peut surement être optimisé avec une seule ligne de return..."
        text = u""
        for t in self.context.names:
            text += " " + t
        return text
    

class SearchManufacturer(object):
    u"""
    une classe qui effectue la recherche de manufacturer
    """
    def update(self, query):
        catalog=getUtility(ICatalog)
        del self.results
        self.results=[]
        if query!="":
            self.results=catalog.searchResults(manufacturer_names=query)
    def __init__(self, query):
        self.results=[]
        self.update(query)
    def getResults(self):
        return self.results
        
        
        