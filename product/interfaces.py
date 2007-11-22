# -*- coding: utf-8 -*-
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains
from zope.schema import List, TextLine, Choice, Text
from zope.interface import Interface
from zope.index.text.interfaces import ISearchableText


class IProduct(IContained):
    u"""
    IProduct offers the basic attributes of a product
    """
    #containers('zompatible.product.interfaces.IProductContainer')
    #contains('zompatible.driver.interfaces.IDriver')
    names = List(title=u'names', description=u'possible names of the product', min_length=1, value_type=TextLine(title=u'name', description=u'a name for the product (commercial name, code name, etc.)'))
    organization = Choice(title=u'Organization', description=u'the organization producing this product', source="orgasource", required=False)
    description = Text(title=u"description", description=u"description of the product", required=False, max_length=1000)
#    physicalinterfaces = List(title=u'physical interfaces', description=u'list of physical interfaces on the product', value_type=Object(title=u'physical interface', description=u'a physical interface on the product', schema=IPhysicalInterface))
#    existingdrivers = List(title=u'existing drivers', description=u'list of supported OS', value_type=Object(title=u'supported OS', description=u'OS on which the product works', schema=IDriver))
    pciid = TextLine(title=u'pci id', description=u'PCI identifier', required=False)
    usbid = TextLine(title=u'usb id', description=u'USB identifier', required=False)

class IProductContainer(IContainer, IContained):
    u"""
    a toplevel product container. This is a base storage for products.
    """
    contains(IProduct)

class ISubProducts(IContainer):
    u"""
    Interface provided by products that have suproducts.
    This gives access to the subproducts of a product
    in a simple containment manner.
    """

class ISearchableTextOfProduct(ISearchableText):
    u"""
    Marker interface that allows to index products separately
    """

class IDevice(IProduct):
    u"""
    A device is a physical product
    """

class ISoftware(IProduct):
    u"""
    A piece of software is also a product, with some specific fields
    """
    #architectures = List(title=u'architectures', description=u'architectures that software applies to', value_type=Object(title=u'architecture',description=u'list of architectures', schema=IArchitecture))
    version = TextLine(title=u'version', description=u'a text string describing the version', required=True)
    builtVersion = TextLine(title=u'built version', description=u'built version', required=False)
    codename=TextLine(title=u'code name (if any)', description=u'the code name of the software', required=False)
    description=Text(title=u'Description', description=u'Software description', required=False)
    #license = Choice......(title=u'which license?', description=u'the licence of the software', schema=ILicense)
    #features = List(title=u'features', description=u'list of features of the driver', value_type=Object(title=u'feature', description=u'a feature of the driver', schema=IFeature))
    #stabilityreports = List(title=u'stability levels', description=u'provided stability levels', value_type=Object(title=u'stability level',description=u'stability level', schema=IStabilityReport))
    url = URI(title=u'a link to software', description=u'link to the software', required=False)

class IFuzzy(Interface): # FIXME confirm the usefulness of this interface
    u"""
    interface for an imprecise product
    a product we don't really know which one it is.
    """
    group = List(title=u'variations', description=u'variations of the software', min_length=1, value_type=Choice(title=u"variation", source="softwaresource"))



# ce qui est dessous ne sert pas pour l'instant


class ILicense(Interface):
    u"""
    un objet licence (GPL 2.0 est un objet licence, GPL 3.0 un autre)
    """
    name = TextLine(title=u'license name', description=u'the name of the license')
    version = TextLine(title=u'license version', description=u'the version of the license')
    free = Bool(title=u'real free software licence?')
    terms = Text(title=u'license terms', description=u'the terms of the license')


class IPatchableSoftware(ISoftware):
    u"""
    When a software is patched over an original, the original receives this interface
    to keep the list of derived software
    """
    patched = List(title=u'derivatives', description=u'existing patched versions of this software', value_type=Object(ISoftware, title=u'derivative'))
    
class IPatchedSoftware(ISoftware):
    u"""
    This interface can be used to create all flavours of the kernel : (ex: 2_ubuntu1).
    the implementation would link to the original software (aka upstream)
    An original kernel must be created, then all distribution specific flavours must provide this interface.
    This interface must not be user for real forks, but only patched/modified software.
    Real forks must become independant objects
    """
    upstream = Object(title=u'patched over', description=u'original software from which this one was derived', schema=ISoftware)

  
class IDriver(ISoftware):
    u"""
    a driver for a software
    we must think of how to speak about ndiswrapper, which is not a driver
    And a driver can apply to a kernel, or be in userspace for xorg. So... ?
    We must express that a linux driver may exist for a product, but not be included in a distro, or in the kernel
    In hardware reviews, we can often find references to kernel versions, so we should include IKernel?
    a driver is included in the kernel, and can be added by a distro
    so a driver applies to a kernel AND a distro
    We must express that the fact that distroX use kernelY automatically brings POSSIBLE support of a particular product
    a distro contains a kernel, that contains a driver
    The features of the driver should be a subset of the features of the product
    subset : one of the product features is not accessible from the computer, or a feature is not implemented in the driver.
    superset : the driver offers a feature purely by software (ex: winmodem) (?)
    """
    subsystems = List(title=u'for which subsystems?', description=u'the driver is for which subsystems? (kernel, xorg, ...)', value_type=Object(title=u'subsystem', description=u'subsystem this driver applies to', schema=(ISoftware)))

class IInclusionLevel(Interface):
    u"""
    tells how software is included in the distro
    For Debian, inclusion can be main, contrib, non-free, etc.
    A REVOIR !
    """
    software = Object(title=u'os', description=u'os', schema=ISoftware)
    inclusion=TextLine(title=u'included', description=u'inclusion type')

