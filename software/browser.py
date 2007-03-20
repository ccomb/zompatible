# -*- coding: utf-8 -*-
from interfaces import *
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import AbsoluteURL
from zope.app.container.interfaces import INameChooser
from zope.formlib.form import Actions, Action, getWidgetsData
from zope.copypastemove import ContainerItemRenamer
import string

from software import Software

class SoftwareAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    form_fields=Fields(ISoftware).omit('__name__', '__parent__')
    label=u"Adding an Software"
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
    form_fields=Fields(ISoftware).omit('__name__', '__parent__')
    #template=ViewPageTemplateFile("software_form.pt")
    u"On crée la liste des actions du formulaire"
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
        u"on récupère les données du formulaire et on remplit data"
        getWidgetsData(self.widgets, 'form', data)
        u"on crée un objet temporaire pour tester le nouveau nom"
        dummy=Software()
        u"on applique le formulaire au nouveau"
        applyChanges(dummy, self.form_fields, data)
        u"on calcule le nouveau nom avec le dummy (un peu loourdingue)"
        newname = INameChooser(dummy).chooseName(u"",dummy)
        u"s'il existe déjà on retourne une erreur"
        if newname in list(self.context.__parent__.keys()) and self.context != self.context.__parent__[newname]:
            return ("The name <i>"+newname+"</i> conflicts with another Software",)
        return super(SoftwareEdit, self).validate(action, data)
    

class SoftwareView(BrowserPage):
    label="View of a software"
    __call__=ViewPageTemplateFile("software.pt")
    def __init__(self, context, request):
        self.context, self.request = context, request
    def prettyName(self):
        return "%s %s %s" % (self.context.names[0], self.context.version, self.context.codename) 
    
class SoftwareContainerView(object):
    u"""
    la vue du container de softwares.
    Pour l'instant on se contente d'afficher la liste des softwares.
    Ensuite il sera possible d'afficher par exemple des classements
    """
    label = u"Software list"
    def getitems(self):
        return self.context.items()
