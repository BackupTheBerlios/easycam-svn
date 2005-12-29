#!/usr/bin/env python

##
# This module creates the easycam XML config file 
#
# Sources of information
# - all regular files in ./cams
# - easycamurl in this file
#
# Dependencies: PyXML (Debian package: Python-XML) for PrettyPrint
#
# change log
# 2005-12-28 [mistr] moved files around, adjusted paths
##

import xml.dom.minidom
from xml.dom.minidom import Node
import xml.dom.ext
import os
import re
import time

##
# URL from which the a more current config file can be downloaded

easycamurl = "http://blognux.free.fr/easycam/latestconfig.xml"

namespace = "http://blognux.free.fr/easycam"

##
# subdirectory with ini files

subdir = "cams/"


##
# read one ini file and store info in XML node
#
# @param xmltree    XML tree to be created, needed for createElement function
# @param rootele    "easycam" element
# @param filename   filename of the ini file
# @param drivername "name" of the driver (e.g. spca, ov511, etc.)

def readini(xmltree,rootele,filename,drivername):
	# only use regular files
	if os.path.isdir(filename):
		return
	
	print "Reading ", filename, " for driver:", drivername	
	ein = open(filename,"r")
	
	# create element "driver", set name attribute and append to root element "easycam"
	driver = xmltree.createElementNS(namespace,"driver")
	driver.setAttributeNS(namespace,"driver:name",drivername)
	rootele.appendChild(driver)
	
	for line in open(filename,"r"):
		line = line.rstrip()		# strip newline
		if line == "":			# don't process empty lines
			continue
		if line.startswith("#"):	# don't process comment lines
			continue

		# search for "ID xxxx:xxxx yadayadayada"
		ma = re.match("^ID\s([\da-zA-Z]{4}:[\da-zA-Z]{4})\s*($|(.*))",line)
		if ma:
			usbid = ma.group(1).lower()	# make ID lower case
			camname = ma.group(3)

			# store camera name in element "camera"
			cameraele = xmltree.createElementNS(namespace,"camera")
			camnameele = xmltree.createElementNS(namespace,"cameraname")
			camtext = xmltree.createTextNode(camname)
			camnameele.appendChild(camtext)
			cameraele.appendChild(camnameele)

			# store usb id in element "usbid"
			usbidele = xmltree.createElementNS(namespace,"usbid")
			usbidtxt = xmltree.createTextNode(usbid)
			usbidele.appendChild(usbidtxt)
			cameraele.appendChild(usbidele)
		
			driver.appendChild(cameraele)
			continue
		
		# search for "homepage http://......."
		ma = re.match("^homepage\s(.+)",line)
		if ma:
			page = ma.group(1)
			driver.setAttributeNS(namespace,"driver:homepage",page)
			continue

		# search for "source http://........"
		ma = re.match("^source\s(.+)",line)
		if ma:
			source = ma.group(1)
			driver.setAttributeNS(namespace,"driver:source",source)
			continue

		# search for "needs .."
		ma = re.match("^needs\s(.+)",line)
		if ma:
			needs = ma.group(1)
			driver.setAttributeNS(namespace,"driver:needs",needs)
			continue
			
		# everything else
		print "Wrong line format: ", line
		
	ein.close()

def mainloop():
	doc = xml.dom.minidom.Document()
	easy = doc.createElementNS(namespace,"easycam")
	easy.setAttributeNS(namespace,"easycam:date",time.strftime("%Y-%m-%d",time.localtime()))
	easy.setAttributeNS(namespace,"easycam:url",easycamurl)
	doc.appendChild(easy)

	files = os.listdir(subdir)
	for inifile in files:
		readini(doc,easy,subdir + inifile,inifile)
		
	xml.dom.ext.PrettyPrint(doc,open("../easycam.xml","w"))
	doc.unlink()	


if __name__ == "__main__": 
   mainloop()
   
