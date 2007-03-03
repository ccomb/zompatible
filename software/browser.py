# -*- coding: utf-8 -*-
from interfaces import *
from zope.interface import implements
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.app.container.browser.contents import Contents
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder
from zope.index.text.interfaces import ISearchableText
from zope.component import adapts
from zope.app.folder.interfaces import IFolder
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.traversing.browser.absoluteurl import AbsoluteURL
from zope.app.container.interfaces import INameChooser

from software import OperatingSystem

class OperatingSystemAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    form_fields=Fields(IOperatingSystem).omit('__name__', '__parent__')
    label=u"Adding an Operating System"
    def nextURL(self):
        return AbsoluteURL(self.operatingsystem, self.request)
    #template=ViewPageTemplateFile("operatingsystem_form.pt")
    def create(self, data):
        self.operatingsystem=OperatingSystem()
        applyChanges(self.operatingsystem, self.form_fields, data)
        self.context.contentName=INameChooser(self.operatingsystem).chooseName(u"toto",self.operatingsystem)
        return self.operatingsystem


class OperatingSystemEdit(EditForm):
  label="Edit operatingsystem details"
  form_fields=Fields(IOperatingSystem).omit('__name__', '__parent__')
  #template=ViewPageTemplateFile("operatingsystem_form.pt")

class OperatingSystemView(BrowserPage):
    label="View of a operatingsystem"
    __call__=ViewPageTemplateFile("operatingsystem.pt")

class OperatingSystemContainerView(object):
    u"""
    la vue du container de operatingsystems.
    Pour l'instant on se contente d'afficher la liste des operatingsystems.
    Ensuite il sera possible d'afficher par exemple des classements
    """
    label = u"List of operatingsystems"
    def getoperatingsystems(self):
        return self.context.items()
