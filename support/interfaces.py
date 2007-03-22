from zope.interface import Interface, Attribute
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers


class ISupport(IContainer, IContained):
    u"""
    objet qui fait le lien entre un Device et un Software.
    Il pointe vers un Device et un Software,
    et contient des UserReports (en tant que Container)
    """
    containers('zompatible.support.interfaces.ISupportContainer')
    device = Attribute("The device we're speaking about")
    software = Attribute("Software we're speaking about")
    


class ISupportContainer(IContainer, IContained):
    u"""
    Le conteneur qui stocke les objets Support
    """
    contains(ISupport)



class IOsSupport(Interface):
  u"""
  
    Ancienne interface issue d'une réflexion précédente.  
  
  objet qui fait le lien entre un OS et un matériel
  this is the high level object to display in the support page
  supportlevel is an average computed from supportreports and other objects
  OsSupport est question de présence d'un pilote ou pas, et de l'intégration, et des rapports des gens
  Cet objet est le coeur du site !
  Normalement cet objet est inutile, mais il devrait servir de cache pour éviter de recalculer l'OsSupportLevel à chaque visite.
  Il doit donc être recalculé automatiquement grâce à un subscriber lors de l'ajout d'un userreport.
  Néanmoins, on va essayer de faire sans au début.
  """
  #operatingsystem = Object(title=u'Operating System', description=u'supported operating system', schema=IOperatingSystem)
  #supportlevel = Object(title=u'support level', description=u'the average of user repots', schema=ILevel)
  #supportreports = List(title=u'user reports', description=u'list of user reports', value_type=Object(title=u'user report', description=u'user report', schema=IReport))
