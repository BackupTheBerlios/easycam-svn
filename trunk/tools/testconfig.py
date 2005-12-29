#!/usr/bin/env python

from easycamconfig import *

if __name__ == "__main__":

	# Loading config from easycam.xml
	try:
		cf = ConfigInfo()
	except IOError:
		print "config file is missing"
		sys.exit(1)
	except xml.parsers.expat.ExpatError:
		print "XML error in config file"
		sys.exit(1)


	# check if USB ID is stored in database at all
	# returns empty list if ID is not found
	info = cf.getDriverListByID("1234:abcd")
	if info:
		pass	# do something
	else:
		print "USB ID not found"
		print


	# example with device that is present in more than one list
	info = cf.getDriverListByID("054c:0155")
	if info:
		print "number of entries for this USB id:", len(info)
		for singledriver in info:
			moreinfo = cf.getDriverInfo(singledriver)
			print "------------"
			print "driver name:", moreinfo['name']
			print "needs easycam v.", moreinfo['needs']
	else:
		print "No info for this camera"
