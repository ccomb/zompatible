# -*- coding: utf-8 -*-
from interfaces import *
from persistent import Persistent  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder
from zope.interface import implements
from zope.app.component.site import LocalSiteManager, SiteManagerContainer
from zope.app.container.btree import BTreeContainer
from zope.component import adapter
from zope.app.container.interfaces import IObjectAddedEvent
from zope.event import notify
from zope.app.intid.interfaces import IIntIds
from zope.app.intid import IntIds
from zope.app.catalog.catalog import Catalog, ICatalog
from zope.app.catalog.text import TextIndex, ITextIndex
from zope.index.text.interfaces import ISearchableText

from manufacturer.manufacturer import ManufacturerContainer
from manufacturer.interfaces import ISearchableTextOfManufacturer
from device.interfaces import ISearchableTextOfDevice

class ZompatibleSiteManagerSetEvent(object):
    implements(IZompatibleSiteManagerSetEvent)
    def __init__(self, site):
        self.object=site


class ZompatibleSite(SiteManagerContainer, BTreeContainer):
    u"""
    Le principe est qu'on ajoute un site zompatible,
    puis on déclenche un subscriber au moment de l'ajout qui va le transformer en site.
    A ce moment un evenement est déclenché et appelle un autre subscriber qui va
    créer le nécessaire pour faire fonctionner le site
    """
    implements(IZompatibleSite)
    def setSiteManager(self, sm):
        u"on surcharge cette méthode pour pouvoir lancer l'evenement"
        super(ZompatibleSite, self).setSiteManager(sm)
        notify(ZompatibleSiteManagerSetEvent(self))
    

@adapter(IZompatibleSite, IObjectAddedEvent)
def newZompatibleSiteAdded(site, event):
    u"a subscriber that do the necessary after the site is added"
    site.setSiteManager(LocalSiteManager(site))
    
@adapter(IZompatibleSiteManagerSetEvent)
def ZompatibleSetup(event):
    u"do the necessary!"
    site=event.object
    sm = site.getSiteManager()
    u"first create the manufacturers folder"
    manufacturers=ManufacturerContainer()
    event.object['manufacturers']=manufacturers
    u"then create and register the intid utility"
    intid = IntIds()
    sm['intid']=intid
    sm.registerUtility(intid, IIntIds)
    u"then create and register the catalog"
    catalog = Catalog()
    sm['catalog']=catalog
    sm.registerUtility(catalog, ICatalog)
    u"then create and register the wanted indices in the catalog"
    catalog['device_names'] = TextIndex(interface=ISearchableTextOfDevice, field_name='getSearchableText', field_callable=True)
    catalog['manufacturer_names'] = TextIndex(interface=ISearchableTextOfManufacturer, field_name='getSearchableText', field_callable=True)
    catalog['all_searchable_text'] = TextIndex(interface=ISearchableText, field_name='getSearchableText', field_callable=True)
    
    