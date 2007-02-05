




class IReport(Interface):
  date = Datetime(title=u'date/time', description=u'date/time of the report')
  comment = Text(title=u'comment about the report', description=u'comment of the support level')



class IStabilityReport(IReport):
  stability = Object(title=u'stability level', description=u'level of stability', schema=ILevel)






class IErrorReport(IReport):
  u"""
  this report is about a specific object that implements IErrorReportable
  it allows to store the bad attribute and the proposition
  """
  badattribute = Attribute(u'the bad attribute') 
  proposition = Attribute(u'the replacement proposition')

class IErrorReportable(Interface):
  u"""
  each object should implement this in order for the users to report errors on it
  """
  reportederrors = List(title=u'reported errors', description=u'list of errors reported by the users', value_type=Object(title=u'error', description=u'reported error', schema=IErrorReport))



class IDeviceExperienceReport(IReport):
  u"""
  le rapport d'un utilisateur à propos de l'utilisation d'un matériel sur une distro
  What is your experience?
  """
  operatingsystem = Object(title=u'Operating System', description=u'supported operating system', schema=IOperatingSystem)
  support = Object(title=u'support level', description=u'the support level according to the user', schema=ILevel)
  seeninaction = Bool(title=u'personaly seen', description=u'the user has personaly seen the device work')
  actions = List(title=u'actions to do to make the device work', description=u'list of actions', value_type=Object(title=u'action', description=u'action', schema=IAction))
