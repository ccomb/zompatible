# -*- coding: utf-8 -*-

from zope.interface import implements
from interfaces import IImport, IImportPciData
from persistent.list import PersistentList
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

def getUrlString(s):
	"""
	"""
	if s:
		s=s.replace(u'/',u'-') 
		while  (len(s) >=1) and (s[0] in u'+@'):
			s = s[1:len(s)]
	return s

statusAdded = 0
statusUpdated = 1
statusExist = 2

class Import(object):
	implements(IImport)
	pass
	
class ImportPciData(Import):
	implements(IImportPciData)

	data = u''
	status = u''

	def getOnlyInterestingData(self):
		l = self.data.split(u'# Syntax:')
		if len(l) >= 2:
			self.data = l[1]
		lignes = self.data.split("\n")
		# Get rid of empty lignes
		lignes = [ l for l in lignes if len(l)>0]
		# Get rid of comments (elements have at least one caracter)
		lignes = [ l for l in lignes if l[0]!='#']
		# split Id and description
		lignes = [ l.split("  ") for l in lignes]
		
		return lignes
	
	def addPciOrganization(self, name, id):
		""" Add the name and the pciid of an organisation to the ZODB.
	     	If the oraganization does not exists, it is created and stored,
	     	if it exists but still do not has this pciid, the organization data are updated,
	     	if those data are already in the ZODB, it does nothing.
		"""
		root = getSite()
		root = root[u'zompatible'] # TODO: remove it. Without this, it does not work any longer sine import is located in "++etc++site".
		# Check if the organisation already exists
		mainOrga = None
		
		# First, look for the same usb/pci ids
		# and look for the same name (in case the name was added by an other file) 		
		for orga in  root[u'organizations']: 
			if ((self.fileType == u'pciids' and id in root[u'organizations'][orga].pciids) or
				 (self.fileType == u'usbids' and id in root[u'organizations'][orga].usbids) or
				 name in root[u'organizations'][orga].names):
				mainOrga = root[u'organizations'][orga]
				break

		if mainOrga:
			status = statusExist
			if not name in mainOrga.names:
				mainOrga.names.append(name)
				status = statusUpdated
			if self.fileType == u'pciids' and not id in mainOrga.pciids:
				mainOrga.pciids.append(id)
				status = statusUpdated
			if self.fileType == u'usbids' and not id in mainOrga.usbids:
				mainOrga.usbids.append(id)
				status = statusUpdated

			return status
							
		# Otherwise, the organization does not exists, we add it
		else:
			urlName = getUrlString(name)
			toto = createObject(u"zompatible.Organization")
			toto.names = [ name ]
			if self.fileType == u'pciids':
				toto.pciids  = [ id ]
				toto.usbids = []
			elif self.fileType == u'usbids':
				toto.pciids  = []
				toto.usbids = [ id]
			toto.interfaces = [ IManufacturer ]
			alsoProvides(toto, IManufacturer)
			# Do not use HTTP reserved caracters in URL path !
			root[u'organizations'][urlName] = toto
			toto[u'devices'] = DeviceContainer()
			
			return statusAdded


	def addPciDevice(self, orga, name, id, subdevOrgaName=None, subdevId=None):
		root = getSite()
		root = root[u'zompatible'] # TODO: remove it. Without this, it does not work any longer sine import is located in "++etc++site".
		
		# Check if a device already exists with the same id
		mainDev = None
		for dev in  root[u'organizations'][orga][u'devices']: 
			if (self.fileType == u'pciids' and root[u'organizations'][orga][u'devices'][dev].pciid == id or
				  self.fileType == u'usbids' and root[u'organizations'][orga][u'devices'][dev].usbid == id):
				mainDev = root[u'organizations'][orga][u'devices'][dev]
				break
				
		# If a device already exists and if the new name of this device is not in the list, we add it 
		if mainDev:
			if not name in mainDev.names:
				mainDev.names.append(name)
				status = statusUpdated
			else:
				status = statusExist
			
		# Otherwise, the device does not exists, we add it
		else:
			urlName = urlName2 = getUrlString(name)
			i=0
			# This is needed as some devices has the same name, but not the same id !!!
			while urlName in root[u'organizations'][orga][u'devices']:
				urlName = u'%s_%d' % (urlName2,i)
				i = i + 1
				
			a = createObject(u"zompatible.Device")
			a.names = [ name ]
			if self.fileType == u'pciids':
				a.pciid = id
				a.usbid = u''
			if self.fileType == u'usbids':
				a.pciid = u''
				a.usbid = id
			a.subdevices = []
			# Do not use HTTP reserved caracters in URL path !
			root[u'organizations'][orga][u'devices'][urlName] = a
			mainDev = root[u'organizations'][orga][u'devices'][urlName]
			status = statusAdded
	
		# Subdevice part
		if not (not subdevOrgaName or not subdevId):
			# First, check if the subdevice is already in the subdevice list
			l = [ u'' for dev in mainDev.subdevices if subdevId == dev.pciid ]
			if len(l) == 0:
				# Then, we look for the subdevice object
				subdev=None
				for dev in root[u'organizations'][subdevOrgaName][u'devices']:
					if subdevId == root[u'organizations'][subdevOrgaName][u'devices'][dev].pciid:
						subdev=root[u'organizations'][subdevOrgaName][u'devices'][dev]
						break
						
				# Finaly, we add it to the list
				if subdev:
					mainDev.subdevices.append(subdev)

		return status
		
	def updateZodbFromPciData(self):
		self.fileType = u'pciids'
		self.updateZodbFromData()
		
	def updateZodbFromUsbData(self):
		self.fileType = u'usbids'
		self.updateZodbFromData()

	def updateZodbFromData(self):
		lignes = self.getOnlyInterestingData()

		# Then first we add the organisation and after the devices
		orgas = [ l for l in lignes if ( len(l)>=2 and
																	len(l[0])==4 and  
																	l[1]!=None)             ]
																	
		root = getSite()
		root = root[u'zompatible'] # TODO: remove it. Without this, it does not work any longer sine import is located in "++etc++site".
		nOrga = [ 0, 0, 0 ]
		for orga in orgas:
			name = orga[1]
			id = orga[0]
			
			nOrga[self.addPciOrganization(name, id)] += 1
		
		nDev = [ 0, 0, 0]
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
					orgaName = getUrlString(l[1])
					orgaId = l[0]
				# One tab => device
				elif l[0].count(u'\t') == 1:		
					chipName = l[1]
					chipId = l[0].replace(u'\t',u'').strip()
					nDev[self.addPciDevice(orgaName,chipName,chipId)] += 1
				# Two tabs => subsystem device
				elif l[0].count(u'\t') == 2:		
					productName = l[1]
					Ids = l[0].replace(u'\t',u'').strip().split(" ")
					productVendorId = Ids[0]
					productDeviceId = Ids[1]
					for o in root[u'organizations']:
						# If we find the organization from its id
						if productVendorId in root[u'organizations'][o].pciids:
							nDev[self.addPciDevice(o,productName,productDeviceId,orgaName,chipId)] += 1						
							break
								
				elif l[0] != None:
					print "%s non traitée" % (l[0])
				
		transaction.commit()
		
		self.status = u'Organizations:\n%d added,\n%d updated,\n%d not modified.\n' % (nOrga[statusAdded], nOrga[statusUpdated], nOrga[statusExist])
		self.status += u'Devices:\n%d added,\n%d updated,\n%d not modified.\n' % (nDev[statusAdded], nDev[statusUpdated], nDev[statusExist])
		if self.fileType == u'pci.ids':
			self.status += u'pci.ids: import successfull'				
		elif self.fileType == u'usbids':
			self.status += u'usb.ids: import successfull'				
		
from zope.component.factory import Factory

importPciDataFactory = Factory(
    ImportPciData,
    title=u"Create a new importPciData object",
    description = u"This factory instantiates new importPciDatas."
    )

@adapter(IImportPciData, IObjectModifiedEvent)
def updateZodbFromData(importPciData, event):
	if importPciData.data.find(u'http://pciids.sf.net/') >=0:
		importPciData.updateZodbFromPciData()
	elif importPciData.data.find(u'http://www.linux-usb.org/usb.ids') >=0:
		importPciData.updateZodbFromUsbData()
	else:
		importPciData.status = u'File format not recognized'
		


from zope.component import provideHandler

provideHandler(updateZodbFromData)
