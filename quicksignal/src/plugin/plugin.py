##
## Quick Signal
## by big-town
## modifed by Metabox1
##
from Components.ActionMap import ActionMap
from Components.config import config, ConfigInteger, ConfigSubsection, ConfigYesNo
#from Components.Language import language
#from Components.MenuList import MenuList
from GlobalActions import globalActionMap
from keymapparser import readKeymap, removeKeymap
from enigma import ePoint, eTimer, getDesktop
from Components.Pixmap import Pixmap
from os import environ
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
import gettext

##############################################################################
config.plugins.QuickSignal = ConfigSubsection()
config.plugins.QuickSignal.enabled = ConfigYesNo(default=True)
config.plugins.QuickSignal.enabled.value = False

##############################################################################


SKIN = """
	<screen name="QuickSignalScreen" position="50,65" size="1180,625"  title="Quick Signal Info" zPosition="1">
	        <widget source="session.FrontendStatus" render="Label"    position="420,20" zPosition="2" size="360,50" font="Regular;45" foregroundColor="#AAAAAA" halign="center" valign="center" transparent="1" >
			<convert type="FrontendInfo">SNRdB</convert>
		</widget>
		
		<!-- SNR -->
		<eLabel name="snr" text="SNR:"                              position="5,110" size="100,35" font="Regular;33" halign="right" foregroundColor="#AAAAAA" transparent="1" />
		<widget source="session.FrontendStatus" render="Progress"  position="135,80" size="910,100" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_snr-scan.png"    zPosition="2" borderWidth="4" borderColor="#656565">
			<convert type="FrontendInfo">SNR</convert>
		</widget>
		<widget source="session.FrontendStatus" render="Label"    position="1080,110" size="100,35" font="Regular;33" foregroundColor="#AAAAAA" transparent="1">
			<convert type="FrontendInfo">SNR</convert>
		</widget>
		
		<!-- AGC -->
		<eLabel name="agc" text="AGC:" 	                            position="5,240" size="100,35" font="Regular;33" halign="right" foregroundColor="#AAAAAA" transparent="1" />
		<widget source="session.FrontendStatus" render="Progress" position="135,210" size="910,100" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_snr-scan.png"    zPosition="2" borderWidth="4" borderColor="#656565">
			<convert type="FrontendInfo">AGC</convert>
		</widget>
		<widget source="session.FrontendStatus" render="Label"    position="1080,240" size="100,35" font="Regular;33" foregroundColor="#AAAAAA" transparent="1">
			<convert type="FrontendInfo">AGC</convert>
		</widget>
		
		<!-- BER -->
		<eLabel name="ber" text="BER:"                              position="5,370" size="100,35" font="Regular;33" halign="right" foregroundColor="#AAAAAA" transparent="1" />
		<widget source="session.FrontendStatus" render="Progress" position="135,340" size="910,100" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_off.png" zPosition="1" borderWidth="4" borderColor="#656565">
			<convert type="FrontendInfo">BER</convert>
		</widget>
		<widget source="session.FrontendStatus" render="Label"    position="320,450" size="540,40" font="Regular;38" foregroundColor="#AAAAAA" halign="center" valign="center" transparent="1">
			<convert type="FrontendInfo">BER</convert>
		</widget>

		<widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="4,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">1,10</convert> <convert type="ConditionalShowHide"/> 
                </widget>
		<widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="8,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">11,20</convert> <convert type="ConditionalShowHide"/> 
                </widget>
		<widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="12,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">21,30</convert> <convert type="ConditionalShowHide"/> 
                </widget>
		<widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="16,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">31,40</convert> <convert type="ConditionalShowHide"/> 
                </widget>
		<widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="20,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">41,50</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="25,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">51,60</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="30,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">61,70</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="35,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">71,80</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="40,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">81,90</convert> <convert type="ConditionalShowHide"/> 
                </widget>
		<widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="45,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">91,100</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="50,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">101,200</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="55,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">201,300</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="60,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">301,400</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="65,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">401,500</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="70,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">501,600</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="75,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">601,700</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="80,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">701,800</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="85,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">801,900</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="90,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">901,1000</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="95,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">1001,5000</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="100,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">5001,10000</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="150,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">9001,10000</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="200,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">10001,50000</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="250,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">50001,100001</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="400,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">100001,150000</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="600,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">150001,200000</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="700,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">200001,250000</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="800,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">250001,319999</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                <widget source="session.FrontendStatus" render="Pixmap"   position="135,340" size="910,100" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/icon_ber-scan_on.png" transparent="1" >
			<convert type="QuickSignalText">BerNum</convert> <convert type="ValueRange">320000,320000</convert> <convert type="ConditionalShowHide"/> 
                </widget>
                
	        <!-- Picon -->
	        <ePixmap position="135,538" size="100,60" zPosition="1" transparent="1" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/icons_quick/picon_fon.png" />
		<widget source="session.CurrentService" render="QuickPicon"     position="135,538" size="100,60" zPosition="3" alphatest="on">
			<convert type="QuickServName2">Reference</convert>
		</widget>
		
		<!-- Channel and Provider -->
                <widget source="session.CurrentService" render="Label"          position="260,540" size="325,25" font="Regular;23" backgroundColor="#000000" foregroundColor="#dddddd" transparent="1">
			<convert type="QuickServName2">Name</convert>
		</widget>
		<widget source="session.CurrentService" render="Label"          position="260,575" size="280,23" font="Regular;21" backgroundColor="#000000" foregroundColor="#aaaaaa" transparent="1">
			<convert type="QuickServName2">Provider</convert>
		</widget>
		
		<!-- Tuner Info  -->  
		<widget source="session.CurrentService" render="Label"    position="595,538" size="450,30" font="Regular;27" halign="right" backgroundColor="#000000" foregroundColor="#cccccc" transparent="1">
                       <convert type="QuickServName2">%F %p %Y %f %M %s</convert>
                </widget>
                <widget source="session.CurrentService" render="Label"    position="545,575" size="500,23" font="Regular;21" halign="right" backgroundColor="#000000" foregroundColor="#aaaaaa" transparent="1">
                       <convert type="QuickServName2">%c %l %h %m %g %b %e %S</convert>
                </widget>
		
	</screen>"""
	

##############################################################################

class QuickSignalScreen(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = SKIN


##############################################################################

class QuickSignal():
	def __init__(self):
		self.dialog = None

	def gotSession(self, session):
		keymap = "/usr/lib/enigma2/python/Plugins/Extensions/QuickSignal/keymap.xml"
		global globalActionMap
		readKeymap(keymap)
		self.dialog = session.instantiateDialog(QuickSignalScreen)
		#self.dialog.show()
		globalActionMap.actions['showQuickSignal'] = ShowHide
		#self.ShowHide()

pSignal = QuickSignal()

def ShowHide():
	if config.plugins.QuickSignal.enabled.value:
		config.plugins.QuickSignal.enabled.value = False
		pSignal.dialog.hide()
	else:
		config.plugins.QuickSignal.enabled.value = True
		pSignal.dialog.show()




##############################################################################


def sessionstart(reason, **kwargs):
	if reason == 0:
		pSignal.gotSession(kwargs["session"])

##############################################################################

def Plugins(**kwargs):
	return [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart)]
	
