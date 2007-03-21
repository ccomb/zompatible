# -*- coding: utf-8 -*-
from zope.interface.interfaces import Interface
from zope.schema import TextLine, List, Object, URI, Bool, Text
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers
from zope.index.text.interfaces import ISearchableText

class ISoftware(IContainer, IContained):
    u"maybe this is more generic than IXserver, IKernel, IAlsa, etc. ?"
    names = List(title=u'names', description=u'possible software names', value_type=TextLine(title=u'name', description=u'possible software names (commercial name, code name, etc.'))
    #architectures = List(title=u'architectures', description=u'architectures that software applies to', value_type=Object(title=u'architecture',description=u'list of architectures', schema=IArchitecture))
    version = TextLine(title=u'version', description=u'a text string describing the version', required=False)
    codename=TextLine(title=u'code name (if any)', description=u'the code name of the software', required=False)
    #license = Choice......(title=u'which license?', description=u'the licence of the software', schema=ILicense)
    #features = List(title=u'features', description=u'list of features of the driver', value_type=Object(title=u'feature', description=u'a feature of the driver', schema=IFeature))
    #stabilityreports = List(title=u'stability levels', description=u'provided stability levels', value_type=Object(title=u'stability level',description=u'stability level', schema=IStabilityReport))
    link = URI(title=u'a link to software', description=u'link to the software', required=False)

class IOperatingSystem(IContainer, IContained, ISoftware):
    u"""an software: linux distribution, freebsd, etc...
    the version is included here because 2 versions of a distro are 2 different software
    Cette interface est vide car tout ce qui concerne les OS concerne avant tout les logiciels,
    donc le schema est dans ISoftware
    """
    containers("zompatible.software.interfaces.ISoftwareContainer")

class ISoftwareContainer(IContainer, IContained):
    u"""
    L'interface du dossier racine qui contient les OS
    """
    contains(ISoftware)

class ISearchableTextOfSoftware(ISearchableText):
    u"""
    on déclare un index juste pour cette interface de façon à indexer juste les software
    """



# ce qui est dessous ne sert pas pour l'instant

class ILicense(Interface):
    u"""
    un objet licence (GPL 2.0 est un objet licence, GPL 3.0 un autre)
    """
    name = TextLine(title=u'license name', description=u'the name of the license')
    version = TextLine(title=u'license version', description=u'the version of the license')
    free = Bool(title=u'real free software licence?')
    terms = Text(title=u'license terms', description=u'the terms of the license')
    
class IKernel(ISoftware):
    pass
  
class IPatchedKernel(IKernel):
    flavour=Object(title=u'for which OS?', description=u'the specific version of which OS?', schema=ISoftware)
    packageversion=TextLine(title=u'package version', description=u'the version of the kernel package (ex: 2_ubuntu1')
  
class IXserver(ISoftware):
    pass

class IPatchedXserver(IXserver):
    flavour = Object(title=u'for which OS?', description=u'the specific version of which OS?', schema=ISoftware)
    packageversion = TextLine(title=u'package version', description=u'the version of the Xserver package (ex: 2_ubuntu1)')

class IDistribution(ISoftware):
    u"all the flavours of linux, bsd or anything else"
    
class IDriver(ISoftware):
    u"""
    a driver for an software
    we must think of how to speak about ndiswrapper, which is not a driver
    And a driver can apply to a kernel, or be in userspace for xorg. So... ?
    We must express that a linux driver may exist for a device, but not be included in a distro, or in the kernel
    In hardware reviews, we can often find references to kernel versions, so we should include IKernel?
    a driver is included in the kernel, and can be added by a distro
    so a driver applies to a kernel AND a distro
    We must express that the fact that distroX use kernelY automatically brings POSSIBLE support of a particular device
    a distro contains a kernel, that contains a driver
    The features of the driver should be a subset of the features of the device
    subset : one of the device features is not accessible from the computer, or a feature is not implemented in the driver.
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

