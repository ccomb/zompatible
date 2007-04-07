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


def getUrlString(s):
	"""
	"""
	if s:
		s=s.replace(u'/',u'-') 
		while  (len(s) >=1) and (s[0] in u'+@'):
			s = s[1:len(s)]
	return s

def addPciOrganization(name, id):
	""" Add the name and the pciid of an organisation to the ZODB.
	     If the oraganization does not exists, it is created and stored,
	     if it exists but still do not has this pciid, the organization data are updated,
	     if those data are already in the ZODB, it does nothing.
	"""
	root = getSite()
	urlName = getUrlString(name)
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

def addPciDevice(orga, name, id, subdevOrgaName=None, subdevId=None):
	root = getSite()
	
	# Check if a device already exists with the same id
	mainDev = None
	for dev in  root[u'organizations'][orga][u'devices']: 
		if root[u'organizations'][orga][u'devices'][dev].pciid == id:
			mainDev = root[u'organizations'][orga][u'devices'][dev]
			break
			
	# If a device already exists and if the new name of this device is not in the list, we add it 
	if mainDev:
		if not name in mainDev.names:
			mainDev.names.append(name)
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
		a.pciid = id
		a.subdevices = []
		# Do not use HTTP reserved caracters in URL path !
		root[u'organizations'][orga][u'devices'][urlName] = a
		mainDev = root[u'organizations'][orga][u'devices'][urlName]

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
		
		addPciOrganization(name, id)
			
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
				if orgaId == u'ffff':
					# We have reach the end of organizations (ffff stands for "Illegal Vendor ID"
					break
			# One tab => device
			elif l[0].count(u'\t') == 1:		
				chipName = l[1]
				chipId = l[0].replace(u'\t',u'').strip()
				addPciDevice(orgaName,chipName,chipId)
			# Two tabs => subsystem device
			elif l[0].count(u'\t') == 2:		
				productName = l[1]
				Ids = l[0].replace(u'\t',u'').strip().split(" ")
				productVendorId = Ids[0]
				productDeviceId = Ids[1]
				for o in root[u'organizations']:
					# If we find the organization from its id
					if productVendorId in root[u'organizations'][o].pciids:
						addPciDevice(o,productName,productDeviceId,orgaName,chipId)						
						break
							
			elif l[0] != None:
				print "%s non traitée" % (l[0])
			
	transaction.commit()
	
	importPciData.status = u"Import successfull"

from zope.component import provideHandler

provideHandler(updateZodbFromPciData)
