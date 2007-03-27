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
    implements(IReport, IStabilityReport, IEasinessReport, IActionsReport)
    date = comment = stability = easiness = actions = None