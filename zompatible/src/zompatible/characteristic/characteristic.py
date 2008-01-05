from zope.interface import implements, Interface
from zope.component import adapts, getUtility
from zope.interface import providedBy, alsoProvides, directlyProvidedBy, directlyProvides
from zope.component.interface import queryInterface
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.location import Location
from zope.annotation.interfaces import IAnnotations
from persistent.list import PersistentList
from interfaces import *

CHARACTERISTICS_KEY = 'zompatible.category'

class Characteristics(Location):
    u"""
    The adapter that writes and retrieves the characteristics put on any object
    """
    adapts(ICharacterizable)
    implements(ICharacteristics)

    def __init__(self, context):
        self.context = context

    def _get_characteristics(self):
        try:
            return IAnnotations(self.context)[CHARACTERISTICS_KEY]
        except KeyError:
            characteristics = PersistentList()
            IAnnotations(self.context)[CHARACTERISTICS_KEY] = characteristics
            return characteristics

    def _set_characteristics(self, categories):
        IAnnotations(self.context)[CHARACTERISTICS_KEY] = PersistentList(characteristics)

    characteristics = property(_get_characteristics, _set_characteristics)


#################
# ABSTRACT CLASS
#################
class CharacteristicBase(object):
    """ Base class for any characteristic adapter. 
    
        It stores interface attributes into the adapted object.
        These attributes are stored with the adapter class name
        as prefix to be sure not to override any data of the object.
        
        The concrete characteristic class should adapt the
        characteristicName attribute and the Display() method
        to itself.
    """
    characteristicName = u'You should name this characteristic'

# PUBLIC

    def __init__(self, context):
        self.context = context

    def Name(self):
        """ Return the characteristic name.
        """
        return self.characteristicName

# PRIVATE

    def InterfaceAttributes(self):
        """ Return all the attributes from the interfaces implemented.
        """
        l = []
        for e in list(self.__provides__):
            l.extend(e.names())
        return l
    
    def InterfaceAttributesType(self):
        l = []
        for e in list(self.__provides__):
            l.extend(e.namesAndDescriptions())
        d = {}
        for e in l:
            d[e[0]] = e[1].__class__.__name__
        return d
        
    def Prefix(self):
        """ Return the adapter class name
        """
        return self.__class__.__name__

    def TranslateAttribute(self, key):
        """ Return the key prefixed with the adapter class name.
        """
        return u'%s.%s' % (self.Prefix(), key)

# PUBLIC 
    def CanDisplay(self):
        """ Return True if data can be displayed. False, otherwise.
            Data connot if at least one interface attribute is not initialized (==None)
        """
        for e in self.InterfaceAttributes():
            if self.__getattr__(e) == None:
                return False
            elif self.__getattr__(e) == []:
                return False
            
        return True

    def Display(self):
        """ Return the values of the characteristic.
        """
        print u'Display the characteristic value overriding the Display() method'

    def __str__(self):
        """ Return the values of the characteristic.
        """
        return u'Display the characteristic value overriding the Display() method'

    def __getattr__(self, key):
        if key in self.InterfaceAttributes():
            # Get all object attributes that are not callable to verify that the key exists
            attributeList = [e for e in dir(self.context) if not callable(getattr(self.context, e))]
            prefixedKey = self.TranslateAttribute(key)
            if prefixedKey in attributeList:
                return getattr(self.context, prefixedKey)
            else:
                # Default initial value depends on the field type
                if self.InterfaceAttributesType()[key] == 'List':
                    return []
                return None
        else:
            # If key is not in the interface, we call the default method
            object.__getattr__(self, key)
        
    def __setattr__(self, key, value):
        if key in self.InterfaceAttributes():
            prefixedKey = self.TranslateAttribute(key)
            setattr(self.context, prefixedKey, value)
        else:
            # If key is not in the interface, we call the default method
            object.__setattr__(self, key, value)
        
        

###################
# CONCRETE CLASSES
###################
class CharacteristicManager(object):
    implements(ICharacteristicManager)
    adapts(ICharacterizable)

    def __init__(self, context):
        self.context = context

    def AvailableList(self):
        l = CharacteristicBase.__class__.__subclasses__(CharacteristicBase)
        nameList = [ e.characteristicName for e in l ]
        #TODO: remove the element from the l list to avoid list with different sizes
        nameList.remove(u'You should name this characteristic')
        l = [str(e) for e in l]
        l = [e for e in l if e.find('characteristic.characteristic.Has') >= 0]
        l = [ e.replace(u'characteristic.Has',u'interfaces.I') for e in l ]
        l = [e.strip('><').split()[1].strip("'") for e in l]
        interfaceList = l
        markerList = [e.replace(u'interfaces.I',u'interfaces.IHas') for e in l]
        i = 0
        l = []
        for e in interfaceList:
            iface = queryInterface(e)
            l.append({ u'name': nameList[i], 
                       u'description':iface.__doc__, 
                       u'marker':markerList[i], 
                       u'interface':e})
            i = i + 1

        return l
  
    def CurrentList(self):
        l = list(directlyProvidedBy(self.context))
        l = [str(e) for e in l]
        l = [e for e in l if e.find('characteristic.interfaces.IHas') >= 0]
        l = [ e.replace(u'interfaces.IHas',u'interfaces.I') for e in l ]
        l = [e.strip('><').split()[1] for e in l]
    
        return l  

    def CharToHasChar(self, l):
        u""" Transform characteristic interface names into marker interface name
        """
        return [e.replace(u'interfaces.I', u'interfaces.IHas') for e in l]

    def HasCharToChar(self, l):
        u""" Transform characteristic interface names into marker interface name
        """
        return [e.replace(u'interfaces.IHas', u'interfaces.I') for e in l]

    def IfaceToStr(self, iface):
        return [str(e).strip('><').split()[1] for e in iface]
        
    def Add(self, iface):
        # TODO: Verify that the interface is an ICharacteristic ?
        l = self.AvailableList()
        char = None
        for e in l:
            if queryInterface(e['interface']) == iface:
                char = e
        if char != None:
            alsoProvides(self.context, queryInterface(char['marker']))
    
    def Remove(self, iface):
        l = self.AvailableList()
        char = None
        for e in l:
            if queryInterface(e['interface']) == iface:
                char = e
        if char != None:
            directlyProvides(self.context, directlyProvidedBy(self.context) - queryInterface(char['marker']))
        
    def Provides(self, ifaceList):
        l = self.CharToHasChar(self.CurrentList())
        previousIface = [queryInterface(e) for e in l]

        l = self.CharToHasChar(ifaceList)
        newIface = [queryInterface(e) for e in l]
        
        iface = directlyProvidedBy(self.context)
        iface = [e for e in iface if not e in previousIface]
        iface.extend(newIface)
        directlyProvides(self.context, iface)


    def __getattr__(self, key):
        if key=='characteristicInterfaces':
            return [e['name'] for e in self.AvailableList() if e['interface'] in self.CurrentList()]
        else:
            # If key is not in the interface, we call the default method
            object.__getattr__(self, key)

    def __setattr__(self, key, value):
        if key=='characteristicInterfaces':
            self.Provides([e['interface'] for e in self.AvailableList() if e['name'] in value ])
        else:
            # If key is not in the interface, we call the default method
            object.__setattr__(self, key, value)


def characteristicNameVocabulary(context):
    l = CharacteristicBase.__class__.__subclasses__(CharacteristicBase)
    nameList = [ e.characteristicName for e in l ]
    nameList.remove(u'You should name this characteristic')
    return SimpleVocabulary.fromValues(nameList)

class Characteristic(CharacteristicBase):
    implements(ICharacteristic)
    adapts(Interface)

    

class PhysInterface(CharacteristicBase):
    implements(IPhysInterface)
    adapts(IHasPhysInterfaces)
    
    characteristicName = u'Interface'

    def Display(self):
        if self.CanDisplay():
            print u'%s: %s' % (self.Name(), self.interface)

    def __str__(self):
        if self.CanDisplay():
            return u'%s: %s' % (self.Name(), self.interface)
        else:
            return u''


class Resolution(CharacteristicBase):
    implements(IResolution)
    adapts(IHasResolution)
    
    characteristicName = u'Resolution'
   
    def Display(self):
        if self.CanDisplay():
            print u'%s: %dx%d %s' % (self.Name(),
                                     self.x,
                                     self.y,
                                     self.unit
                                     )

    def __str__(self):
        if self.CanDisplay():
            return u'%s: %dx%d %s' % (self.Name(),
                                     self.x,
                                     self.y,
                                     self.unit
                                     )
        else:
            return u''

    def __cmp__(self, other):
        """ TODO: units management !
        """
        reso1 = self.x  * self.y
        reso2 = other.x * other.y

        return cmp(reso1, reso2)
 
        
class FlashCardSlots(CharacteristicBase):
    implements(IFlashCardSlots)
    adapts(IHasFlashCardSlots)
    
    characteristicName = u'Flash card slots'
   
    def Display(self):
        if self.CanDisplay():
            s = u'%s: ' % self.Name()
            for e in self.type:
                s = s + e + u','
            print s

    def __str__(self):
        if self.CanDisplay():
            s = u'%s: ' % self.Name()
            for e in self.type:
                s = s + e + u','
            return s
        else:
            return u''

class PaperFormat(CharacteristicBase):
    implements(IPaperFormat)
    adapts(IHasPaperFormat)
    
    characteristicName = u'Paper format'
   
    def Display(self):
        if self.CanDisplay():
            s = u'%s: %s' % (self.Name(), self.paperType)
            print s

    def __str__(self):
        if self.CanDisplay():
            s = u'%s: ' % self.Name()
            for e in self.paperType:
                s = s + e + u','
            return s
        else:
            return u''

            