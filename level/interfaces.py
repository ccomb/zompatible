





class ILevel(Interface):
  u"""
  must be implemented by support, trust and stability levels
  """
  level = Int(title=u'support level', description=u'support level for this OS')
  description = Text(title=u'support level description', description=u'description of the support level')

