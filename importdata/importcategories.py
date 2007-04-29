# -*- coding: utf-8 -*-

from importdata import ImportFile
from zope.component import createObject
from zompatible.category.interfaces import IAvailableCategories

from interfaces import *

class ImportCategoryFile(ImportFile):
    u"""
    An import utility for default categories
    See initial_device_categories.txt
    """
    def importdata(self, context):
        if self.infile == u"":
            raise "No file provided"
        categorycontainer = IAvailableCategories(context)
        parentcategory = previouscategory = categorycontainer
        for line in open(self.infile):
                if line.strip() == '':
                    continue
                newlevel = line.find(line.lstrip())/4 # the number of '    ' before the first letter
                if newlevel == 0:
                    parentcategory = categorycontainer
                    currentlevel = 0
                if newlevel == currentlevel + 1:
                    parentcategory = previouscategory
                if newlevel == currentlevel:
                    pass
                if newlevel < currentlevel:
                    for i in range(currentlevel - newlevel):
                        parentcategory = parentcategory.__parent__
                currentlevel = newlevel
                name = line.split(':')[0].strip()
                description = u""
                if len(line.split(':')) > 1:
                    description = line.split(':')[1].strip()
                new = createObject("zompatible.Category", name = name, description = description)
                previouscategory = parentcategory[name.decode('utf-8')] = new


