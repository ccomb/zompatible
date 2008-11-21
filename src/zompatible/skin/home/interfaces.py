# -*- coding: utf-8 -*-
from zope.viewlet.interfaces import IViewletManager

class IMainAreaManager(IViewletManager):
    u"""
    This is the viewlet manager for the central area in the homepage.
    It should at least contain the main search viewlet
    """
