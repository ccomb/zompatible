# -*- coding: utf-8 -*-
from interfaces import *
from persistent import Persistent  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder
from zope.interface import implements


class SupportLevel(Persistent):
  """
  green :
  1 = works without doing anything
  2 = works by just declaring the new device
  3 = works by starting some program
  4 = works after adding a few integrated packages
  5 = works after adding third party packages
  orange :
  3 = need additional work
  6 = works after installing a driver
  7 = works after compiling and installing a driver
  8 = works after patching, compiling and installing a driver
  9 = works after doing some weird things
  Also express the fact that a user may think a device should work without having checked himself?
  In this case, his opinion may be based on another compatibility list (ex : alsa matrix)
  The support level should be an instance of SupportLevel 
  implement this as a Level
  """
  implements(ILevel)

class TrustLevel(Persistent):
  "level of trust to integrate into ISupportLevel or others"
  implements(ILevel)

class StabilityLevel(Persistent):
  """
  a level of stability
  """
  implements(ILevel)

  
