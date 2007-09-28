from zope.interface import providedBy

def getCategoryInterfaces(obj):
    l = list(providedBy(obj))
    l = [str(e) for e in l]
    l = [e for e in l if e.find('zompatible.categorynew.interfaces.IIs') >= 0]
    
    return l
