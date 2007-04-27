# -*- coding: utf-8 -*-
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import SiteAbsoluteURL, AbsoluteURL
from zope.viewlet.interfaces import IViewlet
from zope.viewlet.manager import ViewletManagerBase
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import implements, Interface
from zope.component import adapts
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.app.component.hooks import getSite
from zope.component import createObject

from interfaces import *
from organization.interfaces import IOrganization

class MainPage(object):
    u"""
    La vue correspondant à la page d'accueil du projet.
    Cette page n'est pas la vue d'un objet, mais juste une page.
    Elle devra inclure probablement des viewlets.
    Elle est déclarée (ah voilà la meilleure traduction pour register) comme vue par défaut
    pour les objets fournissant IFolder, en écrasant celle de Rotterdam grâce à l'overrides.zcml
    """
    main_page = True # Just to detect the main page in the main_template
    __call__ = ViewPageTemplateFile("index.pt")
    def __init__(self, context, request):
        self.context=context
        self.request=request


class PageTitleContentProvider(object):
    u"""
    Un Content Provider qui permet d'afficher le titre de la page (dans le header html)
    C'est important car ça aide le référencement
    """
    global sitename
    implements(IContentProvider)
    adapts(Interface, IDefaultBrowserLayer, Interface)
    def __init__(self, context, request, view):
        self.context=context
    def update(self):
        u"on récupère le nom du contexte s'il en a un"
        if hasattr(self.context,'__name__') and self.context.__name__ is not None:
            self._pagetitle = self.context.__name__ + " - " + sitename
        else:
            self._pagetitle = sitename
    def render(self):
        return self._pagetitle

class SiteUrlProvider(object):
    u"""
    Un Content Provider qui permet d'afficher l'url de la racine du site.
    Ca c'est juste pour créer le lien home dans le template général. Tant qu'on a pas mis en place
    le virtual hosting, il faut pouvoir diriger à la racine du site, mais pas à la racine de la zodb.
    
    inutilisé pour l'instant
    """
    implements(IContentProvider)
    adapts(Interface, IDefaultBrowserLayer, Interface)
    def __init__(self, context, request, view):
        self.request=request
        self.context=context
    def update(self):
        self._site=SiteAbsoluteURL(self.context, self.request).breadcrumbs()
    def render(self):
        return str(self._site)

class MainAreaManager(ViewletManagerBase):
    u"""
    Ceci est l'implémentation du viewlet manager de la mainArea.
    Le viewletmanager est normalement automatiquement créé par la déclaration zcml correspondante,
    mais en ajoutant la directive class dans le zcml, on peut choisir d'implémenter le viewlet manager
    pour de vrai. Ca permet par exemple de gérer et classer les viewlets comme o veut.
    Cette implémentation est basée sur un viewlet manager de base.
    Dans l'implémentation, la fonction filter sert à n'afficer qu'un partie des viewlets
    et la fonction sort les trie.
    """
    implements(IMainAreaManager)
    ordre = [ 'mainSearch', 'mainLinks' ]
    def sort(self, viewlets):
        viewlets = dict(viewlets)
        return [(name, viewlets[name]) for name in self.ordre if name in viewlets]

class MainSearchViewlet(object):
    u"""
    le viewlet qui permet d'afficher le champ de recherche principal
    Le template utilisé est défini dans le configure.zcml
    """

class MainSearch(object):
    u"""
    La vue qui gère la recherche depuis le champ de recherche principal
    """
    def __init__(self, context, request):
        self.context=context
        self.request=request
    def __call__(self):
        self.mainsearch = self.request['mainsearch']
        if self.mainsearch == "":
            return ViewPageTemplateFile("index.pt")(self)
        u"on décompose la chaine de recherche en mots"
        devices={}
        organizations={}
        software={}
        categorizable={}
        result=u""
        for word in self.mainsearch.split():
            organizations[word]=createObject(u"zompatible.SearchObject", organization_text=word).getResults()
            software[word]=createObject(u"zompatible.SearchObject", software_text=word).getResults()
            devices[word]=createObject(u"zompatible.SearchObject", device_text=word).getResults()
            categorizable[word]=createObject(u"zompatible.SearchObject", categorizable_text=word).getResults()
        for word in self.mainsearch.split():
            result += "pour le mot : " + word + "\n***********\n"
            result += "organizations: "
            for organization in organizations[word]:
                result += organization.__name__ + " "
            result += "\n"
            result += "Software: "
            for software in software[word]:
                result += software.__name__ + " "
            result += "\n"
            result += "devices: "
            for device in devices[word]:
                result += device.__name__ + " "
            result += "\n"
            result += "categorizable: "
            for categorizable in categorizable[word]:
                result += categorizable.__name__ + " "
            result += "\n"
            result += "\n"
        return result

class AdminAreaManager(ViewletManagerBase):
    u"The viewlet manager for the adminarea"
    ordre = ['adminheader', 'login', 'adminmenu' ]
    implements(IAdminAreaManager)
    def sort(self, viewlets):
        viewlets = dict(viewlets)
        return [(name, viewlets[name]) for name in self.ordre if name in viewlets]

class AdminHeaderViewlet(object):
    u"""
    The viewlet that displays the title of the admin area
    No template here, we do a real implementation od IViewlet just to test.
    """
    implements(IViewlet)
    def update(self):
        pass
    def render(self):
        u"""
        Here we could use a template by calling ViewPageTemplateFile
        We actually just return bare HTML (in utf-8)
        """
        return u'<div id="admin_header">Zone admin</div>'

class MainLinksViewlet(object):
    u"""
    The viewlet that displays the links under the main search field
    For now we display the folders of the root, and forbid a few ones
    """
    def getitems(self):
        forbidden = [ 'supports', 'trash' ]
        return [ { 'name':i, 'url':i} for i in getSite().keys() if i not in forbidden ]

class FailsafeAbsoluteURL(AbsoluteURL):
    u"""
    This implementation of absolute_url view was made
    to prevent an error when accessing a Support whose device was deleted.
    """
    def __call__(self):
        try:
            return super(FailsafeAbsoluteURL,self).__call__()
        except:
            return "javascript: alert('This object cannot be located')"

class ToolboxManager(ViewletManagerBase):
    u"""
    a viewlet manager for a side toolbox.
    """
    implements(IToolboxManager)

class ProductSearchViewlet(object):
    u"""
    the viewlet that displays the searchbox for a product.
    its behaviour depends on when we are (see organization.browser.SearchProductView)
    It is defined by a template (see configure.zcml)
    """
    def only_organization(self):
        if (IOrganization.providedBy(self.context) or IOrganization.providedBy(self.context.__parent__)): 
            return True
        return False
    def organization_name(self):
        if IOrganization.providedBy(self.context):
            return self.context.names[0]
        if IOrganization.providedBy(self.context.__parent__):
            return self.context.__parent__.names[0] 
