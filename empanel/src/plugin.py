#Emicro Panel (c)2boom 2012-13
from enigma import eConsoleAppContainer, eDVBDB
from Components.MenuList import MenuList
from Screens.Screen import Screen
from Components.PluginComponent import plugins
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Components.Input import Input
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Harddisk import harddiskmanager
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.ConfigList import ConfigListScreen
from Tools.Directories import fileExists
from Screens.Standby import TryQuitMainloop
from enigma import eTimer
from os import environ
from time import *
import gettext
import time
import datetime
import os
from enigma import eEPGCache, getDesktop
from types import *
from enigma import *
import sys, traceback
import re
import new
import _enigma
import enigma

global min
min = 0

adress = "http://gisclub.tv/gi/softcam/SoftCam.Key"
pluginpath = "/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/"

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("EMPanel", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/EM-Panel/locale/"))

def _(txt):
	t = gettext.dgettext("EMPanel", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t
######################################################################################
skin_hd_EMMain = """
<screen name="EMMain" position="center,140" size="750,460" title="EMicro Panel (c)2boom">
<ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
<ePixmap position="180,455" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
<ePixmap position="380,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
 <ePixmap position="550,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="550,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />

<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="key_yellow" render="Label" position="380,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="key_green" render="Label" position="180,425" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="menu" render="Listbox" position="15,10" size="720,400" scrollbarMode="showOnDemand">
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
</screen>"""
skin_sd_EMMain = """
<screen name="EMMain" position="center,60" size="560,460" title="EMicro Panel (c)2boom">
  <ePixmap position="5,455" zPosition="1" size="130,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <ePixmap position="135,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <ePixmap position="305,455" zPosition="1" size="130,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
<ePixmap position="435,455" zPosition="1" size="130,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="5,425" zPosition="2" size="130,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <widget source="key_yellow" render="Label" position="305,425" zPosition="2" size="130,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <widget source="key_green" render="Label" position="135,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
 <widget source="key_blue" render="Label" position="435,425" zPosition="2" size="130,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <widget source="menu" render="Listbox" position="5,10" size="550,400" scrollbarMode="showOnDemand">
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
</screen>"""

skin_hd_EMInstall = """
<screen name="EMInstall" position="center,140" size="750,460" title="EMicro Manual Installer">
<widget source="menu" render="Listbox" position="15,10" size="720,400" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
}
</convert>
</widget>
<ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" transparent="1" alphatest="on" />
<ePixmap position="180,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" transparent="1" alphatest="on" />
<ePixmap position="350,455" zPosition="1" size="225,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" transparent="1" alphatest="on" />
<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
<widget source="key_green" render="Label" position="180,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
<widget source="key_yellow" render="Label" position="350,425" zPosition="2" size="225,30" valign="center" halign="center" font="Regular;20" transparent="1" />
</screen>"""
skin_sd_EMInstall = """
<screen name="EMInstall" position="center,60" size="560,460" title="EMicro Manual Installer">
<widget source="menu" render="Listbox" position="5,10" size="550,400" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
}
</convert>
</widget>
<ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" transparent="1" alphatest="on" />
<ePixmap position="180,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" transparent="1" alphatest="on" />
<ePixmap position="350,455" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" transparent="1" alphatest="on" />
<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
<widget source="key_green" render="Label" position="180,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
<widget source="key_yellow" render="Label" position="350,425" zPosition="2" size="200,30" valign="center" halign="center" font="Regular;20" transparent="1" />
</screen>"""

skin_hd_EMUninst = """
<screen name="EMUninst" position="center,140" size="750,460" title="EMicro Uninstaller">
<widget source="menu" position="20,10" render="Listbox" size="710,400">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap position="20,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" transparent="1" alphatest="on" />
	<ePixmap position="360,455" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
	<widget source="key_green" render="Label" position="180,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
	<widget source="key_yellow" render="Label" position="350,425" zPosition="2" size="200,30" valign="center" halign="center" font="Regular;20" transparent="1" />
</screen>"""
skin_sd_EMUninst = """
<screen name="EMUninst" position="center,60" size="560,460" title="EMicro Uninstaller">
<widget source="menu" position="5,10" render="Listbox" size="550,400">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap position="20,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" transparent="1" alphatest="on" />
	<ePixmap position="360,455" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
	<widget source="key_green" render="Label" position="180,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
	<widget source="key_yellow" render="Label" position="350,425" zPosition="2" size="200,30" valign="center" halign="center" font="Regular;20" transparent="1" />
</screen>"""

skin_hd_EMSoftcam = """
<screen name="EMSoftcam" position="center,140" size="750,460" title="EMicro SoftCam/CardServer">
  <widget source="menu" render="Listbox" position="15,10" size="720,200" scrollbarMode="showOnDemand">
    <convert type="TemplatedMultiContent">
  {"template": [
  MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
  MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
  MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
  ],
"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
"itemHeight": 50
}
</convert>
  </widget>
  <ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" transparent="1" alphatest="on" />
  <ePixmap position="180,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" transparent="1" alphatest="on" />
  <ePixmap position="350,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" transparent="1" alphatest="on" />
<ePixmap position="520,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue.png" transparent="1" alphatest="on" />
  <widget name="key_red" position="10,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
  <widget name="key_green" position="180,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
  <widget name="key_yellow" position="350,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
<widget name="key_blue" position="520,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
  <widget name="text" position="20,225" size="710,205" font="Console; 22" noWrap="1" halign="center" valign="top" />
  <eLabel position="30,217" size="690,2" backgroundColor="grey" zPosition="5" />
</screen>"""
skin_sd_EMSoftcam = """
<screen name="EMSoftcam" position="center,60" size="560,460" title="EMicro SoftCam/CardServer">
  <widget source="menu" render="Listbox" position="5,10" size="550,200" scrollbarMode="showOnDemand">
    <convert type="TemplatedMultiContent">
  {"template": [
  MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
  MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
  MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
  ],
"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
"itemHeight": 50
}
</convert>
  </widget>
  <ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" transparent="1" alphatest="on" />
  <ePixmap position="180,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" transparent="1" alphatest="on" />
  <ePixmap position="350,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" transparent="1" alphatest="on" />
<ePixmap position="527,427" zPosition="3" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue_key.png" transparent="1" alphatest="blend" />
  <widget name="key_red" position="10,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
  <widget name="key_green" position="180,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
  <widget name="key_yellow" position="350,425" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;20" transparent="1" />
  <widget name="text" position="5,225" size="550,205" font="Console; 17" noWrap="1" halign="center" valign="top" />
  <eLabel position="10,217" size="540,2" backgroundColor="grey" zPosition="5" />
</screen>"""

skin_hd_EMSwapScreen = """
<screen name="EMSwapScreen" position="center,140" size="750,460" title="EMicro Swap Menager">
<ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="menu" render="Listbox" position="20,10" size="710,400" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
{"template": [
	MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
	MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
	MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
	],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
</convert>
</widget>
</screen>"""
skin_sd_EMSwapScreen = """
<screen name="EMSwapScreen" position="center,60" size="560,460" title="EMicro Swap Menager">
<ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="menu" render="Listbox" position="5,10" size="550,400" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
{"template": [
	MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
	MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
	MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
	],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
</convert>
</widget>
</screen>"""

skin_hd_EMSwapScreen2 = """
<screen name="EMSwapScreen2" position="center,140" size="750,460" title="EMicro Swap Menager">
<ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="menu" render="Listbox" position="20,10" size="710,400" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
{"template": [
	MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
	MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
	MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 3), # index 4 is the pixmap
		],
"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
"itemHeight": 50
}
</convert>
</widget>
</screen>"""
skin_sd_EMSwapScreen2 = """
<screen name="EMSwapScreen2" position="center,60" size="560,460" title="EMicro Swap Menager">
<ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="menu" render="Listbox" position="5,10" size="550,400" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
{"template": [
	MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
	MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
	MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 3), # index 4 is the pixmap
		],
"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
"itemHeight": 50
}
</convert>
</widget>
</screen>"""

skin_hd_EMUsbUmount = """
<screen name="EMUsbUmount" position="center,140" size="750,460" title="EMicro USB Unmount">
<ePixmap position="20,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
<widget source="key_red" render="Label" position="20,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="key_green" render="Label" position="190,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="key_yellow" render="Label" position="360,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<ePixmap position="190,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
<ePixmap position="360,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
<widget source="menu" render="Listbox" position="20,10" size="710,400" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
{"template": [
	MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
	MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
	MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
			],
"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
"itemHeight": 50
}
</convert>
</widget>
</screen>"""
skin_sd_EMUsbUmount = """
<screen name="EMUsbUmount" position="center,60" size="560,460" title="EMicro USB Unmount">
<ePixmap position="20,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
<widget source="key_red" render="Label" position="20,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="key_green" render="Label" position="190,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<widget source="key_yellow" render="Label" position="360,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
<ePixmap position="190,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
<ePixmap position="360,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
<widget source="menu" render="Listbox" position="5,10" size="550,400" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
{"template": [
	MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
	MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
	MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
			],
"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
"itemHeight": 50
}
</convert>
</widget>
</screen>"""

skin_hd_EMScriptScreen = """
<screen name="EMScriptScreen" position="center,140" size="750,460" title="EMicro Script Executer">
	<widget name="list" position="20,10" size="710,400" scrollbarMode="showOnDemand" />
	<ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
skin_sd_EMScriptScreen = """
<screen name="EMScriptScreen" position="center,60" size="560,460" title="EMicro Script Executer">
	<widget name="list" position="5,10" size="550,400" scrollbarMode="showOnDemand" />
	<ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

skin_hd_EMNTPScreen = """
<screen name="EMNTPScreen" position="center,140" size="750,460" title="EMicro NTP Menager">
 <widget position="15,10" size="720,400" name="config" scrollbarMode="showOnDemand" />
 <ePixmap position="10,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
 <widget source="key_red" render="Label" position="10,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
 <ePixmap position="180,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
 <widget source="key_green" render="Label" position="180,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
 <ePixmap position="350,455" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
 <widget source="key_yellow" render="Label" position="350,425" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
 <ePixmap position="545,455" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue.png" alphatest="blend" />
 <widget source="key_blue" render="Label" position="545,425" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
skin_sd_EMNTPScreen = """
<screen name="EMNTPScreen" position="center,60" size="560,460" title="EMicro NTP Menager">
  <widget position="5,10" size="550,400" name="config" scrollbarMode="showOnDemand" />
  <ePixmap position="5,455" zPosition="1" size="120,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="5,425" zPosition="2" size="120,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="125,455" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="125,425" zPosition="2" size="120,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="245,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="245,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="415,455" zPosition="1" size="145,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="415,425" zPosition="2" size="145,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

skin_hd_EMEPG = """
<screen name="EMEPG" position="center,140" size="750,460" title="EMicro EPG downloader">
  <widget position="15,10" size="720,400" name="config" scrollbarMode="showOnDemand" />
  <ePixmap position="10,455" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,425" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,455" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,425" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,455" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,425" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="541,455" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="541,425" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
skin_sd_EMEPG = """
<screen name="EMEPG" position="center,60" size="560,460" title="EMicro EPG downloader">
  <widget position="5,10" size="550,400" name="config" scrollbarMode="showOnDemand" />
  <ePixmap position="5,455" zPosition="1" size="120,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="5,425" zPosition="2" size="120,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="125,455" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="125,425" zPosition="2" size="120,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="245,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="245,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="415,455" zPosition="1" size="145,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="415,425" zPosition="2" size="145,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

skin_hd_EMEPGMAN = """
<screen name="EMEPGMAN" position="center,260" size="850,50" title="EPG from linux-sat.tv (exUSSR)">
  <ePixmap position="10,40" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,10" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,40" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,10" zPosition="2" size="220,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="395,40" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="395,10" zPosition="2" size="220,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="614,40" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="614,10" zPosition="2" size="220,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
skin_sd_EMEPGMAN = """
<screen name="EMEPGMAN" position="center,260" size="460,95" title="EPG from linux-sat.tv (exUSSR)">
  <ePixmap position="10,40" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,10" zPosition="2" size="220,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="230,40" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="230,10" zPosition="2" size="220,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="10,80" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="10,50" zPosition="2" size="220,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="230,80" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="230,50" zPosition="2" size="220,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
skin_hd_EMConfigScreen = """
<screen name="EMConfigScreen" position="center,140" size="750,460" title="EMicro Show in ExtentionMenu">
  <widget position="15,10" size="720,400" name="config" scrollbarMode="showOnDemand" />
  <ePixmap position="10,455" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,425" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,455" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,425" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
skin_sd_EMConfigScreen = """
<screen name="EMConfigScreen" position="center,60" size="560,460" title="EMicro Show in ExtentionMenu">
  <widget position="5,10" size="550,400" name="config" scrollbarMode="showOnDemand" />
  <ePixmap position="10,455" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,425" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,455" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,425" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
skin_hd_EMSoftcamUpd = """
<screen name="EMSoftcamUpd" position="center,140" size="750,460" title="SoftCam.Key Updater">
  <widget position="15,10" size="720,400" name="config" scrollbarMode="showOnDemand" />
  <ePixmap position="10,455" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,425" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,455" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,425" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,455" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,425" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
skin_sd_EMSoftcamUpd = """
<screen name="EMSoftcamUpd" position="center,60" size="560,460" title="SoftCam.Key Updater">
  <widget position="5,10" size="550,400" name="config" scrollbarMode="showOnDemand" />
  <ePixmap position="5,455" zPosition="1" size="120,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="5,425" zPosition="2" size="120,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="125,455" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="125,425" zPosition="2" size="120,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="245,455" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EM-Panel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="245,425" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
######################################################################################
config.plugins.empanel = ConfigSubsection()
config.plugins.empanel.manual = ConfigSelection(default = "0", choices = [
		("0", _("Auto")),
		("1", _("Manual")),
		])
config.plugins.empanel.manualserver = ConfigText(default="ntp.ubuntu.com", visible_width = 70, fixed_size = False)
config.plugins.empanel.server = ConfigSelection(default = "ua.pool.ntp.org", choices = [
		("ao.pool.ntp.org",_("Angola")),
		("mg.pool.ntp.org",_("Madagascar")),
		("za.pool.ntp.org",_("South Africa")),
		("tz.pool.ntp.org",_("Tanzania")),
		("bd.pool.ntp.org",_("Bangladesh")),
		("cn.pool.ntp.org",_("China")),
		("hk.pool.ntp.org",_("Hong Kong")),
		("in.pool.ntp.org",_("India")),
		("id.pool.ntp.org",_("Indonesia")),
		("ir.pool.ntp.org",_("Iran")),
		("jp.pool.ntp.org",_("Japan")),
		("kz.pool.ntp.org",_("Kazakhstan")),
		("kr.pool.ntp.org",_("Korea")),
		("my.pool.ntp.org",_("Malaysia")),
		("pk.pool.ntp.org",_("Pakistan")),
		("ph.pool.ntp.org",_("Philippines")),
		("sg.pool.ntp.org",_("Singapore")),
		("tw.pool.ntp.org",_("Taiwan")),
		("th.pool.ntp.org",_("Thailand")),
		("tr.pool.ntp.org",_("Turkey")),
		("ae.pool.ntp.org",_("United Arab Emirates")),
		("uz.pool.ntp.org",_("Uzbekistan")),
		("vn.pool.ntp.org",_("Vietnam")),
		("at.pool.ntp.org",_("Austria")),
		("by.pool.ntp.org",_("Belarus")),
		("be.pool.ntp.org",_("Belgium")),
		("bg.pool.ntp.org",_("Bulgaria")),
		("cz.pool.ntp.org",_("Czech Republic")),
		("dk.pool.ntp.org",_("Denmark")),
		("ee.pool.ntp.org",_("Estonia")),
		("fi.pool.ntp.org",_("Finland")),
		("fr.pool.ntp.org",_("France")),
		("de.pool.ntp.org",_("Germany")),
		("gr.pool.ntp.org",_("Greece")),
		("hu.pool.ntp.org",_("Hungary")),
		("ie.pool.ntp.org",_("Ireland")),
		("it.pool.ntp.org",_("Italy")),
		("lv.pool.ntp.org",_("Latvia")),
		("lt.pool.ntp.org",_("Lithuania")),
		("lu.pool.ntp.org",_("Luxembourg")),
		("mk.pool.ntp.org",_("Macedonia")),
		("md.pool.ntp.org",_("Moldova")),
		("nl.pool.ntp.org",_("Netherlands")),
		("no.pool.ntp.org",_("Norway")),
		("pl.pool.ntp.org",_("Poland")),
		("pt.pool.ntp.org",_("Portugal")),
		("ro.pool.ntp.org",_("Romania")),
		("ru.pool.ntp.org",_("Russian Federation")),
		("sk.pool.ntp.org",_("Slovakia")),
		("si.pool.ntp.org",_("Slovenia")),
		("es.pool.ntp.org",_("Spain")),
		("se.pool.ntp.org",_("Sweden")),
		("ch.pool.ntp.org",_("Switzerland")),
		("ua.pool.ntp.org",_("Ukraine")),
		("uk.pool.ntp.org",_("United Kingdom")),
		("bs.pool.ntp.org",_("Bahamas")),
		("ca.pool.ntp.org",_("Canada")),
		("gt.pool.ntp.org",_("Guatemala")),
		("mx.pool.ntp.org",_("Mexico")),
		("pa.pool.ntp.org",_("Panama")),
		("us.pool.ntp.org",_("United States")),
		("au.pool.ntp.org",_("Australia")),
		("nz.pool.ntp.org",_("New Zealand")),
		("ar.pool.ntp.org",_("Argentina")),
		("br.pool.ntp.org",_("Brazil")),
		("cl.pool.ntp.org",_("Chile")),
		])
config.plugins.empanel.onoff = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Yes")),
		])
config.plugins.empanel.time = ConfigSelection(default = "30", choices = [
		("30", _("30 min")),
		("1", _("60 min")),
		("2", _("120 min")),
		("3", _("180 min")),
		("4", _("240 min")),
		])
config.plugins.empanel.TransponderTime = ConfigSelection(default = "0", choices = [
		("0", _("Off")),
		("1", _("On")),
		])
config.plugins.empanel.cold = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Yes")),
		])
config.plugins.empanel.epgname = ConfigSelection(default = "epg.dat", choices = [
		("epg.dat", "epg.dat"),
		("epg_true.dat", "epg_true.dat"),
		])
config.plugins.empanel.e2shpatch = ConfigSelection(default = "no", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
config.plugins.empanel.direct = ConfigSelection(default = "/media/usb/", choices = [
		("/media/hdd/", _("/media/hdd/")),
		("/media/usb/", _("/media/usb/")),
		("/usr/share/enigma2/", _("/usr/share/enigma2/")),
])
config.plugins.empanel.auto = ConfigSelection(default = "no", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
config.plugins.empanel.lang = ConfigSelection(default = "ru", choices = [
		("ru", _("Russian")),
		("ua", _("Ukrainian")),
		])
config.plugins.empanel.timedwn = ConfigClock(default = ((16*60) + 15) * 60) # 18:15
config.plugins.empanel.weekday = ConfigSelection(default = "0", choices = [
		("0", _("Mo")),
		("1", _("Tu")),
		("2", _("We")),
		("3", _("Th")),
		("4", _("Fr")),
		("5", _("Sa")),
		("6", _("Su")),
		])
config.plugins.empanel.autosave = ConfigSelection(default = '0', choices = [
		('0', _("Off")),
		('29', _("30 min")),
		('59', _("60 min")),
		('119', _("120 min")),
		('179', _("180 min")),
		('239', _("240 min")),
		])
config.plugins.empanel.path = ConfigSelection(default = "/usr/keys/", choices = [
		("/usr/keys/", "/usr/keys/"),
		("/etc/keys/", "/etc/keys/"),
		("/etc/tuxbox/config/", "/etc/tuxbox/config/"),
		("/etc/tuxbox/config/oscam-stable/", "/etc/tuxbox/config/oscam-stable/"),
		])
config.plugins.empanel.keyname = ConfigSelection(default = "SoftCam.Key", choices = [
		("SoftCam.Key", "SoftCam.Key"),
		("oscam.keys", "oscam.keys"),
		("oscam.biss", "oscam.biss"),
		])

config.plugins.empanel.checkepgfile = ConfigYesNo(default = False)
config.plugins.empanel.autobackup = ConfigYesNo(default = False)
config.plugins.empanel.showemsoftcam = ConfigYesNo(default = True)
config.plugins.empanel.showeminstall = ConfigYesNo(default = True)
config.plugins.empanel.showemuninstall = ConfigYesNo(default = False)
config.plugins.empanel.showemswap = ConfigYesNo(default = False)
config.plugins.empanel.showemusb = ConfigYesNo(default = False)
config.plugins.empanel.showemntp = ConfigYesNo(default = False)
config.plugins.empanel.showemepg = ConfigYesNo(default = False)
config.plugins.empanel.showemepg2 = ConfigYesNo(default = True)
config.plugins.empanel.showemscript = ConfigYesNo(default = False)
config.plugins.empanel.showemmain = ConfigYesNo(default = True)
config.plugins.empanel.showemmainmenu = ConfigYesNo(default = True)
######################################################################
class EMMain(Screen):
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMMain
		else:
			self.skin = skin_sd_EMMain
		self.setTitle(_("EMicro Panel (c)2boom"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.keyok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.keygreen,
			"yellow": self.keyyellow,
			"blue": self.keyblue,
			
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Restart enigma"))
		self["key_yellow"] = StaticText(_("Clear /tmp"))
		self["key_blue"] = StaticText(_("Config"))
		self.list = []
		self["menu"] = List(self.list)
		self.menuList()
		
	def menuList(self):
		self.list = []
		self.list.append((_("EMicro SoftCam/CardServer"),"1", _("start, stop, restart Sofcam/Cardserver"), LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/softcam.png"))))
		self.list.append((_("EMicro Manual Installer"),"2", _("install ipk & tar.gz files from /tmp"), LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/tar.png")) ))
		self.list.append((_("EMicro Uninstaller"),"3", _("uninstall ipk packets"),  LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/removeipk.png")) ))
		self.list.append((_("EMicro Swap Menager"),"5", _("menage swap file"), LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/swap.png"))))
		self.list.append((_("EMicro USB Unmount"),"6", _("unmount usb devices"), LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/unusb.png"))))
		self.list.append((_("EMicro NTP Menager"),"4", _("time synchronization"), LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/ntp.png"))))
		self.list.append((_("EMicro EPG Downloader"),"7", _("dowload and menage epg from linux-sat.tv"), LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/epg.png"))))
		self.list.append((_("EMicro Script Executer"),"8", _("run user's script"), LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/script.png"))))
		self["menu"].setList(self.list)
		
	def keyok(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "1":
				self.session.open(EMSoftcam)
			elif returnValue is "2":
				self.session.open(EMInstall)
			elif returnValue is "3":
				self.session.open(EMUninst)
			elif returnValue is "4":
				self.session.open(EMNTPScreen)
			elif returnValue is "5":
				self.session.open(EMSwapScreen)
			elif returnValue is "6":
				self.session.open(EMUsbUmount)
			elif returnValue is "7":
				self.session.open(EMEPG)
			elif returnValue is "8":
				self.session.open(EMScriptScreen)
			else:
				self.close()
				
	def exit(self):
		self.close()
		
	def keyblue(self):
		self.session.open(EMConfigScreen)
		
	def keygreen(self):
		self.session.open(TryQuitMainloop, 3)
		
	def keyyellow(self):
		os.system("rm /tmp/*.tar.gz /tmp/*.bh.tgz /tmp/*.ipk /tmp/*.nab.tgz")
		self.mbox = self.session.open(MessageBox,_("*.tar.gz & *.bh.tgz & *.ipk removed"), MessageBox.TYPE_INFO, timeout = 4 )
#######################################################################################
class EMConfigScreen(ConfigListScreen, Screen):
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMConfigScreen
		else:
			self.skin = skin_sd_EMConfigScreen
		self.setTitle(_("EMicro Show in ExtentionMenu"))
		self.list = []
		self.list.append(getConfigListEntry(_("EMicro Panel in MainMenu"), config.plugins.empanel.showemmainmenu))
		self.list.append(getConfigListEntry(_("EMicro Panel"), config.plugins.empanel.showemmain))
		self.list.append(getConfigListEntry(_("EMicro SoftCam/CardServer"), config.plugins.empanel.showemsoftcam))
		self.list.append(getConfigListEntry(_("EMicro Manual Installer"), config.plugins.empanel.showeminstall))
		self.list.append(getConfigListEntry(_("EMicro Uninstaller"), config.plugins.empanel.showemuninstall))
		self.list.append(getConfigListEntry(_("EMicro Swap Menager"), config.plugins.empanel.showemswap))
		self.list.append(getConfigListEntry(_("EMicro USB Unmount"), config.plugins.empanel.showemusb))
		self.list.append(getConfigListEntry(_("EMicro NTP Menager"), config.plugins.empanel.showemntp))
		self.list.append(getConfigListEntry(_("EMicro EPG Downloader"), config.plugins.empanel.showemepg))
		self.list.append(getConfigListEntry(_("EMicro Reload epg.dat"), config.plugins.empanel.showemepg2))
		self.list.append(getConfigListEntry(_("EMicro Script Executer"), config.plugins.empanel.showemscript))
		#self.list.append(getConfigListEntry(_("Crontab path"), config.plugins.empanel.crontab))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"ok": self.save
		}, -2)

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)

	def save(self):
		from Components.PluginComponent import plugins
		plugins.reloadPlugins()
		config.plugins.empanel.showemsoftcam.save()
		config.plugins.empanel.showeminstall.save()
		config.plugins.empanel.showemuninstall.save()
		config.plugins.empanel.showemswap.save()
		config.plugins.empanel.showemusb.save()
		config.plugins.empanel.showemntp.save()
		config.plugins.empanel.showemepg.save()
		config.plugins.empanel.showemepg2.save()
		config.plugins.empanel.showemscript.save()
		config.plugins.empanel.showemmain.save()
		config.plugins.empanel.showemmainmenu.save()
		#config.plugins.empanel.crontab.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
#######################################################################################
class EMInstall(Screen):
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMInstall
		else:
			self.skin = skin_sd_EMInstall
		self.setTitle(_("EMicro Manual Installer"))
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.okInst,
				"green": self.okInst,
				"red": self.cancel,
				"yellow": self.AdvInst,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_yellow"] = StaticText(_("Forced Install"))
		self["key_blue"] = StaticText(_("Clear /tmp"))
		
	def nList(self):
		self.list = []
		workdir = "/tmp/" 
		ipklist = os.listdir(workdir)
		ipkminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/ipkmini.png"))
		tarminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/tarmini.png"))
		for line in ipklist:
			if line.find(".tar.gz") > -1 or line.find(".bh.tgz") > -1 or line.find(".nab.tgz") > -1:
				try:
					self.list.append((line.strip("\n"), "%s Kb,  %s" % ((os.path.getsize(workdir + line.strip("\n")) / 1024),time.ctime(os.path.getctime(workdir + line.strip("\n")))), tarminipng))
				except:
					pass
			elif line.find(".ipk") > -1:
				try:
					self.list.append((line.strip("\n"), "%s Kb,  %s" % ((os.path.getsize(workdir + line.strip("\n")) / 1024),time.ctime(os.path.getctime(workdir + line.strip("\n")))), ipkminipng))
				except:
					pass
		self.list.sort()
		self["menu"].setList(self.list)
		
	def okInst(self):
		if self["menu"].getCurrent()[0][-4:] == '.ipk':
			try:
				self.session.open(Console,title = _("Install packets"), cmdlist = ["opkg install /tmp/%s" % self["menu"].getCurrent()[0]])
			except:
				pass
		else:
			try:
				self.session.open(Console,title = _("Install tar.gz, bh.tgz, nab.tgz"), cmdlist = ["tar -C/ -xzpvf /tmp/%s" % self["menu"].getCurrent()[0]])
			except:
				pass
			
	def AdvInst(self):
		if self["menu"].getCurrent()[0][-4:] == '.ipk':
			try:
				self.session.open(Console,title = _("Install packets"), cmdlist = ["opkg install -force-overwrite -force-downgrade /tmp/%s" % self["menu"].getCurrent()[0]])
			except:
				pass
		else:
			try:
				self.session.open(Console,title = _("Install tar.gz, bh.tgz, nab.tgz"), cmdlist = ["tar -C/ -xzpvf /tmp/%s" % self["menu"].getCurrent()[0]])
			except:
				pass
	
	def cancel(self):
		self.close()
########################################################################################################
class EMUninst(Screen):
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.setTitle(_("EMicro Uninstaller"))
		self.session = session
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMUninst
		else:
			self.skin = skin_sd_EMUninst
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnInstall"))
		self["key_yellow"] = StaticText(_("Adv. UnInstall"))
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.Remove,
				"green": self.Remove,
				"red": self.cancel,
				"yellow": self.ARemove,
			},-1)
		
	def nList(self):
		self.list = []
		linetrue = 0
		ipkminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/ipkmini.png"))
		for line in open(self.status()):
			try:
				if line.find("Package:") > -1 and (line.find("dvbapp2-plugin-") > -1 or line.find("enigma2-plugin-") > -1):
					name1 = line.replace("\n","").split()[-1]
					linetrue = 1
				if line.find("Version:") > -1 and linetrue == 1:
					name2 = line.split()[-1] + "\n"
					self.list.append((name1, name2, ipkminipng))
					linetrue = 0
			except:
				pass
		self.list.sort()
		self["menu"].setList(self.list)
		
	def status(self):
		if fileExists("/usr/lib/opkg/status"):
			status = "/usr/lib/opkg/status"
		elif fileExists("/var/lib/opkg/status"):
			status = "/var/lib/opkg/status"
		elif fileExists("/var/opkg/status"):
			status = "/var/opkg/status"
		return status
		
	def cancel(self):
		self.close()
		
	def Remove(self):
		try:
			os.system("opkg remove %s" % self["menu"].getCurrent()[0])
			self.mbox = self.session.open(MessageBox, _("%s is UnInstalled" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox, _("%s is Error UnInstalled" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()

	def ARemove(self):
		try:
			os.system("opkg remove -force-remove %s" % self["menu"].getCurrent()[0])
			self.mbox = self.session.open(MessageBox, _("%s is UnInstalled" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox, _("%s is Error UnInstalled" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()
########################################################################################################
class EMSoftcam(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("EMicro SoftCam/CardServer"))
		self.session = session
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMSoftcam
		else:
			self.skin = skin_sd_EMSoftcam
		self.list = []
		self.indexpos = None
		self["menu"] = List(self.list)
		self.selemulist()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.ok,
				"green": self.start,
				"red": self.stop,
				"yellow": self.restart,
				"blue": self.softcam,
			},-1)
		self.list = [ ]
		self["key_red"] = Label(_("Stop"))
		self["key_green"] = Label(_("Start"))
		self["key_yellow"] = Label(_("ReStart"))
		self["key_blue"] = Label(_("SoftCam.Key"))
		self["text"] = ScrollLabel("")
		self.listecm()
		self.Timer = eTimer()
		self.Timer.callback.append(self.listecm)
		self.Timer.start(1000*4, False)
		
	def softcam(self):
		self.session.open(EMSoftcamUpd)
		
	def selemulist(self):
		self.list = []
		typeemu = ' '
		camdlist = os.listdir("/etc/init.d/")
		for line in camdlist:
			if line.find(".None") == -1:
				if line.split(".")[0] == 'softcam':
					typeemu = 'softcam'
					if self.emuversion(line) == self.emuversion('softcam'):
						softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/%s" % 'emuact.png'))
					else:
						softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/%s" % 'emumini.png'))
				elif line.split(".")[0] == 'cardserver':
					typeemu = 'cardserver'
					if self.emuversion(line) == self.emuversion('cardserver'):
						softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/%s" % 'cardact.png'))
					else:
						softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/%s" % 'cardmini.png'))
				try:
					if line.find('softcam.') > -1 or line.find('cardserver.') > -1:
						self.list.append((line, self.emuversion(line), softpng, typeemu))
				except:
					pass
		self.list.sort()
		self["menu"].setList(self.list)
		if self.indexpos != None:
			self["menu"].setIndex(self.indexpos)
		
	def emuversion(self, what):
		emuname = " "
		nameemu = []
		if fileExists("/etc/init.d/%s" % what.split("\n")[0]):
			try:
				for line in open("/etc/init.d/%s" % what.split("\n")[0]):
					if line.find("echo") > -1:
						nameemu.append(line)
				emuname =  "%s" % nameemu[1].split('"')[1]
			except:
				emuname = " "
		return emuname
		
	def start(self):
		clearlist = ""
		emutype = self["menu"].getCurrent()[3]
		if self["menu"].getCurrent()[1] != self.emuversion(emutype):
			os.system("/etc/init.d/%s stop" % emutype)
			if fileExists("/etc/init.d/%s" % emutype):
				os.unlink("/etc/init.d/%s" % emutype)
			if fileExists("/tmp/ecm.info"):
				os.system("rm /tmp/ecm.info")
			os.symlink("/etc/init.d/%s" % self["menu"].getCurrent()[0], "/etc/init.d/%s" % emutype)
			os.chmod("/etc/init.d/%s" % emutype, 0777)
			os.system("/etc/init.d/%s start" % emutype)
			self.mbox = self.session.open(MessageBox, _("Please wait, starting %s") % self["menu"].getCurrent()[0], MessageBox.TYPE_INFO, timeout = 4 )
			self.indexpos = self["menu"].getIndex()
			self["text"].setText(clearlist)
			self.selemulist()
		
	def stop(self):
		clearlist = ""
		emutype = self["menu"].getCurrent()[3]
		if self.emuversion(emutype) != " ":
			os.system("/etc/init.d/%s stop" % emutype)
			os.unlink("/etc/init.d/%s" % emutype)
			if fileExists("/tmp/ecm.info"):
				os.system("rm /tmp/ecm.info")
			if not fileExists("/etc/init.d/%s.None" % emutype):
				os.system("echo -e '# Placeholder for no cam' >> /etc/init.d/%s.None" % emutype)
			os.symlink("/etc/init.d/%s.None" % emutype, "/etc/init.d/%s" % emutype)
			os.chmod("/etc/init.d/%s" % emutype, 0777)
			self.mbox = self.session.open(MessageBox, _("Please wait, stoping softcam or cardserver"), MessageBox.TYPE_INFO, timeout = 4)
			self.indexpos = self["menu"].getIndex()
			self["text"].setText(clearlist)
			self.selemulist()
		
	def restart(self):
		emutype = self["menu"].getCurrent()[3]
		if self.emuversion(emutype) != " ":
			os.system("/etc/init.d/%s restart" % emutype)
			self.mbox = self.session.open(MessageBox,_("Please wait, restarting %s")% self.emuversion(emutype), MessageBox.TYPE_INFO, timeout = 4)
			self.indexpos = self["menu"].getIndex()
		
	def ok(self):
		emutype = self["menu"].getCurrent()[3]
		if self["menu"].getCurrent()[1] != self.emuversion(emutype):
			self.start()
		
	def cancel(self):
		self.close()
		
	def listecm(self):
		list = ""
		port_flag = 0
		if fileExists("/tmp/ecm.info"):
			try:
				ecmfiles = open("/tmp/ecm.info", "r")
				for line in ecmfiles:
					if line.find('port:') > -1: 
						port_flag  = 1
					if line.find("caid:") > -1 or line.find("provider:") > -1 or line.find("provid:") > -1 or line.find("pid:") > -1 or line.find("hops:") > -1  or line.find("system:") > -1 or line.find("address:") > -1 or line.find("using:") > -1 or line.find("ecm time:") > -1:
						line = line.replace(' ',"").replace(":",": ")
					if line.find("from:") > -1 or line.find("protocol:") > -1 or line.find("caid:") > -1 or line.find("pid:") > -1 or line.find("reader:") > -1 or line.find("hops:") > -1  or line.find("system:") > -1 or line.find("Service:") > -1 or line.find("CAID:") > -1 or line.find("Provider:") > -1:
						line = line.strip('\n') + "  "
					if line.find("Signature") > -1:
						line = ""
					if line.find("=") > -1:
						line = line.lstrip('=').replace('======', "").replace('\n', "").rstrip() + ', '
					if line.find("ecmtime:") > -1:
						line = line.replace("ecmtime:", "ecm time:")
					if line.find("response time:") > -1:
						line = line.replace("response time:", "ecm time:").replace("decoded by", "by")
					if not line.startswith('\n'): 
						if line.find('protocol:') > -1 and port_flag == 0:
							line = '\n' + line
						if line.find('pkey:') > -1:
							line = '\n' + line + '\n'
						list += line
				self["text"].setText(list)
				ecmfiles.close()
			except:
				pass
		
########################################################################################################
class EMSwapScreen(Screen):
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMSwapScreen
		else:
			self.skin = skin_sd_EMSwapScreen
		self.setTitle(_("EMicro Swap Menager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.Menu,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.Menu()
		
	def Menu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/swapmini.png"))
		minisonpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/swapminion.png"))
		for line in self.mountp():
			if line not in "/usr/share/enigma2/":
				try:
					if self.swapiswork() in line:
						self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minisonpng, line))
					else:
						self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
				except:
					self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.MenuDo, "cancel": self.close}, -1)
		
	def swapiswork(self):
		if fileExists("/proc/swaps"):
			for line in open("/proc/swaps"):
				if line.find("media") > -1:
					return line.split()[0][:-9]
		else:
			return " "
		
	def MenuDo(self):
		swppath = self["menu"].getCurrent()[3] + "swapfile"
		self.session.openWithCallback(self.Menu,EMSwapScreen2, swppath)
		
	def mountp(self):
		pathmp = []
		if fileExists("/proc/mounts"):
			for line in open("/proc/mounts"):
				if line.find("/dev/sd") > -1:
					pathmp.append(line.split()[1].replace('\\040', ' ') + "/")
		pathmp.append("/usr/share/enigma2/")
		return pathmp
	
	def exit(self):
		self.close()
####################################################################
class EMSwapScreen2(Screen):
	def __init__(self, session, swapdirect):
		self.swapfile = swapdirect
		self.session = session
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMSwapScreen2
		else:
			self.skin = skin_sd_EMSwapScreen2
		Screen.__init__(self, session)
		self.setTitle(_("EMicro Swap Menager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.CfgMenuDo,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()

	def isSwapPossible(self):
		for line in open("/proc/mounts"):
			fields= line.rstrip('\n').split()
			if fields[1] == "%s" % self.swapfile[:-9]:
				if fields[2] == 'ext2' or fields[2] == 'ext3' or fields[2] == 'ext4' or fields[2] == 'vfat':
					return 1
				else:
					return 0
		return 0
		
	def isSwapRun(self):
		try:
			for line in open('/proc/swaps'):
				if line.find(self.swapfile) > -1:
					return 1
			return 0
		except:
			pass
			
	def isSwapSize(self):
		try:
			swapsize = os.path.getsize(self.swapfile) / 1048576
			return ("%sMb" % swapsize)
		except:
			pass
			
	def makeSwapFile(self, size):
		try:
			os.system("dd if=/dev/zero of=%s bs=1024 count=%s" % (self.swapfile, size))
			os.system("mkswap %s" % (self.swapfile))
			self.mbox = self.session.open(MessageBox,_("Swap file created"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		except:
			pass
	
	def CfgMenu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/swapmini.png"))
		minisonpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/swapminion.png"))
		if self.isSwapPossible():
			if os.path.exists(self.swapfile):
				if self.isSwapRun() == 1:
					self.list.append((_("Swap off"),"5", (_("Swap on %s off (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minisonpng))
				else:
					self.list.append((_("Swap on"),"4", (_("Swap on %s on (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
					self.list.append((_("Remove swap"),"7",( _("Remove swap on %s (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
			else:
				self.list.append((_("Make swap"),"11", _("Make swap on %s (128MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"12", _("Make swap on %s (256MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"13", _("Make swap on %s (512MB)") % self.swapfile[7:10].upper(), minispng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.CfgMenuDo, "cancel": self.close}, -1)
			
	def CfgMenuDo(self):
		m_choice = self["menu"].getCurrent()[1]
		if m_choice is "4":
			try:
				for line in open("/proc/swaps"):
					if  line.find("swapfile") > -1:
						os.system("swapoff %s" % (line.split()[0]))
			except:
				pass
			os.system("swapon %s" % (self.swapfile))
			os.system("sed -i '/swap/d' /etc/fstab")
			os.system("echo -e '%s/swapfile swap swap defaults 0 0' >> /etc/fstab" % self.swapfile[:10])
			self.mbox = self.session.open(MessageBox,_("Swap file started"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		elif m_choice is "5":
			os.system("swapoff %s" % (self.swapfile))
			os.system("sed -i '/swap/d' /etc/fstab")
			self.mbox = self.session.open(MessageBox,_("Swap file stoped"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		elif m_choice is "11":
			self.makeSwapFile("131072")

		elif m_choice is "12":
			self.makeSwapFile("262144")

		elif m_choice is "13":
			self.makeSwapFile("524288")

		elif m_choice is "7":
			os.system("rm %s" % (self.swapfile))
			self.mbox = self.session.open(MessageBox,_("Swap file removed"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
			
	def exit(self):
		self.close()
####################################################################
class EMUsbUmount(Screen):
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMUsbUmount
		else:
			self.skin = skin_sd_EMUsbUmount
		self.setTitle(_("EMicro USB Unmount"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.CfgMenu,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnMount"))
		self["key_yellow"] = StaticText(_("reFresh"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/EM-Panel/images/usbico.png"))
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				hdd = hddlist[count][1]
				devpnt = self.devpoint(hdd.mountDevice())
				if hdd.mountDevice() != '/media/hdd':
					if devpnt != None:
						if int(hdd.free()) > 1024:
							self.list.append(("%s" % hdd.model(),"%s  %s  %s (%d.%03d GB free)" % (devpnt, self.filesystem(hdd.mountDevice()),hdd.capacity(), hdd.free()/1024 , hdd.free()%1024 ), minipng, devpnt))
						else:
							self.list.append(("%s" % hdd.model(),"%s  %s  %s (%03d MB free)" % (devpnt, self.filesystem(hdd.mountDevice()), hdd.capacity(),hdd.free()), minipng, devpnt))
		else:
			hddinfo = _("none")
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)
		
	def Ok(self):
		try:
			item = self["menu"].getCurrent()[3]
			os.system("umount -f %s" % item)
			self.mbox = self.session.open(MessageBox,_("Unmounted %s" % item), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			pass
		self.CfgMenu()
		
	def filesystem(self, mountpoint):
		try:
			for line in open("/proc/mounts"):
				if line.find(mountpoint)  > -1:
					return "%s  %s" % (line.split()[2], line.split()[3].split(',')[0])
		except:
			pass
			
	def devpoint(self, mountpoint):
		try:
			for line in open("/proc/mounts"):
				if line.find(mountpoint)  > -1:
					return line.split()[0]
		except:
			pass
			
	def exit(self):
		self.close()
		
####################################################################
class EMScriptScreen(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMScriptScreen
		else:
			self.skin = skin_sd_EMScriptScreen
		self.setTitle(_("EMicro Script Executer"))
		self.scrpit_menu()
		self["key_red"] = StaticText(_("Close"))
		self["actions"] = ActionMap(["OkCancelActions","ColorActions"], {"ok": self.run, "red": self.exit, "cancel": self.close}, -1)
		
	def scrpit_menu(self):
		list = []
		try:
			list = os.listdir("/usr/script/")
			list = [x[:-3] for x in list if x.endswith('.sh')]
		except:
			list = []
		list.sort()
		self["list"] = MenuList(list)
		
	def run(self):
		script = self["list"].getCurrent()
		if script is not None:
			name = ("%s%s.sh" % ("/usr/script/", script))
			os.chmod(name, 0755)
			self.session.open(Console, script.replace("_", " "), cmdlist=[name])

	def exit(self):
		self.close()
####################################################################
class EMNTPScreen(ConfigListScreen, Screen):
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMNTPScreen
		else:
			self.skin = skin_sd_EMNTPScreen
		self.setTitle(_("EMicro NTP Menager"))
		self.cfgMenu()
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Update Now"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.UpdateNow,
			"blue": self.Manual,
			"ok": self.save
		}, -2)
		
	def cfgMenu(self):
		self.list = []
		self.list.append(getConfigListEntry(_("NtpTime Updater"), config.plugins.empanel.onoff))
		self.list.append(getConfigListEntry(_("Set time to update"), config.plugins.empanel.time))
		self.list.append(getConfigListEntry(_("Set Transponder time update"), config.plugins.empanel.TransponderTime))
		self.list.append(getConfigListEntry(_("StartUp synchronization"), config.plugins.empanel.cold))
		self.list.append(getConfigListEntry(_("Set choice server mode"), config.plugins.empanel.manual))
		self.list.append(getConfigListEntry(_("Set your country"), config.plugins.empanel.server))
		self.list.append(getConfigListEntry(_("Set manual ntp server address"), config.plugins.empanel.manualserver))
		ConfigListScreen.__init__(self, self.list)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
		
	def Manual(self):
		EMManualSetTime(self.session)
	
	def save(self):
		if os.path.exists("/etc/crontabs"):
			path = "/etc/crontab/root"
		elif os.path.exists("/var/spool/cron/crontabs"):
			path = "/var/spool/cron/crontabs/root"
		elif os.path.exists("/etc/cron/crontabs"):
			path = "/etc/cron/crontabs/root"
		if config.plugins.empanel.onoff.value == "0":
			if fileExists(path):
				os.system("sed -i '/ntp./d' %s" % path)
		if config.plugins.empanel.onoff.value == "1":
			if fileExists(path):
				os.system("sed -i '/ntp./d' %s" % path)
			if config.plugins.empanel.manual.value == "0":
				if config.plugins.empanel.time.value == "30":
					os.system("echo -e '*/%s * * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.empanel.time.value, config.plugins.empanel.server.value, path))
				else:
					os.system("echo -e '1 */%s * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.empanel.time.value, config.plugins.empanel.server.value, path))
			else:
				if config.plugins.empanel.time.value == "30":
					os.system("echo -e '*/%s * * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.empanel.time.value, config.plugins.empanel.manualserver.value, path))
				else:
					os.system("echo -e '1 */%s * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.empanel.time.value, config.plugins.empanel.manualserver.value, path))
		os.system("echo -e 'root' >> %scron.update" % path[:-4])
		if fileExists(path):
			os.chmod("%s" % path, 0644)
		if config.plugins.empanel.TransponderTime.value == "0": 
			config.misc.useTransponderTime.value = False
			config.misc.useTransponderTime.save()
		else:
			config.misc.useTransponderTime.value = True
			config.misc.useTransponderTime.save()
		config.plugins.empanel.cold.save()
		config.plugins.empanel.manual.save()
		config.plugins.empanel.server.save()
		config.plugins.empanel.manualserver.save()
		configfile.save()
		if config.plugins.empanel.cold.value == "0":
			if fileExists("/etc/rcS.d/S42ntpdate.sh"):
				os.system("rm -f /etc/rcS.d/S42ntpdate.sh")
		else:
			if fileExists("/etc/rcS.d/S42ntpdate.sh"):
				os.system("rm -f /etc/rcS.d/S42ntpdate.sh")
			if os.path.exists("/usr/bin/ntpdate"):
				if not fileExists("/etc/rcS.d/S42ntpdate.sh"):
					os.system("echo -e '#!/bin/sh\n\n[ -x /usr/bin/ntpdate ] && /usr/bin/ntpdate -b -s -u %s\n\nexit 0' >> /etc/rcS.d/S42ntpdate.sh" % config.plugins.empanel.server.value)
				if fileExists("/etc/rcS.d/S42ntpdate.sh"):
					os.chmod("/etc/rcS.d/S42ntpdate.sh", 0755)
			if config.plugins.empanel.manual.value == "1":
				if fileExists("/etc/rcS.d/S42ntpdate.sh"):
					os.system("rm -f /etc/rcS.d/S42ntpdate.sh")
				os.system("echo -e '#!/bin/sh\n\n[ -x /usr/bin/ntpdate ] && /usr/bin/ntpdate -b -s -u %s\n\nexit 0' >> /etc/rcS.d/S42ntpdate.sh" % config.plugins.empanel.manualserver.value)
				if fileExists("/etc/rcS.d/S42ntpdate.sh"):
					os.chmod("/etc/rcS.d/S42ntpdate.sh", 0755)
		for i in self["config"].list:
			i[1].save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def UpdateNow(self):
		os.system("/usr/bin/ntpdate -v -u pool.ntp.org")
		self.mbox = self.session.open(MessageBox,(_("time updated")), MessageBox.TYPE_INFO, timeout = 6 )
####################################################################
class EMManualSetTime(Screen):
	def __init__(self, session):
		self.session = session
		self.currentime = strftime("%d:%m:%Y %H:%M",localtime())
		self.session.openWithCallback(self.newTime,InputBox, text="%s" % (self.currentime), maxSize=16, type=Input.NUMBER)

	def newTime(self,what):
		try:
			lenstr=len(what)
		except:
			lengstr = 0
		if what is None:
			self.breakSetTime(_("new time not available"))
		elif ((what.count(" ") < 1) or (what.count(":") < 3) or (lenstr != 16)):
			self.breakSetTime(_("bad format"))
		else:
			newdate = what.split(" ",1)[0]
			newtime = what.split(" ",1)[1]
			newday = newdate.split(":",2)[0]
			newmonth = newdate.split(":",2)[1]
			newyear = newdate.split(":",2)[2]
			newhour = newtime.split(":",1)[0]
			newmin = newtime.split(":",1)[1]
			maxmonth = 31
			if (int(newmonth) == 4) or (int(newmonth) == 6) or (int(newmonth) == 9) or (int(newmonth) == 11):
				maxmonth=30
			elif (int(newmonth) == 2):
				if ((4*int(int(newyear)/4)) == int(newyear)):
					maxmonth=28
				else:
					maxmonth=27
			if (int(newyear) < 2007) or (int(newyear) > 2027)  or (len(newyear) < 4):
				self.breakSetTime(_("bad year %s") %newyear)
			elif (int(newmonth) < 0) or (int(newmonth) >12) or (len(newmonth) < 2):
				self.breakSetTime(_("bad month %s") %newmonth)
			elif (int(newday) < 1) or (int(newday) > maxmonth) or (len(newday) < 2):
				self.breakSetTime(_("bad day %s") %newday)
			elif (int(newhour) < 0) or (int(newhour) > 23) or (len(newhour) < 2):
				self.breakSetTime(_("bad hour %s") %newhour)
			elif (int(newmin) < 0) or (int(newmin) > 59) or (len(newmin) < 2):
				self.breakSetTime(_("bad minute %s") %newmin)
			else:
				self.newtime = "%s%s%s%s%s" %(newmonth,newday,newhour,newmin,newyear)
				self.session.openWithCallback(self.ChangeTime,MessageBox,_("Apply the new System time?"), MessageBox.TYPE_YESNO)

	def ChangeTime(self,what):
		if what is True:
			os.system("date %s" % (self.newtime))
		else:
			self.breakSetTime(_("not confirmed"))

	def breakSetTime(self,reason):
		self.session.open(MessageBox,(_("Change system time was canceled, because %s") % reason), MessageBox.TYPE_WARNING)
######################################################################
class EMEPG(ConfigListScreen, Screen):
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMEPG
		else:
			self.skin = skin_sd_EMEPG
		self.setTitle(_("EMicro EPG downloader"))
		self.list = []
		self.list.append(getConfigListEntry(_("Select path to save epg.dat"), config.plugins.empanel.direct))
		self.list.append(getConfigListEntry(_("Select EPG filename"), config.plugins.empanel.epgname))
		self.list.append(getConfigListEntry(_("Select EPG language"), config.plugins.empanel.lang))
		self.list.append(getConfigListEntry(_("Patch enigma2.sh (need restart enigma2)"), config.plugins.empanel.e2shpatch))
		self.list.append(getConfigListEntry(_("AutoDownload epg.dat"), config.plugins.empanel.auto))
		self.list.append(getConfigListEntry(_("AutoDownload time"), config.plugins.empanel.timedwn))
		self.list.append(getConfigListEntry(_("AutoDownload weekday"), config.plugins.empanel.weekday))
		self.list.append(getConfigListEntry(_("Automatic save/load EPG"), config.plugins.empanel.autosave))
		self.list.append(getConfigListEntry(_("Autobackup to ../epgtmp.gz"), config.plugins.empanel.autobackup))
		self.list.append(getConfigListEntry(_("Check if epg.dat exists"), config.plugins.empanel.checkepgfile))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Download EPG"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.downepg,
			"blue": self.manual,
			"ok": self.save
		}, -2)
	
	def downepg(self):
		if self.ismounted(config.plugins.empanel.direct.value) == 1 or config.plugins.empanel.direct.value == "/usr/share/enigma2/":
			try:
				os.system("wget -q http://linux-sat.tv/epg/epg_%s.dat.gz -O %s%s.gz" % (config.plugins.empanel.lang.value, config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
				if fileExists("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value)):
					os.unlink("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
					os.system("rm -f %s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
				if not os.path.exists("%sepgtmp" % config.plugins.empanel.direct.value):
					os.system("mkdir -p %sepgtmp" % config.plugins.empanel.direct.value)
				os.system("cp -f %s%s.gz %sepgtmp" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value, config.plugins.empanel.direct.value))
				os.system("gzip -df %s%s.gz" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
				if fileExists("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value)):
					os.chmod("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value), 0644)
				self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
				epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
				epgcache = eEPGCache.getInstance().load()
			except:
				self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,(_("EPG save not possible, your device %s is not mounted") % config.plugins.empanel.direct.value), MessageBox.TYPE_INFO, timeout = 4 )

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)

	def save(self):
		config.misc.epgcache_filename.value = ("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
		config.misc.epgcache_filename.save()
		config.plugins.empanel.weekday.save()
		config.plugins.empanel.timedwn.save()
		config.plugins.empanel.lang.save()
		config.plugins.empanel.auto.save()
		config.plugins.empanel.epgname.save()
		config.plugins.empanel.direct.save()
		config.plugins.empanel.autosave.save()
		config.plugins.empanel.e2shpatch.save()
		config.plugins.empanel.autobackup.save()
		config.plugins.empanel.checkepgfile.save()
		configfile.save()
		if config.plugins.empanel.e2shpatch.value == "yes":
			os.system("sed -i '/.dat/d' /usr/bin/enigma2.sh")
			os.system("sed -i '3i [ -f %sepgtmp/%s.gz ] && cp -f %sepgtmp/%s.gz %s && gzip -df %s%s.gz' /usr/bin/enigma2.sh" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value, config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value, config.plugins.empanel.direct.value, config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
		else:
			os.system("sed -i '/.dat/d' /usr/bin/enigma2.sh")
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def manual(self):
		self.session.open(EMEPGMAN)

	def ismounted(self, what):
		for line in open("/proc/mounts"):
			if line.find(what[:-1]) > -1:
				return 1
		return 0
################################################################################################################
class EMEPGMAN(Screen):
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMEPGMAN
		else:
			self.skin = skin_sd_EMEPGMAN
		self.setTitle(_("EPG from linux-sat.tv (exUSSR)"))
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save epg.dat"))
		self["key_yellow"] = StaticText(_("Restore epg.dat"))
		self["key_blue"] = StaticText(_("Reload epg.dat"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.savepg,
			"yellow": self.restepg,
			"blue": self.reload,
		}, -2)
################################################################################################################
	def reload(self):
		try:
			if fileExists("%sepgtmp/%s.gz" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value)):
				os.system("cp -f %sepgtmp/%s.gz %s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value, config.plugins.empanel.direct.value))
				os.system("gzip -df %s%s.gz" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
			os.chmod("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value), 0644)
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
			self.mbox = self.session.open(MessageBox,(_("epg.dat reloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("reload epg.dat failed")), MessageBox.TYPE_INFO, timeout = 4 )
################################################################################################################
	def savepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_save,None,eEPGCache)
		epgcache = eEPGCache.getInstance().save()
		self.mbox = self.session.open(MessageBox,(_("epg.dat saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def restepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
		epgcache = eEPGCache.getInstance().load()
		self.mbox = self.session.open(MessageBox,(_("epg.dat restored")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def cancel(self):
		self.close(False)
####################################################################
class loadEPG():
	def __init__(self):
		self.dialog = None

	def gotSession(self, session):
		self.session = session
		self.timer = enigma.eTimer() 
		self.timer.callback.append(self.update)
		self.timer.start(60000, True)

	def update(self):
		self.timer.stop()
		now = time.localtime(time.time())
		if config.plugins.empanel.checkepgfile.value:
			if not fileExists("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value)):
				if fileExists("%sepgtmp/%s.gz" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value)):
					os.system("cp -f %sepgtmp/%s.gz %s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value, config.plugins.empanel.direct.value))
					os.system("gzip -df %s%s.gz" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
					os.chmod("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value), 0644)
				epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
				epgcache = eEPGCache.getInstance().load()
		if (config.plugins.empanel.auto.value == "yes" and config.plugins.empanel.timedwn.value[0] == now.tm_hour and config.plugins.empanel.timedwn.value[1] == now.tm_min and int(config.plugins.empanel.weekday.value) == int(now.tm_wday)):
			self.dload()
		if config.plugins.empanel.autosave.value != '0':
			if min > int(config.plugins.empanel.autosave.value) and config.plugins.empanel.timedwn.value[1] != now.tm_min:
				global min
				min = 0
				self.save_load_epg()
				if config.plugins.empanel.autobackup.value:
					self.autobackup()
			else:
				global min
				min = min + 1
		self.timer.start(60000, True)
		
	def autobackup(self):
		os.system("gzip -c %s%s > %sepgtmp/%s.gz" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value, config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
		
	def save_load_epg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_save,None,eEPGCache)
		epgcache = eEPGCache.getInstance().save()
		
	def dload(self):
		try:
			os.system("wget -q http://linux-sat.tv/epg/epg_%s.dat.gz -O %s%s.gz" % (config.plugins.empanel.lang.value, config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
			if fileExists("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value)):
				os.unlink("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
				os.system("rm -f %s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
			if not os.path.exists("%sepgtmp" % config.plugins.empanel.direct.value):
				os.system("mkdir -p %sepgtmp" % config.plugins.empanel.direct.value)
			os.system("cp -f %s%s.gz %sepgtmp" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value, config.plugins.empanel.direct.value))
			os.system("gzip -df %s%s.gz" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value))
			if fileExists("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value)):
				os.chmod("%s%s" % (config.plugins.empanel.direct.value, config.plugins.empanel.epgname.value), 0644)
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
			self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )
###############################################################################################
class EMSoftcamUpd(ConfigListScreen, Screen):
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = skin_hd_EMSoftcamUpd
		else:
			self.skin = skin_sd_EMSoftcamUpd
		self.setTitle(_("SoftCam.Key Updater"))
		self.list = []
		self.list.append(getConfigListEntry(_("Path to save keyfile"), config.plugins.empanel.path))
		self.list.append(getConfigListEntry(_("Name of keyfile"), config.plugins.empanel.keyname))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Download"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.downkey,
			"ok": self.save
		}, -2)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)
	
	def save(self):
		config.plugins.empanel.path.save()
		config.plugins.empanel.keyname.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def downkey(self):
		try:
			if fileExists("/tmp/SoftCam.Key"):
				os.system("rm /tmp/SoftCam.Key")
			os.system("wget -P /tmp %s" % ( adress))
			os.system("mv /tmp/SoftCam.Key /tmp/keyfile.tmp")
			if fileExists("%s%s" % (config.plugins.empanel.path.value, config.plugins.empanel.keyname.value)):
				if config.plugins.empanel.keyname.value == "SoftCam.Key":
					os.system("cp %s%s %s%s.old" % (config.plugins.empanel.path.value, config.plugins.empanel.keyname.value, config.plugins.empanel.path.value, config.plugins.empanel.keyname.value[:-4]))
				else:
					os.system("cp %s%s %s%s.old" % (config.plugins.empanel.path.value, config.plugins.empanel.keyname.value, config.plugins.empanel.path.value, config.plugins.empanel.keyname.value[:-5]))
				os.system("rm %s%s" % (config.plugins.empanel.path.value, config.plugins.empanel.keyname.value))
			os.system("cp /tmp/keyfile.tmp %s%s" % (config.plugins.empanel.path.value, config.plugins.empanel.keyname.value))
			os.chmod(("%s%s" % (config.plugins.empanel.path.value, config.plugins.empanel.keyname.value)), 0644)
			os.system("rm /tmp/keyfile.tmp")
			self.mbox = self.session.open(MessageBox,(_("%s downloaded Successfull" % config.plugins.empanel.keyname.value)), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			os.system("cp /usr/keys/SoftCam.old /usr/keys/SoftCam.Key")
			self.mbox = self.session.open(MessageBox,(_("%s downloaded UnSuccessfull" % config.plugins.empanel.keyname.value)), MessageBox.TYPE_INFO, timeout = 4 )
######################################################################################
def main(session, **kwargs):
	session.open(EMMain)
##############################################################################
pEmu = loadEPG()
##############################################################################
def sessionstart(reason,session=None, **kwargs):
	if reason == 0:
		pEmu.gotSession(session)
##############################################################################
def EMInstall2(session, **kwargs):
	session.open(EMInstall)
	
def EMSoftcam2(session, **kwargs):
	session.open(EMSoftcam)

def EMEPGMAN2(session, **kwargs):
	session.open(EMEPGMAN)
	
def EMUninst2(session, **kwargs):
	session.open(EMUninst)

def EMSwapScreen3(session, **kwargs):
	session.open(EMSwapScreen)
	
def EMUsbUmount2(session, **kwargs):
	session.open(EMUsbUmount)
	
def EMNTPScreen2(session, **kwargs):
	session.open(EMNTPScreen)
	
def EMEPG2(session, **kwargs):
	session.open(EMEPG)
	
def EMScriptScreen2(session, **kwargs):
	session.open(EMScriptScreen)
	
def menu(menuid, **kwargs):
	if menuid == "mainmenu":
		return [(_("EMicro Panel"), main, _("emicro_panel"), 49)]
	return []
##############################################################################
def Plugins(**kwargs):
	list = [PluginDescriptor(where = [PluginDescriptor.WHERE_AUTOSTART, PluginDescriptor.WHERE_SESSIONSTART], fnc = sessionstart)]
	if config.plugins.empanel.showemmain.value:
		list.append(PluginDescriptor(name=_("EMicro Panel"), description= _("simple tools"), where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU], icon="emicro.png", fnc=main))
	if config.plugins.empanel.showeminstall.value:
		list.append(PluginDescriptor(name=_("EMicro Manual Installer"), description=_("install ipk & tar.gz files from /tmp"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=EMInstall2))
	if config.plugins.empanel.showemsoftcam.value:
		list.append(PluginDescriptor(name=_("EMicro SoftCam/CardServer"), description=_("start, stop, restart Sofcam/Cardserver"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=EMSoftcam2))
	if config.plugins.empanel.showemepg2.value:
		list.append(PluginDescriptor(name=_("EMicro Reload epg.dat"), description=_("reload epg.dat"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=EMEPGMAN2))
	if config.plugins.empanel.showemuninstall.value:
		list.append(PluginDescriptor(name=_("EMicro Uninstaller"), description=_("uninstall ipk packets"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=EMUninst2))
	if config.plugins.empanel.showemswap.value:
		list.append(PluginDescriptor(name=_("EMicro Swap Menager"), description=_("menage swap file"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=EMSwapScreen3))
	if config.plugins.empanel.showemusb.value:
		list.append(PluginDescriptor(name=_("EMicro USB Unmount"), description=_("unmount usb devices"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=EMUsbUmount2))
	if config.plugins.empanel.showemntp.value:
		list.append(PluginDescriptor(name=_("EMicro NTP Menager"), description=_("time synchronization"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=EMNTPScreen2))
	if config.plugins.empanel.showemepg.value:
		list.append(PluginDescriptor(name=_("EMicro EPG Downloader"), description=_("dowload and menage epg from linux-sat.tv"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=EMEPG2))
	if config.plugins.empanel.showemscript.value:
		list.append(PluginDescriptor(name=_("EMicro Script Executer"), description=_("run user's script"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=EMScriptScreen2))
	if config.plugins.empanel.showemmainmenu.value:
		list.append(PluginDescriptor(name=_("EMicro Panel"), description=_("simple tools"), where = [PluginDescriptor.WHERE_MENU], fnc=menu))
	return list
