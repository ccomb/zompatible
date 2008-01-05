# -*- coding: utf-8 -*-
from zope.viewlet.interfaces import IViewletManager
from zope.publisher.interfaces.browser import IBrowserView

class IToolboxManager(IViewletManager):
    u"""
    The viewlet manager for a side toolbox
    """


class IPrettyName(IBrowserView):
    u"""
    The view provided by any object that wants to be displayed with a pretty name
    """
