# -*- coding: utf-8 -*-
from zope.publisher.interfaces.browser import IDefaultBrowserLayer, IBrowserView

class IZompatibleSkin(IDefaultBrowserLayer):
  """
  the main skin of the application
  We cannot provide IBrowserSkinType here because this interface must be registered with a name (the name of the skin)
  So it is registered for IBrowserSkinType in ZCML.
  This skin is activated by default with overrides zcml
  """

class IPrettyName(IBrowserView):
    u"""
    The view provided by any object that wants to be displayed with a pretty name
    """
