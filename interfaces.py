# -*- coding: utf-8 -*-
from zope.interface.interfaces import Interface
from zope.schema import TextLine, Object, List, Text, Int
from zope.viewlet.interfaces import IViewletManager

sitename="Zompatible"

class IMainArea(IViewletManager):
    u"""
    Ceci est le viewlet manager correspondant à la zone centrale de la page d'accueil.
    Il devra au moins contenir le viewlet de recherche principal.
    """

class IAdminArea(IViewletManager):
    u"""
    Le viewlet manager qui gère les viewlets d'administration
    """




# définir une interface IVersionned pour dire qu'un truc est versionné ?

# reste des définitions initiales non déplacées dans des packages séparés.
# voir au début du memo.txt  IOsSupport et IAction
