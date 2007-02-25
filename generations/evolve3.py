# -*- coding: utf-8 -*-
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding
from zompatible.manufacturer.interfaces import IManufacturerContainer



def evolve(context):
    for manufacturercontainer in findObjectsProviding(getRootFolder(context),IManufacturerContainer):
            manufacturer.__name__='manufacturers'
            manufacturer.__parent__= getRootFolder(context)
