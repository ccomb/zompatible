from zope.interface import Interface
from zope.schema import Text, TextLine

class IImport(Interface):
	"""Import information to fill the data base
	This interface could provide: date of the last import, ...
	"""
	pass

class IImportPciData(IImport):
	"""Import data as they are formated in pci.ids files.
	"""
	data = Text(
		title=u"pci.ids file content",
		description=u"Holds the data to analyse, coming from a pci.ids file.",
		required=True)

	status = TextLine(
		title=u"Status",
		description=u"Report status of the last import",
		required=False
		)

