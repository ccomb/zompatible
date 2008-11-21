# -*- coding: utf-8 -*-
from interfaces import *
from zope.interface import implements
from importdata import ImportFile
import os
from lxml import etree

class CategoryDesc(object):
    def __init__(self, name, id, score, attrib):
        self.name = name
        self.id = id
        self.score = score
        self.attrib = attrib
        self.children = []
        self.parents = []

class ImportICEcat(ImportFile):
    u""" Manages import from xml files coming from ICEcat website.
    """
    implements(IImportFile)
    categories = {}
    
    def validate(self):
        u""" Validates the xml file against the ICECAT-interface_response.dtd
        stored in the ./doc directory.
        
        TODO: validate against the url stored in the xml header.
        """
        try:
            doc = etree.ElementTree ( file=self.infile )
        except etree.XMLSyntaxError, detail:
            print "*** XML file not well-formed: %s" % detail
            return False
        except IOError, detail:
            print "*** I/O error reading '%s': %s" % (self.infile, detail)
            return False
        
        path = os.path.split(__file__)[0]
        try:
            dtd = etree.DTD(os.path.join(path, 
                                         "doc", 
                                         "ICECAT-interface_response.dtd"))
        except etree.DTDParseError, detail:
            print "*** DTD file not well-formed: %s" % detail
            return False
        # Rk: IOError exception is not raised if the file does not exist.
        #     etree.DTDParseError is raised instead.
        
        return dtd.validate(doc) == 1
    
    def categoryTree(self, cat, niv, car):
        u""" Return a tree of categories in a string form.
        cat : root category
        niv : level of the category
        car : should be "|" but "`" for the las child of a category
        """
        s = ""
        for i in range(niv):
            s = s + "|  "
            
        s = s + car + "-- %s (%s)" % (cat.name, cat.id) + "\n"
        
        for c in cat.children:
            if c == cat.children[len(cat.children)-1]:
                s = s + self.categoryTree(self.categories[c], niv+1, "`")
            else:
                s = s +self.categoryTree(self.categories[c], niv+1, "|")
        
        return s
    
    def importCategories(self):
        u""" 
        import categories into the 'categories' attribute
        (FIXME: add an interface describing this attribute?)
        """
        if self.validate() != True:
            print "*** DTD not satisfied by the XML file %s" % self.infile
            return
        
        # First pass : import categories
        # Rk: 'ID' attribute is required
        doc = etree.ElementTree ( file=self.infile )
        
        for cat in doc.getiterator(tag="Category"):
            for elt in cat:
                if elt.tag == "Name" and \
                   elt.attrib.has_key("langid") and \
                   elt.attrib["langid"] == "3":
                    cat_desc = CategoryDesc(name=elt.attrib.get('Value','').encode('utf-8'), 
                                            id=cat.attrib['ID'],
                                            score=cat.attrib.get('Score',''),
                                            attrib=elt.attrib)
                    self.categories[cat.attrib['ID']] = cat_desc

        # Second pass: set link between categories
        doc = doc.getroot()
        
        for child in doc.getiterator(tag="Category"):
           for elt in child:
                if elt.tag == "ParentCategory":
                    if self.categories.has_key(elt.attrib['ID']):
                        child_id = child.attrib['ID']
                        parent_id = elt.attrib['ID']
                        if child_id != parent_id:
                            # Avoid direct loops !
                            self.categories[child_id].parents.append(parent_id)
                            self.categories[parent_id].children.append(child_id)
                    else:
                        print "Category ID not found: %s" % elt.attrib['ID']
             
                            
    def do_import(self):
        u"See IImportFile. Real import should be done here"
        pass
    
    def __str__(self):
       text = ""
       for c in self.categories.iteritems():
            if len(c[1].parents) == 0:
                text = text + self.categoryTree(c[1], 0, "|")
#        import odbchelper
#        for el in dir(odbchelper):
#            print "%s:%s" % (el,odbchelper[el])
#        print "__file__:%s" % __file__
#        print "__name__:%s" % __name__
#        file_dir = os.path.split(__file__)[0]
#        print "dir=%s" % file_dir
#        for line in open(self.infile):
#            text = text + line + "\n"
       return text
