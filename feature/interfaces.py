# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContained, IContainer
from zope.app.container.constraints import contains, containers
from zope.schema import List, TextLine
from zope.interface import Interface


class IFeatured(Interface):
    """
    a device that has features
    """
    #features = List(title=u'features', description=u'list of features of the device, in addition of those from the chip', value_type=Object(title=u'feature', description=u'a feature of the device', schema=IFeature))


class IFeature(Interface):
    """
    a feature or protocol offered by the device or driver (ex: wpa, pptp, opengl, etc.)
    we must find a way to differenciate USB 1.1 from USB 2.0, 802.11b from 802.11g, etc.
    Trouver un moyen de stocker le PCIID d'un device PCI.
    """
    containers('zompatible.feature.interfaces.IFeatureContainer')
    names = List(title=u'names', description=u'possible names of the feature', value_type=TextLine(title=u'feature', description=u'a name for the feature (ex: wifi, wi-fi, 802.11'))
    version = TextLine(title=u'feature version', description=u'the version of the feature (ex: 2)')


class IFeatureContainer(IContainer):
    """
    a feature container
    """
    contains(IFeature)