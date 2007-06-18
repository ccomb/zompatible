# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import AbsoluteURL
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import TextAreaWidget
from zope.app.form.browser.itemswidgets import MultiCheckBoxWidget
from zope.app.form.browser.interfaces import ITerms, ISourceQueryView
from zope.component import getAdapter, createObject, adapts, getUtility
from zope.app.container.interfaces import INameChooser
from zope.proxy import removeAllProxies
from zope.formlib.form import Actions, Action, getWidgetsData
from zope.copypastemove import ContainerItemRenamer
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleTerm

import string, urllib

from interfaces import *
from organization import Organization, OrgaSource
from zompatible.software.browser import SoftwareView
from zompatible.device.browser import DeviceView


class MyMultiCheckBoxWidget(MultiCheckBoxWidget):
    u"utilisé pour choisir IManufacturer et ISoftwareEditor dans une Organization"
    def __init__(self, field, subfield, request):
        u" encapsulation de l'init sans quoi ça marche pas..."
        super(MyMultiCheckBoxWidget, self).__init__(field,  field.value_type.vocabulary, request)


class CustomTextWidget(TextAreaWidget):
    width=40
    height=5

class OrganizationAdd(AddForm):
    u"""
    The view class for adding an organization
    The next URL allows to choose the product types
    """
    form_fields=Fields(IOrganization).omit('__name__', '__parent__')
    form_fields['description'].custom_widget=CustomTextWidget
    label=u"Adding an organization"
    def nextURL(self):
        return "%s/edit_organization_products.html" % AbsoluteURL(self.organization, self.request) 
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
    actions = Actions(Action('Apply', success='handle_edit_action'), )
    def __init__(self, context, request):
        self.context, self.request = context, request
        self.form_fields=Fields(IOrganization, *[ removeAllProxies(type) for type in IOrganizationInterfaces(self.context).interfaces ]).omit('__name__', '__parent__')
        self.form_fields['description'].custom_widget=CustomTextWidget
        super(OrganizationEdit, self).__init__(context, request)
        #template=ViewPageTemplateFile("organization_form.pt")
    def handle_edit_action(self, action, data):
        super(OrganizationEdit, self).handle_edit_action.success(data)
        oldname=self.context.__name__
        newname=string.lower(INameChooser(self.context).chooseName(u"",self.context))
        if string.lower(oldname)!=newname:
            renamer = ContainerItemRenamer(self.context.__parent__)
            renamer.renameItem(oldname, newname)
        return self.request.response.redirect(AbsoluteURL(self.context, self.request)()+"/edit_organization.html")
    def validate(self, action, data):
        u"on récupère les données du formulaire et on remplit data"
        getWidgetsData(self.widgets, 'form', data)
        u"on crée un objet temporaire pour tester le nouveau nom"
        dummy=Organization()
        u"on applique le formulaire au nouveau"
        applyChanges(dummy, self.form_fields, data)
        u"on calcule le nouveau nom avec le dummy (un peu loourdingue)"
        newname = INameChooser(dummy).chooseName(u"",dummy)
        u"s'il existe déjà on retourne une erreur"
        u"#####################  REMPLACER CA PAR LE CHECKNAME :"
        if newname in list(self.context.__parent__.keys()) and self.context != self.context.__parent__[newname]:
            return ("The name <i>"+newname+"</i> conflicts with another Organization",)
        return super(OrganizationEdit, self).validate(action, data)

class OrganizationInterfacesEdit(EditForm):
    label="Edit Organization Products"
    form_fields=Fields(IOrganizationInterfaces)
    form_fields['interfaces'].custom_widget = CustomWidgetFactory(MyMultiCheckBoxWidget)
    def __call__(self):
        u"""
        if we come from here, it means we've just modified the form, so we return to the organization
        """
        if 'form.actions.apply' in self.request :
            super(OrganizationInterfacesEdit, self).__call__()
            self.request.response.redirect(AbsoluteURL(self.context, self.request))
        else :
            return super(OrganizationInterfacesEdit, self).__call__()

class OrganizationView(BrowserPage):
    u"la vue qui permet d'afficher un organization"
    label="View of an Organization"
    __call__=ViewPageTemplateFile("organization.pt")
    def __init__(self, context, request):
        self.context, self.request = context, request
    def get_product_interfaces(self):
        return  [ {'name':type.getTaggedValue('name'), 'url':AbsoluteURL(getAdapter(self.context, type).products, self.request) } for type in IOrganizationInterfaces(self.context).interfaces ]

class OrganizationContainerView(object):
    u"""
    la vue du container de organizations.
    Pour l'instant on se contente d'afficher la liste des organizations.
    Ensuite il sera possible d'afficher par exemple des classements
    """
    label = u"List of organizations"
    def getorganizations(self):
        return ( (urllib.quote(orga[0]),orga[1]) for orga in self.context.items() )

class SearchProductView(BrowserPage):
    u"""
    La vue de recherche de produit, qui contient
    la méthode lancée depuis le template pour effectuer la recherche
    """
    def __call__(self, query=u""):
        organization=None
        self.results={}
        if IOrganization.providedBy(self.context):
            organization=self.context
        if IOrganization.providedBy(self.context.__parent__):
            organization=self.context.__parent__
        if IOrganization.providedBy(self.context.__parent__.__parent__):
            organization=self.context.__parent__.__parent__
        if organization is not None:
            self.results['devices']=createObject("zompatible.SearchObject", device_text=query, device_organization=organization).getResults()
            self.results['software']=createObject("zompatible.SearchObject", software_text=query, software_organization=organization).getResults()
        else:
            self.results['devices']=createObject("zompatible.SearchObject", device_text=query).getResults()
            self.results['software']=createObject("zompatible.SearchObject", software_text=query).getResults()
        return ViewPageTemplateFile('search_product.pt')(self)
    def getDevices(self):
        return self.results['devices']
    def getSoftwares(self):
        return self.results['software']
            
class OrgaTerms(object):
    u"""
    la vue fournissant les termes de la source à des fins d'affichage dans le widget
    (adapter de ISource vers ITerms)
    """
    implements(ITerms)
    adapts(OrgaSource, IBrowserRequest)
    def __init__(self, source, request):
        self.source=source
        self.intid=getUtility(IIntIds)
    def getTerm(self, value):
        u"""
        on crée un term à partir d'une orga
        On utilise le Unique Integer Id comme token
        (puisqu'il a fallu forcément en créer un pour la recherche dans le Catalog)
        """
        token = self.intid.getId(value)
        title = unicode(value.__name__)
        return SimpleTerm(value, token, title)
    def getValue(self, token):
        u"""
        on récupère le device à partir du token
        """
        return self.intid.getObject(int(token))

class OrgaQueryView(object):
    implements(ISourceQueryView)
    adapts(OrgaSource, IBrowserRequest)
    def __init__(self, source, request):
        u"source est le contexte"
        self.source=source
        self.request=request
    def render(self, name):
        u"""
        le code qui affiche la vue permettant la recherche
        Il pourrait être intéressant d'y mettre un viewlet (??) ou au moins un template
        'name' est le préfixe pour les widgets.
        """
        return('<input name="%s.string" /><input type="submit" name="%s" value="chercher" />' % (name, name) )
    def results(self, name):
        if name in self.request:
            search_string = self.request.get(name+'.string')
            if search_string is not None:
                return createObject(u"zompatible.SearchObject", organization_text=search_string).getResults()





