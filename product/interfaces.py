from zope.schema import TextLine, List
from zope.interface import Interface


class IProduct(Interface):
    """
    """
    name = TextLine (
                    title = u"Name",
                    description = u"Name of the product",
                    required = True
                    )

    """ Sould it be a list or only one category ? (As the product should contain
         sub products describing each category)
    """ 
    Categories = List(
                      title = u"Categories",
                      description = u"List of categories the product belongs to",
                      required = False
                      )