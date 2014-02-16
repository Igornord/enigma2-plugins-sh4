#by 2boom 4bob@ua.fm 2011-14
from Screens.Screen import Screen
from Screens.PluginBrowser import PluginBrowser
from Components.PluginComponent import plugins
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Components.Console import Console as iConsole
from Components.Label import Label
from Components.MenuList import MenuList
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigDateTime, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.ConfigList import ConfigListScreen
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from os import environ
import os
import gettext
import emuman
import minstall
import tools
from enigma import eEPGCache
from types import *
from enigma import *
import sys, traceback
import re
import time
import new
import _enigma
import enigma

global min, min_ntp
min, min_ntp = 0, 0

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("epanel", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/epanel/locale/"))

def _(txt):
	t = gettext.dgettext("epanel", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

######################################################################################
config.plugins.epanel.showmain = ConfigYesNo(default = True)
config.plugins.epanel.showepanelmenu = ConfigYesNo(default = True)
config.plugins.epanel.showextsoft = ConfigYesNo(default = True)
config.plugins.epanel.showclviewer = ConfigYesNo(default = False)
config.plugins.epanel.showscriptex = ConfigYesNo(default = False)
config.plugins.epanel.showusbunmt = ConfigYesNo(default = False)
config.plugins.epanel.showsetupipk = ConfigYesNo(default = False)
config.plugins.epanel.showpbmain = ConfigYesNo(default = False)
config.plugins.epanel.filtername = ConfigYesNo(default = False)
config.plugins.epanel.showepgreload = ConfigYesNo(default = False)
config.plugins.epanel.showepgdwnload = ConfigYesNo(default = False)
config.plugins.epanel.currentclock = ConfigClock(default = 0)
config.plugins.epanel.multifilemode = ConfigSelection(default = "Multi", choices = [
		("Multi", _("Multi files")),
		("Single", _("Single file")),
])
config.plugins.epanel.crashpath = ConfigSelection(default = '/media/hdd/', choices = [
		('/media/hdd/', _('/media/hdd')),
		('/home/root/', _('/home/root')),
		('/tmp/', _('/tmp')),
])
config.plugins.epanel.userdir = ConfigText(default="/ipk/", visible_width = 70, fixed_size = False)
######################################################################################
class easyPanel2(Screen):
	skin = """
<screen name="easyPanel2" position="center,160" size="750,420" title="E-Panel">
<ePixmap position="10,408" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
<widget source="key_red" render="Label" position="10,378" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<ePixmap position="175,408" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
<widget source="key_green" render="Label" position="175,378" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<ePixmap position="340,408" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
<widget source="key_yellow" render="Label" position="340,378" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<ePixmap position="505,408" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/blue.png" alphatest="blend" />
<widget source="key_blue" render="Label" position="505,378" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="menu" render="Listbox" position="15,10" size="720,350" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (120, 2), size = (600, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (130, 29), size = (600, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
		</widget>
<ePixmap position="675,381" size="70,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/info.png" zPosition="2" alphatest="blend" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("E-Panel"))
		self.iConsole = iConsole()
		self.indexpos = None
		self.iConsole.ePopen("opkg update")
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions", "EPGSelectActions"],
		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"info": self.infoKey,
			"green": self.keyGreen,
			"yellow": self.keyYellow,
			"blue": self.keyBlue,
			
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Softcam"))
		self["key_yellow"] = StaticText(_("Tools"))
		self["key_blue"] = StaticText(_("Install"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/softcam.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/cardserver.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/tools.png"))
		backuppng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/backup.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/install.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/epp2.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/system.png"))
		sevenpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/addon.png"))
		self.list.append((_("Simple Softcam/Cardserver"), 1, _("Start, Stop, Restart Sofcam/Cardserver"), onepng))
		self.list.append((_("Service Tools"), 2, _("Manage epg, ntp, unmount, script, info ..."), twopng ))
		self.list.append((_("System Tools"), 3, _("kernel modules manager, manage swap, ftp, samba, unmount USB"), sixpng ))
		self.list.append((_("Manual Installer/Uninstaller"), 4, _("install/uninstall local .ipk & .tar.gz files from /tmp"), treepng))
		if config.plugins.epanel.showpbmain.value:
			self.list.append((_("Plugin Browser"), 5, _("Install & Remove Plugins, Addons, Softcams"), sevenpng))
		self.list.append((_("E-Panel Config"), 6, _("config menu and extentionsmenu foe E-Panel items"), fourpng))
		if self.indexpos != None:
			self["menu"].setIndex(self.indexpos)
		self["menu"].setList(self.list)

	def exit(self):
		self.close()

	def keyOK(self, item = None):
		self.indexpos = self["menu"].getIndex()
		if item == None:
			item = self["menu"].getCurrent()[1]
			if item is 1:
				self.session.open(emuman.SoftcamPanel2)
			elif item is 2:
				self.session.open(tools.ToolsScreen2)
			elif item is 3:
				self.session.open(tools.SystemScreen)
			elif item is 4:
				self.session.open(minstall.IPKToolsScreen2)
			elif item is 5:
				self.session.open(PluginBrowser)
			elif item is 6:
				self.session.open(ConfigExtentions2)
			else:
				self.close(None)

	def keyBlue (self):
		self.session.open(minstall.IPKToolsScreen2)
				
	def keyYellow (self):
		self.session.open(tools.ToolsScreen2)
		
	def keyGreen (self):
		self.session.open(emuman.emuSel4)
	
	def infoKey (self):
		self.session.openWithCallback(self.mList,epanelinfo)
######################################################################################
class epanelinfo(Screen):
	skin = """
<screen name="epanelinfo" position="center,105" size="600,570" title="E-Panel">
	<ePixmap position="20,562" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,532" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="MemoryLabel" render="Label" position="20,375" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="SwapLabel" render="Label" position="20,400" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="FlashLabel" render="Label" position="20,425" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="memTotal" render="Label" position="180,375" zPosition="2" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="swapTotal" render="Label" position="180,400" zPosition="2" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="flashTotal" render="Label" position="180,425" zPosition="2" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="deviceLabel" render="Label" position="20,250" size="200,22" font="Regular; 20" halign="left" foregroundColor="#aaaaaa" />
	<widget source="device" render="Label" position="20,275" zPosition="2" size="560,88" font="Regular;20" halign="left" valign="top" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Hardware" render="Label" position="230,10" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Image" render="Label" position="230,35" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Kernel" render="Label" position="230,60" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="EnigmaVersion" render="Label" position="230,110" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="HardwareLabel" render="Label" position="20,10" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="ImageLabel" render="Label" position="20,35" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="KernelLabel" render="Label" position="20,59" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="EnigmaVersionLabel" render="Label" position="20,110" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="nimLabel" render="Label" position="20,145" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="nim" render="Label" position="20,170" zPosition="2" size="500,66" font="Regular;20" halign="left" valign="top" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="driver" render="Label" position="230,85" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="driverLabel" render="Label" position="20,85" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<eLabel position="30,140" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="30,242" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="30,367" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="30,454" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="230,494" size="320,2" backgroundColor="#aaaaaa" />
	<ePixmap position="20,463" size="180,47" zPosition="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/2boom.png" alphatest="blend" />
	<widget source="panelver" render="Label" position="470,463" zPosition="2" size="100,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="plipanel" render="Label" position="215,463" zPosition="2" size="250,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="cardserver" render="Label" position="350,528" zPosition="2" size="225,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="cardserverLabel" render="Label" position="215,528" zPosition="2" size="130,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="softcam" render="Label" position="350,503" zPosition="2" size="225,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="softcamLabel" render="Label" position="215,503" zPosition="2" size="130,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("E-Panel"))
		self.iConsole = iConsole()
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.cancel,
			"back": self.cancel,
			"red": self.cancel,
			"ok": self.cancel,
			})
		self["key_red"] = StaticText(_("Close"))
		self["MemoryLabel"] = StaticText(_("Memory:"))
		self["SwapLabel"] = StaticText(_("Swap:"))
		self["FlashLabel"] = StaticText(_("Flash:"))
		self["memTotal"] = StaticText()
		self["swapTotal"] = StaticText()
		self["flashTotal"] = StaticText()
		self["device"] = StaticText()
		self["deviceLabel"] = StaticText(_("Devices:"))
		self["Hardware"] = StaticText()
		self["Image"] = StaticText()
		self["Kernel"] = StaticText()
		self["nim"] = StaticText()
		self["nimLabel"] = StaticText(_("Detected NIMs:"))
		self["EnigmaVersion"] = StaticText()
		self["HardwareLabel"] = StaticText(_("Hardware:"))
		self["ImageLabel"] = StaticText(_("Image:"))
		self["KernelLabel"] = StaticText(_("Kernel Version:"))
		self["EnigmaVersionLabel"] = StaticText(_("Last Upgrade:"))
		self["driver"] = StaticText()
		self["driverLabel"] = StaticText(_("Driver Version:"))
		self["plipanel"] = StaticText(_("E-Panel Ver:"))
		self["panelver"] = StaticText()
		self["softcamLabel"] = StaticText(_("Softcam:"))
		self["softcam"] = StaticText()
		self["cardserverLabel"] = StaticText(_("Cardserver:"))
		self["cardserver"] = StaticText()
		self.memInfo()
		self.FlashMem()
		self.devices()
		self.mainInfo()
		self.verinfo()
		self.emuname()
		
	def status(self):
		path = ' '
		if fileExists("/usr/lib/opkg/status"):
			path = "/usr/lib/opkg/status"
		elif fileExists("/var/lib/opkg/status"):
			path = "/var/lib/opkg/status"
		elif fileExists("/var/opkg/status"):
			path = "/var/opkg/status"
		return path
		
	def emuname(self):
		nameemu = []
		namecard = []
		if fileExists("/etc/init.d/softcam"):
			for line in open("/etc/init.d/softcam"):
				if "echo" in line:
					nameemu.append(line)
			try:
				self["softcam"].text =  "%s" % nameemu[1].split('"')[1]
			except:
				self["softcam"].text =  "Not Active"
		else:
			self["softcam"].text = _("Not Installed")
		if fileExists("/etc/init.d/cardserver"):
			for line in open("/etc/init.d/cardserver"):
				if "echo" in line:
					namecard.append(line)
			try:
				self["cardserver"].text = "%s" % namecard[1].split('"')[1]
			except:
				self["softcam"].text =  "Not Active"
		else:
			self["cardserver"].text = _("Not Installed")
		
	def devices(self):
		list = ""
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				hdd = hddlist[count][1]
				if int(hdd.free()) > 1024:
					list += ((_("%s  %s  (%d.%03d GB free)\n") % (hdd.model(), hdd.capacity(), hdd.free()/1024 , hdd.free()%1024)))
				else:
					list += ((_("%s  %s  (%03d MB free)\n") % (hdd.model(), hdd.capacity(),hdd.free())))
		else:
			hddinfo = _("none")
		self["device"].text = list
		
	def HardWareType(self):
		if os.path.isfile("/proc/stb/info/boxtype"):
			return open("/proc/stb/info/boxtype").read().strip().upper()
		if os.path.isfile("/proc/stb/info/vumodel"):
			return "VU+" + open("/proc/stb/info/vumodel").read().strip().upper()
		if os.path.isfile("/proc/stb/info/model"):
			return open("/proc/stb/info/model").read().strip().upper()
		return _("unavailable")
		
	def mainInfo(self):
		listnims = ""
		package = 0
		self["Hardware"].text = self.HardWareType()
		self["Image"].text = about.getImageTypeString()
		self["Kernel"].text = about.getKernelVersionString()
		self["EnigmaVersion"].text = about.getImageVersionString()
		nims = nimmanager.nimList()
		for count in range(len(nims)):
			if count < 4:
				listnims += "%s\n" % nims[count]
			else:
				listnims += "\n"
		self["nim"].text = listnims
		for line in open(self.status()):
			if "-dvb-modules" in line and "Package:" in line:
				package = 1
			if "Version:" in line and package == 1:
				package = 0
				self["driver"].text = line.split()[1]
				break

	def memInfo(self):
		for line in open("/proc/meminfo"):
			if "MemTotal:" in line:
				memtotal = line.split()[1]
			elif "MemFree:" in line:
				memfree = line.split()[1]
			elif "SwapTotal:" in line:
				swaptotal =  line.split()[1]
			elif "SwapFree:" in line:
				swapfree = line.split()[1]
		self["memTotal"].text = _("Total: %s Kb  Free: %s Kb") % (memtotal, memfree)
		self["swapTotal"].text = _("Total: %s Kb  Free: %s Kb") % (swaptotal, swapfree)
		
	def FlashMem(self):
		self.iConsole.ePopen("df | grep root", self.rootfs_info)
	
	def rootfs_info(self, result, retval, extra_args):
		if retval is 0:
			for line in result.splitlines():
				if "rootfs" in line:
					self["flashTotal"].text = _("Total: %s Kb  Free: %s Kb") % (line.split()[1], line.split()[3])

	def verinfo(self):
		package = 0
		self["panelver"].text = " "
		for line in open(self.status()):
			if "epanel" in line:
				package = 1
			if "Version:" in line and package is 1:
				package = 0
				self["panelver"].text = line.split()[1]
				break
		
	def cancel(self):
		self.close()
######################################################################################
class ConfigExtentions2(ConfigListScreen, Screen):
	skin = """
<screen name="ConfigExtentions2" position="center,160" size="750,370" title="E-Panel Menu/Extensionmenu config">
		<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("E-Panel Menu/Extensionmenu config"))
		self.list = []
		self.list.append(getConfigListEntry(_("Show E-Panel in MainMenu"), config.plugins.epanel.showmain))
		self.list.append(getConfigListEntry(_("Show E-Panel in ExtensionMenu"), config.plugins.epanel.showepanelmenu))
		self.list.append(getConfigListEntry(_("Show E-SoftCam manager in ExtensionMenu"), config.plugins.epanel.showextsoft))
		self.list.append(getConfigListEntry(_("Show E-CrashLog viewr in ExtensionMenu"), config.plugins.epanel.showclviewer))
		self.list.append(getConfigListEntry(_("Show E-Script Executter in ExtensionMenu"), config.plugins.epanel.showscriptex))
		self.list.append(getConfigListEntry(_("Show E-Usb Unmount in ExtensionMenu"), config.plugins.epanel.showusbunmt))
		self.list.append(getConfigListEntry(_("Show E-Installer in ExtensionMenu"), config.plugins.epanel.showsetupipk))
		self.list.append(getConfigListEntry(_("Show reload epg.dat in ExtensionMenu"), config.plugins.epanel.showepgreload))
		self.list.append(getConfigListEntry(_("Show E-EPG Downloader in ExtensionMenu"), config.plugins.epanel.showepgdwnload))
		self.list.append(getConfigListEntry(_("Show PluginBrowser in E-Panel MainMenu"), config.plugins.epanel.showpbmain))
		self.list.append(getConfigListEntry(_("E-Installer: User directory on mount device"), config.plugins.epanel.userdir))
		self.list.append(getConfigListEntry(_("E-Installer: Selection mode"), config.plugins.epanel.multifilemode))
		self.list.append(getConfigListEntry(_("Filter by Name in download extentions"), config.plugins.epanel.filtername))
		self.list.append(getConfigListEntry(_("Crashlog viewer path"), config.plugins.epanel.crashpath))
		self.list.append(getConfigListEntry(_("E-script path"), config.plugins.epanel.scriptpath))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"ok": self.save
		}, -2)
		
	def cancel(self):
		self.close(False)

	
	def save(self):
		from Components.PluginComponent import plugins
		plugins.reloadPlugins()
		for i in self["config"].list:
			i[1].save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
######################################################################################
class loadEPG():
	def __init__(self):
		self.dialog = None

	def gotSession(self, session):
		self.session = session
		self.iConsole = iConsole()
		self.timer = enigma.eTimer() 
		self.timer.callback.append(self.update)
		self.timer.start(60000, True)
	
	def restore_epgfile(self):
		self.iConsole.ePopen("cp -f %sepgtmp/epg.dat.gz %s && gzip -df %sepg.dat.gz" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value, config.plugins.epanel.direct.value), self.check_epgfile)
		
	def check_epgfile(self, result, retval, extra_args):
		if retval is 0:
			if fileExists("%sepg.dat" % config.plugins.epanel.direct.value):
				self.iConsole.ePopen("chmod 644 %sepg.dat" % config.plugins.epanel.direct.value)
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()

	def update(self):
		self.timer.stop()
		time_min = 0
		now = time.localtime(time.time())
		if config.plugins.epanel.checkepgfile.value:
			if not fileExists("%sepg.dat" % config.plugins.epanel.direct.value):
				if fileExists("%sepgtmp/epg.dat.gz" % config.plugins.epanel.direct.value):
					self.restore_epgfile()
		if (config.plugins.epanel.auto.value == "yes" and config.plugins.epanel.timedwn.value[0] == now.tm_hour and config.plugins.epanel.timedwn.value[1] == now.tm_min and int(config.plugins.epanel.weekday.value) == int(now.tm_wday)):
			self.dload()
		if config.plugins.epanel.autosave.value is not '0':
			if min > int(config.plugins.epanel.autosave.value) and config.plugins.epanel.timedwn.value[1] != now.tm_min:
				global min
				min = 0
				self.save_load_epg()
				if config.plugins.epanel.autobackup.value:
					self.autobackup()
			else:
				global min
				min += 1
		if config.plugins.epanel.onoff.value is '1':
			time_min = int(config.plugins.epanel.time.value)
			if time_min == 30:
				time_min = 30
			else:
				time_min = time_min * 60
			if min_ntp > time_min:
				global min_ntp
				min_ntp = 0
				self.ntd_time_update()
			else:
				global min_ntp
				min_ntp += 1
		self.timer.start(60000, True)
	
	def ntd_time_update(self):
		if config.plugins.epanel.onoff.value is '1':
			if config.plugins.epanel.manual.value is '1':
				self.iConsole.ePopen("/usr/bin/ntpdate -v -u %s" % config.plugins.epanel.server.value)
			else:
				self.iConsole.ePopen("/usr/bin/ntpdate -v -u %s" % config.plugins.epanel.manualserver.value)
			
	def autobackup(self):
		self.iConsole.ePopen("gzip -c %sepg.dat > %sepgtmp/epg.dat.gz" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value))
		
	def save_load_epg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_save,None,eEPGCache)
		epgcache = eEPGCache.getInstance().save()
		
	def dload(self):
		if config.plugins.epanel.direct_source.value is '0':
			self.iConsole.ePopen("wget -q http://linux-sat.tv/epg/epg_%s.dat.gz -O %sepg.dat.gz" % (config.plugins.epanel.lang.value, config.plugins.epanel.direct.value), self.remove_epgfile)
		else:
			self.iConsole.ePopen("wget -q http://piconload.ru/upload/epg/epg_new.dat.gz -O %sepg.dat.gz" % config.plugins.epanel.direct.value, self.remove_epgfile)
		
	def remove_epgfile(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("mkdir -p %sepgtmp && rm -f %sepg.dat" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value), self.copy_tmp)
		
	def copy_tmp(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("cp -f %sepg.dat.gz %sepgtmp" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value), self.unpack_zip)
			
	def unpack_zip(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("gzip -df %sepg.dat.gz " % config.plugins.epanel.direct.value, self.attr_epgfile)
			
	def attr_epgfile(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("chmod 644 %sepg.dat" % config.plugins.epanel.direct.value, self.loadepg)
			
	def loadepg(self, result, retval, extra_args):
		if retval is 0:
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
			self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )
######################################################################################
pEmu = loadEPG()
######################################################################################
def sessionstart(reason,session=None, **kwargs):
	if reason == 0:
		pEmu.gotSession(session)
######################################################################################
def main(session, **kwargs):
	session.open(easyPanel2)

def menu(menuid, **kwargs):
	if menuid == "mainmenu":
		return [(_("E-Panel"), main, _("e-panel_"), 48)]
	return []

def extsoft(session, **kwargs):
	session.open(emuman.emuSel4)
	
def clviewer(session, **kwargs):
	session.open(tools.CrashLogScreen)
	
def scriptex(session, **kwargs):
	session.open(tools.ScriptScreen2)
	
def epgreload(session, **kwargs):
	session.open(tools.epgdmanual)
	
def epgdwnload(session, **kwargs):
	session.open(tools.epgdn)

def usbunmt(session, **kwargs):
	session.open(tools.UsbScreen)
	
def setupipk(session, **kwargs):
	session.open(minstall.InstallAll4)
	
def mgcamd_sw(session, **kwargs):
	config.plugins.usw.activeconf.value = config.plugins.uswmgcamd.activeconf.value
	config.plugins.usw.configpath.value = config.plugins.uswmgcamd.configpath.value
	config.plugins.usw.emu.value = "Mgcamd"
	config.plugins.usw.configfile.value = config.plugins.uswmgcamd.configfile.value
	config.plugins.usw.configext.value = config.plugins.uswmgcamd.configext.value
	session.open(emuman.uniswitcher)
	
def wicardd_sw(session, **kwargs):
	config.plugins.usw.activeconf.value = config.plugins.uswwicardd.activeconf.value
	config.plugins.usw.configpath.value = config.plugins.uswwicardd.configpath.value
	config.plugins.usw.emu.value = "Wicardd"
	config.plugins.usw.configfile.value = config.plugins.uswwicardd.configfile.value
	config.plugins.usw.configext.value = config.plugins.uswwicardd.configext.value
	session.open(emuman.uniswitcher)
	
def oscam_sw(session, **kwargs):
	config.plugins.usw.activeconf.value = config.plugins.uswoscam.activeconf.value
	config.plugins.usw.configpath.value = config.plugins.uswoscam.configpath.value
	config.plugins.usw.emu.value = "Oscam"
	config.plugins.usw.configfile.value = config.plugins.uswoscam.configfile.value
	config.plugins.usw.configext.value = config.plugins.uswoscam.configext.value
	session.open(emuman.uniswitcher)
	
def cccam_sw(session, **kwargs):
	config.plugins.usw.activeconf.value = config.plugins.uswcccam.activeconf.value
	config.plugins.usw.configpath.value = config.plugins.uswcccam.configpath.value
	config.plugins.usw.emu.value = "CCcam"
	config.plugins.usw.configfile.value = config.plugins.uswcccam.configfile.value
	config.plugins.usw.configext.value = config.plugins.uswcccam.configext.value
	session.open(emuman.uniswitcher)
	
def Plugins(**kwargs):
	list = [PluginDescriptor(name=_("E-Panel"), description=_("set of utilities for enigma2"), where = [PluginDescriptor.WHERE_PLUGINMENU], icon="epp.png", fnc=main)]
	if config.plugins.epanel.showepanelmenu.value:
		list.append(PluginDescriptor(name=_("E-Panel"), description=_("set of utilities for enigma2"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=main))
	if config.plugins.epanel.showextsoft.value:
		list.append(PluginDescriptor(name=_("E-SoftCam manager"), description=_("Start, Stop, Restart Sofcam/Cardserver"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=extsoft))
	if config.plugins.uswmgcamd.active.value:
		list.append(PluginDescriptor(name=_("E-Newcamd.list switcher"), description=_("Switch newcamd.list with remote conrol"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=mgcamd_sw))
	if config.plugins.uswwicardd.active.value:
		list.append(PluginDescriptor(name=_("E-Wicardd.conf switcher"), description=_("Switch wicardd.conf with remote conrol"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=wicardd_sw))
	if config.plugins.epanel.showclviewer.value:
		list.append(PluginDescriptor(name=_("E-Crashlog viewer"), description=_("Switch newcamd.list with remote conrol"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=clviewer))
	if config.plugins.epanel.showscriptex.value:
		list.append(PluginDescriptor(name=_("E-Script Executer"), description=_("Start scripts from /usr/script"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=scriptex))
	if config.plugins.epanel.showepgreload.value:
		list.append(PluginDescriptor(name=_("E-Reload epg.dat"), description=_("Reload epg.dat"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=epgreload))
	if config.plugins.epanel.showepgdwnload.value:
		list.append(PluginDescriptor(name=_("E-EPG Downloader"), description=_("EPG Downloader"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=epgdwnload))
	if config.plugins.epanel.showusbunmt.value:
		list.append(PluginDescriptor(name=_("E-Unmount USB"), description=_("Unmount usb devices"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=usbunmt))
	if config.plugins.epanel.showsetupipk.value:
		list.append(PluginDescriptor(name=_("E-Installer"), description=_("install & forced install ipk, bh.tgz, tar.gz, nab.tgz from /tmp"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=setupipk))
	if config.plugins.epanel.showmain.value:
		list.append(PluginDescriptor(name=_("E-Panel"), description=_("E-Panel"), where = [PluginDescriptor.WHERE_MENU], fnc=menu))
	if config.plugins.uswoscam.active.value:
		list.append(PluginDescriptor(name= _("E-Oscam.conf switcher"), description= _("Switch oscam condig with remote control"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=oscam_sw))
	if config.plugins.uswcccam.active.value:
		list.append(PluginDescriptor(name= _("E-CCcam.Cfg switcher"), description= _("Switch cccam condig with remote control"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=cccam_sw))
	list.append(PluginDescriptor(name=_("E-Panel"), description=_("E-Panel"), where = [PluginDescriptor.WHERE_AUTOSTART, PluginDescriptor.WHERE_SESSIONSTART], fnc = sessionstart))
	return list


