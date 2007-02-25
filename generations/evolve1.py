# -*- coding: utf-8 -*-
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding
from zompatible.manufacturer.interfaces import IManufacturer



def evolve(context):
    u"""
    script d'évolution depuis la version 0 vers la version 1 du schema de db
    Ce script sert juste à tester l'ajout de l'URL au schema manufacturer.
    """
    for manufacturer in findObjectsProviding(getRootFolder(context),IManufacturer):
        if not hasattr(manufacturer, 'url'):
            manufacturer.url=None