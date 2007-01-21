








class IUser(Interface):
  firstname = TextLine(title=u'first name', description=u'your first name')
  lastname = TextLine(title=u'last name', description=u'your last name')
  email = TextLine(title=u'e-mail', description=u'your e-mail')
  reports = List(title=u'informations', description=u'list of provided information', value_type=Object(title=u'information', description=u'an information', schema=IReport))
