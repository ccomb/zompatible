# -*- coding: utf-8 -*-
from zope.formlib.form import EditForm, Fields
from zope.app.form.browser.itemswidgets import MultiCheckBoxWidget
from zope.app.form import CustomWidgetFactory
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import AbsoluteURL

from interfaces import *


class MyMultiCheckBoxWidget(MultiCheckBoxWidget):
    u"utilisé pour choisir une catégorie"
    def __init__(self, field, subfield, request):
        u" encapsulation de l'init sans quoi ça marche pas..."
        super(MyMultiCheckBoxWidget, self).__init__(field,  field.value_type.vocabulary, request)

class CategoriesEdit(EditForm):
    label=u"Edit the categories"
    form_fields=Fields(ICategories)
    form_fields['categories'].custom_widget = CustomWidgetFactory(MyMultiCheckBoxWidget)
    #__call__=ViewPageTemplateFile('edit_categories.pt')
    def __init__(self, context, request):
        self.context, self.request = context, request
        super(CategoriesEdit, self).__init__(context,request)
        self.setUpWidgets()

class CategoriesView(BrowserPage):
    label=u"View the categories"
    form_fields=Fields(ICategories)
    __call__=ViewPageTemplateFile('categories.pt')
    def get_categories(self):
        return ICategories(self.context).categories

class AvailableCategoriesEdit(BrowserPage):
    def __call__(self):
        available_categories = IAvailableCategories(self.context)
        return self.request.response.redirect(AbsoluteURL(available_categories, self.request)()+"/contents.html")
