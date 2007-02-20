# -*- coding: utf-8 -*-
from persistent import Persistent
from zope.interface import implements  
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.folder.folder import Folder
from interfaces import *
from zope.index.text.interfaces import ISearchableText
from zope.component import adapts, getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.form.browser.editview import EditView
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget, ListSequenceWidget
from zope.schema.fieldproperty import FieldProperty
from persistent.list import PersistentList
from zope.app.form.browser.widget import SimpleInputWidget
from device import Device, SearchDevice, DeviceSource
from zope.app.form.browser.interfaces import ITerms
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.vocabulary import SimpleTerm
from zope.app.form.browser.interfaces import ISourceQueryView


    

# choix du widget pour l'élément de la liste des subdevices
#device_widget = CustomWidgetFactory(ObjectWidget, Device)
# choix du widget pour les subdevices
#subdevices_widget = CustomWidgetFactory(SearchAndSelectObjectWidget)




class DeviceAdd(AddForm):
  "La vue (classe) de formulaire pour l'ajout"
  form_fields=Fields(IDevice, ISubDevices)
  #form_fields['subdevices'].custom_widget=subdevices_widget
  form_fields=form_fields.omit('__name__', '__parent__')
  label=u"Ajout d'un matériel"
  #####template=ViewPageTemplateFile("device_form.pt")
  def create(self, data):
    u"on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
    device=Device()
    u"puis on applique les données du formulaire à l'objet"
    applyChanges(device, self.form_fields, data)
    u"puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
    self.context.contentName=device.names[0]
    return device


class DeviceEdit(EditForm):
  label=u"Modification d'un matériel"
  form_fields=Fields(IDevice, ISubDevices, render_context=True)
  #form_fields['subdevices'].custom_widget=subdevices_widget
  form_fields=form_fields.omit('__name__', '__parent__')
  ## template désactivé
  ######template=ViewPageTemplateFile("device_form.pt")


class DeviceView(BrowserPage):
    "la vue qui permet d'afficher un device"
    label=u"Visualisation d'un matériel"
    __call__=ViewPageTemplateFile("device.pt")
    def getmainname(self):
        return self.context.__name__
    def getothernames(self):
        return self.context.names


class SearchDeviceView(BrowserPage):
    u"""
    la méthode lancée depuis le template pour effectuer la recherche
    """
    def update(self, query):
        self.search.update(query)

    render = ViewPageTemplateFile('search.pt')
    
    def __call__(self, query):
        self.search=SearchDevice(query)
        return self.render()
    
    def getResults(self):
        for item in self.search.getResults():
            names=""
            for name in item.names:
                names += name + " "
            yield names



class DeviceTerms(object):
    u"""
    la vue fournissant les termes de la source à des fins d'affichage dans le widget
    (adapter de ISource vers ITerms)
    """
    implements(ITerms)
    adapts(DeviceSource, IBrowserRequest)
    def __init__(self, source, request):
        self.source=source
    def getTerm(self, value):
        u"""
        on crée un term à partir d'un device
        """
        token = value.__name__.encode('base64').strip()
        title = unicode(value.__name__)
        return SimpleTerm(value, token, title)
    def getValue(self, token):
        u"""
        on récupère le device à partir du token
        *********WARNING**********
        Il faut améliorer cette partie car effectuer
        une recherche à chaque affichage de terme est lourdingue.
        Deuxieme warning : 
        Si deux devices ont le meme nom, le getvalue retourne le 1er...
        """
        nom=token.decode('base64')
        return list(SearchDevice(nom).getResults())[0]
    
    
class DeviceQueryView(object):
    u"""
    La vue permettant d'interroger la source
    """
    implements(ISourceQueryView)
    adapts(DeviceSource, IBrowserRequest)
    def __init__(self, source, request):
        self.source=source
        self.request=request
    def render(self, name):
        u"""
        le code qui affiche la vue permettant la recherche
        Il pourrait être intéressant d'y mettre un viewlet (??) ou au moins un template
        'name' est le préfixe pour les widgets.
        """
        return('<input name="%s.string"><input type="submit" name="%s" value="Search">' % (name, name) )
    def results(self, name):
        if name in self.request:
            search_string = self.request.get(name+'.string')
            if search_string is not None:
                return SearchDevice(search_string).getResults()








