# -*- coding: utf-8 -*-

from zope.interface import implements
from interfaces import IImport, IImportPciData
from persistent.list import PersistentList

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
from zope.app.component.hooks import getSite
from zope.app.container.contained import setitem
from zope.interface.declarations import alsoProvides
from zompatible.device.device import DeviceContainer
from zompatible.organization.interfaces import IManufacturer

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
																
	root = getSite()
	for orga in orgas:
		name = orga[1]
		id = orga[0]
		if not name in root[u'organizations']:
			toto = createObject(u"zompatible.Organization")
			toto.names = [ name ]
			toto.pciids  = [ id ]
			toto.interfaces = [ IManufacturer ]
			alsoProvides(toto, IManufacturer)
			root[u'organizations'][name] = toto
			toto[u'devices'] = DeviceContainer()
#			transaction.commit()
		elif not id in root[u'organizations'][name].pciids:
			root[u'organizations'][name].pciids.append(id)
#			transaction.commit()
			
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
				if not chipName in root[u'organizations'][orgaName][u'devices']:
					a = createObject(u"zompatible.Device")
					a.names = [ chipName ]
					a.pciid = chipId
					root[u'organizations'][orgaName][u'devices'][chipName] = a
#					transaction.commit()
#				elif not chipId in root[u'organizations'][orgaName][u'devices'][chipName].pciids:
			elif len(l[0]) == 11:		# Two tabs
				productName = l[1]
				productVendorId = l[0][2:6]
				productDeviceId = l[0][7:11]
				for o in root[u'organizations']:
						if productVendorId in root[u'organizations'][o].pciids:
							if not productName in root[u'organizations'][o][u'devices']:
								a = createObject(u"zompatible.Device")
								a.names = [ productName ]
								a.pciid = productDeviceId
								root[u'organizations'][o][u'devices'][productName] = a
#								transaction.commit()
							break
#							elif not productDeviceId in root[u'organizations'][o][u'devices'][productName]
							
			elif l[0] != None:
				print "%s non traitée" % (l[0])
			
	transaction.commit()
	
	importPciData.status = u"Import successfull"

from zope.component import provideHandler

provideHandler(updateZodbFromPciData)
