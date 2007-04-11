from zope.publisher.browser import BrowserPage
from zope.formlib.form import EditForm, Fields
from zompatible.importdata.interfaces import IImportData

class ViewImportData(BrowserPage):
	""" A simple view of ImportData
	"""
	def __call__(self):
		response = self.request.response
		response.setHeader('Content-Type', 'text/plain')
		return self.context.data
		
class ImportDataEditForm(EditForm):
	form_fields = Fields(IImportData).omit('__parent__') # omit parent because containers constraint adds __parent__ in the schema
	label = u"Copy file data here"
	