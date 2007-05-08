# -*- coding: utf-8 -*-

from zope.interface import implements
from interfaces import IImport, IImportData
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.component.hooks import getSite

from zompatible.organization.interfaces import IManufacturer, IOrganizationInterfaces
from zompatible.organization.organization import OrganizationNameChooser, Organization
from zompatible.device.device import DeviceNameChooser, Device
from zompatible.ids.interfaces import IPciDeviceId, IUsbDeviceId

from interfaces import *


statusAdded = 0
statusUpdated = 1
statusExist = 2
statusDeleted = 3

class Import(object):
   implements(IImport)
   pass
   
class ImportData(Import):
   implements(IImportData)

   data = u''
   status = u''

   def getOnlyInterestingData(self):
      l = self.data.split(u'# Syntax:')
      if len(l) >= 2:
         self.data = l[1]
      lignes = self.data.split("\n")
      # Get rid of empty lignes
      lignes = ( l for l in lignes if len(l)>0 )
      # Get rid of comments (elements have at least one caracter)
      lignes = ( l for l in lignes if l[0]!='#' )
      # split Id and description
      lignes = [ l.split("  ") for l in lignes ]
      
      return lignes
   
   def addOrganization(self, name, id):
      """ Add the name and the pciid of an organisation to the ZODB.
           If the oraganization does not exists, it is created and stored,
           if it exists but still do not has this pciid, the organization data are updated,
           if those data are already in the ZODB, it does nothing.
      """
      organizations = getSite()[u'organizations']
      # Check if the organisation already exists
      mainOrga = None

      # First, look for the same usb/pci ids
      # and look for the same name (in case the name was added by an other file)       
      for orga in organizations:
         if ((self.fileType == u'pciids' and id in organizations[orga].pciids) or
             (self.fileType == u'usbids' and id in organizations[orga].usbids) or
             name in organizations[orga].names):
            mainOrga = organizations[orga]
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
         toto = Organization()
         toto.names = [ name ]
         urlName2 = urlName = OrganizationNameChooser(None).chooseName(u"",toto)
         i=0
         while urlName in organizations:
            urlName = u'%s_%d' % (urlName2,i)
            i = i + 1
         if self.fileType == u'pciids':
            toto.pciids  = [ id ]
            toto.usbids = []
         elif self.fileType == u'usbids':
            toto.pciids  = []
            toto.usbids = [ id]
         organizations[urlName] = toto
         IOrganizationInterfaces(toto).interfaces += [ IManufacturer ]
         
         return statusAdded


   def addDevice(self, orga, orgaId, name, id, subdevOrgaName=None, subdevId=None):
      organizations = getSite()[u'organizations']
      
      #Find the ORGA folder FIRST !
      for o in organizations:
         if orga in organizations[o].names:
            orga = o
            break;
      
      IOrganizationInterfaces(organizations[orga]).interfaces += [ IManufacturer ]
      
      # Check if a device already exists with the same id
      mainDev = None
      for dev in  organizations[orga][u'devices']:
         if (self.fileType == u'pciids' and organizations[orga][u'devices'][dev].pciid == id or
              self.fileType == u'usbids' and organizations[orga][u'devices'][dev].usbid == id):
            mainDev = organizations[orga][u'devices'][dev]
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
         a = Device()
         a.names = [ name ]
         urlName = urlName2 = DeviceNameChooser(None).chooseName(u"",a)
         i=0
         # This is needed as some devices has the same name, but not the same id !!!
         while urlName in organizations[orga][u'devices']:
            urlName = u'%s_%d' % (urlName2,i)
            i = i + 1
         if self.fileType == u'pciids':
            a.pciid = id
            a.usbid = u''
            IPciDeviceId(a)._description = name
            IPciDeviceId(a)._vendorId = orgaId
            IPciDeviceId(a)._productId = id
         if self.fileType == u'usbids':
            a.pciid = u''
            a.usbid = id
            IUsbDeviceId(a)._description = name
            IUsbDeviceId(a)._vendorId = orgaId
            IUsbDeviceId(a)._productId = id
         a.subdevices = []
         organizations[orga][u'devices'][urlName] = a
         mainDev = organizations[orga][u'devices'][urlName]
         status = statusAdded
   
      # Subdevice part
      if not (not subdevOrgaName or not subdevId):
         # First, check if the subdevice is already in the subdevice list
         l = [ u'' for dev in mainDev.subdevices if subdevId == dev.pciid ]
         if len(l) == 0:
            # Then, we look for the subdevice object
            subdev=None
            for o in organizations:
               if subdevOrgaName in organizations[o].names:
                  for dev in organizations[o][u'devices']:
                     if subdevId == organizations[o][u'devices'][dev].pciid:
                        subdev=organizations[o][u'devices'][dev]
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
      orgas = ( l for l in lignes if len(l)>=2 and len(l[0])==4 and l[1]!=None )
                                                   
      organizations = getSite()[u'organizations']
      nOrga = [ 0, 0, 0, 0 ]
      for orga in orgas:
         name = orga[1]
         id = orga[0]
         nOrga[self.addOrganization(name, id)] += 1

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
               orgaName = OrganizationNameChooser(None).chooseName(l[1],None)
               orgaId = l[0]
            # One tab => device
            elif l[0].count(u'\t') == 1:      
               chipName = l[1]
               chipId = l[0].replace(u'\t',u'').strip()
               nDev[self.addDevice(orgaName, orgaId, chipName, chipId)] += 1
            # Two tabs => subsystem device
            elif l[0].count(u'\t') == 2:      
               productName = l[1]
               Ids = l[0].replace(u'\t',u'').strip().split(" ")
               productVendorId = Ids[0]
               productDeviceId = Ids[1]
               for o in organizations:
                  # If we find the organization from its id
                  if productVendorId in organizations[o].pciids:
                     nDev[self.addDevice(o, productVendorId, productName, productDeviceId, orgaName, chipId)] += 1                  
                     break
                        
            elif l[0] != None:
               print "%s non traitée" % (l[0])
               
      # Delete empty organizations (work on a copy of the keys because of btree behaviour when deleting on looping)
      for o in [ h for h in organizations.keys()]:
          if ('devices' not in organizations[o] or len(organizations[o]['devices']) == 0) and ('software' not in organizations[o] or len(organizations[o]['software']) == 0 ):
              del organizations[o]
              nOrga[statusDeleted]+=1

      self.status = u'Organizations:\n%d added,\n%d updated,\n%d not modified.\n%d deleted (without device)\n' % (nOrga[statusAdded], nOrga[statusUpdated], nOrga[statusExist], nOrga[statusDeleted])
      self.status += u'Devices:\n%d added,\n%d updated,\n%d not modified.\n' % (nDev[statusAdded], nDev[statusUpdated], nDev[statusExist])
      if self.fileType == u'pci.ids':
         self.status += u'pci.ids: import successfull'            
      elif self.fileType == u'usbids':
         self.status += u'usb.ids: import successfull'            
      
from zope.component.factory import Factory

importDataFactory = Factory(
    ImportData,
    title=u"Create a new importData object",
    description = u"This factory instantiates new importDatas."
    )

@adapter(IImportData, IObjectModifiedEvent)
def updateZodbFromData(importData, event):
   if importData.data.find(u'http://pciids.sf.net/') >=0:
      importData.updateZodbFromPciData()
   elif importData.data.find(u'http://www.linux-usb.org/usb.ids') >=0:
      importData.updateZodbFromUsbData()
   else:
      importData.status = u'File format not recognized'

from zope.component import provideHandler

provideHandler(updateZodbFromData)


class ImportFile(object):
    implements(IImportFile)
    infile = u""
    def __init__(self, infile=u""):
        self.infile = infile
    def do_import(self):
        u"this method must be implemented by the subclass"
        raise NotImplementedError

