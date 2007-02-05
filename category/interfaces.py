from zope.interface import Interface




class ICategorizable(Interface):
    u"""
    l'interface marqueur à poser (par ZCML) sur les objets à catégoriser
    """


class ICategory(Interface):
  u"""
  permettra de définir (implémenter sous forme d'objet) une catégorie de matériel, ou de logiciel, d'action, etc.
  Une catégorie de matériel (une instance) peut être : laptop (ou portable), serveur, etc...
  Une catégorie d'action peut être : installation, configuration, démarrage d'un programme, 
  """
  names = List(title=u'names', description=u'possible names of the category', value_type=TextLine(title=u'name', description=u'a category'))
  description = Text(title=u'category description', description=u'description of the category')



    
class ICategories(Interface):
    u"""
    L'interface par laquelle on accède aux catégories des objets.
    """
    categories = List(title=u'categories', description=u'list of categories', value_type=Choice(title=u'category', vocabulary="mycategories"))





