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
from product.interfaces import ISearchableTextOfProduct
from level.level import EasinessLevels, StabilityLevels
from level.interfaces import ILevels
from category.interfaces import ISearchableTextOfCategorizable
from search.search import ObjectIndex
from importdata.interfaces import IImportData
from importdata.importcategories import ImportCategoryFile
from importdata.importsoftware import ImportSoftwareFile

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
    u"create the initial objects required by the site"
    # do the necessary!
    site=event.object
    sm = site.getSiteManager()
    
    # create and register the intid utility
    intid = IntIds()
    sm['unique integer IDs']=intid
    sm.registerUtility(intid, IIntIds)

    # create and register the importdata utility
    importdata = createObject("zompatible.importData")
    sm['importdata']=importdata
    sm.registerUtility(importdata, IImportData)
    
    # then create the organizations folder
    event.object['organizations'] = createObject(u"zompatible.OrganizationContainer")

    # and the support folder
    event.object['supports'] = createObject(u"zompatible.SupportContainer")
    
    # and the Trash for objects deleted but still referenced in a support object
    event.object['trash'] = Trash()
     
    # then create and register the catalog
    catalog = Catalog()
    sm['catalog']=catalog
    sm.registerUtility(catalog, ICatalog)

    # Register the level utilities
    sm['easiness_levels'] = EasinessLevels()
    sm.registerUtility(sm['easiness_levels'], ILevels, 'easiness_levels')
    sm['stability_levels'] = StabilityLevels()
    sm.registerUtility(sm['stability_levels'], ILevels, 'stability_levels')
     
    # then create and register the wanted indices in the catalog
    catalog['device_text'] = TextIndex(interface=ISearchableTextOfDevice, field_name='getSearchableText', field_callable=True)
    catalog['organization_text'] = TextIndex(interface=ISearchableTextOfOrganization, field_name='getSearchableText', field_callable=True)
    catalog['software_text'] = TextIndex(interface=ISearchableTextOfSoftware, field_name='getSearchableText', field_callable=True)
    # catalog['all_searchable_text'] = TextIndex(interface=ISearchableText, field_name='getSearchableText', field_callable=True)
    catalog['categorizable_text'] = TextIndex(interface=ISearchableTextOfCategorizable, field_name='getSearchableText', field_callable=True)
    catalog['product_organization'] = ObjectIndex(interface=IProduct, field_name='organization', field_callable=False)

    # importcategories needs a context to be able to find its AvailableCategoriesContainer
    sm['temp'] = createObject("zompatible.Product")
    ImportCategoryFile("../lib/python/zompatible/importdata/initial_product_categories.txt").do_import(sm['temp'])
    del sm['temp']
    
    # import initial software list
    ImportSoftwareFile("../lib/python/zompatible/importdata/initial_software.txt").do_import(context=site)
    
    #create an intid for all objects added in content space and site manager. (the intid is not yet active)"
    #KEEP THIS AT THE BOTTOM"
    for object in findObjectsProviding(site,Interface):
        intid.register(object)
    for object in findObjectsProviding(sm,Interface):
        intid.register(object)
    # reindex eveything
    catalog.updateIndexes()

class Trash(Folder):
    u"""the implementation of the site trash as a folder"""
    implements(ITrash)
