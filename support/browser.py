# -*- coding: utf-8 -*-
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib.form import Actions, Action, getWidgetsData
from zope.proxy import removeAllProxies
from zope.app.component.hooks import getSite
from zope.app.container.interfaces import INameChooser

from zompatible.device.interfaces import IDevice
from zompatible.software.interfaces import ISoftware
from support import Support
from interfaces import *

class SupportAdd(AddForm):
    u"""
    La vue (classe) de formulaire pour l'ajout
    Le contexte initial est l'objet supporté (Device ou software)
    Mais on ajoute l'objet dans le dossier supports de la racine
    donc on déplace le contexte du contexte vers lui
    """
    #form_fields=Fields(ISupport)
    #form_fields=form_fields.omit('__name__', '__parent__')
    label=u"Compatibilité entre un matériel et un logiciel"
    def __init__(self, context, request):
        super(SupportAdd, self).__init__(context, request)
        self.supported = context
        self.request = request
        self.context = context
        if (IDevice.providedBy(self.supported)):
            self.form_fields=Fields(ISupport).omit('__name__', '__parent__', 'device')
        if (ISoftware.providedBy(self.supported)):
            self.form_fields=Fields(ISupport).omit('__name__', '__parent__', 'software')
        #template=ViewPageTemplateFile("organization_form.pt")
    def nextURL(self):
        return "compatibility.html"
    #####template=ViewPageTemplateFile("support_form.pt")
    def createAndAdd(self, data):
        u"on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
        supports = getSite()['supports']
        support=Support()
        support.__parent__ = supports
        support.__name__ = INameChooser(support).chooseName(None, support)
        if (IDevice.providedBy(self.supported)):
            support.device = removeAllProxies(self.supported)
        if (ISoftware.providedBy(self.supported)):
            support.software = removeAllProxies(self.supported)
        u"puis on applique les données du formulaire à l'objet"
        applyChanges(support, self.form_fields, data)
        u"Et on ajoute l'objet respectivement dans l'attribut 'supports' de Software ET Device. La clé de l'OOBtree est le device dans le cas du software et inversement."
        support.software.supports[support.device] = support
        support.device.supports[support.software] = support
        supports[support.__name__] = support
        return support

class SupportEdit(EditForm):
    label=u"Modification d'une compatibilité entre soft et hard"
    form_fields=Fields(ISupport, render_context=True)
    #form_fields['subdevices'].custom_widget=subdevices_widget
    form_fields=form_fields.omit('__name__', '__parent__')

class SupportView(BrowserPage):
    u"""The view of a support object"""
    label = u"Compatibility"
    __call__=ViewPageTemplateFile("support.pt")

class CompatibilityView(BrowserPage):
    u"""
    la vue d'un objet ISupported (Software ou Device) qui permet d'afficher les notions de compatibilité
    Pour l'instant on se contente d'afficher la liste des supports.
    Ensuite il sera possible d'afficher par exemple des classements
    
    Si on trouve 'with' dans la requête, on affiche l'objet Support correspondant
    """
    label = u"Compatibility list"
    __call__=ViewPageTemplateFile("compatible.pt")
    support = None
    def __init__(self, context, request):
        super(BrowserPage, self).__init__(context, request)
    def getitems(self):
        u"""
        we return the list of compatible software or hardware depending on the context
        """
        if (IDevice.providedBy(self.context)):
            return ( { 'support': support, 'related' : support.software } for support in self.context.supports.values() )
        if (ISoftware.providedBy(self.context)):
            return ( { 'support': support, 'related' : support.device } for support in self.context.supports.values() )
    def getrelated(self):
        if (IDevice.providedBy(self.context) and self.support is not None):
            return self.support.software
        if (ISoftware.providedBy(self.context) and self.support is not None):
            return self.support.device
