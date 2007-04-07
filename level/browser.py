# -*- coding: utf-8 -*-
from zope.app.form.browser import ListSequenceWidget, ObjectWidget
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import TextAreaWidget
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges, Actions, Action, getWidgetsData

from level import Level
from interfaces import *


objectwidget = CustomWidgetFactory(ObjectWidget, Level)
listwidget = CustomWidgetFactory(ListSequenceWidget, subwidget=objectwidget)

 
class LevelsEdit(EditForm):
    u"""
    The view class to edit the available Levels in the site manager *_levels utilities
    """
    form_fields=Fields(ILevels).omit('__parent__') # omit parent because the containers constraint adds __parent__ in the schema
    label=u"Edit available levels"
    form_fields['levels'].custom_widget = listwidget

