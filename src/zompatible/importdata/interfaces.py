# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.schema import Text, TextLine, List, URI
from zope.app.container.constraints import containers
from zope.app.component.interfaces import ILocalSiteManager


class IImport(Interface):
	"""Import information to fill the data base
	This interface could provide: date of the last import, ...
	"""
	pass

class IImportData(IImport):
	"""Import data as they are formated in pci.ids files.
	"""
	containers(ILocalSiteManager)
	data = Text(
		title=u"pci.ids file content",
		description=u"Holds the data to analyse, coming from a pci.ids file.",
		required=True)

	status = Text(
		title=u"Status",
		description=u"Report status of the last import",
		required=False,
		readonly=True
		)

	def updateZodbFromPciData(self):
		""" Import data from pci.ids file format
		"""
		
	def updateZodbFromUsbData(self):
		""" Import data from usb.ids file format
		"""

class IImportFile(Interface):
    """
    interface of a file import utility.
    The file may come from the local filesystem (→ use filename attribute)
    or from an upload (→ use the fileupload attribute)
    """
    filename = Attribute(u"the filename from which to import")
    fileupload = Attribute(u"the FileUpload object from which to read")
    def importfile():
        u"perform the import"

class ICupsPrinter(Interface):
    """
    Describes a printer with data provided by CUPS web site API.
    """
    identity  = TextLine(
		title=u"Printer ID",
		description=u"""Full printer name (manufacturer name followed
		by the printer model name)""",
		required=True,
		)
    manufacturer  = TextLine(
		title=u"Manufacturer",
		description=u"Printer manufacturer name",
		required=True,
		)
    model  = TextLine(
		title=u"Model",
		description=u"Printer model name",
		required=True,
		)
    compatibility = TextLine(
		title=u"Compatibility",
		description=u"Printer compatibility level",
		required=True,
		)
    recommended_driver = TextLine(
		title=u"Recommended driver",
		description=u"Recommended printer driver to use with CUPS",
		required=False,
		)
    drivers = List(
                title=u"Drivers",
                description=u"""List other drivers that can make the printer
                work""",
		required=False,
                value_type=TextLine(
                            title=u"Driver",
                            description=u"Driver name")
                )
    

class ICupsManufacturer(Interface):
    """
    Describes a manufacturer with data provided by CUPS web site API.
    """
    name  = TextLine(
    		title=u"Name",
		description=u"Printer manufacturer name",
		required=True,
		)

class ICups(Interface):
    """
    This interface allows a simple access to data provided by CUPS
    *openprinting* web site API.
    """
    def manufacturers():
        "Iterator on printer manufacturers."
        
    def printers():
        """Iterator on printers. Returns an object providing ICupsPrinter
        interface."""
        
    def drivers():
        "Iterator on drivers."
        
class IIcecatSuppliers(Interface):
    """
    Describe a Icecat supplier (organization).
    """
    name  = TextLine(
    		title=u"Name",
		description=u"Supplier name",
		readonly=True
		)
    logo_url = URI(
    		title=u"Logo",
		description=u"Supplier's logo url",
		readonly=True
		)
    ID = TextLine(
    		title=u"ID",
		description=u"Supplier ID",
		readonly=True
		)
        
    
    
    
class IIcecatProduct(Interface):
    """
    Decribes products data from Icecat.
    date,
    category (nom ou ID ?),
    supplier name,
    name,
    image_url,
    description,
    features = (name,
                value,
                measure (unit) (+ description ?),
                "intérêt porté à cette fonctionnalité par les utilisateurs",
                description,
                ID
                ),
    feature_groups[features] = (name,
                                feautures_list,
                                ID
                                )
    """
    

class IIceCat(Interface):
    """
    This interface allows a simple access to data provided by ICECAT
    xml data.
    """
    def setFilters():
        """
        Set filters on IceCat data. Influences iterators output. Date, Category,
        product name.
        """
        
    def products():
        "Iterator on products."

