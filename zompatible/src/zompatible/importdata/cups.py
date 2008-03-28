# -*- coding: utf-8 -*-
##======
## CUPS
##======
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component.factory import Factory
from urllib import urlopen
from lxml import etree
from lxml.etree import ElementTree as ET

from interfaces import ICups, ICupsPrinter, ICupsManufacturer

_CUPS_PRINTERS_REQUEST="http://openprinting.org/query.cgi?type=printers&moreinfo=1&format=xml"
_CUPS_MANUFACTURERS_REQUEST="http://openprinting.org/query.cgi?type=manufacturers&format=xml"

class Printer(object):
    implements(ICupsPrinter)

    identity = FieldProperty(ICupsPrinter['identity'])
    manufacturer = FieldProperty(ICupsPrinter['manufacturer'])
    model = FieldProperty(ICupsPrinter['model'])
    compatibility = FieldProperty(ICupsPrinter['compatibility'])
    recommended_driver = FieldProperty(ICupsPrinter['recommended_driver'])
    drivers = FieldProperty(ICupsPrinter['drivers'])

    def __init(self):
        identity = manufacturer = model = compatibility = u""
        recommended_driver = u""
        drivers = {}

    def __str__(self):
        txt = u"id:%s, manuf:%s, model:%s, comp:%s,\
recomm driver:%s\n" % (self.identity,
                    self.manufacturer,
                    self.model,
                    self.compatibility,
                    self.recommended_driver)
        txt += u"Driver list:"
        for drv in self.drivers:
            txt += u"\n" + drv 
        return txt

class Manufacturer(object):
    implements(ICupsManufacturer)

    name = FieldProperty(ICupsManufacturer['name'])

class Cups(object):
    implements(ICups)

    def __init__(self,
                 in_printers_file=None,
                 in_manufacturers_file=None):
        self.in_printers_file = in_printers_file
        self.in_manufacturers_file = in_manufacturers_file

    def _getDocXml(self, url, sample_file):
        """
        Returns the element tree representing the *sample_file* XML file if
        it is not None. Otherwise the XML file will be retreived from the url
        provided and returned as an element tree.
        """
        if sample_file == None:
            # Normal use: we get data from the internet
            try:
                ifile = urlopen(url)
            except IOError, detail:
                print "*** I/O error reading %s" % (detail)
                return None
        else:
            # Test use case: we get data from a file
            ifile = sample_file

        
        try:
            doc = etree.parse(ifile)
        except etree.XMLSyntaxError, detail:
            print "*** XML file not well-formed: %s" % detail
            return None
        except IOError, detail:
            print "*** I/O error reading '%s': %s" % (ifile, detail)
            return None

        return doc
        
    
    def printers(self):
        ""
        doc = self._getDocXml(_CUPS_PRINTERS_REQUEST, self.in_printers_file)

        p = Printer()

        for printer in doc.getiterator(tag="printer"):
            for elt in printer:
                if elt.tag == u"id":
                    p.identity = unicode(elt.text)
                if elt.tag == u"make":
                    p.manufacturer = unicode(elt.text)
                if elt.tag == u"model":
                    p.model = unicode(elt.text)
                if elt.tag == u"functionality":
                    p.compatibility = unicode(elt.text)
                if elt.tag == u"driver":
                    p.recommended_driver = unicode(elt.text)
                if elt.tag == u"drivers":
                    p.drivers = [ unicode(drv.text) for drv in elt if drv.tag == u"driver"]

            yield p

    def manufacturers(self):
        doc = self._getDocXml(_CUPS_MANUFACTURERS_REQUEST,
                              self.in_manufacturers_file)

        manufacturer = Manufacturer()
        
        for manuf in doc.getiterator(tag="make"):
            manufacturer.name = unicode(manuf.text)
            yield manufacturer

    def drivers(self):
        u"Not yet implemented"
        return

        
cups_import_factory = Factory(Cups)
