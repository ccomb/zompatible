from zope.interface import Interface
from zope.schema import Text, TextLine
from zope.app.container.constraints import containers
from zope.app.component.interfaces import ILocalSiteManager

class IImport(Interface):
	"""Import information to fill the data base
	This interface could provide: date of the last import, ...
	"""
	pass

class IImportData(IImport):
	"""Import data as they are formated in pci.ids files.
	"""
	containers(ILocalSiteManager)
	data = Text(
		title=u"pci.ids file content",
		description=u"Holds the data to analyse, coming from a pci.ids file.",
		required=True)

	status = Text(
		title=u"Status",
		description=u"Report status of the last import",
		required=False,
		readonly=True
		)

	def updateZodbFromPciData(self):
		""" Import data from pci.ids file format
		"""
		
	def updateZodbFromUsbData(self):
		""" Import data from usb.ids file format
		"""
		