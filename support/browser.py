# -*- coding: utf-8 -*-
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib.form import Actions, Action, getWidgetsData
from zope.proxy import removeAllProxies
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility

from zompatible.device.interfaces import IDevice
from zompatible.software.interfaces import ISoftware
from support import Support
from interfaces import *

class SupportAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    #form_fields=Fields(ISupport)
    #form_fields=form_fields.omit('__name__', '__parent__')
    label=u"Compatibilité entre un matériel et un logiciel"
    def __init__(self, context, request):
        self.context, self.request = context, request
        if (IDevice.providedBy(self.context)):
            self.form_fields=Fields(ISupport).omit('__name__', '__parent__', 'device')
        if (ISoftware.providedBy(self.context)):
            self.form_fields=Fields(ISupport).omit('__name__', '__parent__', 'software')
        super(SupportAdd, self).__init__(context, request)
        #template=ViewPageTemplateFile("organization_form.pt")
    def nextURL(self):
        return "."
    #####template=ViewPageTemplateFile("support_form.pt")
    def createAndAdd(self, data):
        u"on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
        support=Support()
        if (IDevice.providedBy(self.context)):
            support.device = removeAllProxies(self.context)
        if (ISoftware.providedBy(self.context)):
            support.software = removeAllProxies(self.context)
        u"puis on applique les données du formulaire à l'objet"
        applyChanges(support, self.form_fields, data)
        u"Et on ajoute l'objet respectivement dans l'attribut 'supports' de Software et Device. La clé de l'OOBtree est le device dans le cas du software et inversement."
        support.software.supports[support.device] = support
        support.device.supports[support.software] = support
        return support

class SupportEdit(EditForm):
    label=u"Modification d'une compatibilité entre soft et hard"
    form_fields=Fields(ISupport, render_context=True)
    #form_fields['subdevices'].custom_widget=subdevices_widget
    form_fields=form_fields.omit('__name__', '__parent__')
    

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
        self.context, self.request = context, request
        self.intid=getUtility(IIntIds)
        if (self.request.has_key('id') and self.request.has_key('with')):
            self.support = self.context.supports[self.intid.getObject(int(self.request['id']))]
        super(BrowserPage, self).__init__(context, request)
    def getitems(self):
        u"""
        we return the list of compatible software or hardware depending on the context
        """
        if (IDevice.providedBy(self.context)):
            return ( { 'support': support, 'related' : support[1].software, 'related_id': self.intid.getId(support[1].software) } for support in self.context.supports.items() )
        if (ISoftware.providedBy(self.context)):
            return ( { 'support': support, 'related' : support[1].device, 'related_id': self.intid.getId(support[1].device) } for support in self.context.supports.items() )
    def getrelated(self):
        if (IDevice.providedBy(self.context) and self.support is not None):
            return self.support.software
        if (ISoftware.providedBy(self.context) and self.support is not None):
            return self.support.device
