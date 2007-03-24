# -*- coding: utf-8 -*-



class UserReport(IReport, IStabilityReport, IEasinessReport, IActionsReport):
    u"""
    The implementation of a user report
    """
    date = comment = stability = easiness = actions = None