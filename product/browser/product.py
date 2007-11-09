# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges, Actions, Action, getWidgetsData
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import adapts, getUtility, createObject
from zope.app.form.browser.interfaces import ITerms, ISourceQueryView
from zope.schema.vocabulary import SimpleTerm
from zope.app.intid.interfaces import IIntIds
from zope.copypastemove import ContainerItemRenamer
from zope.app.container.interfaces import INameChooser
from zope.traversing.browser.absoluteurl import AbsoluteURL
from zope.app.form.browser import TextAreaWidget
import string, urllib

from device import Device, DeviceSource
from interfaces import *

from zompatible.product.interfaces import IProduct

class ProductView(BrowserPage):
    u""" Product view for a browser.
    """
    label="Product view"
    __call__=ViewPageTemplateFile("product.pt")

    def __init__(self, context, request):
        self.context, self.request = context, request
        self.char = []
        for e in ICharacteristicManager(self.context).CurrentList():
            iface = queryInterface(e)
            s = str(iface(self.context))
            if s != u'':
                self.char.append(str(iface(self.context)))

class ProductEditForm(EditForm):
    u""" Allows a product edition.
    """
    form_fields = Fields(IProduct).omit('categories') # omit categories because no value type is defined yet.
    label = u"Edit Product"
    
    def __init__(self, context, request):
        self.context, self.request = context, request
        print list(self.form_fields)
        





    
class CustomTextWidget(TextAreaWidget):
    width=40
    height=5

class DeviceAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    form_fields=Fields(IDevice, ISubDevices)
    form_fields['description'].custom_widget = CustomTextWidget
    #form_fields['subdevices'].custom_widget=subdevices_widget
    form_fields=form_fields.omit('__name__', '__parent__', 'organization')
    label=u"Ajout d'un matériel"
    def nextURL(self):
        return AbsoluteURL(self.device,self.request)
    #####template=ViewPageTemplateFile("device_form.pt")
    def create(self, data):
        u"on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
        self.device=Device()
        u"puis on applique les données du formulaire à l'objet"
        applyChanges(self.device, self.form_fields, data)
        u"puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
        self.context.contentName=self.device.names[0]
        return self.device


class DeviceEdit(EditForm):
    label=u"Edit a device"
    form_fields=Fields(IDevice, ISubDevices, render_context=True)
    #form_fields['subdevices'].custom_widget=subdevices_widget
    form_fields['description'].custom_widget = CustomTextWidget
    form_fields=form_fields.omit('__name__', '__parent__')
    ## template désactivé
    #template=ViewPageTemplateFile("device_form.pt")
    actions = Actions(Action('Apply', success='handle_edit_action'), )
    def handle_edit_action(self, action, data):
        super(DeviceEdit, self).handle_edit_action.success(data)
        oldname=self.context.__name__
        newname=string.lower(INameChooser(self.context).chooseName(u"",self.context))
        if string.lower(oldname)!=newname:
            renamer = ContainerItemRenamer(self.context.__parent__)
            renamer.renameItem(oldname, newname)
        return self.request.response.redirect(AbsoluteURL(self.context, self.request)()+"/edit_device.html")
    def validate(self, action, data):
        u"on récupère les données du formulaire et on remplit data"
        getWidgetsData(self.widgets, 'form', data)
        u"on crée un objet temporaire pour tester le nouveau nom"
        dummy=Device()
        u"on applique le formulaire au nouveau"
        applyChanges(dummy, self.form_fields, data)
        u"on calcule le nouveau nom avec le dummy (un peu loourdingue)"
        newname = INameChooser(dummy).chooseName(u"",dummy)
        u"s'il existe déjà on retourne une erreur"
        u"#####################  REMPLACER CA PAR LE CHECKNAME :"
        if newname in list(self.context.__parent__.keys()) and self.context != self.context.__parent__[newname]:
            return ("The name <i>"+newname+"</i> conflicts with another Device",)
        return super(DeviceEdit, self).validate(action, data)

class DeviceView(BrowserPage):
    "la vue qui permet d'afficher un device"
    label=u"Visualisation d'un matériel"
    __call__=ViewPageTemplateFile("device.pt")


class DeviceTerms(object):
    u"""
    la vue fournissant les termes de la source à des fins d'affichage dans le widget
    (adapter de ISource vers ITerms)
    """
    implements(ITerms)
    adapts(DeviceSource, IBrowserRequest)
    def __init__(self, source, request):
        self.source=source
        self.intid=getUtility(IIntIds)
    def getTerm(self, value):
        u"""
        on crée un term à partir d'un device
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

class DeviceQueryView(object):
    u"""
    The view allowing to query the source
    """
    implements(ISourceQueryView)
    adapts(DeviceSource, IBrowserRequest)
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
                return createObject(u"zompatible.SearchObject", device_text=search_string).getResults()

class DeviceContainerView(object):
    u"""
    la vue du container de devices.
    Pour l'instant on se contente d'afficher la liste des devices.
    Ensuite il sera possible d'afficher par exemple des classements
    """
    label = u"List of devices"
    def getitems(self):
        return ( (urllib.quote(dev[0]),dev[1]) for dev in self.context.items() )

##############"

# -*- coding: utf-8 -*-
from interfaces import *
from zope.interface import implements
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges, Actions, Action, getWidgetsData
from zope.publisher.browser import BrowserPage, BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import adapts, getUtility, createObject
from zope.app.form.browser.interfaces import ITerms, ISourceQueryView
from zope.publisher.interfaces.browser import IBrowserRequest, IBrowserView
from zope.schema.vocabulary import SimpleTerm
from zope.app.intid.interfaces import IIntIds
from zope.copypastemove import ContainerItemRenamer
from zope.app.container.interfaces import INameChooser
from zope.traversing.browser.absoluteurl import AbsoluteURL
from zope.app.form.browser import TextAreaWidget
import string

from software import Software, SoftwareSource

class CustomTextWidget(TextAreaWidget):
    width=40
    height=5

class SoftwareAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    form_fields=Fields(ISoftware, ISubSoftware).omit('__name__', '__parent__', 'organization')
    form_fields['description'].custom_widget = CustomTextWidget
    label=u"Adding a Software"
    def nextURL(self):
        return AbsoluteURL(self.software, self.request)
    #template=ViewPageTemplateFile("software_form.pt")
    def create(self, data):
        self.software=Software()
        applyChanges(self.software, self.form_fields, data)
        self.context.contentName=string.lower(INameChooser(self.software).chooseName(u"",self.software))
        return self.software

class SoftwareEdit(EditForm):
    label="Edit Software details"
    form_fields=Fields(ISoftware, ISubSoftware).omit('__name__', '__parent__')
    form_fields['description'].custom_widget = CustomTextWidget
    #template=ViewPageTemplateFile("software_form.pt")
    u"We create the list of actions of the form"
    actions = Actions(Action('Apply', success='handle_edit_action'), )
    def handle_edit_action(self, action, data):
        super(SoftwareEdit, self).handle_edit_action.success(data)
        oldname=self.context.__name__
        newname=string.lower(INameChooser(self.context).chooseName(u"",self.context))
        if string.lower(oldname)!=newname:
            renamer = ContainerItemRenamer(self.context.__parent__)
            renamer.renameItem(oldname, newname)
        return self.request.response.redirect(AbsoluteURL(self.context, self.request)()+"/edit_software.html")
    def validate(self, action, data):
        u"we retrieve data from the form and fill the data attribute"
        getWidgetsData(self.widgets, 'form', data)
        u"we create a temp object to test the new name"
        dummy=Software()
        u"we apply the form on the new object"
        applyChanges(dummy, self.form_fields, data)
        u"we compute the new name with the dummy (a bit ugly)"
        newname = INameChooser(dummy).chooseName(u"",dummy)
        u"if already exists, return an error"
        u"#####################  REMPLACER CA PAR LE CHECKNAME :"
        if newname in list(self.context.__parent__.keys()) and self.context != self.context.__parent__[newname]:
            return ("The name <i>"+newname+"</i> conflicts with another Software",)
        return super(SoftwareEdit, self).validate(action, data)
    

class SoftwareView(BrowserPage):
    label="View of a software"
    __call__=ViewPageTemplateFile("software.pt")
    def __init__(self, context, request):
        self.context, self.request = context, request

class SoftwarePrettyName(BrowserView):
    implements(IBrowserView)
    def __call__(self):
        codename = version = u""
        if self.context.codename is not None:
            codename = self.context.codename
        if self.context.version is not None:
            version = self.context.version
        return "%s %s %s" % (self.context.names[0], version, codename)
    
class SoftwareContainerView(object):
    u"""
    The view for the software container.
    For the moment, we just display the list.
    Then it will be possible to display some classifications
    """
    label = u"Software list"
    def getitems(self):
        return self.context.items()
        
class SoftwareTerms(object):
    u"""
    The view which provides the terms of the source (to display in the widget)
    (adapter from ISource to ITerms)
    """
    implements(ITerms)
    adapts(SoftwareSource, IBrowserRequest)
    def __init__(self, source, request):
        self.source=source
        self.intid=getUtility(IIntIds)
    def getTerm(self, value):
        u"""
        on crée un term à partir d'un software
        On utilise le Unique Integer Id comme token
        (puisqu'il a fallu forcément en créer un pour la recherche dans le Catalog)
        """
        token = self.intid.getId(value)
        title = unicode(value.__name__)
        return SimpleTerm(value, token, title)
    def getValue(self, token):
        u"""
        on récupère le software à partir du token
        """
        return self.intid.getObject(int(token))

    
    
class SoftwareQueryView(object):
    u"""
    La vue permettant d'interroger la source
    """
    implements(ISourceQueryView)
    adapts(SoftwareSource, IBrowserRequest)
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
                return createObject(u"zompatible.SearchObject", software_text=search_string).getResults()
