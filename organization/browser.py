# -*- coding: utf-8 -*-
from interfaces import *
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import AbsoluteURL
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser.itemswidgets import MultiCheckBoxWidget
from zope.component import getAdapter
from zope.proxy import removeAllProxies

from organization import Organization, SearchProduct


class MyMultiCheckBoxWidget(MultiCheckBoxWidget):
    def __init__(self, field, subfield, request):
        super(MyMultiCheckBoxWidget, self).__init__(field,  field.value_type.vocabulary, request)

class OrganizationAdd(AddForm):
    u"""
    The view class for adding an organization
    The next URL allows to choose the product types
    """
    form_fields=Fields(IOrganization).omit('__name__', '__parent__')
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
    def __init__(self, context, request):
        self.context, self.request = context, request
        self.form_fields=Fields(IOrganization, *[ removeAllProxies(type) for type in IOrganizationInterfaces(self.context).interfaces ]).omit('__name__', '__parent__')
        super(OrganizationEdit, self).__init__(context, request)
        #template=ViewPageTemplateFile("organization_form.pt")

class OrganizationInterfacesEdit(EditForm):
    label="Edit Organization Products"
    form_fields=Fields(IOrganizationInterfaces)
    form_fields['interfaces'].custom_widget = CustomWidgetFactory(MyMultiCheckBoxWidget)
    def __call__(self):
        u"""
        if we come from here, we've just modified the form, so we return to the organization
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
        return self.context.items()

    
class SearchProductView(BrowserPage):
    u"""
    La vue de recherche de produit, qui contient
    la méthode lancée depuis le template pour effectuer la recherche
    """
    def __call__(self, query):
        organization=None
        if IOrganization.providedBy(self.context):
            organization=self.context
        self.results=SearchProduct(query, organization).getResults()
        return ViewPageTemplateFile('search_product.pt')(self)
    def getDevices(self):
        return [ { 'device' : device, 'url' : AbsoluteURL(device, self.request) } for device in self.results['devices'] ]
    def getSoftwares(self):
        return [ { 'software' : software, 'url' : AbsoluteURL(software, self.request) } for software in self.results['softwares'] ]
            


