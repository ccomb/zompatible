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
from zope.app.container.interfaces import INameChooser
import urllib

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
		if id == u'ffff':
			# We have reach the end of organizations (ffff stands for "Illegal Vendor ID"
			break
		urlName = urllib.quote_plus(name)
		if not urlName in root[u'organizations']:
			toto = createObject(u"zompatible.Organization")
			toto.names = [ name ]
			toto.pciids  = [ id ]
			toto.interfaces = [ IManufacturer ]
			alsoProvides(toto, IManufacturer)
			# Do not use HTTP reserved caracters in URL path !
			root[u'organizations'][urlName] = toto
			toto[u'devices'] = DeviceContainer()
		elif not id in root[u'organizations'][urlName].pciids:
			root[u'organizations'][urlName].pciids.append(id)
			
	# Now we parse the devices
	orgaName = u''
	orgaId = u''
	chipName = u''
	chipId = u''
	productName = u''
	productvendorId = u''
	productDeviceId = u''
	for l in lignes:
		# Ensure that there are a column for ids and an other for the description
		if len(l) >= 2:
			# No tab => organization
			if l[0].count(u'\t') == 0: 
				orgaName = urllib.quote_plus(l[1])
				orgaId = l[0]
				if orgaId == u'ffff':
					# We have reach the end of organizations (ffff stands for "Illegal Vendor ID"
					break
			# One tab => device
			elif l[0].count(u'\t') == 1:		
				chipName = l[1]
				chipId = l[0].replace(u'\t',u'').strip()
				sameDev = None
				for dev in  root[u'organizations'][orgaName][u'devices']: 
					if root[u'organizations'][orgaName][u'devices'][dev].pciid == chipId:
						sameDev = root[u'organizations'][orgaName][u'devices'][dev]
						break
				# If a device already exists with the same id, we add the new name to this device 
				if sameDev:
					sameDev.names.append(chipName)
				# If the device does not exists, we add it
				elif not urllib.quote_plus(chipName) in root[u'organizations'][orgaName][u'devices']:
					a = createObject(u"zompatible.Device")
					a.names = [ chipName ]
					a.pciid = chipId
					a.subdevices = []
					# Do not use HTTP reserved caracters in URL path !
					urlName = urllib.quote_plus(chipName)
					root[u'organizations'][orgaName][u'devices'][urlName] = a
#				elif not chipId in root[u'organizations'][orgaName][u'devices'][chipName].pciids:
			# Two tabs => subsystem device
			elif l[0].count(u'\t') == 2:		
				productName = l[1]
				Ids = l[0].replace(u'\t',u'').strip().split(" ")
				productVendorId = Ids[0]
				productDeviceId = Ids[1]
				for o in root[u'organizations']:
					# If we find the organization from its id
					if productVendorId in root[u'organizations'][o].pciids:
						sameDev = None
						for dev in  root[u'organizations'][o][u'devices']: 
							if root[u'organizations'][o][u'devices'][dev].pciid == productDeviceId:
								sameDev = root[u'organizations'][o][u'devices'][dev]
								break
						# If a device already exists with the same id, we add the new name to this device 
						if sameDev:
							sameDev.names.append(productName)
#							if not urllib.quote_plus(chipName) in sameDev.subdevices:
#								print "same device:%s, productName:%s, orgaName:%s, chipName:%s" % (sameDev.names[0], productName, orgaName, chipName)
#								sameDev.subdevices.append(root[u'organizations'][orgaName][u'devices'][urllib.quote_plus(chipName)])
#								if len(sameDev.subdevices) >= 2:
#									print "%s/%s has several subdevices !" % (orgaName, sameDev.names[0])
						# If the device does not exists, we add it
						elif not urllib.quote_plus(productName) in root[u'organizations'][o][u'devices']:
							a = createObject(u"zompatible.Device")
							a.names = [ productName ]
							a.pciid = productDeviceId
							a.subdevices = [ root[u'organizations'][orgaName][u'devices'][urllib.quote_plus(chipName)] ]
							print "%s added as subdevice of %s" % (chipName,productName) 
							# Do not use HTTP reserved caracters in URL path !
							urlName = urllib.quote_plus(productName)
							root[u'organizations'][o][u'devices'][urlName] = a
						
						break
#							elif not productDeviceId in root[u'organizations'][o][u'devices'][productName]
							
			elif l[0] != None:
				print "%s non traitée" % (l[0])
			
	transaction.commit()
	
	importPciData.status = u"Import successfull"

from zope.component import provideHandler

provideHandler(updateZodbFromPciData)
