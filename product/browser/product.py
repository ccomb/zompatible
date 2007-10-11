from zope.publisher.browser import BrowserPage
from zope.formlib.form import EditForm, Fields
from zope.app.pagetemplate import ViewPageTemplateFile

from zompatible.product.interfaces import IProduct

class ProductView(BrowserPage):
    u""" Product view for a browser.
    """
    label="Product view"
    __call__=ViewPageTemplateFile("product.pt")


class ProductEditForm(EditForm):
    u""" Allows a product edition.
    """
    form_fields = Fields(IProduct).omit('categories') # omit categories because no value type is defined yet.
    label = u"Edit Product"
    
