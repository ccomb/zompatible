# -*- coding: utf-8 -*-
from zope.interface import Interface
import string
from zope.schema import TextLine, Text, Choice, Int

class IDeviceId(Interface):
   u""" This interface is used to describe pci and usb devices with data coming from 
   pci.ids and usb.ids files. 
   """ 
   def ishex(s):
      u""" Check if the string is in hexadecimal format
      """
      return s.strip(string.hexdigits) == ''

   _typeId = Choice(   title=u'Interface type',
                                 description = u'Interface type',
                                 values=[u'pci', u'usb'],
                                 required = True
                              )
                                         
   _vendorId = TextLine(   title=u'Vendor Id',
                                       description=u'Vendor Id identifier',
                                       constraint = ishex,
                                       required = True,
                                       min_length=0,
                                       max_length=4
                                   )
   _vendorIdNb = Int(   title=u'Vendor Id number',
                                   description=u'Vendor Id identifier',
                                   required = False,
                                   readonly = True
                                   )
   _productId = TextLine(   title=u'Product Id',
                                        description=u'Products Id identifier',
                                        constraint = ishex,
                                        required = True,
                                        min_length=0,
                                        max_length=4
                                     )
   _productIdNb = Int(   title=u'Product Id Number',
                                        description=u'Products Id identifier',
                                        required = False,
                                        readonly = True
                                     )
   _description = Text(  title=u'Description',
                                    description=u'Original description',
                                    required=False
                               )
                               
class IPciDeviceId(IDeviceId):
   pass
   
class IUsbDeviceId(IDeviceId):
   pass
   
   
   
