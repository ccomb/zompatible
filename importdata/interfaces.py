# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.schema import Text
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

class IImportFile(Interface):
    """
    interface of a file import utility.
    The file may come from the local filesystem (→ use filename attribute)
    or from an upload (→ use the fileupload attribute)
    """
    filename = Attribute(u"the filename from which to import")
    fileupload = Attribute(u"the FileUpload object from which to read")
    def importfile():
        u"perform the import"