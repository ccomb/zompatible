# -*- coding: utf-8 -*-
from zope.formlib.form import EditForm, Fields, AddForm
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from interfaces import *

class ReportAdd(AddForm):
    u"""
    The view class for adding a report
    """
    form_fields=Fields(IReport).omit('__name__', '__parent__')
    label=u"Adding a Report"
    #template=ViewPageTemplateFile("organization_form.pt")

class ReportEdit(EditForm):
    u"""
    The view class to edit a Report
    """
    
class ReportView(BrowserPage):
    u"""
    The view class to view a Report
    """
    label="View of a Report"
    __call__=ViewPageTemplateFile("report.pt")

class ReportContainerView(BrowserPage):
    u"""
    The view class to view a ReportContainer (actually a Support)
    """
    label="View of a Report"
    __call__=ViewPageTemplateFile("report_container.pt")
