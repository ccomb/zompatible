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
        txt += u"Driver list:\n"
        for drv in self.drivers:
            txt += drv + u"\n"
        return txt

class Cups(object):
    implements(ICups)

    def __init__(self, infile=None):
        self.infile=infile

    def printers(self):
        u""
        p = Printer()

        if self.infile == None:
            #print "uploading file"
            # Normal use: we get data from the internet
            try:
                feed = urlopen("http://openprinting.org/query.cgi?type=printers&moreinfo=1&format=xml")
            except IOError, detail:
                print "*** I/O error reading %s" % (detail)
                yield None
                
            doc = etree.parse(feed)
        else:
            #print "loading file % s " % self.infile
            # Test use case: we get data from a file
            try:
                doc = etree.ElementTree ( file=self.infile )
            except etree.XMLSyntaxError, detail:
                print "*** XML file not well-formed: %s" % detail
                yield None
            except IOError, detail:
                print "*** I/O error reading '%s': %s" % (self.infile, detail)
                yield None

            doc = etree.parse(self.infile)

#        for printer in doc.getiterator(tag="Printer"):
#            for elt in cat:
#                if elt.tag == "id":
#                    p.identity = elt.text
            p.identity=u"Alps-MD-1000"        
            p.manufacturer = u"Alps"
            p.model = u"MD-1000"
            p.compatibility = u"A"
            p.recommended_driver = u"ppmtomd"
            p.drivers = [ u"md2k",
                      u"ppmtocpva" ]

            while 1:
                yield p


cups_import_factory = Factory(Cups)
