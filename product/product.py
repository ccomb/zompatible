from persistent import Persistent

from zope.app.folder.folder import Folder
from zope.app.folder.interfaces import IFolder

from zope.interface import implements, providedBy

from zompatible.characteristic.characteristic import getCharacteristicInterfaces
from zompatible.categorynew.utilities import getCategoryInterfaces

from interfaces import *

class Product(Folder):
    implements(IProduct, IFolder)
    
    def __init__(self, name=None):
        Folder.__init__(self)
        self.__name__ = name
        self.__parent__ = None

        self.name = name
        self.categories = []
        
    def Display(self):
        # Display the product name
        s = u'Name: %s' % self.name
        print s
        self.DisplayCharacteristics()
        self.DisplayProducts()
    
    def DisplayCharacteristics(self):
        l = getCharacteristicInterfaces(self)
        if len(l) > 0:
            print u'Characteristics:'
            for e in l:
                e(self).Display()
            
    def DisplayProducts(self):
        for e in self.items():
            print u'-----'
            e[1].Display()

    def GetCategories(self):
        u""" Return the list of categories names the product belongs to. 
        """
        cat = []
        for e in self.categories:
            cat.append(e.name)
        for e in self.items():
            cat.extend(e[1].GetCategories())
        return cat
    
    def GetProduct(self, category):
        u""" Return a sub product that belongs to the category
        """
        for e in self.categories:
            if category == e.name:
                return self

        for e in self.items():
            obj = e[1].GetProduct(category)
            if obj != None:
                return obj

        return None

        
