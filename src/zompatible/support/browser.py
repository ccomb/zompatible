# -*- coding: utf-8 -*-
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib.form import Actions, Action, getWidgetsData
from zope.proxy import removeAllProxies
from zope.app.component.hooks import getSite
from zope.app.container.interfaces import INameChooser

from zompatible.product.interfaces import IProduct

from support import Support
from interfaces import *

class SupportAdd(AddForm):
    u"""
    La vue (classe) de formulaire pour l'ajout
    Le contexte initial est l'objet supporté (product)
    Mais on ajoute l'objet dans le dossier supports de la racine
    donc on déplace le contexte du contexte vers lui
    """
    label=u"Compatibility between two or more products"
    def __init__(self, context, request):
        super(SupportAdd, self).__init__(context, request)
        self.supported = context
        self.request = request
        self.context = context
        self.form_fields=Fields(ISupport)
        #template=ViewPageTemplateFile("organization_form.pt")
    def nextURL(self):
        return "compatibility.html"
    #####template=ViewPageTemplateFile("support_form.pt")
    def createAndAdd(self, data):
        # on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)
        supports = getSite()['supports']
        support = Support()
        support.__parent__ = supports
        support.__name__ = INameChooser(supports).chooseName(u"", support)
        support.products.extend([self, removeAllProxies(self.supported)])
        # puis on applique les données du formulaire à l'objet
        applyChanges(support, self.form_fields, data)
        supports[support.__name__] = support
        return support

class SupportEdit(EditForm):
    label=u"Modification d'une compatibilité entre soft et hard"
    form_fields=Fields(ISupport, render_context=True)
    #form_fields['subdevices'].custom_widget=subdevices_widget
    #form_fields=form_fields.omit('__name__', '__parent__')

class SupportView(BrowserPage):
    u"""The view of a support object"""
    label = u"Compatibility"
    __call__=ViewPageTemplateFile("support.pt")

class CompatibilityView(BrowserPage):
    u"""
    la vue d'un objet ISupported (product) qui permet d'afficher les notions de compatibilité
    Pour l'instant on se contente d'afficher la liste des supports.
    Ensuite il sera possible d'afficher par exemple des classements
    
    Si on trouve 'with' dans la requête, on affiche l'objet Support correspondant ?
    """
    label = u"Compatibility list"
    __call__=ViewPageTemplateFile("compatible.pt")
    support = None
    def __init__(self, context, request):
        super(BrowserPage, self).__init__(context, request)
    def getitems(self):
        """
        we return the list of support objects
        """
        return ( support for support in self.context.supports.values() )




