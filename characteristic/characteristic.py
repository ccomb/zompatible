from zope.interface import implements
from zope.component import adapts
from zope.interface import providedBy
from zope.component.interface import queryInterface

from interfaces import *

#################
# ABSTRACT CLASS
#################
class Characteristic(object):
    """ Base class for any characteristic adapter. 
    
        It stores interface attributes into the adapted object.
        These attributes are stored with the adapter class name
        as prefix to be sure not to override any data of the object.
        
        The concrete characteristic class should adapt the
        characteristicName attribute and the Display() method
        to itself.
    """
    characteristicName = u'You should name this caracteristic'

# PUBLIC

    def __init__(self, context):
        self.context = context

    def Name(self):
        """ Return the characteristic name.
        """
        return self.characteristicName

    def Display(self):
        """ Return the values of the caracteristic.
        """
        print u'Display the characteristic value overriding the Display() method'

# PRIVATE

    def InterfaceAttributes(self):
        """ Return all the attributes from the interfaces implemented.
        """
        l = []
        [l.extend(e.names()) for e in list(self.__provides__) ]
        return l

    def Prefix(self):
        """ Return the adapter class name
        """
        l = str(self.__class__).split('\'')[1].split('.')
        return l[len(l)-1]

    def TranslateAttribute(self, key):
        """ Return the key prefixed with the adapter class name.
        """
        return u'%s.%s' % (self.Prefix(), key)

    def __getattr__(self, key):
        if key in self.InterfaceAttributes():
            # Get all object attributes that are not callable to verify that the key exists
            attributeList = [e for e in dir(self.context) if not callable(getattr(self.context, e))]
            key = self.TranslateAttribute(key)
            if key in attributeList:
                return getattr(self.context, key)
            else:
                return None
        else:
            object.__getattr__(self, key)
        
    def __setattr__(self, key, value):
        if key in self.InterfaceAttributes():
            key = self.TranslateAttribute(key)
            setattr(self.context, key, value)
        else:
            object.__setattr__(self, key, value)

def getCharacteristicInterfaces(obj):
    l = list(providedBy(obj))
    l = [str(e) for e in l]
    l = [e for e in l if e.find('zompatible.characteristic.interfaces.') >= 0]
    l = [ e.replace(u'interfaces.IHas',u'interfaces.I') for e in l ]
    l = [e.strip('><').split()[1] for e in l]
    l = [ queryInterface(e) for e in l ]
    
    return l

###################
# CONCRETE CLASSES
###################

class HasPhysInterface(Characteristic):
    implements(IPhysInterface)
    adapts(IHasPhysInterface)
    
    characteristicName = u'Interface'

    def Display(self):
        # TODO : test values data (None)
        print u'%s: %s' % (self.Name(), self.interface)


class HasResolution(Characteristic):
    implements(IResolution)
    adapts(IHasResolution)
    
    characteristicName = u'Resolution'
   
    def Display(self):
        # TODO : test values data (None)
        print u'%s: %dx%d %s' % (self.Name(),
                                 self.x,
                                 self.y,
                                 self.unit
                                 )
        
