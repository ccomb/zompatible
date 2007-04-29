# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component import adapts
from zope.component import provideAdapter

from zompatible.ids.interfaces import  IDeviceId, IPciDeviceId, IUsbDeviceId
from zompatible.device.interfaces import IDevice

class DeviceIdAbstract(object):
  
   def __init__(self, context):
      self.context = context
      attributeList = [e for e in dir(self.context) if not callable(getattr(self.context, e))]
      if not '_typeId' in attributeList:
         self.context._typeId = u''
      if not '_vendorId' in attributeList:
         self.context._vendorId = u''
      if not '_vendorIdNb' in attributeList:
         self.context._vendorIdNb = 0
      if not '_productId' in attributeList:
         self.context._productId = u''
      if not '_productIdNb' in attributeList:
         self.context._productIdNb = 0
      if not '_description' in attributeList:
         self.context._description = u''

   def __setattr__(self, key, value):
      if key == '_typeId':
         self.context._typeId = value
      if key == '_productId':
         self.context._productId = value
         self.context._productIdNb = int(value, 16)
      if key == '_vendorId':
         self.context._vendorId = value
         self.context._vendorIdNb = int(value, 16)
      if key == '_description':
         self.context._description = value
         
      object.__setattr__(self, key, value)

   def __getattr__(self, key):
      # TODO AttributeError: type object 'object' has no attribute '__getattr__' !!!
      # So it does not work... but is it necessary ?
      if key == '_typeId':
         return self.context._typeId
      if key == '_productId':
         return self.context._productId
      if key == '_productIdNb':
         return self.context._productIdNb
      if key == '_vendorId':
         return self.context._vendorId
      if key == '_vendorIdNb':
         return self.context._vendorIdNb
      if key == '_description':
         return self.context._description
      
      return object.__getattr__(self, key)

class DeviceId(DeviceIdAbstract):
   u""" Adapter to be able to add IDeviceId interface to a device
   WARNING: Using this adapter does not  update _productIdNb and _vendorIdNb as
   expected when setting _productId and _vendorId whereas PciDeviceId and 
   UsbDeviceId does. ????!!!!
   """
   implements(IDeviceId)
   adapts(IDevice)
   def __init__(self,context):
      self.context=context
      DeviceIdAbstract.__init__(self,context)

class PciDeviceId(DeviceIdAbstract):
   u""" Adapter to be able to add IPciDeviceId interface to a device 
   """
   implements(IPciDeviceId)
   adapts(IDevice)
   def __init__(self,context):
      self.context=context
      # First we create the attributes,
      DeviceIdAbstract.__init__(self,context)
      # then we update data
      self.context._typeId = u'pci'
      
class UsbDeviceId(DeviceIdAbstract):
   u""" Adapter to be able to add IUsbDeviceId interface to a device 
   """
   implements(IUsbDeviceId)
   adapts(IDevice)
   def __init__(self,context):
      self.context=context
      # First we create the attributes,
      DeviceIdAbstract.__init__(self,context)
      # then we update data
      self.context._typeId = u'usb'
 
      