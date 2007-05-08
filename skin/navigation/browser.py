# -*- coding: utf-8 -*-
from zope.traversing.browser.absoluteurl import SiteAbsoluteURL, AbsoluteURL
from zope.viewlet.manager import ViewletManagerBase
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import implements, Interface
from zope.component import adapts
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.app.component.hooks import getSite
from zope.component import createObject
from zope.publisher.browser import BrowserView

from interfaces import *
from zompatible.organization.interfaces import IOrganization

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

class PageTitleContentProvider(object):
    u"""
    Un Content Provider qui permet d'afficher le titre de la page (dans le header html)
    C'est important car ça aide le référencement
    """
    implements(IContentProvider)
    adapts(Interface, IDefaultBrowserLayer, Interface)
    def __init__(self, context, request, view):
        self.context=context
        self._sitename = getSite().__name__

    def update(self):
        u"on récupère le nom du contexte s'il en a un"
        if hasattr(self.context,'__name__') and self.context.__name__ is not None:
            self._pagetitle = self.context.__name__ + " - " + self._sitename
        else:
            self._pagetitle = self._sitename
    def render(self):
        return self._pagetitle


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

class PrettyName(BrowserView):
    u"""
    the universal adapter that computes a pretty name for http links of any object
    Specialized adapters must be provided for objects that want a particular pretty name
    """
    implements(IBrowserView)
    def __call__(self):
        if hasattr(self.context, 'name') and len(self.context.names)>0:
            return self.context.name
        if hasattr(self.context, 'names') and len(self.context.names)>0:
            return self.context.names[0]
        if hasattr(self.context, '__name__') and len(self.context.__name__)>0:
            return self.context.__name__
            
            
            