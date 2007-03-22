# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import adapts, getUtility
from zope.app.form.browser.interfaces import ITerms, ISourceQueryView
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.vocabulary import SimpleTerm
from zope.app.intid.interfaces import IIntIds
from zope.copypastemove import ContainerItemRenamer
from zope.formlib.form import Actions, Action, getWidgetsData
from zope.app.container.interfaces import INameChooser
from zope.traversing.browser.absoluteurl import AbsoluteURL
import string

from support import Support
from interfaces import *

class SupportAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    form_fields=Fields(ISupport)
    form_fields=form_fields.omit('__name__', '__parent__')
    label=u"Association entre un matériel et un logiciel"
    def nextURL(self):
        return "../.."
    #####template=ViewPageTemplateFile("support_form.pt")
    def create(self, data):
        u"on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
        support=Support()
        u"puis on applique les données du formulaire à l'objet"
        applyChanges(support, self.form_fields, data)
        u"puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
        self.context.contentName=support.device.__name__ + "-" + support.software.__name__
        return support

class SupportEdit(EditForm):
    label=u"Modification d'une association entre soft et hard"
    form_fields=Fields(ISupport, render_context=True)
    #form_fields['subdevices'].custom_widget=subdevices_widget
    form_fields=form_fields.omit('__name__', '__parent__')