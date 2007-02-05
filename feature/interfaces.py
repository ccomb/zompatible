# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContained, IContainer
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine, Object
from zope.interface import Interface, Attribute


class IFeatureContainer(IContainer):
    u"""
    le dossier qui stocke les objets features disponibles
    """
    contains("zompatible.feature.interfaces.IFeature")


class IFeature(Interface):
    u"""
    a feature or protocol offered by the device or driver (ex: wpa, pptp, opengl, etc.)
    we must find a way to differenciate USB 1.1 from USB 2.0, 802.11b from 802.11g, etc.
    Trouver un moyen de stocker le PCIID d'un device PCI.
    """
    names = List(title=u'names', description=u'possible names of the feature', value_type=TextLine(title=u'feature', description=u'a name for the feature (ex: wifi, wi-fi, 802.11'))
    version = TextLine(title=u'feature version', description=u'the version of the feature (ex: 2)')
    value = Attribute()


class IValueFeature(IFeature):
    u"""
    le schema qui permet de stocker une seule feature qui prend la forme d'une valeur
    """
    value = TextLine(title=u'value', description=u'value of the feature')

class IObjectFeature(IFeature):
    u"""
    le schema qui permet de stocker une feature qui prend la forme d'un objet
    """
    value = Choice(title=u'value', description=u'value of the feature', vocabulary="features")
    
    
class IFeatured(Interface):
    u"""
    a device that has features. (marker interface)
    """


class IFeatures(Interface):
    u"""
    l'interface qui permet de connaître les features d'un objet
    """
    features = Attribute()
    

