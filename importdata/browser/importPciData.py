from zope.publisher.browser import BrowserPage
from zope.formlib.form import EditForm, Fields
from zompatible.importdata.interfaces import IImportPciData

class ViewImportPciData(BrowserPage):
	""" A simple view of ImportPciData
	"""
	def __call__(self):
		response = self.request.response
		response.setHeader('Content-Type', 'text/plain')
		return self.context.data
		
class ImportPciDataEditForm(EditForm):
	form_fields = Fields(IImportPciData).omit('__parent__') # omit parent because containers constraint adds __parent__ in the schema
	label = u"Copy pci.ids file data here"
	