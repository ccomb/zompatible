# -*- coding: utf-8 -*-
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile

from report import EasinessReport
from interfaces import *

from datetime import *

class EasinessReportAdd(AddForm):
    u"""
    The view class for adding a report
    """
    form_fields=Fields(IEasinessReport).omit('__name__', '__parent__', 'date')
    label=u"Adding an easiness Report"
    #template=ViewPageTemplateFile("organization_form.pt")
    def create(self, data):
        self.report = EasinessReport()
        self.report.date = datetime.now()
        applyChanges(self.report, self.form_fields, data)
        #self.context.contentName=string.lower(INameChooser(self.report).chooseName(u"",self.report))
        return self.report

class EasinessReportEdit(EditForm):
    u"""
    The view class to edit a Report
    """
    form_fields=Fields(IEasinessReport).omit('__name__', '__parent__', 'date')
    label=u"Edit a Report"
   
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
    def getitems(self):
        return self.context.items()