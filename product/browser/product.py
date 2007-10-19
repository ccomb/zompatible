from zope.publisher.browser import BrowserPage
from zope.formlib.form import EditForm, Fields
from zope.formlib import form
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.form.browser.itemswidgets import MultiCheckBoxWidget
from zope.component.interface import queryInterface
from zope.schema import TextLine

from zompatible.product.interfaces import IProduct
from zompatible.characteristic.interfaces import *

class ProductView(BrowserPage):
    u""" Product view for a browser.
    """
    label="Product view"
    __call__=ViewPageTemplateFile("product.pt")

    def __init__(self, context, request):
        self.context, self.request = context, request
        self.char = []
        for e in ICharacteristicManager(self.context).CurrentList():
            iface = queryInterface(e)
            s = str(iface(self.context))
            if s != u'':
                self.char.append(str(iface(self.context)))

class ProductEditForm(EditForm):
    u""" Allows a product edition.
    """
    form_fields = Fields(IProduct).omit('categories') # omit categories because no value type is defined yet.
    label = u"Edit Product"
    
    def __init__(self, context, request):
        self.context, self.request = context, request
        print list(self.form_fields)
        
