# -*- coding: utf-8 -*-

from importdata import ImportFile
from zope.component import createObject
from zompatible.category.interfaces import IAvailableCategories
from zope.app.component.hooks import getSite
from zope.app.container.interfaces import INameChooser
from zompatible.organization.interfaces import ISoftwareEditor, IOrganizationInterfaces
from interfaces import *

class ImportSoftwareFile(ImportFile):
    u"""
    An import utility for default software objects
    See initial_software.txt
    """
    def do_import(self, context):
        if self.infile == u"":
            raise "No file provided"
        if context is None:
            raise "ImportSoftwareFile Error"
        site = context
        organizations = site['organizations']
        currentorga = None
        
        for line in open(self.infile):
                if line.strip() == '' or line.strip()[0]=='#':
                    continue # skip comments and empty lines
                level = line.find(line.lstrip())/4 # the number of '    ' before the first letter
                lineitems = [ i.strip() for i in line.split(':') ]
                lineitems[0] = [ i.strip() for i in lineitems[0].split(',') ]
                if level == 0: # try to find the orga or create it
                    found = False
                    for o in organizations:
                        for n in lineitems[0]:
                            if n in organizations[o].names:
                                currentorga = organizations[o]
                                found = True
                    if not found:
                        currentorga = createObject("zompatible.Organization", names=lineitems[0])
                        organizations[INameChooser(currentorga).chooseName(u"", currentorga)] = currentorga
                elif level == 1:
                    soft = createObject("zompatible.Software", names=lineitems[0])
                    soft.version = lineitems[1]
                    if len(lineitems) > 2:
                        soft.codename = lineitems[2]
                    IOrganizationInterfaces(currentorga).interfaces += [ ISoftwareEditor ]
                    softname = INameChooser(soft).chooseName(u"", soft)
                    currentorga['software'][softname] = soft
                else:
                    raise "ImportSoftwareFile Format Error"
