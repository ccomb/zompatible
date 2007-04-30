# -*- coding: utf-8 -*-
from interfaces import *
from zope.app.folder.folder import Folder
from zope.interface import implements, Interface
from zope.app.component.site import LocalSiteManager, SiteManagerContainer
from zope.component import adapter
from zope.app.container.interfaces import IObjectAddedEvent
from zope.event import notify
from zope.app.intid.interfaces import IIntIds
from zope.app.intid import IntIds
from zope.app.catalog.catalog import Catalog, ICatalog
from zope.app.catalog.text import TextIndex
from zope.component import createObject
from zope.app.generations.utility import findObjectsProviding

from organization.interfaces import ISearchableTextOfOrganization
from device.interfaces import ISearchableTextOfDevice, IDevice
from software.interfaces import ISearchableTextOfSoftware, ISoftware
from level.level import EasinessLevels, StabilityLevels
from level.interfaces import ILevels
from category.interfaces import ISearchableTextOfCategorizable
from search.search import ObjectIndex
from importdata.interfaces import IImportData
from importdata.importcategories import ImportCategoryFile

class ZompatibleSiteManagerSetEvent(object):
    implements(IZompatibleSiteManagerSetEvent)
    def __init__(self, site):
        self.object=site

class ZompatibleSite(Folder, SiteManagerContainer):
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
def ZompatibleInitialSetup(event):
    u"do the necessary!"
    site=event.object
    sm = site.getSiteManager()
    
    u"create and register the intid utility"
    intid = IntIds()
    sm['unique integer IDs']=intid
    sm.registerUtility(intid, IIntIds)

    u"create and register the importdata utility"
    importdata = createObject("zompatible.importData")
    sm['importdata']=importdata
    sm.registerUtility(importdata, IImportData)
    
    u"then create the organizations folder"
    event.object['organizations'] = createObject(u"zompatible.OrganizationContainer")

    u" and the support folder"
    event.object['supports'] = createObject(u"zompatible.SupportContainer")
    
    u" and the Trash for objects deleted but still referenced in a support object"
    event.object['trash'] = Trash()
     
    u"then create and register the catalog"
    catalog = Catalog()
    sm['catalog']=catalog
    sm.registerUtility(catalog, ICatalog)

    u"Register the level utilities"
    sm['easiness_levels'] = EasinessLevels()
    sm.registerUtility(sm['easiness_levels'], ILevels, 'easiness_levels')
    sm['stability_levels'] = StabilityLevels()
    sm.registerUtility(sm['stability_levels'], ILevels, 'stability_levels')
     
    u"then create and register the wanted indices in the catalog"
    catalog['device_text'] = TextIndex(interface=ISearchableTextOfDevice, field_name='getSearchableText', field_callable=True)
    catalog['organization_text'] = TextIndex(interface=ISearchableTextOfOrganization, field_name='getSearchableText', field_callable=True)
    catalog['software_text'] = TextIndex(interface=ISearchableTextOfSoftware, field_name='getSearchableText', field_callable=True)
    #catalog['all_searchable_text'] = TextIndex(interface=ISearchableText, field_name='getSearchableText', field_callable=True)
    catalog['categorizable_text'] = TextIndex(interface=ISearchableTextOfCategorizable, field_name='getSearchableText', field_callable=True)
    catalog['device_organization'] = ObjectIndex(interface=IDevice, field_name='organization', field_callable=False)
    catalog['software_organization'] = ObjectIndex(interface=ISoftware, field_name='organization', field_callable=False)

    sm['temp'] = createObject("zompatible.Device")
    ImportCategoryFile("../lib/python/zompatible/importdata/initial_device_categories.txt").importdata(sm['temp'])
    del sm['temp']
    
    sm['temp'] = createObject("zompatible.Software")
    ImportCategoryFile("../lib/python/zompatible/importdata/initial_software_categories.txt").importdata(sm['temp'])
    del sm['temp']
    
    u"create an intid for all objects added in content space and site manager. (the intid is not yet active)"
    u"KEEP THIS AT THE BOTTOM"
    for object in findObjectsProviding(site,Interface):
        intid.register(object)
    for object in findObjectsProviding(sm,Interface):
        intid.register(object)

class Trash(Folder):
    u"""the implementation of the site trash as a folder"""
    implements(ITrash)
