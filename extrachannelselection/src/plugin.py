# Plugin for create extra service list on Channel Selection
# Coded by a.k.a. Uchkun - @ 2013  thx to Nikolasi
# version 3.3 - look history of version on www.vuplus.ru
from Components.config import *
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.MenuList import MenuList
from enigma import eSize
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Components.Language import language
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.ServiceList import refreshServiceList
from Components.Label import Label
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE, fileExists
from Tools.LoadPixmap import LoadPixmap
from os import environ, system
import os
import gettext


lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("ExtraChannelSelection", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "SystemPlugins/ExtraChannelSelection/locale/"))


def _(txt):
	t = gettext.dgettext("ExtraChannelSelection", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t


FILEPATH = '/usr/lib/enigma2/python/Components/'
CHANNELPATH = '/usr/lib/enigma2/python/Screens/'
MAPPATH = '/usr/share/enigma2/'
RPATH = '/tmp/'
BACKUPPATH = '/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/backup/'
MAP_FILE = '/usr/share/enigma2/keymap.xml'
pluginversion = "3.3"
config.plugins.ExtraChannelSelection = ConfigSubsection()
config.plugins.ExtraChannelSelection.enabled = ConfigYesNo(default = True)
config.plugins.ExtraChannelSelection.okmode = ConfigYesNo(default = False)
config.plugins.ExtraChannelSelection.endmode = ConfigYesNo(default = True)
config.plugins.ExtraChannelSelection.text = ConfigYesNo(default= False)
config.plugins.ExtraChannelSelection.bordermode = ConfigYesNo(default = False)
config.plugins.ExtraChannelSelection.barpercmode = ConfigYesNo(default= False)
config.plugins.ExtraChannelSelection.doubmode = ConfigYesNo(default= False)
config.plugins.ExtraChannelSelection.percpos = ConfigSelection(default='1', choices=[
 ('1', _('on left')), ('2', _('on right'))])
config.plugins.ExtraChannelSelection.remmode = ConfigSelection(default='1', choices=[
 ('1', _('only minutes')), ('2', _('hours and minutes')),
 ('3', _('Without remain'))])
colordic=[
 ('1', _('Orange')), ('2', _('Denim color')),
 ('3', _('Gray')), ('4', _('Dark slate gray')),
 ('5', _('Blue-green')), ('6', _('Cyan')),
 ('7', _('Midnight blue')), ('8', _('Steel Blue')),
 ('9', _('Green')), ('10', _('Silver')),
 ('11', _('Aquamarine')), ('12', _('Yellow')),
 ('13', _('Red')), ('14', _('Purple')),
 ('15', _('White')), ('16', _('Blue')),
 ('17', _('Saddle Brown')), ('18', _('Crimson')),
 ('19', _('Dim Gray')), ('20', _('Tan')),
 ('21', _('Sea green')), ('22', _('Pink')),
 ('23', _('Medium orchid')), ('24', _('Indian red')),
 ('25', _('Antique white')), ('26', _('Light green')),
 ('27', _('Indigo')), ('28', _('Dark Green')),
 ('29', _('Dark olive')), ('30', _('Color from skin')),
 ('31', _('Black')), ('32', _('Black light')),
 ('33', _('Dark blue')), ('34', _('Navy blue')),
 ('35', _('Selective yellow'))]
fontdic=[
 ('1', '17'), ('2', '18'),
 ('3', '19'), ('4', '20'),
 ('5', '21'), ('6', '22'),
 ('7', '23'), ('8', '24'),
 ('9', '25'), ('10', '26'),
 ('11', _('Size from skin'))]
config.plugins.ExtraChannelSelection.coltext = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colormode = ConfigYesNo(default= True)
config.plugins.ExtraChannelSelection.piconmode = ConfigYesNo(default= True)
config.plugins.ExtraChannelSelection.picomode = ConfigSelection(default='2', choices=[
 ('1', _('on left')), ('2', _('on right'))])
config.plugins.ExtraChannelSelection.listmode = ConfigYesNo(default= False)
config.plugins.ExtraChannelSelection.barmode = ConfigSelection(default='1', choices=[
 ('1', _('ProgressBar with color')), ('2', _('ProgressBar with pixmap'))])
config.plugins.ExtraChannelSelection.picbar = ConfigSelection(default='1', choices=[
 ('1', _('Pixmap from skin')), ('2', _('Light green pixmap')),
 ('3', _('Dark blue pixmap')), ('4', _('Dark green pixmap')),
 ('5', _('Red pixmap')), ('6', _('Striped blue pixmap')),
 ('7', _('Bright yellow pixmap')), ('8', _('Black pixmap')),
 ('9', _('Light blue pixmap')), ('10', _('Varicoloured pixmap')),
 ('11', _('Versicolor pixmap')), ('12', _('Dark yellow pixmap'))])
config.plugins.ExtraChannelSelection.percmode = ConfigSelection(default='2', choices=[
 ('1', _('Without Percent')), ('2', _('Percent without brackets')),
 ('3', _('Percent in brackets'))])
config.plugins.ExtraChannelSelection.eventmode = ConfigSelection(default='1', choices=[
 ('1', _('Event without brackets')), ('2', _('Event in brackets')),
 ('3', _('Event through a dash'))])
config.plugins.ExtraChannelSelection.colremain = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colselremain = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colnum = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colselnum = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colend = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colselend = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colbar = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colbarsel = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colborder = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colbordersel = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colname = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colnamesel = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colperc = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colpercsel = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colevent = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.coleventsel = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colsat = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.colselsat = ConfigSelection(default='30', choices=colordic)
config.plugins.ExtraChannelSelection.fontnum = ConfigSelection(default='11', choices=fontdic)
config.plugins.ExtraChannelSelection.fontperc = ConfigSelection(default='11', choices=fontdic)
config.plugins.ExtraChannelSelection.fontname = ConfigSelection(default='11', choices=fontdic)
config.plugins.ExtraChannelSelection.fontevent = ConfigSelection(default='11', choices=fontdic)
config.plugins.ExtraChannelSelection.fontend = ConfigSelection(default='11', choices=fontdic)
config.plugins.ExtraChannelSelection.fontrem = ConfigSelection(default='11', choices=fontdic)
config.plugins.ExtraChannelSelection.fonttxt = ConfigSelection(default='11', choices=fontdic)
config.plugins.ExtraChannelSelection.fontsat = ConfigSelection(default='11', choices=fontdic)
config.plugins.ExtraChannelSelection.epgext = ConfigYesNo(default= False)


ExtraChannelSelection__init__ = None


def currentSkin():
	w = open("/etc/enigma2/settings", "r")
	e = w.read()
	w.close()
	r = e.split('\n')
	i = ''
	for x in r:
		if x.__contains__('config.skin.primary_skin'):
			i  += x
	curSk = i.replace('/skin.xml', '').replace('config.skin.primary_skin=', '')
	return curSk


def alreadyPatch():
	status = 0
	if fileExists(MAP_FILE):
		r = open(MAP_FILE, 'r')
		exist = False
		for line in r.readlines():
			if exist:
				if line.__contains__('ServiceUp'):
					status += 1
				elif line.__contains__('ServicePageUp'):
					status += 1
					break
			if line.__contains__('<map context="ChannelSelectBaseActions">'):
				exist = True
		r.close()
	if status == 2:
		return True
	return False


def StartMainSession(reason, **kwargs):
	global ExtraChannelSelection__init__
	if not config.plugins.ExtraChannelSelection.enabled.value:
		origreplace = True
		try:
			if fileExists(FILEPATH + 'ServiceList.py') and fileExists(FILEPATH + 'ServiceList-ori.py'):
				if os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-ori.py') and os.path.getsize(FILEPATH + 'ServiceList.py') == os.path.getsize(FILEPATH + 'ServiceList-new.py'):
					system('rm -rf ' + FILEPATH + 'ServiceList.py')
					system('cp -f ' + FILEPATH + 'ServiceList-ori.py ' + FILEPATH + 'ServiceList.py')
					origreplace = False
				elif os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-ori.py') and os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-new.py'):
					system('rm -rf ' + FILEPATH + 'ServiceList-ori.py')
					system('cp -f ' + FILEPATH + 'ServiceList.py ' + FILEPATH + 'ServiceList-ori.py')
					origreplace = False
		except:
			pass
		if alreadyPatch():
			mapreplace = True
			try:
				if fileExists(MAPPATH + 'keymap-ori.xml'):
					system('rm -rf ' + MAPPATH + 'keymap.xml')
					system('cp -f ' + MAPPATH + 'keymap-ori.xml ' + MAPPATH + 'keymap.xml')
					mapreplace = False
				else:
					pass
			except:
				pass
		else:
			pass
		chanreplace = True
		try:
			if fileExists(CHANNELPATH + 'ChannelSelection-new.py') and fileExists(CHANNELPATH + 'ChannelSelection-new2.py') and fileExists(CHANNELPATH + 'ChannelSelection-ori.py') and fileExists(CHANNELPATH + 'ChannelSelection.py'):
				if os.path.getsize(CHANNELPATH + 'ChannelSelection-ori.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and (os.path.getsize(CHANNELPATH + 'ChannelSelection-new.py') == os.path.getsize(CHANNELPATH + 'ChannelSelection.py') or os.path.getsize(CHANNELPATH + 'ChannelSelection-new2.py') == os.path.getsize(CHANNELPATH + 'ChannelSelection.py')):
					system('rm -rf ' + CHANNELPATH + 'ChannelSelection.py')
					system('cp -f ' + CHANNELPATH + 'ChannelSelection-ori.py ' + CHANNELPATH + 'ChannelSelection.py')
					chanreplace = False
				elif os.path.getsize(CHANNELPATH + 'ChannelSelection-ori.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and os.path.getsize(CHANNELPATH + 'ChannelSelection-new.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and os.path.getsize(CHANNELPATH + 'ChannelSelection-new2.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py'):
					system('rm -rf ' + CHANNELPATH + 'ChannelSelection-ori.py')
					system('cp -f ' + CHANNELPATH + 'ChannelSelection.py ' + CHANNELPATH + 'ChannelSelection-ori.py')
					chanreplace = False
		except:
			pass

	elif config.plugins.ExtraChannelSelection.enabled.value:
		origreplace = True
		try:
			if fileExists(FILEPATH + 'ServiceList.py') and fileExists(FILEPATH + 'ServiceList-ori.py') and fileExists(FILEPATH + 'ServiceList-new.py'):
				if os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-ori.py') and os.path.getsize(FILEPATH + 'ServiceList.py') == os.path.getsize(FILEPATH + 'ServiceList-new.py'):
					pass
				elif os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-ori.py') and os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-new.py'):
					system('rm -rf ' + FILEPATH + 'ServiceList-ori.py')
					system('cp -f ' + FILEPATH + 'ServiceList.py ' + FILEPATH + 'ServiceList-ori.py')
					system('rm -rf ' + FILEPATH + 'ServiceList.py')
					system('cp -f ' + FILEPATH + 'ServiceList-new.py ' + FILEPATH + 'ServiceList.py')
					origreplace = False
				elif os.path.getsize(FILEPATH + 'ServiceList.py') == os.path.getsize(FILEPATH + 'ServiceList-ori.py') and os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-new.py'):
					system('rm -rf ' + FILEPATH + 'ServiceList.py')
					system('cp -f ' + FILEPATH + 'ServiceList-new.py ' + FILEPATH + 'ServiceList.py')
					origreplace = False
		except:
			pass
		if not config.plugins.ExtraChannelSelection.okmode.value:
			chanreplace = True
			try:
				if fileExists(CHANNELPATH + 'ChannelSelection-new.py') and fileExists(CHANNELPATH + 'ChannelSelection-new2.py') and fileExists(CHANNELPATH + 'ChannelSelection-ori.py') and fileExists(CHANNELPATH + 'ChannelSelection.py'):
					if os.path.getsize(CHANNELPATH + 'ChannelSelection-ori.py') == os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and (os.path.getsize(CHANNELPATH + 'ChannelSelection-new.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') or os.path.getsize(CHANNELPATH + 'ChannelSelection-new2.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py')):
						system('rm -rf ' + CHANNELPATH + 'ChannelSelection.py')
						system('cp -f ' + CHANNELPATH + 'ChannelSelection-new.py ' + CHANNELPATH + 'ChannelSelection.py')
						chanreplace = False
					elif os.path.getsize(CHANNELPATH + 'ChannelSelection-ori.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and os.path.getsize(CHANNELPATH + 'ChannelSelection-new.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and os.path.getsize(CHANNELPATH + 'ChannelSelection-new2.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py'):
						system('rm -rf ' + CHANNELPATH + 'ChannelSelection-ori.py')
						system('cp -f ' + CHANNELPATH + 'ChannelSelection.py ' + CHANNELPATH + 'ChannelSelection-ori.py')
						system('rm -rf ' + CHANNELPATH + 'ChannelSelection.py')
						system('cp -f ' + CHANNELPATH + 'ChannelSelection-new.py ' + CHANNELPATH + 'ChannelSelection.py')
						chanreplace = False
			except:
				pass
		elif config.plugins.ExtraChannelSelection.okmode.value:
			chanreplace = True
			try:
				if fileExists(CHANNELPATH + 'ChannelSelection-new.py') and fileExists(CHANNELPATH + 'ChannelSelection-new2.py') and fileExists(CHANNELPATH + 'ChannelSelection-ori.py') and fileExists(CHANNELPATH + 'ChannelSelection.py'):
					if os.path.getsize(CHANNELPATH + 'ChannelSelection-ori.py') == os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and (os.path.getsize(CHANNELPATH + 'ChannelSelection-new.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') or os.path.getsize(CHANNELPATH + 'ChannelSelection-new2.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py')):
						system('rm -rf ' + CHANNELPATH + 'ChannelSelection.py')
						system('cp -f ' + CHANNELPATH + 'ChannelSelection-new2.py ' + CHANNELPATH + 'ChannelSelection.py')
						chanreplace = False
					elif os.path.getsize(CHANNELPATH + 'ChannelSelection-ori.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and os.path.getsize(CHANNELPATH + 'ChannelSelection-new.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and os.path.getsize(CHANNELPATH + 'ChannelSelection-new2.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py'):
						system('rm -rf ' + CHANNELPATH + 'ChannelSelection-ori.py')
						system('cp -f ' + CHANNELPATH + 'ChannelSelection.py ' + CHANNELPATH + 'ChannelSelection-ori.py')
						system('rm -rf ' + CHANNELPATH + 'ChannelSelection.py')
						system('cp -f ' + CHANNELPATH + 'ChannelSelection-new2.py ' + CHANNELPATH + 'ChannelSelection.py')
						chanreplace = False
			except:
				pass
		if not alreadyPatch():
			mapreplace = True
			try:
				if not fileExists(MAPPATH + 'keymap-ori.xml'):
					system('cp -f ' + MAPPATH + 'keymap.xml ' + MAPPATH + 'keymap-ori.xml')
					mapreplace = False
				else:
					pass
			except:
				pass
			r = open(MAP_FILE, 'r')
			rewrite = False
			newLines = ''
			for line in r.readlines():
				if rewrite and line.__contains__('</map>'):
					line = line.replace('</map>', '\t<key id="KEY_UP" mapto="ServiceUp" flags="m" />\n\t\t<key id="KEY_DOWN" mapto="ServiceDown" flags="m" />\n\t\t<key id="KEY_RIGHT" mapto="ServicePageDown" flags="m" />\n\t\t<key id="KEY_LEFT" mapto="ServicePageUp" flags="m" />\n\t</map>')
					rewrite = False
				if line.__contains__('<map context="ChannelSelectBaseActions">'):
					rewrite = True
				newLines += line

			r.close()
			r = open(MAP_FILE, 'w')
			r.write(newLines)
			r.close()
		if config.plugins.ExtraChannelSelection.epgext.value:
			epgex = True
			try:
				if os.path.getsize(FILEPATH + 'EpgList.py') != os.path.getsize(FILEPATH + 'EpgList-new.py'):
					if not fileExists(FILEPATH + 'EpgList-ori.py') :
						system('cp -f ' + FILEPATH + 'EpgList.py ' + FILEPATH + 'EpgList-ori.py')
						system('rm -rf ' + FILEPATH + 'EpgList.py')
						system('cp -f ' + FILEPATH + 'EpgList-new.py ' + FILEPATH + 'EpgList.py')
						epgex = False
					elif fileExists(FILEPATH + 'EpgList-ori.py') and os.path.getsize(FILEPATH + 'EpgList.py') != os.path.getsize(FILEPATH + 'EpgList-ori.py'):
						system('rm -rf ' + FILEPATH + 'EpgList-ori.py')
						system('cp -f ' + FILEPATH + 'EpgList.py ' + FILEPATH + 'EpgList-ori.py')
						system('rm -rf ' + FILEPATH + 'EpgList.py')
						system('cp -f ' + FILEPATH + 'EpgList-new.py ' + FILEPATH + 'EpgList.py')
						epgex = False
					else:
						system('rm -rf ' + FILEPATH + 'EpgList.py')
						system('cp -f ' + FILEPATH + 'EpgList-new.py ' + FILEPATH + 'EpgList.py')
						epgex = False
				else:
					pass
			except:
				pass


class PluginHistory(Screen):
	skin = """
<screen name="PluginHistory" position="center,center" size="595,450" title="Plugin History">
  <widget name="text" position="15,20" size="720,410" itemHeight="28" font="Regular;20" halign="left"/>
  <ePixmap position="215,438" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/images/red.png" alphatest="blend" />
  <widget source="red_key" render="Label" position="215,408" zPosition="2" size="165,30" font="Regular; 20" halign="center" valign="center" backgroundColor="#41000000" foregroundColor="#00dddddd" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Plugin History"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.cancel,
			"back": self.cancel,
			"red": self.cancel,
			"ok": self.cancel,
			})
		self["red_key"] = StaticText(_("Close"))
		self["text"] = Label(_("Author: a.k.a. Uchkun (c).\n\nSpecial thanks to Nikolasi for saved time for the\nderivation of Picon.\n\nThe idea of the plugin was born in autumn 2012 in\nthe study of the source listboxservice.cpp.\nIt has become clear that it is achievable.\nA designer multicontent own even novice programmers\nto Enigma.\n\nPurses for transfers:\nWebMoney\nZ108027892539\nR325825136282"))

	def cancel(self):
		self.close()


class BackScreen(Screen):
	skin = """
<screen name="BackScreen" position="center,center" size="595,450" title="Backup settings for current skin">
  <widget name="text" position="69,339" size="500,30" foregroundColor="#00009a00" font="Regular;22" halign="right" transparent="1" />
  <widget name="txt" position="29,237" size="535,30" foregroundColor="#00696969" halign="center" font="Regular;24" transparent="1" />
  <ePixmap position="215,438" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/images/red.png" alphatest="blend" />
  <widget source="red_key" render="Label" position="215,408" zPosition="2" size="165,30" font="Regular; 20" halign="center" valign="center" backgroundColor="#41000000" foregroundColor="#00dddddd" transparent="1" />
  <widget source="menu" render="Listbox" position="15,10" size="570,100" scrollbarMode="showOnDemand" transparent="1">
    <convert type="TemplatedMultiContent">
      {"template": [
        MultiContentEntryText(pos = (15, 5), size = (570, 30), font=0, flags = RT_HALIGN_LEFT, text = 0)
        ],
        "fonts": [gFont("Regular", 23)],
        "itemHeight": 40
      }
    </convert>
  </widget>
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Backup settings for current skin"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.cancel,
			"back": self.cancel,
			"red": self.cancel,
			"ok": self.action,
			})
		self["red_key"] = StaticText(_("Close"))
		self["text"] = Label(_("Current skin - %s") % currentSkin())
		self["txt"] = Label(_("Press OK for action"))
		self.list = []
		self["menu"] = List(self.list)
		self.createList()

	def createList(self):
		self.list = []
		self.list.append((_("Save settings for current skin"), "save"))
		self.list.append((_("Restore settings for current skin"), "restore"))
		self["menu"].setList(self.list)

	def action(self, selectEntry = None):
		if selectEntry == None:
			selectEntry = self["menu"].getCurrent()[1]
			if selectEntry is "save":
				if fileExists((BACKUPPATH + '%s') % currentSkin()):
					self.session.openWithCallback(self.saveset, MessageBox,_("Backup file is already exists!\nDo you want rewrite backup file?"), MessageBox.TYPE_YESNO, timeout = 8, default = False)
				elif not fileExists((BACKUPPATH + '%s') % currentSkin()):
					w = open("/etc/enigma2/settings", "r")
					e = w.read()
					w.close()
					r = e.split('\n')
					s = []
					for x in r:
						if x.__contains__('ExtraChannelSelection'):
							s.append(x)
					q = '\n'.join(s)
					l = q + '\n'
					h = open("/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/backup/%s" % currentSkin(),"w")
					h.write(l)
					h.close()
					self.session.open(MessageBox, _("Settings successfully saved!"), MessageBox.TYPE_INFO, timeout = 6)
			elif selectEntry is "restore":
				if not fileExists((BACKUPPATH + '%s') % currentSkin()):
					self.session.open(MessageBox, _("Backup file not exists!"), MessageBox.TYPE_INFO, timeout = 6)
				elif fileExists((BACKUPPATH + '%s') % currentSkin()):
					self.session.openWithCallback(self.restoreset, MessageBox, _("Do not be afraid, now image will be stopped and restarted for the restore the settings of ExtraChannelSelection for the current skin.\nRestore settings?"), MessageBox.TYPE_YESNO, timeout = 5)

	def cancel(self):
		self.close()

	def saveset(self, answer):
		if answer is True:
			w = open("/etc/enigma2/settings", "r")
			e = w.read()
			w.close()
			r = e.split('\n')
			s = []
			for x in r:
				if x.__contains__('ExtraChannelSelection'):
					s.append(x)
			q = '\n'.join(s)
			l = q + '\n'
			h = open("/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/backup/%s" % currentSkin(),"w")
			h.write(l)
			h.close()
			self.session.open(MessageBox, _("Settings successfully saved!"), MessageBox.TYPE_INFO, timeout = 6)
			
	def restoreset(self, answer):
		if answer is True:
			w = open("/etc/enigma2/settings", "r")
			e = w.read()
			w.close()
			r = e.split('\n')
			s = []
			for x in r:
				if not x.__contains__('ExtraChannelSelection'):
					s.append(x)
			j = '\n'.join(s)
			p = open("/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/backup/%s" % currentSkin(), "r")
			l = p.read()
			p.close()
			m = j + l
			v = open("/tmp/settings", "w")
			v.write(m)
			v.close()
			if fileExists(RPATH + 'listmode'):
				system('rm -rf ' + RPATH + 'listmode')
			if fileExists(RPATH + 'enabled'):
				system('rm -rf ' + RPATH + 'enabled')
			if fileExists(RPATH + 'okmode'):
				system('rm -rf ' + RPATH + 'okmode')
			if fileExists(RPATH + 'epgext'):
				system('rm -rf ' + RPATH + 'epgext')
			if fileExists(RPATH + 'doubmode'):
				system('rm -rf ' + RPATH + 'doubmode')
			from Screens.Console import Console
			print "run script"
			script = "/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/script/restore_settings.sh"
			os.chmod(script, 0755)
			self.session.open(Console, cmdlist=[script])
	


class ExtraChannelSelectionSetup(Screen, ConfigListScreen):
	skin = """
<screen name="ExtraChannelSelectionSetup" position="center,center" size="750,510" title="ExtraChannelSelection settings">
  <widget position="15,10" size="720,300" name="config" itemHeight="30" foregroundColor="#00ffcc33" font="Regular;21" scrollbarMode="showOnDemand" />
  <widget name="description" position="15,315" size="720,150" font="Regular;19" halign="center" valign="center"/>
  <ePixmap position="375,498" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/images/yellow.png" alphatest="blend" />
  <widget source="yellow_key" render="Label" position="375,468" zPosition="2" size="165,30" font="Regular; 20" halign="center" valign="center" backgroundColor="#41000000" foregroundColor="#00dddddd" transparent="1" />
  <ePixmap position="45,498" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/images/red.png" alphatest="blend" />
  <widget source="red_key" render="Label" position="45,468" zPosition="2" size="165,30" font="Regular; 20" halign="center" valign="center" backgroundColor="#41000000" foregroundColor="#00dddddd" transparent="1" />
  <ePixmap position="540,498" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/images/blue.png" alphatest="blend" />
  <widget source="blue_key" render="Label" position="540,468" zPosition="2" size="165,30" font="Regular; 20" halign="center" valign="center" backgroundColor="#41000000" foregroundColor="#00dddddd" transparent="1" />
  <ePixmap position="210,498" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/ExtraChannelSelection/images/green.png" alphatest="blend" />
  <widget source="green_key" render="Label" position="210,468" zPosition="2" size="165,30" font="Regular; 20" halign="center" valign="center" backgroundColor="#41000000" foregroundColor="#00dddddd" transparent="1" />
</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		if config.plugins.ExtraChannelSelection.listmode.value:
			a = open("/tmp/listmode","w")
			a.write('a\n')
			a.close()
		if config.plugins.ExtraChannelSelection.enabled.value:
			c = open("/tmp/enabled","w")
			c.write('a\n')
			c.close()
		if config.plugins.ExtraChannelSelection.okmode.value:
			d = open("/tmp/okmode","w")
			d.write('a\n')
			d.close()
		if config.plugins.ExtraChannelSelection.epgext.value:
			h = open("/tmp/epgext","w")
			h.write('a\n')
			h.close()
		if config.plugins.ExtraChannelSelection.doubmode.value:
			h = open("/tmp/doubmode","w")
			h.write('a\n')
			h.close()
		self.setup_title = _("ExtraChannelSelection - Version: %s") % pluginversion
		self["red_key"] = StaticText(_("Close"))
		self["green_key"] = StaticText(_("Save"))
		self["yellow_key"] = StaticText(_("Info"))
		self["blue_key"] = StaticText(_("Backup"))
		self["description"] = Label("")
		self["setupActions"] = ActionMap(["SetupActions", "OkCancelActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.info,
			"blue": self.back,
			"ok": self.save
		}, -2)

		ConfigListScreen.__init__(self, [])

		self.initConfig()
		self.createSetup()

		self.onClose.append(self.__closed)
		self.onLayoutFinish.append(self.__layoutFinished)
		if not self.displayText in self["config"].onSelectionChanged:
			self["config"].onSelectionChanged.append(self.displayText)

	def displayText(self):
		if self["config"].getCurrent() == self.cfg_enabled:
			self["description"].setText(_("Enable or disable the plugin. Plugin's menu is dynamic. When open any items, other items opened or closed. Restart required."))
		elif self["config"].getCurrent() == self.cfg_okmode:
			self["description"].setText(_("When enabled, double tap OK in the channel list is working. First press - show channel in the PIG, the second press - close channel list. Restart required."))
		elif self["config"].getCurrent() == self.cfg_text:
			self["description"].setText(_("When enabled, if EPG from TV Guide is not available, will be shown static text - 'No EPG data available'. No restart required."))
		elif self["config"].getCurrent() == self.cfg_coltext:
			self["description"].setText(_("Color selection for the above text - 'No EPG data available'. No restart required."))
		elif self["config"].getCurrent() == self.cfg_listmode:
			self["description"].setText(_("When enabled, each channel in the selector will occupy two lines with additional information, and advanced settings for double-row configuration will appear in the menu, and vice versa, settings for only single-row configuration on the channel list will disappear. Restart required."))
		elif self["config"].getCurrent() == self.cfg_doubmode:
			self["description"].setText(_("Choose a type of the doubleline channellist."))
		elif self["config"].getCurrent() == self.cfg_bordermode:
			self["description"].setText(_("When enabled, the long progress-bar will be with a border. No restart required."))
		elif self["config"].getCurrent() == self.cfg_barpercmode:
			self["description"].setText(_("Showing percent above the progressbar to saving space in the channel list. It is necessary to configure the location of percent and location of progressbar at one side - at the left side or at the right side for both. Location percent set in the same menu in item 'Percent location' and the progressbar in the settings of the image 'Main Menu-Settings-System-User Interface-Progressbar Type'. No restart required."))
		elif self["config"].getCurrent() == self.cfg_percpos:
			self["description"].setText(_("Configure the location of percent - at the left or at the right side. Keep in mind, if you have included on the previous item 'Bar and percent together', then will need to put a progressbar in the same side in the settings of the image in the user interface. No restart required."))
		elif self["config"].getCurrent() == self.cfg_remmode:
			self["description"].setText(_("Select the type of display the time remaining in the double-row list of channels. Two types, number of minutes or hours with minutes. No restart required."))
		elif self["config"].getCurrent() == self.cfg_endmode:
			self["description"].setText(_("When enabled, In the double-row channel list will be displayed start-time and end-time of event. No restart required."))
		elif self["config"].getCurrent() == self.cfg_barmode:
			self["description"].setText(_("'ProgressBar with color' means that you will need to choose the color for progressbar. At a choice of this option, be convinced that in the skin.xml a certain picture isn't applied to the cursor. 'ProgressBar with pixmap' means that you will need to choose a pixmap as a progressbar. In the version with the picture color will turn richer and brighter. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colbar:
			self["description"].setText(_("Choose a color to the progressbar. Valid only if you select the 'ProgressBar with color'. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colbarsel:
			self["description"].setText(_("Choose a color to the progressbar, when it selected. Valid only if you select the 'ProgressBar with color'. No restart required."))
		elif self["config"].getCurrent() == self.cfg_picbar:
			self["description"].setText(_("Choose a pixmap to the progressbar. Valid only if you select the 'ProgressBar with pixmap'. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colbordersel:
			self["description"].setText(_("Choose a color to the border of progressbar, when it selected. Valid only if you select the 'ProgressBar with pixmap'. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colborder:
			self["description"].setText(_("Choose a color to the border of progressbar. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colsat:
			self["description"].setText(_("Choose a color to the satlist and providerlist. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colselsat:
			self["description"].setText(_("Choose a color to the satlist and providerlist, when it selected. No restart required."))
		elif self["config"].getCurrent() == self.cfg_percmode:
			self["description"].setText(_("Select the type of display of percent. In brackets or without brackets, or you can disable display of percent. No restart required."))
		elif self["config"].getCurrent() == self.cfg_eventmode:
			self["description"].setText(_("Select the type of display the name of the event. In brackets or without brackets, or through a dash. No restart required."))
		elif self["config"].getCurrent() == self.cfg_piconmode:
			self["description"].setText(_("Specify whether or not to show picons in the channel list. No restart required."))
		elif self["config"].getCurrent() == self.cfg_picomode:
			self["description"].setText(_("Configure the location of picons - at the left or at the right side in the channel list. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colormode:
			self["description"].setText(_("If you choose 'yes', a plug-in will try to choose colors for elements of the list of channels from settings of the current skin. Some colors in a skin can be not set. Also there are elements for which colors in skins aren't set in general. To these cases, default colors will be applied. If you choose 'no', further will it is necessary to adjust colors for all elements. No restart required."))
		elif self["config"].getCurrent() == self.cfg_fontnum:
			self["description"].setText(_("Select a font size for the number of channel. No restart required."))
		elif self["config"].getCurrent() == self.cfg_fontperc:
			self["description"].setText(_("Select a font size for the percent. No restart required."))
		elif self["config"].getCurrent() == self.cfg_fontname:
			self["description"].setText(_("Select a font size for the Service Name. No restart required."))
		elif self["config"].getCurrent() == self.cfg_fontevent:
			self["description"].setText(_("Select a font size for the Event. No restart required."))
		elif self["config"].getCurrent() == self.cfg_fontend:
			self["description"].setText(_("Select a font size for the start- and end- time for event in the double-row list of channels. No restart required."))
		elif self["config"].getCurrent() == self.cfg_fontrem:
			self["description"].setText(_("Select a font size for the remaining time for event in the double-row list of channels. No restart required."))
		elif self["config"].getCurrent() == self.cfg_fonttxt:
			self["description"].setText(_("Select a font size for the text - 'No EPG data available'. No restart required."))
		elif self["config"].getCurrent() == self.cfg_fontsat:
			self["description"].setText(_("Select a font size for the satlist and providerlist. No restart required."))
		elif self["config"].getCurrent() == self.cfg_epgext:
			self["description"].setText(_("If enabled, the usual guide (Eventview) present in the image will be replaced by an extended program guide. The new TV guide with more information and more colorful. Restart required."))
		elif self["config"].getCurrent() == self.cfg_colnum:
			self["description"].setText(_("Choose a color for the number of channel. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colselnum:
			self["description"].setText(_("Choose a color for the number of channel, when it selected. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colname:
			self["description"].setText(_("Choose a color for the Service Name. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colnamesel:
			self["description"].setText(_("Choose a color for the Service Name, when it selected. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colperc:
			self["description"].setText(_("Choose a color for the percent. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colpercsel:
			self["description"].setText(_("Choose a color for the percent, when it selected. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colevent:
			self["description"].setText(_("Choose a color for the Event. No restart required."))
		elif self["config"].getCurrent() == self.cfg_coleventsel:
			self["description"].setText(_("Choose a color for the Event, when it selected. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colend:
			self["description"].setText(_("Choose a color for the start- and end- time for event in the double-row list of channels. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colselend:
			self["description"].setText(_("Choose a color for the start- and end- time for event in the double-row list of channels, when it selected. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colremain:
			self["description"].setText(_("Choose a color for the remaining time for event in the double-row list of channels. No restart required."))
		elif self["config"].getCurrent() == self.cfg_colselremain:
			self["description"].setText(_("Choose a color for the remaining time for event in the double-row list of channels, when it selected. No restart required."))

	def __closed(self):
		pass

	def __layoutFinished(self):
		self.setTitle(self.setup_title)

	def initConfig(self):

		def getPrevValues(section):
			res = { }
			for (key,val) in section.content.items.items():
				if isinstance(val, ConfigSubsection):
					res[key] = getPrevValues(val)
				else:
					res[key] = val.value
			return res

		self.ECS = config.plugins.ExtraChannelSelection
		self.prev_values = getPrevValues(self.ECS)
		self.cfg_enabled = getConfigListEntry(_("ExtraChannelSelection Enabled"), self.ECS.enabled)
		self.cfg_okmode = getConfigListEntry(_("Enable double-click OK"), self.ECS.okmode)
		self.cfg_text = getConfigListEntry(_("The text in the absence of an event"), self.ECS.text)
		self.cfg_coltext = getConfigListEntry(_("Color for this text"), self.ECS.coltext)
		self.cfg_listmode = getConfigListEntry(_("Doubleline channellist"), self.ECS.listmode)
		self.cfg_doubmode = getConfigListEntry(_("Doubleline with big picons"), self.ECS.doubmode)
		self.cfg_bordermode = getConfigListEntry(_("Long bar with border"), self.ECS.bordermode)
		self.cfg_barpercmode = getConfigListEntry(_("Bar and percent together"), self.ECS.barpercmode)
		self.cfg_percpos = getConfigListEntry(_("Percent location"), self.ECS.percpos)
		self.cfg_remmode = getConfigListEntry(_("Remaining time type"), self.ECS.remmode)
		self.cfg_endmode = getConfigListEntry(_("Start-end time enabled"), self.ECS.endmode)
		self.cfg_barmode = getConfigListEntry(_("ProgressBar Type"), self.ECS.barmode)
		self.cfg_colbar = getConfigListEntry(_("Color for Bar"), self.ECS.colbar)
		self.cfg_colbarsel = getConfigListEntry(_("Color for selected Bar"), self.ECS.colbarsel)
		self.cfg_picbar = getConfigListEntry(_("Pixmap for Bar"), self.ECS.picbar)
		self.cfg_colbordersel = getConfigListEntry(_("Color for selected BarBorder"), self.ECS.colbordersel)
		self.cfg_colborder = getConfigListEntry(_("Color for BarBorder"), self.ECS.colborder)
		self.cfg_colsat = getConfigListEntry(_("Color for Satlist"), self.ECS.colsat)
		self.cfg_colselsat = getConfigListEntry(_("Color for selected Satlist"), self.ECS.colselsat)
		self.cfg_percmode = getConfigListEntry(_("Percent Type"), self.ECS.percmode)
		self.cfg_eventmode = getConfigListEntry(_("Eventview type"), self.ECS.eventmode)
		self.cfg_piconmode = getConfigListEntry(_("Show picon"), self.ECS.piconmode)
		self.cfg_picomode = getConfigListEntry(_("Picon location"), self.ECS.picomode)
		self.cfg_colormode = getConfigListEntry(_("Colors of elements from a skin"), self.ECS.colormode)
		self.cfg_fontnum = getConfigListEntry(_("Font-size Number"), self.ECS.fontnum)
		self.cfg_fontperc = getConfigListEntry(_("Font-size Percent"), self.ECS.fontperc)
		self.cfg_fontname = getConfigListEntry(_("Font-size Service Name"), self.ECS.fontname)
		self.cfg_fontevent = getConfigListEntry(_("Font-size Event"), self.ECS.fontevent)
		self.cfg_fontend = getConfigListEntry(_("Font-size Start-End"), self.ECS.fontend)
		self.cfg_fontrem = getConfigListEntry(_("Font-size Remain"), self.ECS.fontrem)
		self.cfg_fonttxt = getConfigListEntry(_("Font-size Text"), self.ECS.fonttxt)
		self.cfg_fontsat = getConfigListEntry(_("Font-size Sat & Prov"), self.ECS.fontsat)
		self.cfg_epgext = getConfigListEntry(_("Change EPG window"), self.ECS.epgext)
		self.cfg_colnum = getConfigListEntry(_("Color for number"), self.ECS.colnum)
		self.cfg_colselnum = getConfigListEntry(_("Color for number when selected"), self.ECS.colselnum)
		self.cfg_colname = getConfigListEntry(_("Color for Service Name"), self.ECS.colname)
		self.cfg_colnamesel = getConfigListEntry(_("Color for Service Name when selected"), self.ECS.colnamesel)
		self.cfg_colperc = getConfigListEntry(_("Color for percent"), self.ECS.colperc)
		self.cfg_colpercsel = getConfigListEntry(_("Color for percent when selected"), self.ECS.colpercsel)
		self.cfg_colevent = getConfigListEntry(_("Color for event"), self.ECS.colevent)
		self.cfg_coleventsel = getConfigListEntry(_("Color for event when selected"), self.ECS.coleventsel)
		self.cfg_colend = getConfigListEntry(_("Start-end Color"), self.ECS.colend)
		self.cfg_colselend = getConfigListEntry(_("Start-end Color when selected"), self.ECS.colselend)
		self.cfg_colremain = getConfigListEntry(_("Color for remaining time"), self.ECS.colremain)
		self.cfg_colselremain = getConfigListEntry(_("Color for remaining time when selected"), self.ECS.colselremain)

	def createSetup(self):
		list = [ self.cfg_enabled ]
		if self.ECS.enabled.value:
			list.append(self.cfg_okmode)
			list.append(self.cfg_text)
			if self.ECS.text.value:
				list.append(self.cfg_coltext)
			list.append(self.cfg_listmode)
			if not self.ECS.listmode.value:
				list.append(self.cfg_barpercmode)
				if self.ECS.barpercmode.value:
					list.append(self.cfg_percpos)
			if self.ECS.listmode.value:
				list.append(self.cfg_doubmode)
				list.append(self.cfg_remmode)
				list.append(self.cfg_endmode)
				list.append(self.cfg_fontend)
				list.append(self.cfg_fontrem)
				if self.ECS.doubmode.value:
					list.append(self.cfg_bordermode)
			list.append(self.cfg_barmode)
			if self.ECS.barmode.value == '1':
				list.append(self.cfg_colbar)
				list.append(self.cfg_colbarsel)
			elif self.ECS.barmode.value == '2':
				list.append(self.cfg_picbar)
				list.append(self.cfg_colbordersel)
			list.append(self.cfg_colborder)
			list.append(self.cfg_percmode)
			list.append(self.cfg_eventmode)
			list.append(self.cfg_piconmode)
			if self.ECS.piconmode.value:
				list.append(self.cfg_picomode)
			list.append(self.cfg_colormode)
			if not self.ECS.colormode.value:
				list.append(self.cfg_colnum)
				list.append(self.cfg_colselnum)
				list.append(self.cfg_colname)
				list.append(self.cfg_colnamesel)
				list.append(self.cfg_colperc)
				list.append(self.cfg_colpercsel)
				list.append(self.cfg_colevent)
				list.append(self.cfg_coleventsel)
				if self.ECS.listmode.value:
					list.append(self.cfg_colend)
					list.append(self.cfg_colselend)
					list.append(self.cfg_colremain)
					list.append(self.cfg_colselremain)
			list.append(self.cfg_colsat)
			list.append(self.cfg_colselsat)
			list.append(self.cfg_fontnum)
			list.append(self.cfg_fontperc)
			list.append(self.cfg_fontname)
			list.append(self.cfg_fontevent)
			list.append(self.cfg_fonttxt)
			list.append(self.cfg_fontsat)
			list.append(self.cfg_epgext)

		self["config"].list = list
		self["config"].l.setList(list)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.newConfig()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.newConfig()

	def newConfig(self):
		cur = self["config"].getCurrent()
		if cur in (self.cfg_enabled, self.cfg_text, self.cfg_barmode, self.cfg_colormode, self.cfg_piconmode, self.cfg_listmode, self.cfg_doubmode, self.cfg_barpercmode):
			self.createSetup()

	def cancel(self):
		def setPrevValues(section, values):
			for (key,val) in section.content.items.items():
				value = values.get(key, None)
				if value is not None:
					if isinstance(val, ConfigSubsection):
						setPrevValues(val, value)
					else:
						val.value = value

		setPrevValues(self.ECS, self.prev_values)
		self.session.openWithCallback(self.exitConfirmed, MessageBox, _("Really close without saving settings?"), MessageBox.TYPE_YESNO, timeout = 8)

	def exitConfirmed(self, answer):
		if answer:
			self.ECS.save()
			if fileExists(RPATH + 'listmode'):
				system('rm -rf ' + RPATH + 'listmode')
			if fileExists(RPATH + 'enabled'):
				system('rm -rf ' + RPATH + 'enabled')
			if fileExists(RPATH + 'okmode'):
				system('rm -rf ' + RPATH + 'okmode')
			if fileExists(RPATH + 'epgext'):
				system('rm -rf ' + RPATH + 'epgext')
			if fileExists(RPATH + 'doubmode'):
				system('rm -rf ' + RPATH + 'doubmode')
			self.close()

	def save(self):
		for i in self["config"].list:
			i[1].save()
		configfile.save()
		if config.plugins.ExtraChannelSelection.enabled.value:
			state = True
			try:
				if os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-new.py'):
					if not fileExists(FILEPATH + 'ServiceList-ori.py') :
						system('cp -f ' + FILEPATH + 'ServiceList.py ' + FILEPATH + 'ServiceList-ori.py')
						system('rm -rf ' + FILEPATH + 'ServiceList.py')
						system('cp -f ' + FILEPATH + 'ServiceList-new.py ' + FILEPATH + 'ServiceList.py')
						state = False
					elif fileExists(FILEPATH + 'ServiceList-ori.py') and os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-ori.py'):
						system('rm -rf ' + FILEPATH + 'ServiceList-ori.py')
						system('cp -f ' + FILEPATH + 'ServiceList.py ' + FILEPATH + 'ServiceList-ori.py')
						system('rm -rf ' + FILEPATH + 'ServiceList.py')
						system('cp -f ' + FILEPATH + 'ServiceList-new.py ' + FILEPATH + 'ServiceList.py')
						state = False
					else:
						system('rm -rf ' + FILEPATH + 'ServiceList.py')
						system('cp -f ' + FILEPATH + 'ServiceList-new.py ' + FILEPATH + 'ServiceList.py')
						state = False
				else:
					state = False
			except:
				pass
			chan = True
			try:
				if os.path.getsize(CHANNELPATH + 'ChannelSelection-new.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and os.path.getsize(CHANNELPATH + 'ChannelSelection-new2.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py') and os.path.getsize(CHANNELPATH + 'ChannelSelection-ori.py') == os.path.getsize(CHANNELPATH + 'ChannelSelection.py'):
					system('rm -rf ' + CHANNELPATH + 'ChannelSelection.py')
					system('cp -f ' + CHANNELPATH + 'ChannelSelection-new.py ' + CHANNELPATH + 'ChannelSelection.py')
					chan = False
				else:
					chan = False
			except:
				pass
			if not alreadyPatch():
				mapreplace = True
				try:
					if not fileExists(MAPPATH + 'keymap-ori.xml'):
						system('cp -f ' + MAPPATH + 'keymap.xml ' + MAPPATH + 'keymap-ori.xml')
						mapreplace = False
					else:
						pass
				except:
					pass
				r = open(MAP_FILE, 'r')
				rewrite = False
				newLines = ''
				for line in r.readlines():
					if rewrite and line.__contains__('</map>'):
						line = line.replace('</map>', '\t<key id="KEY_UP" mapto="ServiceUp" flags="m" />\n\t\t<key id="KEY_DOWN" mapto="ServiceDown" flags="m" />\n\t\t<key id="KEY_RIGHT" mapto="ServicePageDown" flags="m" />\n\t\t<key id="KEY_LEFT" mapto="ServicePageUp" flags="m" />\n\t</map>')
						rewrite = False
					if line.__contains__('<map context="ChannelSelectBaseActions">'):
						rewrite = True
					newLines = newLines + line

				r.close()
				r = open(MAP_FILE, 'w')
				r.write(newLines)
				r.close()
			else:
				pass
		elif not config.plugins.ExtraChannelSelection.enabled.value:
			origreplace = True
			try:
				if os.path.getsize(FILEPATH + 'ServiceList.py') == os.path.getsize(FILEPATH + 'ServiceList-new.py'):
					if fileExists(FILEPATH + 'ServiceList-ori.py'):
						system('rm -rf ' + FILEPATH + 'ServiceList.py')
						system('cp -f ' + FILEPATH + 'ServiceList-ori.py ' + FILEPATH + 'ServiceList.py')
						origreplace = False
					else:
						pass
				else:
					if fileExists(FILEPATH + 'ServiceList-ori.py') and os.path.getsize(FILEPATH + 'ServiceList.py') != os.path.getsize(FILEPATH + 'ServiceList-ori.py'):
						system('rm -rf ' + FILEPATH + 'ServiceList-ori.py')
						system('cp -f ' + FILEPATH + 'ServiceList.py ' + FILEPATH + 'ServiceList-ori.py')
						origreplace = False
					else:
						pass
			except:
				pass
			chan = True
			try:
				if os.path.getsize(CHANNELPATH + 'ChannelSelection-ori.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py'):
					system('rm -rf ' + CHANNELPATH + 'ChannelSelection.py')
					system('cp -f ' + CHANNELPATH + 'ChannelSelection-ori.py ' + CHANNELPATH + 'ChannelSelection.py')
					chan = False
				else:
					chan = False
			except:
				pass
			if alreadyPatch():
				mapreplace = True
				try:
					if fileExists(MAPPATH + 'keymap-ori.xml'):
						system('rm -rf ' + MAPPATH + 'keymap.xml')
						system('cp -f ' + MAPPATH + 'keymap-ori.xml ' + MAPPATH + 'keymap.xml')
						mapreplace = False
					else:
						pass
				except:
					pass
			else:
				pass

			epgex = True
			try:
				if os.path.getsize(FILEPATH + 'EpgList.py') == os.path.getsize(FILEPATH + 'EpgList-new.py'):
					if fileExists(FILEPATH + 'EpgList-ori.py'):
						system('rm -rf ' + FILEPATH + 'EpgList.py')
						system('cp -f ' + FILEPATH + 'EpgList-ori.py ' + FILEPATH + 'EpgList.py')
						epgex = False
					else:
						pass
				else:
					if fileExists(FILEPATH + 'EpgList-ori.py') and os.path.getsize(FILEPATH + 'EpgList.py') != os.path.getsize(FILEPATH + 'EpgList-ori.py'):
						system('rm -rf ' + FILEPATH + 'EpgList-ori.py')
						system('cp -f ' + FILEPATH + 'EpgList.py ' + FILEPATH + 'EpgList-ori.py')
						epgex = False
					else:
						pass
			except:
				pass

		if config.plugins.ExtraChannelSelection.okmode.value and config.plugins.ExtraChannelSelection.enabled.value:
			chan = True
			try:
				if os.path.getsize(CHANNELPATH + 'ChannelSelection-new2.py') != os.path.getsize(CHANNELPATH + 'ChannelSelection.py'):
					system('rm -rf ' + CHANNELPATH + 'ChannelSelection.py')
					system('cp -f ' + CHANNELPATH + 'ChannelSelection-new2.py ' + CHANNELPATH + 'ChannelSelection.py')
					chan = False
				else:
					chan = False
			except:
				pass

		elif not config.plugins.ExtraChannelSelection.okmode.value and config.plugins.ExtraChannelSelection.enabled.value:
			chan = True
			try:
				if os.path.getsize(CHANNELPATH + 'ChannelSelection-new2.py') == os.path.getsize(CHANNELPATH + 'ChannelSelection.py'):
					system('rm -rf ' + CHANNELPATH + 'ChannelSelection.py')
					system('cp -f ' + CHANNELPATH + 'ChannelSelection-new.py ' + CHANNELPATH + 'ChannelSelection.py')
					chan = False
				else:
					chan = False
			except:
				pass

		if config.plugins.ExtraChannelSelection.epgext.value and config.plugins.ExtraChannelSelection.enabled.value:
			epgex = True
			try:
				if os.path.getsize(FILEPATH + 'EpgList.py') != os.path.getsize(FILEPATH + 'EpgList-new.py'):
					if not fileExists(FILEPATH + 'EpgList-ori.py') :
						system('cp -f ' + FILEPATH + 'EpgList.py ' + FILEPATH + 'EpgList-ori.py')
						system('rm -rf ' + FILEPATH + 'EpgList.py')
						system('cp -f ' + FILEPATH + 'EpgList-new.py ' + FILEPATH + 'EpgList.py')
						epgex = False
					elif fileExists(FILEPATH + 'EpgList-ori.py') and os.path.getsize(FILEPATH + 'EpgList.py') != os.path.getsize(FILEPATH + 'EpgList-ori.py'):
						system('rm -rf ' + FILEPATH + 'EpgList-ori.py')
						system('cp -f ' + FILEPATH + 'EpgList.py ' + FILEPATH + 'EpgList-ori.py')
						system('rm -rf ' + FILEPATH + 'EpgList.py')
						system('cp -f ' + FILEPATH + 'EpgList-new.py ' + FILEPATH + 'EpgList.py')
						epgex = False
					else:
						system('rm -rf ' + FILEPATH + 'EpgList.py')
						system('cp -f ' + FILEPATH + 'EpgList-new.py ' + FILEPATH + 'EpgList.py')
						epgex = False
				else:
					epgex = False
			except:
				pass

		elif not config.plugins.ExtraChannelSelection.epgext.value and config.plugins.ExtraChannelSelection.enabled.value:
			epgex = True
			try:
				if os.path.getsize(FILEPATH + 'EpgList.py') == os.path.getsize(FILEPATH + 'EpgList-new.py'):
					if fileExists(FILEPATH + 'EpgList-ori.py'):
						system('rm -rf ' + FILEPATH + 'EpgList.py')
						system('cp -f ' + FILEPATH + 'EpgList-ori.py ' + FILEPATH + 'EpgList.py')
						epgex = False
					else:
						pass
				else:
					if fileExists(FILEPATH + 'EpgList-ori.py') and os.path.getsize(FILEPATH + 'EpgList.py') != os.path.getsize(FILEPATH + 'EpgList-ori.py'):
						system('rm -rf ' + FILEPATH + 'EpgList.py')
						system('cp -f ' + FILEPATH + 'EpgList-ori.py ' + FILEPATH + 'EpgList.py')
						epgex = False
					else:
						pass
			except:
				pass

		listmode = True if fileExists(RPATH + 'listmode') else False
		enabled = True if fileExists(RPATH + 'enabled') else False
		okmode = True if fileExists(RPATH + 'okmode') else False
		epgext = True if fileExists(RPATH + 'epgext') else False
		doubmode = True if fileExists(RPATH + 'doubmode') else False
		if ((not config.plugins.ExtraChannelSelection.enabled.value and enabled) or
		 (config.plugins.ExtraChannelSelection.enabled.value and not enabled) or
		 (not config.plugins.ExtraChannelSelection.okmode.value and okmode) or
		 (config.plugins.ExtraChannelSelection.okmode.value and not okmode) or
		 (not config.plugins.ExtraChannelSelection.doubmode.value and doubmode) or
		 (config.plugins.ExtraChannelSelection.doubmode.value and not doubmode) or
		 (not config.plugins.ExtraChannelSelection.epgext.value and epgext) or
		 (config.plugins.ExtraChannelSelection.epgext.value and not epgext) or
		 (not config.plugins.ExtraChannelSelection.listmode.value and listmode) or
		 (config.plugins.ExtraChannelSelection.listmode.value and not listmode)):
			self.session.openWithCallback(self.restart, MessageBox,_("GUI needs a restart to apply a new settings\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO, timeout = 8)
		else:
			if fileExists(RPATH + 'listmode'):
				system('rm -rf ' + RPATH + 'listmode')
			if fileExists(RPATH + 'enabled'):
				system('rm -rf ' + RPATH + 'enabled')
			if fileExists(RPATH + 'okmode'):
				system('rm -rf ' + RPATH + 'okmode')
			if fileExists(RPATH + 'epgext'):
				system('rm -rf ' + RPATH + 'epgext')
			if fileExists(RPATH + 'doubmode'):
				system('rm -rf ' + RPATH + 'doubmode')
			self.close()

	def info(self):
		self.session.open(PluginHistory)

	def back(self):
		self.session.open(BackScreen)

	def restart(self, answer):
		if answer is True:
			if fileExists(RPATH + 'listmode'):
				system('rm -rf ' + RPATH + 'listmode')
			if fileExists(RPATH + 'enabled'):
				system('rm -rf ' + RPATH + 'enabled')
			if fileExists(RPATH + 'okmode'):
				system('rm -rf ' + RPATH + 'okmode')
			if fileExists(RPATH + 'epgext'):
				system('rm -rf ' + RPATH + 'epgext')
			if fileExists(RPATH + 'doubmode'):
				system('rm -rf ' + RPATH + 'doubmode')
			self.session.open(TryQuitMainloop, 3)

def main(session, **kwargs):
	session.open(ExtraChannelSelectionSetup)


def Plugins(path, **kwargs):
	list = [PluginDescriptor(name=_('ExtraChannelSelectionSetup'), description=_('Settings of service list on channel selection'), where = [PluginDescriptor.WHERE_PLUGINMENU], icon="ecs.png", fnc=main), PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=StartMainSession)]
	return list

