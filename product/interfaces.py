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

    subProducts = List(
                    title = u"Sub products",
                    description = u"Sub products describing specific categories",
                    required = False
                    )