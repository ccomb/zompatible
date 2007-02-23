# -*- coding: utf-8 -*-
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserPage
from zope.traversing.api import getRoot
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.viewlet.interfaces import IViewlet
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import implements, Interface
from zope.component import adapts
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.app.container.interfaces import IContained

from interfaces import *
from device.device import SearchDevice
from manufacturer.manufacturer import SearchManufacturer

class MainPage(object):
    u"""
    La vue correspondant à la page d'accueil du projet.
    Cette page n'est pas la vue d'un objet, mais juste une page.
    Elle devra inclure probablement des viewlets.
    Elle est déclarée (ah voilà la meilleure traduction pour register) comme vue par défaut
    pour les objets fournissant IFolder, en écrasant celle de Rotterdam grâce à l'overrides.zcml
    """
    __call__ = ViewPageTemplateFile("index.pt")
    def __init__(self, context, request):
        self.context=context
        self.request=request

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
        manufacturers={}
        result=u""
        for word in self.mainsearch.split():
            devices[word]=SearchDevice(word+"*").getResults()
            manufacturers[word]=SearchManufacturer(word+"*").getResults()
        for word in self.mainsearch.split():
            result += "pour le mot : " + word + "\n***********\n"
            result += "devices: "
            for device in devices[word]:
                result += device.__name__ + " "
            result += "\n"
            result += "manufacturers: "
            for manufacturer in manufacturers[word]:
                result += manufacturer.__name__ + " "
            result += "\n\n"
        return result


class AdminHeaderViewlet(object):
    u"""
    le viewlet qui affiche le titre de la zone d'admin
    Pas de template pour celui-ci, on fait une vraie implémentation d'IViewlet pour tester.
    """
    implements(IViewlet)
    def update(self):
        pass
    def render(self):
        u"""
        ici on pourrait utiliser un template grâce à ViewPageTemplateFile
        On se contente de renvoyer du bête HTML (en utf-8)
        """
        return u'<div id="admin_header">Zone admin</div>'
    


    
class ManufacturerListViewlet(object):
    u"""
    un viewlet (temporaire ?) qui permet d'afficher la liste des fabricants
    """
    def getmanufacturers(self):
        u"Il serait préférable de registrer le dossier des manufacturers comme un named utility"
        return getRoot(self.context)['manufacturers'].items()


class PageTitleViewlet(object):
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
        if hasattr(self.context,'__name__') and self.context.__name__ is not None:
            self._pagetitle = self.context.__name__ + " - " + sitename
        else:
            self._pagetitle = sitename
    def render(self):
        return self._pagetitle
    
    
    