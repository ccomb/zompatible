# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.schema import Datetime, Text, Object, List, Choice, Field
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers

class IReportContainer(IContainer):
    u"""
    The container for reports
    the Support objet should act as a report container
    """
    contains("zompatible.report.interfaces.IReport")

class IReport(IContained):
    u"""
    The basic user report, which contains basic informations
    """
    containers(IReportContainer)
    date = Datetime(title=u'date/time', description=u'date/time of the report')
    comment = Text(title=u'comment about the report', description=u'comment of the support level')
    level = Field(u"a level") #this Field is really defined in subclasses
    #user = Object(title=u'user', description=u'user of this report', schema="zompatible.user.interfaces.IUser")

class IStabilityReport(IReport):
    u"""
    the stability of the soft-hard combination, as reported by the user
    """
    level = Choice(title=u'Stability Level', description=u'Stability Level', vocabulary="stability_levels")

class IEasinessReport(IReport):
    u"""
    the user report that tells whether making things (?) work was easy or not
    ("things" will probably be features)
    """
    level = Choice(title=u'Easiness', description=u'Easiness', vocabulary="easiness_levels")


# Error report management
class IErrorReport(IReport):
    u"""
    this report is about a specific object that implements IErrorReportable
    it allows to store the bad attribute and the new proposition for the attribute
    """
    badattribute = Attribute(u'the bad attribute') 
    proposition = Attribute(u'the replacement proposition')

class IErrorReportable(Interface):
    u"""
    each object should implement this in order for the users to report errors on it
    """
    reportederrors = List(title=u'reported errors', description=u'list of errors reported by the users', value_type=Object(IErrorReport, title=u'error', description=u'reported error'))



class IAction(Interface):
    u"""
    Peut-être à déplacer dans un module séparé
    """

class IActionsReport(IReport):
    u"""
    The actions the user made to make things work
    """
    actions = List(title=u"Actions", description=u"Actions to do to make things work", value_type=Object(title=u'error', description=u'reported error', schema=IAction))



