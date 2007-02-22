# -*- coding: utf-8 -*-
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserPage
from zope.traversing.api import getRoot
from zope.traversing.browser.interfaces import IAbsoluteURL


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
    def getmanufacturers(self):
        u"Il serait préférable de registrer le dossier des manufacturers comme un named utility"
        print list(getRoot(self.context)['manufacturers'].items())
        return getRoot(self.context)['manufacturers'].items()