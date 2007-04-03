# -*- coding: utf-8 -*-
from zope.app.folder import Folder
from zope.interface import implements
from interfaces import *

class ReportContainer(Folder):
    implements(IReportContainer)
    __name__=__parent__=None

class Report(object):
    u"""
    The implementation of a user report
    """
    date = comment =__parent__ = __name__ = None

class EasinessReport(Report):
    implements(IEasinessReport)
    easiness = None

class StabilityReport(Report):
    implements(IStabilityReport)
    stability = None
