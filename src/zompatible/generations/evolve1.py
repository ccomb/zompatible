# -*- coding: utf-8 -*-
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding
from zompatible.organization.interfaces import IOrganization



def evolve(context):
    u"""
    script d'évolution depuis la version 0 vers la version 1 du schema de db
    Ce script sert juste à tester l'ajout de l'URL au schema organization.
    """
    for organization in findObjectsProviding(getRootFolder(context),IOrganization):
        if not hasattr(organization, 'url'):
            organization.url=None