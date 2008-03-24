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
            # Normal use: we get data from the internet
            feed = urlopen("http://openprinting.org/query.cgi?type=printers&moreinfo=1&format=xml")
            tree = etree.parse(feed)
        else:
            # Test use case: we get data from a file
            doc = ET(self.infile)
        
        p.identity = u"Alps-MD-1000"
        p.manufacturer = u"Alps"
        p.model = u"MD-1000"
        p.compatibility = u"A"
        p.recommended_driver = u"ppmtomd"
        p.drivers = [ u"md2k",
                      u"ppmtocpva" ]

        while (1):
            yield p


cups_import_factory = Factory(Cups)
