# -*- coding: utf-8 -*-
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.viewlet.manager import ViewletManagerBase
from zope.app.component.hooks import getSite
from zope.component import createObject
from zope.interface import implements

from interfaces import *

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

class MainLinksViewlet(object):
    u"""
    The viewlet that displays the links under the main search field
    For now we display the folders of the root, and forbid a few ones
    """
    def getitems(self):
        forbidden = [ 'supports', 'trash' ]
        return [ { 'name':i, 'url':i} for i in getSite().keys() if i not in forbidden ]

