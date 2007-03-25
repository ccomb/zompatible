
from zope.interface import implements
from interfaces import IImport, IImportPciData
#from zompatible.organization.interfaces 

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
from zope.component import createObject	
import transaction
from zompatible.organization.organization import Organization

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
	orgas = [ l for l in lignes if ( len(l)>=2 and
																len(l[0])==4 and  
																l[1]!=None)             ]

	print "ORGANISATION list:"
	for orga in orgas:
		print "pciid:%s \tName:%s" %(orga[0], orga[1])
#		a=Organization()
#		a = createObject(u"zompatible.Organization")
#		a.names.append(orga[1])
#		a.pciids.append(orga[0])
	
	# Now we parse the devices
	orgaName = u''
	orgaId = u''
	chipName = u''
	chipId = u''
	productName = u''
	productvendorId = u''
	productDeviceId = u''
	for l in lignes:
		if len(l) >= 2:
			if    len(l[0]) == 4:		# No tab
				orgaName = l[1]
				orgaId = l[0]
			elif len(l[0]) == 5:		# One tab
				chipName = l[1]
				chipId = l[0][1:5]
			elif len(l[0]) == 11:		# Two tabs
				productName = l[1]
				productVendorId = l[0][2:6]
				productDeviceId = l[0][7:11]
				print "%s(%s,%s) includes the chip %s(%s) from the manufacturer %s(%s)" % (	productName, productVendorId, productDeviceId,
																																														chipName, chipId, 
																																														orgaName, orgaId)
			elif l[0] != None:
				print "%s non traitée" % (l[0])
			
#transaction.commit()
	
	importPciData.status = u"Import successfull"

from zope.component import provideHandler

provideHandler(updateZodbFromPciData)
