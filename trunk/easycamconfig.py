#!/usr/bin/env python

##
# Module for accessing the easycam config file
#
# (c) Michael Strecke, 2005
# Lizence: GPL
##

import xml.dom.minidom
from xml.dom.minidom import Node

namespace = "http://blognux.free.fr/easycam"

##
# Class for accessing config information
#
class ConfigInfo:
	doc = None		# The XML document
	easy = None		# The root element

	##
	# reads configuration info 
	#
	# @param filename  filename of config file, default is "easycam.xml"
	# @exception IOError  config file is missing
	# @exception xml.parsers.expat.ExpatError  error in XML structure
	#
	# todo: raise exception if easycam element is missing
	def __init__(self,filename="easycam.xml"):
		self.doc = xml.dom.minidom.parse(filename)
		if self.doc:
			self.easy = self.doc.getElementsByTagNameNS(namespace,"easycam")
			# getElements returned a *list* with (one) root element
			# we want the element
			if self.easy:
				self.easy = self.easy[0]
			else:
				self.doc = None
								
	##
	# returns pointer to "driver" element based on camera USB id
	#
	# @param usbid  usb of the camera, e.g. "1234:abcd"
	# @return list with pointer(s) to driver element(s), or empty list, if not found
	
	def getDriverListByID(self,usbid):
		# IDs are stored in lowercase, so we have to search in lowercase
		usbid = usbid.lower()
		idfoundin = []
		# iterating through the XML tree
		for mod in self.easy.childNodes:
			if mod.nodeType == mod.ELEMENT_NODE and mod.localName == "driver":
				foundhere = 0
				for cam in mod.childNodes:
					if cam.nodeType == cam.ELEMENT_NODE and cam.localName == "camera":
						for usb in cam.childNodes:
							if usb.nodeType == usb.ELEMENT_NODE and usb.localName == "usbid":
								for tx in usb.childNodes:
									if tx.nodeValue == usbid:
										idfoundin.append(mod)
										foundhere = 1
										break
								if foundhere:	# if usbid was found in this driver
									break	# we can skip the rest of the driver
						if foundhere:
							break
				

		return idfoundin
	
	##
	# returns infos for driver for camera with USB ID
	#
	# @param mod pointer to driver element
	# @return dictionary with information, or None, if not found
	def getDriverInfo(self,mod):
		infos = None

		name = None
		needs = None
		home = None
		source = None
		if mod:
			try:
				name = mod.getAttribute("driver:name")
			except AttributeError:
				pass
			try:
				needs = mod.getAttribute("driver:needs")
			except AttributeError:
				pass
			try:
				home =  mod.getAttribute("driver:homepage")
			except AttributeError:
				pass
			try:
				source = mod.getAttribute("driver:source")
			except AttributeError:
				pass
			infos = {'name': name, 'needs': needs, 'homepage': home, 'source': source}
		return infos

	##
	# returns the name of the driver for camera with USB ID
	#
	# If more than one drivers are present, it will pick the first
	# one, silently dropping the rest. 
	#
	# @param mod pointer to driver element
	# @return name of the driver, or "", if none is found
	def getDriverName(self,usbid):
		name = None
		mods = self.getDriverListByID(usbid)
		if mods:
			infos = self.getDriverInfo(mods[0])
			name = infos['name']
		if name == None:
			name = ""
		return name


