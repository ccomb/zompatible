# -*- coding: utf-8 -*-
from zope.viewlet.interfaces import IViewlet
from zope.viewlet.manager import ViewletManagerBase
from zope.interface import implements

from interfaces import *

class AdminAreaManager(ViewletManagerBase):
    u"The viewlet manager for the adminarea"
    ordre = ['adminheader', 'login', 'adminmenu' ]
    implements(IAdminAreaManager)
    def sort(self, viewlets):
        viewlets = dict(viewlets)
        return [(name, viewlets[name]) for name in self.ordre if name in viewlets]

class AdminHeaderViewlet(object):
    u"""
    The viewlet that displays the title of the admin area
    No template here, we do a real implementation od IViewlet just to test.
    """
    implements(IViewlet)
    def update(self):
        pass
    def render(self):
        u"""
        Here we could use a template by calling ViewPageTemplateFile
        We actually just return bare HTML (in utf-8)
        """
        return u'<div id="admin_header">Zone admin</div>'

