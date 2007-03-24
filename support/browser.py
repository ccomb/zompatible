# -*- coding: utf-8 -*-
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib.form import Actions, Action, getWidgetsData
from zope.proxy import removeAllProxies

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
        if (IDevice.providedBy(self.context.__parent__.__parent__)):
            self.form_fields=Fields(ISupport).omit('__name__', '__parent__', 'device')
        if (ISoftware.providedBy(self.context.__parent__.__parent__)):
            self.form_fields=Fields(ISupport).omit('__name__', '__parent__', 'software')
        super(SupportAdd, self).__init__(context, request)
        #template=ViewPageTemplateFile("organization_form.pt")
    def nextURL(self):
        return "../.."
    #####template=ViewPageTemplateFile("support_form.pt")
    def create(self, data):
        u"on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
        support=Support()
        if (IDevice.providedBy(self.context.__parent__.__parent__)):
            support.device = removeAllProxies(self.context.__parent__.__parent__)
        if (ISoftware.providedBy(self.context.__parent__.__parent__)):
            support.software = removeAllProxies(self.context.__parent__.__parent__)
        u"puis on applique les données du formulaire à l'objet"
        applyChanges(support, self.form_fields, data)
        u"puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
        #self.context.contentName=support.device.__name__ + "-" + support.software.__name__
        return support

class SupportEdit(EditForm):
    label=u"Modification d'une compatibilité entre soft et hard"
    form_fields=Fields(ISupport, render_context=True)
    #form_fields['subdevices'].custom_widget=subdevices_widget
    form_fields=form_fields.omit('__name__', '__parent__')
    
    
class SupportView(BrowserPage):
    "la vue qui permet d'afficher un objet support"
    label=u"Niveau de compatibilité"
    __call__=ViewPageTemplateFile("support.pt")

class SupportContainerView(object):
    u"""
    la vue du container de supports.
    Pour l'instant on se contente d'afficher la liste des supports.
    Ensuite il sera possible d'afficher par exemple des classements
    """
    label = u"Compatibility list"
    def getitems(self):
        u"we return the list of compatible software or hardware depending on the context"
        if (IDevice.providedBy(self.context.__parent__)):
            return ( { 'support': support, 'related' : support.software } for support in self.context.values() )
        if (ISoftware.providedBy(self.context.__parent__)):
            return ( { 'support': support, 'related' : support.device } for support in self.context.values() )
