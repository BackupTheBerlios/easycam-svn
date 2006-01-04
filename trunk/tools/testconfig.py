#!/usr/bin/env python
#
# This demo is stored in: easycam/tools/
# The module(s) and the config file are stored in parent directory: easycam/
#
# Therefore we have to make changes that are NOT required if
# easycamconfig.py and easycam.xml are in the same directory
# (which is usually the case when they are accessed from easycam.py).
#
# The changes are:
#
# Tell Python to search for modules in the parent directory:
#    sys.path.append("../")
#
# Overwrite the default file name in easycamconfig.ConfigInfo()
# The default value is "easycam.xml". 
#
#    cf = easycamconfig.ConfigInfo()
#      becomes
#    cf = easycamconfig.ConfigInfo("../easycam.xml")  # two dots!
#
#
# Functions description:
#
# easycamconfig.ConfigInfo():
# ---------------------------
# easycamconfig defines the class ConfigInfo. 
# If you create a variable of this type, the config file is 
# loaded into memory:
#
#    cf = easycamconfig.ConfigInfo()
#
# This function throws exceptions, if the file is missing or
# the XML file in malformed (see example below).
#
# ConfigInfo.getDriverListByID(usbid):
# ------------------------------------
# Example:
#
#   info = cf.getDriverListByID("1234:abcd")
#
# This returns a list (!) of nodes from the XML tree. 
# These nodes represent the driver which can handle
# the USB id.
# Usually this list is either empty (-> no driver found)
# or contains only one entry (-> exactly 1 driver found).
# But in some cases, more than one driver are available.
#
#
# ConfigInfo.getDriverInfo(singledriver):
# ---------------------------------------
# Example:
#
#    moreinfo = cf.getDriverInfo(singledriver)
#
# This function takes ONE driver node from the list returned 
# by getDriverListByID and returns a dictionary with 
# additional info:
#
#  infos = {'name': name, 'needs': needs, 'homepage': home, 'source': source}
#
# which can be accessed like this:
#
#   moreinfo = cf.getDriverInfo(singledriver)
#   print "driver name:", moreinfo['name']
#
# ConfigInfo.getDriverName(usbid):
# --------------------------------
# This function returns the name of the driver or "" when no driver is found
#
#

import sys
sys.path.append("../")	# see above remarks

import easycamconfig

if __name__ == "__main__":

	# Loading config file into memory
	try:
		cf = easycamconfig.ConfigInfo("../easycam.xml")  # see above remarks
	except IOError:
		print "config file is missing"
		sys.exit(1)
	except xml.parsers.expat.ExpatError:
		print "XML error in config file"
		sys.exit(1)


	# check if USB ID is stored in database at all
	# returns empty list if ID is not found
	info = cf.getDriverListByID("1234:abcd")
	if info:				# list not empty
		pass				# do something
	else:					# list empty
		print "USB ID not found"	# do something else
		print


	# example with device that is present in more than one list
	info = cf.getDriverListByID("054c:0155")
	if info:				# list not empty
		print "number of entries for this USB id:", len(info)
		# iterate over the driver node(s)
		for singledriver in info:
			moreinfo = cf.getDriverInfo(singledriver)
			print "------------"
			print "driver name:", moreinfo['name']
			print "needs easycam v.", moreinfo['needs']
	else:					# list was empty
		print "No info for this camera"

	print "No driver of 0123.abcd: ", cf.getDriverName("1234:abcd")
	print "only the first pick for 054c:0155: ", cf.getDriverName("054c:0155")
