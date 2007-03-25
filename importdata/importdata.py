
from zope.interface import implements
from interfaces import IImport, IImportPciData

class Import(object):
	implements(IImport)
	pass
	
class ImportPciData(Import):
	implements(IImportPciData)

	data = u''
	status = u''


from zope.component.factory import Factory

importPciDataFactory = Factory(
    ImportPciData,
    title=u"Create a new importPciData object",
    description = u"This factory instantiates new importPciDatas."
    )

from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

@adapter(IImportPciData, IObjectModifiedEvent)
def updateZodbFromPciData(importPciData, event):
	data = importPciData.data
	lignes = data.split("\n")
	# Get rid of empty lignes
	lignes = [ l for l in lignes if len(l)>0]
	# Get rid of comments (elements have at least one caracter)
	lignes = [ l for l in lignes if l[0]!='#']
	# split Id and description
	lignes = [ l.split("  ") for l in lignes]
	
	# Then first we add the organisation and after the devices
	orga = [ l for l in lignes if l[0][0]!='\t']
	
	print orga	
	
	importPciData.status = u"Import successfull"

from zope.component import provideHandler

provideHandler(updateZodbFromPciData)
