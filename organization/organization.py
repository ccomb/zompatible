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
from zope.component import adapts, adapter
from zope.app.folder.interfaces import IFolder
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.keyreference.persistent import connectionOfPersistent

from zompatible.device.device import DeviceContainer
from zompatible.device.interfaces import IDeviceContainer

from ZODB.interfaces import IConnection

class OrganizationContainer(Folder):
  "a organization container"
  implements(IOrganizationContainer)
  __name__=__parent__=None


@adapter(IOrganization, IObjectAddedEvent)
def createOrganizationSubfolders(organization, event):
    devices=DeviceContainer()
    organization['devices']=devices


class Organization(Folder):
  implements(IOrganization,IFolder)
  names=[]
  url=""
  __name__=__parent__=None
  def get_devices(self):
      return self['devices'].items()
  

class SearchableTextOfOrganization(object):
    u"""
    l'adapter qui permet d'indexer les organizations
    """
    implements(ISearchableTextOfOrganization)
    adapts(IOrganization)
    def __init__(self, context):
        self.context = context
    def getSearchableText(self):
        u"peut surement être optimisé avec une seule ligne de return..."
        text = u""
        for t in self.context.names:
            text += " " + t
        return text
    

class SearchOrganization(object):
    u"""
    une classe qui effectue la recherche de organization
    """
    def update(self, query):
        catalog=getUtility(ICatalog)
        del self.results
        self.results=[]
        if query!="":
            self.results=catalog.searchResults(organization_names=query)
    def __init__(self, query):
        self.results=[]
        self.update(query)
    def getResults(self):
        return self.results
        
        
        