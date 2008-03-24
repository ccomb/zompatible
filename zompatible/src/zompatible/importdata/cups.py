# -*- coding: utf-8 -*-
##======
## CUPS
##======
from zope.interface import implements
from zope.component.factory import Factory

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

    def printers(self):
        u""
        p = Printer()


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
