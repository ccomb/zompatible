from interfaces import *
from persistent import Persistent  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder

# MANUFACTURER


class ManufacturerContainer(Folder):
  "a container that contains manufacturers"
  implements(IManufacturerContainer)

class Manufacturer(Persistent):
  implements(IManufacturer)
  names=[]
  # IManufacturer fournit IContained donc il faut mettre ces attributs :
  __name__=__parent__=None

class ManufacturerAdd(AddForm):
  "La classe de formulaire pour l'ajout"
  form_fields=Fields(IManufacturer).omit('__name__', '__parent__')
  label=u"Ajout d'un fabricant"
  template=ViewPageTemplateFile("toto.pt")
  def create(self, data):
    "on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
    manufacturer=Manufacturer()
    "puis on applique les données du formulaire à l'objet"
    applyChanges(manufacturer, self.form_fields, data)
    "puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
    self.context.contentName=manufacturer.names[0]
    return manufacturer

class ManufacturerEdit(EditForm):
  label="Modification d'un fabricant"
  form_fields=Fields(IManufacturer).omit('__name__', '__parent__')
  template=ViewPageTemplateFile("toto.pt")

class ManufacturerView(BrowserPage):
  __call__=ViewPageTemplateFile("manufacturer.pt")
  def getmainname(self):
    return self.context.names[0]

class Device(Persistent):
  implements(IDevice)
  def __init__(self):
        pass

class DeviceEdit(EditForm):
  form_fields=Fields(IDevice)

class DeviceAdd(AddForm):
  form_fields=Fields(IDevice)
  def create(self, data):
         # applyChanges applies all changed fields named in form_fields
         # to the object, taking the field values from data.
         # In a new object, that's *all* fields.
         device = Device()
         applyChanges(device, self.form_fields, data)
         return device

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

  
