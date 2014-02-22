from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Tools.Directories import fileExists
from Tools.HardwareInfo import HardwareInfo
import os
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

class RebootMENU(Screen):
    skin = """
    <screen position="center,center" size="380,260" title="DuckBA multiboot" >
        <ePixmap position="5,9" zPosition="4" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/icons/key_info.png" transparent="1" alphatest="on" />
        <widget render="Label" source="key_red" position="45,9" size="140,27" zPosition="5" valign="center" halign="left" font="Regular;21" transparent="1" foregroundColor="white" />
        <widget name="list" position="0,40" size="380,200" scrollbarMode="showOnDemand" />
        <widget name="statustext" position="5,235" size="200,25" font="Regular;20" halign="center" valign="center" transparent="0"  backgroundColor="#00000000"/>
    </screen>"""

    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        self.FirstUsage = True
        self.session = session
        self.path = '/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/bin/'
        self.senv = self.path + 'fw_setenv'
        self.penv = self.path + 'fw_printenv'
        self.model = HardwareInfo().get_device_name()
        self.list = []
        self.list.append((_('Reboot to E2/N from NAND'), 'E2flash', ''))
        printenv = []
        usedPartitions = []
        os.system('echo 1 > /proc/sys/vm/drop_caches')
        #If Spark (AA,GM990, Pingulux) let's get list of images from uboot as first)
        if self.model == 'spark':
            readprintenv = os.popen(self.penv + " | grep 'DuckBA_bootname_'")
            for readvalue in readprintenv.readlines():
                printenv.append(readvalue)
                #print '[DBA] printenv value: %s\n' % readvalue
            for blkid in printenv:
                if 'DuckBA_bootname_' in blkid:
                    try:
                        BootItem = blkid.strip('\n')
                        BootItem = BootItem.replace('DuckBA_bootname_', '')
                        BootItem_SDXY = BootItem.split('=', 1)[0]
                        BootItem_NAME = BootItem.split('=', 1)[1]
                        self.list.append(('Reboot ' + BootItem_NAME + _(' on ') + BootItem_SDXY, 'enableUSB', BootItem_SDXY, 'UBOOT'))
                        usedPartitions.append(BootItem_SDXY)
                    except:
                        print '[DBA] Error during splitting of BootItem:', BootItem
        #new DuckBA version (4 spark7162 too) - bootitmes taken directly from filesystem
        os.system('echo 1 > /proc/sys/vm/drop_caches')
        blkids=os.popen("blkid -c /dev/null -w /dev/null | grep '\.DBA' | awk '{print $2$1}'")
        for blkid in blkids.readlines():
            try:
                BootItem = blkid.strip('\n')
                BootItem = BootItem.replace('LABEL="','')
                BootItem = BootItem.replace('.DBA"/dev/','|')
                BootItem = BootItem.replace(":","")
                BootItem_NAME = BootItem.split("|",1)[0]
                BootItem_SDXY = BootItem.split("|",1)[1]
            	if BootItem_SDXY not in usedPartitions:
                    self.list.append(("Reboot to " + BootItem_NAME + _(" on ") + BootItem_SDXY, 'enableUSB', BootItem_SDXY, 'DBA'))
                    usedPartitions.append(BootItem_SDXY)
            except:
                print "Error during splitting of .DBA blkid:", BootItem 
        #as last resort, possible images only taken from filesystem
        os.system('echo 1 > /proc/sys/vm/drop_caches')
        blkids=os.popen("blkid -c /dev/null -w /dev/null | grep 'ext'")
        for blkid in blkids.readlines():
            try:
                BootItem = blkid.strip('\n')
                if BootItem.find('TYPE="ext') > 0: # only ext2/3
                    if BootItem.upper().find('"RECORD"') < 1 and BootItem.upper().find('"SWAP"') < 1: # exclude record and swap partitions
                        BootItem_SDXY = BootItem.split(":",1)[0].replace("/dev/","")
                        if BootItem.find('LABEL="') > 0:
                            BootItem_NAME = BootItem[BootItem.find('LABEL="')+7:]
                            BootItem_NAME = BootItem_NAME[:BootItem_NAME.find('"')]
                        else:
                            BootItem_NAME = BootItem_SDXY
                        if BootItem_SDXY not in usedPartitions:
                            self.list.append((_("Try reboot to ") + BootItem_NAME + _(" on ") + BootItem_SDXY, 'enableUSB', BootItem_SDXY, 'GUESS'))
                            usedPartitions.append(BootItem_SDXY)
            except:
                print "[DBA] Error during guessing of blkid:", BootItem 

        if fileExists('/usr/local/bin/enigma2.eplayer'):
            self.list.append((_('Use openPLI with eplayer3'), 'FFM', ''))
        elif fileExists('/usr/local/bin/enigma2.eplayer3'):
            self.list.append((_('Use openPLI with eplayer3'), 'FFM', ''))
        if fileExists('/usr/local/bin/enigma2.gstreamer'):
            self.list.append((_('Use openPLI with gstreamer'), 'GST', ''))
        self.list.append((_('Reboot to Spark'), 'SPARK', ''))

        self['list'] = MenuList(self.list)
        self["key_red"] = StaticText("Info")
        self["statustext"] = Label("Select software...")
        self['actions'] = ActionMap(['WizardActions', "InfobarShowHideActions"],
        {
            'ok': self.run,
            'back': self.close,
            #"green": self.green_pressed,
            #"blue": self.blue_pressed,
            'toggleShow': self.red_pressed
        },-1)

    def run(self):
        #if self.FirstUsage == True:
        #    self.FirstUsage = False
        #    return
        CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        BOOTITEM = self['list'].getCurrent()
        print 'DBA selected menu: %s , DuckBA_ON: %s, DuckBA_sda_NO: %s\n' % (BOOTITEM[0], BOOTITEM[1], BOOTITEM[2])
        REBOOTSYSTEM = 0
        if BOOTITEM[1] == 'NA':
            return
        elif BOOTITEM[1] == 'E2flash':
            self["statustext"].setText("Configuring boot from NAND")
            os.system(self.path + 'setIMG.sh NAND')
            REBOOTSYSTEM = 1
        elif BOOTITEM[1] == 'SPARK':
            os.system(self.path + 'setspark.sh')
            REBOOTSYSTEM = 1
        elif BOOTITEM[1] == 'FFM':
            os.system('ln -sf /usr/local/bin/enigma2.eplayer /usr/local/bin/enigma2')
            from enigma import quitMainloop
            quitMainloop(3)
        elif BOOTITEM[1] == 'GST':
            os.system('ln -sf /usr/local/bin/enigma2.gstreamer /usr/local/bin/enigma2')
            from enigma import quitMainloop
            quitMainloop(3)
        elif BOOTITEM[1] == 'enableUSB':
            os.system(self.path + 'setIMG.sh %s %s' % ('USB', BOOTITEM[2]))
            REBOOTSYSTEM = 1
        else:
            REBOOTSYSTEM = 0
        if REBOOTSYSTEM == 1:
            if fileExists('/tmp/dba.log'):
                file = open('/tmp/dba.log', "r")
                lines = file.readlines()
                file.close()
                self.session.open(MessageBox, ''.join(lines), type = MessageBox.TYPE_INFO, timeout = 10 )
            if fileExists('/tmp/dba.ok'):
                from enigma import quitMainloop
                quitMainloop(2)
            elif fileExists('/tmp/dba.error'):
                pass
            else:
                self.session.open(MessageBox, "Unknown error occured :(", type = MessageBox.TYPE_INFO, timeout = 10 )
        self.session.nav.playService(CurrentService)

    def rebootSYSTEM(self):
        from enigma import quitMainloop
        quitMainloop(2)

    def red_pressed(self):
        if fileExists(self.path + '../readme.EN'):
            file = open(self.path + '../readme.EN', "r")
            lines = file.readlines()
            file.close()
            self.session.open(MessageBox, ''.join(lines), type = MessageBox.TYPE_INFO, timeout = 15 )

class ReadME(Screen):
    skin = """
        <screen position="50,70" size="1180,600" title="DuckBA info..." >
            <widget name="text" position="0,0" size="1180,600" font="Console;24" />
        </screen>"""
        
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self.myTEXT = "readme.[PL|EN|DE]"
        self["text"] = ScrollLabel("")
        self["actions"] = ActionMap(["WizardActions", "DirectionActions"], 
        {
            "ok": self.cancel,
            "back": self.cancel,
            "up": self["text"].pageUp,
            "down": self["text"].pageDown
        }, -1)
        self.onLayoutFinish.append(self.startRun) # dont start before gui is finished

    def startRun(self):
        self["text"].setText(self.myTEXT)

    def cancel(self):
        self.close()

def mainMENU(session, **kwargs):
    session.open(RebootMENU)

def Plugins(**kwargs):
    return [PluginDescriptor(name = _('USB multiboot'),
			where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = mainMENU)]
