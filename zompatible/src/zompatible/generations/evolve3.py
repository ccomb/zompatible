# -*- coding: utf-8 -*-
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding
from zompatible.organization.interfaces import IOrganizationContainer



def evolve(context):
    for organizationcontainer in findObjectsProviding(getRootFolder(context),IOrganizationContainer):
            organization.__name__='organizations'
            organization.__parent__= getRootFolder(context)
