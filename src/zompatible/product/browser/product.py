# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.formlib.form import EditForm, Fields, AddForm, applyChanges, Actions, Action, getWidgetsData
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import adapts, getUtility, createObject
from zope.app.form.browser.interfaces import ITerms, ISourceQueryView
from zope.schema.vocabulary import SimpleTerm
from zope.app.intid.interfaces import IIntIds
from zope.copypastemove import ContainerItemRenamer
from zope.app.container.interfaces import INameChooser
from zope.traversing.browser.absoluteurl import AbsoluteURL
from zope.app.form.browser import TextAreaWidget
import string, urllib

from zompatible.product.product import Product, ProductSource
from zompatible.product.interfaces import IProduct, ISubProducts

class CustomTextWidget(TextAreaWidget):
    width=40
    height=5

class ProductAdd(AddForm):
    "La vue (classe) de formulaire pour l'ajout"
    form_fields=Fields(IProduct, ISubProducts)
    form_fields['description'].custom_widget = CustomTextWidget
    #form_fields['subdevices'].custom_widget=subdevices_widget
    form_fields=form_fields.omit('__name__', '__parent__', 'organization')
    label=u"Ajout d'un matériel"
    def nextURL(self):
        return AbsoluteURL(self.product,self.request)
    #####template=ViewPageTemplateFile("device_form.pt")
    def create(self, data):
        u"on crée l'objet (ici avec le constructeur, mais on devrait utiliser une named factory)"
        self.product=Product()
        u"puis on applique les données du formulaire à l'objet"
        applyChanges(self.product, self.form_fields, data)
        u"puis on choisit le nom de l'objet dans le container (le 1er nom dans la liste)"
        self.context.contentName = INameChooser(self.context.context).chooseName(self.product.names[0],
                                                                                 self.product)
        return self.product

class ProductEdit(EditForm):
    label=u"Edit a product"
    form_fields=Fields(IProduct, ISubProducts, render_context=True)
    #form_fields['subdevices'].custom_widget=subdevices_widget
    form_fields['description'].custom_widget = CustomTextWidget
    form_fields=form_fields.omit('__name__', '__parent__')
    ## template désactivé
    #template=ViewPageTemplateFile("device_form.pt")
    actions = Actions(Action('Apply', success='handle_edit_action'), )
    def handle_edit_action(self, action, data):
        super(ProductEdit, self).handle_edit_action.success(data)
        oldname=self.context.__name__
        newname=string.lower(INameChooser(self.context.__parent__).chooseName(u"",self.context))
        if string.lower(oldname)!=newname:
            renamer = ContainerItemRenamer(self.context.__parent__)
            renamer.renameItem(oldname, newname)
        nexturl = AbsoluteURL(self.context, self.request)() + "/edit_product.html"
        return self.request.response.redirect(nexturl)
    
class ProductView(BrowserPage):
    "la vue qui permet d'afficher un device"
    label=u"Visualisation d'un matériel"
    __call__=ViewPageTemplateFile("product.pt")

class ProductTerms(object):
    u"""
    la vue fournissant les termes de la source à des fins d'affichage dans le widget
    (adapter de ISource vers ITerms)
    """
    implements(ITerms)
    adapts(ProductSource, IBrowserRequest)
    def __init__(self, source, request):
        self.source=source
        self.intid=getUtility(IIntIds)
    def getTerm(self, value):
        u"""
        on crée un term à partir d'un product
        On utilise le Unique Integer Id comme token
        (puisqu'il a fallu forcément en créer un pour la recherche dans le Catalog)
        """
        token = self.intid.getId(value)
        title = unicode(value.__name__)
        return SimpleTerm(value, token, title)
    def getValue(self, token):
        u"""
        on récupère le product à partir du token
        """
        return self.intid.getObject(int(token))

class ProductQueryView(object):
    u"""
    The view allowing to query the source
    """
    implements(ISourceQueryView)
    adapts(ProductSource, IBrowserRequest)
    def __init__(self, source, request):
        u"source est le contexte"
        self.source=source
        self.request=request
    def render(self, name):
        u"""
        le code qui affiche la vue permettant la recherche
        Il pourrait être intéressant d'y mettre un viewlet (??) ou au moins un template
        'name' est le préfixe pour les widgets.
        """
        return('<input name="%s.string" /><input type="submit" name="%s" value="chercher" />' % (name, name) )
    def results(self, name):
        if name in self.request:
            search_string = self.request.get(name+'.string')
            if search_string is not None:
                return createObject(u"zompatible.SearchObject", product_text=search_string).getResults()

class ProductContainerView(object):
    u"""
    la vue du container de products.
    Pour l'instant on se contente d'afficher la liste des products.
    Ensuite il sera possible d'afficher par exemple des classements
    """
    label = u"List of products"
    def getitems(self):
        return ( (urllib.quote(dev[0]),dev[1]) for dev in self.context.items() )

