# -*- coding: utf-8 -*-
from zope.publisher.browser import BrowserPage
from zope.formlib.form import EditForm, Fields
from zompatible.importdata.interfaces import IImportData
from zope.app.form.browser.widget import DisplayWidget

class StatusWidget(DisplayWidget):
    def __call__(self):
        return self.context.context.status.replace('\n','<br/>')

class ViewImportData(BrowserPage):
	""" A simple view of ImportData
	"""
	def __call__(self):
		response = self.request.response
		response.setHeader('Content-Type', 'text/plain')
		return self.context.data
		
class ImportDataEditForm(EditForm):
	form_fields = Fields(IImportData).omit('__parent__') # omit parent because containers constraint adds __parent__ in the schema
	form_fields['status'].custom_widget = StatusWidget
	label = u"Copy file data here"
