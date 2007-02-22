# -*- coding: utf-8 -*-
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserPage
from zope.traversing.api import getRoot
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.viewlet.interfaces import IViewlet
from zope.interface import implements


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
        print list(getRoot(self.context)['manufacturers'].items())
        return getRoot(self.context)['manufacturers'].items()

