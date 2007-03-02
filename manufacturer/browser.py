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

from manufacturer import Manufacturer
from zompatible.device.device import DeviceContainer

class ManufacturerAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    form_fields=Fields(IManufacturer).omit('__name__', '__parent__')
    label=u"Adding a manufacturer"
    def nextURL(self):
        return AbsoluteURL(self.manufacturer, self.request)
    #template=ViewPageTemplateFile("manufacturer_form.pt")
    def create(self, data):
        u"on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
        self.manufacturer=Manufacturer()
        u"puis on applique les données du formulaire à l'objet (data contient les données du formulaire !)"
        applyChanges(self.manufacturer, self.form_fields, data)
        u"puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
        self.context.contentName=self.manufacturer.names[0]
        return self.manufacturer


class ManufacturerEdit(EditForm):
  label="Edit manufacturer details"
  form_fields=Fields(IManufacturer).omit('__name__', '__parent__')
  #template=ViewPageTemplateFile("manufacturer_form.pt")

class ManufacturerView(BrowserPage):
    "la vue qui permet d'afficher un manufacturer"
    label="View of a manufacturer"
    __call__=ViewPageTemplateFile("manufacturer.pt")
    def testannotations(self):
        IAnnotations(self.context)['zompatible.manufacturer.manufacturer.Manufacturer.category']='toto'
        return IAnnotations(self.context)['zompatible.manufacturer.manufacturer.Manufacturer.category']


class ManufacturerContainerView(object):
    u"""
    la vue du container de manufacturers.
    Pour l'instant on se contente d'afficher la liste des manufacturers.
    Ensuite il sera possible d'afficher par exemple des classements
    """
    label = u"List of manufacturers"
    def getmanufacturers(self):
        return self.context.items()
