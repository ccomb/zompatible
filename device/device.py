# -*- coding: utf-8 -*-
from interfaces import *
from persistent import Persistent  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder


class Device(Persistent):
  implements(IDevice)
  names=[]
  # IDevice fournit IContained donc il faut mettre ces attributs :
  __name__=__parent__=None

class DeviceAdd(AddForm):
  "La vue (classe) de formulaire pour l'ajout"
  form_fields=Fields(IDevice).omit('__name__', '__parent__')
  label=u"Ajout d'un matériel"
  template=ViewPageTemplateFile("device_form.pt")
  def create(self, data):
    "on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
    device=Device()
    "puis on applique les données du formulaire à l'objet"
    applyChanges(device, self.form_fields, data)
    "puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
    self.context.contentName=device.names[0]
    return device

class DeviceEdit(EditForm):
  label=u"Modification d'un matériel"
  form_fields=Fields(IDevice).omit('__name__', '__parent__')
  template=ViewPageTemplateFile("device_form.pt")

class DeviceView(BrowserPage):
    "la vue qui permet d'afficher un device"
    label=u"Visualisation d'un matériel"
    __call__=ViewPageTemplateFile("device.pt")
    def getmainname(self):
        return self.context.__name__
    def getothernames(self):
        return self.context.names