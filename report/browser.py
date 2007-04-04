# -*- coding: utf-8 -*-
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile

from report import EasinessReport, StabilityReport
from interfaces import *

from datetime import *

class EasinessReportAdd(AddForm):
    u"""
    The view class for adding an easiness report
    """
    form_fields=Fields(IEasinessReport).omit('__name__', '__parent__', 'date')
    label=u"Adding an easiness Report"
    def create(self, data):
        self.report = EasinessReport()
        self.report.date = datetime.now()
        applyChanges(self.report, self.form_fields, data)
        return self.report

class StabilityReportAdd(AddForm):
    u"""
    The view class for adding a stability report
    """
    form_fields=Fields(IStabilityReport).omit('__name__', '__parent__', 'date')
    label=u"Adding a stability Report"
    def create(self, data):
        self.report = StabilityReport()
        self.report.date = datetime.now()
        applyChanges(self.report, self.form_fields, data)
        return self.report

class EasinessReportEdit(EditForm):
    u"""
    The view class to edit an easiness Report
    """
    form_fields=Fields(IEasinessReport).omit('__name__', '__parent__', 'date')
    label=u"Edit an easiness Report"

class StabilityReportEdit(EditForm):
    u"""
    The view class to edit a stability Report
    """
    form_fields=Fields(IStabilityReport).omit('__name__', '__parent__', 'date')
    label=u"Edit a stability Report"
    
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
    label="List of Reports"
    __call__=ViewPageTemplateFile("report_container.pt")
    def getitems(self):
        return self.context.items()