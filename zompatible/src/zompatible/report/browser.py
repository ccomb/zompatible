# -*- coding: utf-8 -*-
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.form.browser.itemswidgets import RadioWidget
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import TextAreaWidget

from report import EasinessReport, StabilityReport
from interfaces import *

from datetime import *

class CustomTextWidget(TextAreaWidget):
    width=50
    height=5
    
class EasinessReportAdd(AddForm):
    u"""
    The view class for adding an easiness report
    """
    label=u"Adding an easiness Report"
    form_fields=Fields(IEasinessReport).select('level','comment')
    form_fields['level'].custom_widget = CustomWidgetFactory(RadioWidget)
    form_fields['comment'].custom_widget = CustomTextWidget
    def create(self, data):
        self.report = EasinessReport()
        self.report.date = datetime.now()
        applyChanges(self.report, self.form_fields, data)
        return self.report

class StabilityReportAdd(AddForm):
    u"""
    The view class for adding a stability report
    """
    label=u"Adding a stability Report"
    form_fields=Fields(IStabilityReport).select('level','comment')
    form_fields['level'].custom_widget = CustomWidgetFactory(RadioWidget)
    def create(self, data):
        self.report = StabilityReport()
        self.report.date = datetime.now()
        applyChanges(self.report, self.form_fields, data)
        return self.report

class EasinessReportEdit(EditForm):
    u"""
    The view class to edit an easiness Report
    """
    label=u"Edit an easiness Report"
    form_fields=Fields(IEasinessReport).select('level','comment')
    form_fields['level'].custom_widget = CustomWidgetFactory(RadioWidget)
    form_fields['comment'].custom_widget = CustomTextWidget

class StabilityReportEdit(EditForm):
    u"""
    The view class to edit a stability Report
    """
    label=u"Edit a stability Report"
    form_fields=Fields(IStabilityReport).select('level','comment')
    form_fields['level'].custom_widget = CustomWidgetFactory(RadioWidget)
    form_fields['comment'].custom_widget = CustomTextWidget
    
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