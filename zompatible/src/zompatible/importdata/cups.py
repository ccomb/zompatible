# -*- coding: utf-8 -*-
##======
## CUPS
##======
from zope.interface import implements
from zope.component.factory import Factory
from urllib import urlopen
from lxml import etree
from lxml.etree import ElementTree as ET

from interfaces import ICups, ICupsPrinter

class Printer(object):
    implements(ICupsPrinter)

    identity = manufacturer = model = compatibility = None
    recommended_driver = None
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

class Cups(object):
    implements(ICups)

    def __init__(self, in_printers_file=None):
        self.in_printers_file=in_printers_file

    def printers(self):
        ""

        if self.in_printers_file == None:
            # Normal use: we get data from the internet
            try:
                file = urlopen("http://openprinting.org/query.cgi?type=printers&moreinfo=1&format=xml")
            except IOError, detail:
                print "*** I/O error reading %s" % (detail)
                return
        else:
            # Test use case: we get data from a file
            file = self.in_printers_file

        
        try:
            doc = etree.parse(file)
        except etree.XMLSyntaxError, detail:
            print "*** XML file not well-formed: %s" % detail
            return
        except IOError, detail:
            print "*** I/O error reading '%s': %s" % (self.in_printers_file, detail)
            return

        p = Printer()

        for printer in doc.getiterator(tag="printer"):
            for elt in printer:
                if elt.tag == u"id":
                    p.identity = elt.text
                if elt.tag == u"make":
                    p.manufacturer = elt.text
                if elt.tag == u"model":
                    p.model = elt.text
                if elt.tag == u"functionality":
                    p.compatibility = elt.text
                if elt.tag == u"driver":
                    p.recommended_driver = elt.text
                if elt.tag == u"drivers":
                    p.drivers = [ drv.text for drv in elt if drv.tag == u"driver"]

            yield p
            


cups_import_factory = Factory(Cups)
