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

from organization import Organization
from zompatible.device.device import DeviceContainer

class OrganizationAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    form_fields=Fields(IOrganization).omit('__name__', '__parent__')
    label=u"Adding a organization"
    def nextURL(self):
        return AbsoluteURL(self.organization, self.request)
    #template=ViewPageTemplateFile("organization_form.pt")
    def create(self, data):
        u"on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
        self.organization=Organization()
        u"puis on applique les données du formulaire à l'objet (data contient les données du formulaire !)"
        applyChanges(self.organization, self.form_fields, data)
        u"puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
        self.context.contentName=self.organization.names[0]
        return self.organization


class OrganizationEdit(EditForm):
  label="Edit organization details"
  form_fields=Fields(IOrganization).omit('__name__', '__parent__')
  #template=ViewPageTemplateFile("organization_form.pt")

class OrganizationView(BrowserPage):
    "la vue qui permet d'afficher un organization"
    label="View of a organization"
    __call__=ViewPageTemplateFile("organization.pt")
    def testannotations(self):
        IAnnotations(self.context)['zompatible.organization.organization.Organization.category']='toto'
        return IAnnotations(self.context)['zompatible.organization.organization.Organization.category']


class OrganizationContainerView(object):
    u"""
    la vue du container de organizations.
    Pour l'instant on se contente d'afficher la liste des organizations.
    Ensuite il sera possible d'afficher par exemple des classements
    """
    label = u"List of organizations"
    def getorganizations(self):
        return self.context.items()
