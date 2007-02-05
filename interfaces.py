# -*- coding: utf-8 -*-
from zope.interface.interfaces import Interface
from zope.schema import TextLine, Object, List, Text, Int


# définir une interface IVersionned pour dire qu'un truc est versionné ?








class IOsSupport(Interface):
  u"""
  objet qui fait le lien entre un OS et un matériel
  this is the high level object to display in the support page
  supportlevel is an average computed from supportreports and other objects
  OsSupport est question de présence d'un pilote ou pas, et de l'intégration, et des rapports des gens
  Cet objet est le coeur du site !
  Normalement cet objet est inutile, mais il devrait servir de cache pour éviter de recalculer l'OsSupportLevel à chaque visite.
  Il doit donc être recalculé automatiquement grâce à un subscriber lors de l'ajout d'un userreport.
  Néanmoins, on va essayer de faire sans au début.
  """
  operatingsystem = Object(title=u'Operating System', description=u'supported operating system', schema=IOperatingSystem)
  supportlevel = Object(title=u'support level', description=u'the average of user repots', schema=ILevel)
  supportreports = List(title=u'user reports', description=u'list of user reports', value_type=Object(title=u'user report', description=u'user report', schema=IReport))



class IAction(Interface):
  type = Object(title=u'action', description=u'the action to do', schema=ICategory)
  title = TextLine(title=u'action type', description=u'the type of action')


