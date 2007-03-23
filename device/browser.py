# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges, Actions, Action, getWidgetsData
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import adapts, getUtility
from zope.app.form.browser.interfaces import ITerms, ISourceQueryView
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.vocabulary import SimpleTerm
from zope.app.intid.interfaces import IIntIds
from zope.copypastemove import ContainerItemRenamer
from zope.app.container.interfaces import INameChooser
from zope.traversing.browser.absoluteurl import AbsoluteURL
import string

from device import Device, SearchDevice, DeviceSource
from interfaces import *
    


class DeviceAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    form_fields=Fields(IDevice, ISubDevices)
    #form_fields['subdevices'].custom_widget=subdevices_widget
    form_fields=form_fields.omit('__name__', '__parent__')
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
    label=u"Modification d'un matériel"
    form_fields=Fields(IDevice, ISubDevices, render_context=True)
    #form_fields['subdevices'].custom_widget=subdevices_widget
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
    La vue permettant d'interroger la source
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
                return SearchDevice(search_string).getResults()



class DeviceContainerView(object):
    u"""
    la vue du container de devices.
    Pour l'instant on se contente d'afficher la liste des devices.
    Ensuite il sera possible d'afficher par exemple des classements
    """
    label = u"List of devices"
    def getitems(self):
        return self.context.items()




