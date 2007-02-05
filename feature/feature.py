# -*- coding: utf-8 -*-
from persistent import Persistent
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserPage
from zope.app.folder import Folder
from zope.interface import implements
from interfaces import *

class Feature(Folder):
    """
    une feature
    """
    implements(IFeature)
    __name__=__parent__=None
    names=[]
    version=None
    
class FeatureAdd(AddForm):
  "La vue (classe) de formulaire pour l'ajout"
  form_fields=Fields(IFeature).omit('__name__', '__parent__')
  label=u"Ajout d'une fonctionnalité"
  template=ViewPageTemplateFile("feature_form.pt")
  def create(self, data):
    "on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
    feature=Feature()
    "puis on applique les données du formulaire à l'objet"
    applyChanges(feature, self.form_fields, data)
    "puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
    self.context.contentName=feature.names[0]
    return feature

class FeatureEdit(EditForm):
  label=u"Modification d'un matériel"
  form_fields=Fields(IFeature).omit('__name__', '__parent__')
  template=ViewPageTemplateFile("feature_form.pt")

class FeatureView(BrowserPage):
    "la vue qui permet d'afficher un feature"
    label=u"Visualisation d'un matériel"
    __call__=ViewPageTemplateFile("feature.pt")
    def getmainname(self):
        return self.context.__name__
    def getothernames(self):
        return self.context.names
        
