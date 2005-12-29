#!/usr/bin/env python
# Module d'install d'EasyCam
import os
import gtk, gtk.glade
from easycam import *

def base(self, drivers, gcc):
    r = 'sudo rm -rf /lib/modules/`uname -r`/kernel/drivers/usb/media/%s' %drivers
    rm = r+"*"
    rmmod = 'sudo rmmod %s' % drivers
    os.system(rmmod)
    os.system(rm)
    os.system("mknod /dev/video0 c 81 0")
    os.system("mknod /dev/video1 c 81 1")
    os.system("chmod a+rw /dev/video0")
    os.system("ln -s /dev/video0 /dev/video")
    progressbar = self.gui.get_widget("progressbar1")
    compilateur = gcc
    chemin = drivers
    export1 = 'export CC=%s' % gcc
    export2 = 'export cc=%s' % gcc
    dir = '/usr/share/EasyCam/%s' % chemin
    mod = 'sudo modprobe -f %s' % chemin
    os.system("sudo ln -s /usr/src/linux-headers-`uname -r` /lib/modules/`uname -r`/build")
    os.system(export1)
    os.system(export2)
    progressbar.set_text("Installation du drivers")
    os.system("make clean")
    progressbar.set_fraction(0.15) 
    os.chdir(dir)
    os.system("make")
    if drivers == "spca":
        os.system("sudo mv /lib/modules/`uname -r`/kernel/drivers/usb/media/spca5xx.ko /lib/modules/`uname -r`/kernel/drivers/usb/media/spca5xx.ko.DIST")
    progressbar.set_fraction(0.66)
    os.system("sudo make install")
    if drivers == "spca":
        os.system("modprobe -r spca5xx")
        os.system("insmod spca5xx.ko")              
    progressbar.set_fraction(0.80)
    try:
        os.system(mod)
        progressbar.set_fraction(1)
        progressbar.set_text("Installation du drivers : OK")
        self.gui.get_widget("druidpagefinish1").show()
    except:
        progressbar.set_fraction(0)
        progressbar.set_text("Installation du drivers : KO")
        self.gui.get_widget("errorwindows").show()
   