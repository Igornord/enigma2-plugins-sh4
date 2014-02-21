from Screens.Screen import Screen
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.config import config, ConfigSubsection, ConfigSelection, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Language import language
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import gettext
from os import environ
import os

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("ImageManager", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/ImageManager/locale/"))

def _(txt):
	t = gettext.dgettext("ImageManager", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

config.plugins.ImageManager = ConfigSubsection()

def getMountedDevs():
    mountedDevs = []
    mountedDevs.append(('NAND NAND', 'NAND-Flash'))
    blkids=os.popen("blkid -c /dev/null -w /dev/null | grep 'ext'")
    for blkid in blkids.readlines():
        DevList = blkid.strip('\n')
        if DevList.find('TYPE="ext') > 0:
            if DevList.upper().find('"RECORD"') < 1 and DevList.upper().find('"SWAP"') < 1:
                SDXY = DevList.split(":",1)[0]
                if DevList.find('LABEL="') > 0:
                    NAME = DevList[DevList.find('LABEL="')+7:]
                    NAME = NAME[:NAME.find('"')]
                else:
                    NAME = SDXY
                mountedDevs.append((NAME+' '+SDXY, NAME +_(' on ')+SDXY))
    return mountedDevs

config.plugins.ImageManager.devs = ConfigSelection(choices=getMountedDevs())
config.plugins.ImageManager.imagetype = ConfigSelection(default="NO", choices = [
           ("YES", _("YES")),
           ("NO", _("NO"))])
config.plugins.ImageManager.archivetype = ConfigSelection(default="IMG", choices = [
           ("IMG", _("IMG")),
           ("TAR", _("TAR")),
           ("TARGZ", _("TAR.GZ"))])

class ImageManager(ConfigListScreen, Screen):
    skin = """
    <screen name="ImageManager" position="center,center" size="700,200" >
    <widget name="config" position="10,15" size="680,100" transparent="1" scrollbarMode="showOnDemand"/>
    <widget render="Label" source="key_red" position="30,100" size="300,40" zPosition="5" valign="center" halign="left" font="Regular;21" foregroundColor="red" />
    <widget render="Label" source="key_green" position="380,100" size="300,40" zPosition="5" valign="center" halign="left" font="Regular;21" foregroundColor="green" />
    <widget render="Label" source="key_blue" position="30,130" size="400,40" zPosition="5" valign="center" halign="left" font="Regular;21" foregroundColor="blue" />
    </screen>"""

    def __init__(self, session, args = 0):
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.list.append(getConfigListEntry(_("Select partition:"), config.plugins.ImageManager.devs))
        self.list.append(getConfigListEntry(_("Delete the configuration file?"), config.plugins.ImageManager.imagetype))
        self.list.append(getConfigListEntry(_("Select the type of archive:"), config.plugins.ImageManager.archivetype))
        ConfigListScreen.__init__(self, self.list)
        self.setTitle(_("Image Manager"))
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('Backup'))
        self['key_blue'] = Label(_('Copying from nand-flash'))
        self['myActionMap'] = ActionMap(['ColorActions', 'OkCancelActions'], {'ok': self.makebackup,
            'red': self.cancel,
            'green': self.makebackup,
            'blue': self.copyNAND,
            'cancel': self.cancel}, -2)

    def makebackup(self):
        if environ['LANGUAGE'] == 'ru':
            self.makeBackup = '/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/bc_ru.sh'
        else:
            self.makeBackup = '/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/bc.sh'
        self.makeBackup += ' %s %s %s' % (config.plugins.ImageManager.devs.value, config.plugins.ImageManager.archivetype.value, config.plugins.ImageManager.imagetype.value)
        self.session.open(Console, _('Backup Creator'), ['%s' % self.makeBackup])

    def copyNAND(self):
        a = config.plugins.ImageManager.devs.value.find('/dev/sd')
        c = config.plugins.ImageManager.devs.value[a:a+9]
        f = open("/proc/cmdline", "r")
        b = f.readline()
        f.close()
        if b.find(c) > 0:
            self.session.open(MessageBox, _("Can not copy to the active partition!"), type = MessageBox.TYPE_INFO, timeout = 5 )
            return

        if config.plugins.ImageManager.devs.value == 'NAND NAND':
            self.session.open(MessageBox, _("Can not copy to NAND-Flash!"), type = MessageBox.TYPE_INFO, timeout = 5 )
            return

        if environ['LANGUAGE'] == 'ru':
            self.makeCopy = '/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/cpn_ru.sh'
        else:
            self.makeCopy = '/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/cpn.sh'

        self.makeCopy += ' %s %s' % (config.plugins.ImageManager.devs.value, config.plugins.ImageManager.imagetype.value)
        self.session.openWithCallback(self.Yes, Console,  _('Image Backup'), ['%s' % self.makeCopy])
        return

    def Yes(self):
            self.DuckBA = '/DuckBA/bin/setIMG.sh'
            if fileExists(self.DuckBA):
                self.session.openWithCallback(self.reBoot, MessageBox,_("Do you want to reboot with the new partition?"), timeout =0, default = False)

    def reBoot(self, answer):
        if answer is False:
            return
        else:
            a = config.plugins.ImageManager.devs.value.find('/dev/sd')
            devBoot = config.plugins.ImageManager.devs.value[a:a+9]
            self.session.nav.stopService()
            os.system(self.DuckBA + ' %s %s' % ('USB', devBoot))
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
                return

    def cancel(self):
        self.close(None)

def start(session, **kwargs):
        session.open(ImageManager)

def Plugins(**kwargs):
    return PluginDescriptor(name=_('Image Manager'), description = _("creating backup of your image Enigma"),
        where = [PluginDescriptor.WHERE_PLUGINMENU,  PluginDescriptor.WHERE_EXTENSIONSMENU], icon="ImageManager.png", fnc=start)
