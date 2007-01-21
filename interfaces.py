# -*- coding: utf-8 -*-
from zope.interface.interfaces import Interface, Attribute
from zope.schema import TextLine, Bool, Object, URI, Datetime, List, Text, Int
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.component.interface import provideInterface
from manufacturer.interfaces import IManufacturer
from device.interfaces import IDevice


# définir une interface IVersionned pour dire qu'un truc est versionné ?


class IArchitecture(Interface):
  u"pour logiciel ou matériel ??"
  names = List(title=u'names', description=u'possible names of the architecture', value_type=TextLine(title=u'name', description=u'possible name'))



class ILevel(Interface):
  u"""
  must be implemented by support, trust and stability levels
  """
  level = Int(title=u'support level', description=u'support level for this OS')
  description = Text(title=u'support level description', description=u'description of the support level')





class IOsSupport(Interface):
  u"""
  objet qui fait le lien entre un OS et un matériel
  this is the high level object to display in the support page
  supportlevel is an average computed from supportreports and other objects
  OsSupport est question de présence d'un pilote ou pas, et de l'intégration, et des rapports des gens
  Cet objet est le coeur du site !
  """
  operatingsystem = Object(title=u'Operating System', description=u'supported operating system', schema=IOperatingSystem)
  supportlevel = Object(title=u'support level', description=u'the average of user repots', schema=ILevel)
  supportreports = List(title=u'user reports', description=u'list of user reports', value_type=Object(title=u'user report', description=u'user report', schema=IReport))

class ICategory(Interface):
  u"""
  permettra de définir (implémenter sous forme d'objet) une catégorie de matériel, ou de logiciel, d'action, etc.
  Une catégorie de matériel (une instance) peut être : laptop (ou portable), serveur, etc...
  Une catégorie d'action peut être : installation, configuration, démarrage d'un programme, 
  """
  names = List(title=u'names', description=u'possible names of the category', value_type=TextLine(title=u'name', description=u'a category'))
  description = Text(title=u'category description', description=u'description of the category')
  #interface = the interface the category applies to

class IAction(Interface):
  type = Object(title=u'action', description=u'the action to do', schema=ICategory)
  title = TextLine(title=u'action type', description=u'the type of action')


