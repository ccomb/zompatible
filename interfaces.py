from zope.interface import Interface
from zope.schema import TextLine, Bool, Object, URI, DateTime

class IDevice(Interface):
  "IDevice offers basic attributes of a device"
  names = List(title=u'names', description=u'possible names of the device', value_type=TextLine(title=u'name', description=u'a name for the device (commercial name, code name, etc.'))
  manufacturer = Object(title=u'Manufacturer', description=u'the manufacturer of the device', schema=IManufacturer)
  features = List(title=u'features', description=u'list of features of the device, in addition of those from the chip', value_type=Object(title=u'feature', description=u'a feature of the device'), schema=IFeature)
  chips = List(title=u'chips', description=u'list of chips on the device', value_type=Object(title=u'chip', description=u'a chip on the device', schema=IChip))
  physicalinterfaces = List(title=u'physical interfaces', description=u'list of physical interfaces on the device', value_type=List(title=u'physical interface', description=u'a physical interface on the device'), schema=IPhysicalInterface)
  existingdrivers = List(title=u'existing drivers', description=u'list of supported OS', value_type=Object(u'supported OS', description=u'OS on which the device works', schema=IDriver))

class IOsSupport(Interface):
  "
  objet qui fait le lien entre un OS et un matériel
  this is the high level object to display in the support page
  supportlevel is an average computed from supportreports and other objects
  OsSupport est question de présence d'un pilote ou pas, et de l'intégration, et des rapports des gens
  Cet objet est le coeur du site !
  "
  operatingsystem = Object(title=u'Operating System', description=u'supported operating system', schema=IOperatingSystem)
  supportlevel = Object(title=u'support level', description=u'the average of user repots', schema=ILevel)
  supportreports = List(title=u'user reports', description=u'list of user reports', value_type=Object(u'user report', description=u'user report', schema=IUserReport))
  drivers 

class IAction(Interface):
  type = Object(title=u'action', description=u'the action to do', schema=ICategory)
  title = TextLine(title=u'action type', description=u'the type of action')

class IReport(Interface):
  date = DateTime(title=u'date/time', description=u'date/time of the report')
  user = Object(title=u'user', description=u'the user that provided the information', schema=IUser)
  comment = Text(u'comment about the report', description=u'comment of the support level')

class IDeviceExperienceReport(IReport):
  "
  le rapport d'un utilisateur à propos de l'utilisation d'un matériel sur une distro
  What is your experience?
  "  
  operatingsystem = Object(title=u'Operating System', description=u'supported operating system', schema=IOperatingSystem)
  supportlevel = Object(title=u'support level', description=u'the support level according to the user', schema=ILevel)
  seeninaction = Bool(title=u'personaly seen', description=u'the user has personaly seen the device work')
  actions = List(title=u'actions to do to make the device work', description=u'list of actions', Object(title=u'action', description=u'action', schema=IAction))

class IUser(Interface):
  firstname = TextLine(title=u'first name', description=u'your first name')
  lastname = TextLine(title=u'last name', description=u'your last name')
  email = TextLine(title=u'e-mail', description=u'your e-mail')
  reports = List(title=u'informations', description=u'list of provided information', value_type=Object(title=u'information', description=u'an information', schema=IUserInformation))

class IHardwareSystem(Interface):
  names = List(title=u'names', description=u'possible names of the system', value_type=TextLine(title=u'name', description=u'a name for the chip (commercial name, code name, etc.'))
  categories = List(title=u'categories', description=u'categories the system is part of', value_type=Object(title=u'category', description=u'category', schema=ICategory))

class ICategory(Interface):
  "
  permettra de définir (implémenter sous forme d'objet) une catégorie de matériel, ou de logiciel, d'action, etc.
  Une catégorie de matériel (une instance) peut être : laptop (ou portable), serveur, etc...
  Une catégorie d'action peut être : installation, configuration, démarrage d'un programme, 
  "
  names = List(title=u'names', description=u'possible names of the category', value_type=TextLine(title=u'name', description=u'a category'))
  description = Text(u'category description', description=u'description of the category')
  #interface = the interface the category applies to

class IPciDevice(IDevice):
  pciid = TextLine(title=u'pciid', description=u'the pciid of the device')

class IChip(Interface):
  "a chip on the device ex: emu10k1, MD3200"
  names = List(title=u'names', description=u'possible names of the chip', value_type=TextLine(title=u'name', description=u'a name for the chip (commercial name, code name, etc.'))
  manufacturer = Object(title=u'Manufacturer', description=u'the manufacturer of the chip', schema=IManufacturer)
  features = List(title=u'features', description=u'list of features of the chip', value_type=Object(title=u'feature', description=u'a feature of the chip', schema=IFeature))

class IPhysicalInterface(Interface):
  "for example a PCI socket, USB plug, etc."
  name = List(title=u'names',description=u'list of names of the physical interface', value_type=TextLine(title=u'interface', description=u'a physical interface offered by the device'))

class IManufacturer(Interface):
  name=List(title=u'names', description=u'possible names of the manufacturer', value_type=TextLine(title=u'name', description=u'a name for the manufacturer'))

class IDriver(ISoftware):
  "
  a driver for an operating system
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
  "
  subsystems = List(title=u'for which subsystems?', description=u'the driver is for which subsystems? (kernel, xorg, ...)', value_type=Object(title=u'subsystem', description=u'subsystem this driver applies to', schema=(IKernel,IXserver))  

class ISoftware(Interface):
  "maybe this is more generic than IXserver, IKernel, IAlsa, etc. ?"
  names = List(title=u'names', description=u'possible software names', value_type=TextLine(title=u'name', description=u'possible software names (commercial name, code name, etc.'))
  architecture = List(title=u'architectures', description=u'architectures that software applies to', value_type=Object(title=u'architecture',description=u'list of architectures', schema=IArchitecture))
  version = TextLine(title=u'version', description=u'a text string describing the version')
  license = Object(title=u'which license?', description=u'the licence of the driver', schema=ILicense)
  features = List(title=u'features', description=u'list of features of the driver', value_type=List(title=u'feature', description=u'a feature of the driver'), schema=IFeature)
  stabilityreports = List(title=u'stability levels', description=u'provided stability levels', value_type=Object(title=u'stability level',description=u'stability level', schema=IStabilityReport))
  inclusionlevels = List(title=u'Operating Systems', description=u'list of OS that provide this software', schema=IInclusionLevel)
  link = URI(title=u'a link to software', description=u'link to the driver')

class IStabilityReport(IReport):
  stability = Object(title=u'stability level', description=u'level of stability', schema=ILevel)

class ILevel(Interface):
  "
  must be implemented by support, trust and stability levels
  "
  level = Int(title=u'support level', description=u'support level for this OS', min_value=0, max_value=10)
  description = Text(u'support level description', description=u'description of the support level')

class IInclusionLevel(Interface):
  "
  tells how software is included in the distro
  For Debian, inclusion can be main, contrib, non-free, etc.
  "
  operatingsystem = Object(title=u'os', description=u'os', schema=IOperatingSystem)
  inclusion=TextLine(title=u'included', description=u'inclusion type')
  
class IErrorReportable(Interface):
  "
  each object should implement this in order for the users to report errors on it
  "
  reportederrors = List(title=u'reported errors', description=u'list of errors reported by the users', Object(title=u'error', description='reported error', schema=IErrorReport))

class IErrorReport(IReport):
  "
  this report is about a specific object that implements IErrorReportable
  it allows to store the bad attribute and the proposition
  "
  badattribute = object 
  proposition = object
  comment = Text(title=u'comment', description=u'comment on the error')

class IKernel(ISoftware):
  pass
  
class IPatchedKernel(IKernel):
  flavour=Object(title=u'for which OS?', description=u'the specific version of which OS?', schema=IOperatingSystem)
  packageversion=TextLine(title=u'package version', description=u'the version of the kernel package (ex: 2_ubuntu1')
  
class IXserver(ISoftware):
  pass

class IPatchedXserver(IXserver):
  flavour = Object(title=u'for which OS?', description=u'the specific version of which OS?', schema=IOperatingSystem)
  packageversion = TextLine(title=u'package version', description=u'the version of the Xserver package (ex: 2_ubuntu1)')

class ILicense(Interface):
  name = TextLine(title=u'license name', description=u'the name of the license')
  free = Bool(title=u'real free software licence?')
  terms = Text(title=u'license terms', description=u'the terms of the license')

class IFeature(Interface):
  "a feature or protocol offered by the device or driver (ex: wpa, pptp, opengl, etc.)"
  "we must find a way to differenciate USB 1.1 from USB 2.0, 802.11b from 802.11g, etc."
  names = List(title=u'names', description=u'possible names of the feature', value_type=TextLine(title=u'feature', description=u'a name for the feature (ex: wifi, wi-fi, 802.11'))
  version = TextLine(title=u'feature version', description=u'the version of the feature (ex: 2)')

class IOperatingSystem(ISoftware):
  "an operating system: linux distribution, freebsd, etc..."
  "the version is included here because 2 versions of a distro are 2 different OS" 
  codename=TextLine(title=u'code name (if any)', description=u'the version of the operating system')
  
class IDistribution(ISoftware):
  "all the flavours of linux, bsd or anything else"
  

