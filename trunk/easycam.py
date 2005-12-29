#!/usr/bin/env python
# Written by Anbreizh
#
#
    #################################
    #         EASYCAM        #
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
import easycamconfig

APPNAME="Easy Cam"
APPVERSION="1.99"

gtk.glade.bindtextdomain("easycam","./locale")
gtk.glade.textdomain("easycam")
_ = gettext.gettext



class MakeGui:
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
        os.system( "lsusb > /tmp/lsusb" )
        combobox = self.gui.get_widget( "comboboxentry1" )
        f = open( "/tmp/lsusb", "r" )
        for line in f.readlines():
            combobox.insert_text( 0, line )  
        combobox.connect( 'changed', self.changed_cb )
        combobox.set_active( 0 )
        f.close()

    def changed_cb( self, combobox ):
        model = combobox.get_model()
        index = combobox.get_active()
        a = model[index][0]
        f = open( "/tmp/lsusb", "w" )        
        f.write( a )
        f.close()

    
    def on_close2_clicked ( self, gui ):
        self.gui.get_widget( "errorwindows" ).hide()

    def on_go_clicked ( self, gui ):
        # global variable cf holds the config info
        import install
        f = open( "/tmp/lsusb", "r" )
        a = f.readline()
        b = a[23:32]

        identi = ""
        info = cf.getDriverListByID(b)

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

    # Loading config from easycam.xml
    try:
        cf = easycamconfig.ConfigInfo()
    except IOError:
        print "config file is missing"                # a french info window, please
        sys.exit(1)
    except xml.parsers.expat.ExpatError:
        print "XML error in config file"              # a french info window, please
        sys.exit(1)

    gtk.main()
    
