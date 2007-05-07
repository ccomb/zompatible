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
    def do_import(self, context):
        if self.infile == u"":
            raise "No file provided"
        if context is None:
            raise "ImportCategoryFile Error"
        categorycontainer = IAvailableCategories(context)
        parentcategory = previouscategory = categorycontainer
        currentlevel = 0
        for line in open(self.infile):
                if line.strip() == '' or line.strip()[0]=='#':
                    continue # skip comments and empty lines
                newlevel = line.find(line.lstrip())/4 # the number of '    ' before the first letter
                if newlevel == currentlevel + 1: # a subcategory
                    parentcategory = previouscategory
                if newlevel == currentlevel: # a category at the same level
                    pass
                if newlevel < currentlevel: # an upper category
                    for i in range(currentlevel - newlevel):
                        parentcategory = parentcategory.__parent__
                currentlevel = newlevel
                names = [ name.strip() for name in line.split(':')[0].split(',') ]
                description = u""
                if len(line.split(':')) > 1:
                    description = line.split(':')[1].strip()
                new = createObject("zompatible.Category", names = names, description = description)
                previouscategory = parentcategory[names[0].decode('utf-8').strip().replace(' ','-').replace(u'/',u'-').lstrip('+@')] = new


