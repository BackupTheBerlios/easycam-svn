#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written by Anbreizh
#
    #################################
    #         EASYCAM               #
    #################################
#
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
import os, sys
import gettext
import gnome.ui
import gtk, gtk.glade
import time
import xml
import easycamconfig

APPNAME="Easy Cam"
APPVERSION="1.99"

gtk.glade.bindtextdomain("easycam","./locale")
gtk.glade.textdomain("easycam")
gettext.bindtextdomain("easycam","./locale")
gettext.textdomain("easycam")
_ = gettext.gettext

def simpleErrorMessageDialog(message):
   d = gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,message)
   d.run()
   d.destroy()
     
class MakeGui:
    ##
    # storage for selected USB id
    installid = ""

    def __init__( self ):
        gnome.init( APPNAME, APPVERSION )
        self.gui = gtk.glade.XML( "easycam.glade" )
        self.gui.get_widget( "EasyCamwindows" ).connect( "delete_event", self.destroy )
        self.gui.signal_autoconnect( self )
        self.gui.get_widget( "druidpagestart1" ).show()

    def destroy( self, widget, data=None ):
        gtk.main_quit()
    
    def on_quit_activate( self, gui ):
        gtk.main_quit()

    def on_about_activate( self, gui ):
        about=self.gui.get_widget( "about" )
        about.connect( "delete_event", self.hidewindow )
        about.show()

    def on_druidpagestart1_cancel( self, widget, gui ):
        gtk.main_quit()
        
    def on_druidpagestandard1_cancel( self, widget, gui ):
        gtk.main_quit()
        
    def on_propertieclose_clicked( self, gui ):
        properties=self.gui.get_widget( "properties" )
        properties.hide()
        
    def on_druidpagestandard2_cancel( self, widget, gui ):
        gtk.main_quit()
        
    def on_druidpagefinish1_finish (self, widget, gui):
        gtk.main_quit()
    
    def on_druid1_cancel( self, gui ):
        gtk.main_quit()
    
    def on_properties_activate( self, gui ):
        properties=self.gui.get_widget( "properties" )
        properties.connect( "delete_event", self.hidewindow )
        properties.show()

    def hidewindow( self, w, event, data=None ):
        w.hide()
        return True

    def on_druidpagestart1_next( self, widget, gui ):
        global cf
        combobox = self.gui.get_widget( "comboboxentry1" )
        cnt = 0
	f = os.popen("lsusb","r")
        for line in f.readlines():
            id = line[23:32]			# get USB ID
            if cf.getDriverListByID(id):	# put id only in list, if we know how to handle it
               combobox.insert_text( 0, line.lstrip() )
               cnt += 1  
        f.close()
        if cnt:
           combobox.connect( 'changed', self.changed_cb )
           combobox.set_active( 0 )
        else:
           simpleErrorMessageDialog( _( u"Aucune caméra trouvée ou caméra non compatible") )
           gtk.main_quit()

    def changed_cb( self, combobox ):
        model = combobox.get_model()
        index = combobox.get_active()
        self.installid = model[index][0][23:32]  # USB ID of selected device
    
    def on_close2_clicked ( self, gui ):
        self.gui.get_widget( "errorwindows" ).hide()

    def on_go_clicked ( self, gui ):
        global cf	# holds the config info
        import install

        identi = ""
        info = cf.getDriverListByID(self.installid)
        if info:
            if len(info) == 1:
                moreinfo = cf.getDriverInfo(info[0])
                identi = moreinfo['name']
            else:                   # there are MORE THAN ONE driver for this camera
                pass                # do nothing, perhaps a selector screen would be nice
	else:                       # there is NO drive for this camera
                pass                # do nothing, perhaps an info window would be nice
	
        if identi == "pwc" :
            install.base( self, 'drivers/pwc', 'gcc-3.4' )
            
        if identi == "sqcam" :
            install.base( self, 'drivers/sqcam', 'gcc-3.4' )

        if identi == "toys" :
            install.base( self, 'drivers/toys', 'gcc-3.4' )

        if identi == "spca" :
            install.base( self, 'drivers/spca', 'gcc-4.0' )

        if identi =="qcnews" :
            install.base( self, 'drivers/qcnews', 'gcc-3.4' )

        if identi == "ov519" :
            install.base( self, 'drivers/ov519', 'gcc-3.4' )

        if identi == "ov511" :
            install.base( self, 'drivers/ov511', 'gcc-3.4' )

if __name__ == "__main__":
    ui = MakeGui()

    error = 0
    # Loading config from easycam.xml
    try:
        cf = easycamconfig.ConfigInfo()
    except IOError:
        # config file is missing
        simpleErrorMessageDialog( _( u"Le fichier de configuration n'a pas été détecter!\nReinstallez easycam"))
        error = 1
    except xml.parsers.expat.ExpatError:
        # error in XML syntax
        simpleErrorMessageDialog( _( u"Le fichier de configuration est défectueux.\nReinstallez easycam") )
        error = 1

    if error == 0:
        ui.gui.get_widget( "EasyCamwindows" ).show()
        gtk.main()
    
