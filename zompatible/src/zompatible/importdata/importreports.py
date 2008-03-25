# -*- coding: utf-8 -*-
from zope.component import adapts
from zope.interface import implements
from importdata import ImportFile
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile

from interfaces import *


class ImportModulesPciMap(ImportFile):
    u"""
    create reports from module.pcimap file
    These reports must just tell that « it might work because there is a module for that device »
    """
    # trouver un moyen de ne l'associer qu'à une distro linux via les catégories
    def do_import(self, context):
    
        return self.fileupload.read()
        

class UploadModulesPciMap(BrowserPage):
    u"""
    the view that offers the upload field
    """
    def errors(self):
        u"""
        the method that does the job and return the status
        """
        if "UPLOAD" in self.request.form:
            return ImportModulesPciMap(fileupload=self.request.form[u"field.data"]).do_import(self.context)
            
    def __call__(self):
        u"the template calls the errors() method to iniate the import"
        return ViewPageTemplateFile("browser/file_import.pt")(self)
	