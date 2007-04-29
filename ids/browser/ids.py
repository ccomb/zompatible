from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile

class DeviceIdsView(BrowserPage):
   u""" The view used to display device ids (pci or usb)
   """
   label=u"Data coming from pci.ids or usb.ids file"
   __call__=ViewPageTemplateFile("deviceids.pt")

	