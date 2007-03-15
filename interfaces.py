# -*- coding: utf-8 -*-
from zope.viewlet.interfaces import IViewletManager
from zope.app.container.interfaces import IContainer
from zope.app.component.interfaces import IPossibleSite
from zope.component.interfaces import IObjectEvent

sitename="Zompatible"


class IZompatibleSite(IPossibleSite, IContainer):
    u"""
    l'interface (vide) du conteneur principal du site
    """
    
class IZompatibleSiteManagerSetEvent(IObjectEvent):
    u"""
    l'événement qui devra être généré lorsque qu'on ajoute un site zompatible.
    Le subscriber devra créer les outils nécessaires au fonctionnement du site,
    en particulier le IntId, le catalog et ses index.
    """ 




class IMainAreaManager(IViewletManager):
    u"""
    Ceci est le viewlet manager correspondant à la zone centrale de la page d'accueil.
    Il devra au moins contenir le viewlet de recherche principal.
    """

class IAdminAreaManager(IViewletManager):
    u"""
    Le viewlet manager qui gère les viewlets d'administration
    """




# définir une interface IVersionned pour dire qu'un truc est versionné ?

# reste des définitions initiales non déplacées dans des packages séparés.
# voir au début du memo.txt  IOsSupport et IAction
