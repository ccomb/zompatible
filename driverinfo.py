#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

print u"#\n# driverinfo output\n#"

def printLinuxData(filename,bus_type):
	try:
		f = open(filename,"rt")
	except IOError:
		print u"The file %s does not exist" % filename
		exit(-1)
	try:
		data = f.read()
	except IOError:
		print u"Unable to read the file %s" % filename
	f.close()
	
	lignes = data.split("\n")
	# Get rid of empty lignes
	lignes = [ l for l in lignes if len(l)>0]
	# Get rid of comments (elements have at least one caracter)
	lignes = [ l for l in lignes if l[0]!='#']
	lignes = [ l.split() for l in lignes]
	
	currentModule = u''
	for l in lignes:
		if currentModule != l[0]:
			currentModule = l[0]
			print u"module:%s" % currentModule
			print u"bustype:%s" % bus_type 
			print u"filename:%s" % os.popen("modinfo %s -F filename" % currentModule).read().strip()
			print u"vermagic:%s" % os.popen("modinfo %s -F vermagic" % currentModule).read().strip()
			print u"srcversion:%s" % os.popen("modinfo %s -F srcversion" % currentModule).read().strip()
			print u"description:%s" % os.popen("modinfo %s -F description" % currentModule).read().strip()
			print u"license:%s" % os.popen("modinfo %s -F license" % currentModule).read().strip()
		
		l.remove(l[0])
		print u"device:%s" % ";".join(l)

kName=os.popen('uname -s').read().strip()
kVersion=os.popen('uname -v').read().strip()
kRelease=os.popen('uname -r').read().strip()
Os=os.popen('uname -o').read().strip()

print u'OS:%s' % Os
print u'kernelName:%s' % kName
print u'kernelRelease:%s' % kRelease
print u'kernelVersion:%s' % kVersion


if kName == u'Linux':
	filename=u'/lib/modules/'+kRelease+u'/modules.pcimap'
	printLinuxData(filename,u'pci')
	filename=u'/lib/modules/'+kRelease+u'/modules.usbmap'
	printLinuxData(filename,u'usb')
	
else:
	print u'Kernel type not supported'
	
