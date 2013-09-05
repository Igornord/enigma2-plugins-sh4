# New component ServiceList.py, working on only OpenPli
# Coded by a.k.a. Uchkun - 2013 (c) thxs to Nikolasi
# The idea is based on the source code listboxservice.cpp, peeped here http://code.google.com/p/taapat-enigma2-pli/source/browse/lib/service/listboxservice.cpp?r=8528cb48c2ef7add5686f00cbefc967f7472e9ba
# but used another module eListboxPythonMultiContent
#

# imported
from HTMLComponent import HTMLComponent
from GUIComponent import GUIComponent
from enigma import eListboxServiceContent, eListbox, eServiceCenter,eServiceCenter_getInstance, eServiceReference, gFont, eRect, eEnv, eListboxPythonMultiContent, RT_WRAP, RT_VALIGN_TOP, RT_VALIGN_CENTER, RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, iServiceInformation, eEPGCache, eLabel, eSize, ePicLoad
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, fileExists, SCOPE_CURRENT_PLUGIN, SCOPE_SKIN_IMAGE
from Components.config import *
from ServiceReference import ServiceReference
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from time import time, localtime
from skin import dom_skins, parseColor, parseFont

# taken from the config settings
config.plugins.ExtraChannelSelection = ConfigSubsection()
config.plugins.ExtraChannelSelection.listmode = ConfigYesNo(default=False)
config.plugins.ExtraChannelSelection.text = ConfigYesNo(default=False)
config.plugins.ExtraChannelSelection.piconmode = ConfigYesNo(default=True)
config.plugins.ExtraChannelSelection.colormode = ConfigYesNo(default= True)


# the use of plugin options
DOUBLE = False
try:
	if config.plugins.ExtraChannelSelection.listmode.value:
		DOUBLE = True
except:
	pass


# function only for openpli
def refreshServiceList(configElement = None):
	from Screens.InfoBar import InfoBar
	InfoBarInstance = InfoBar.instance
	if InfoBarInstance is not None:
		servicelist = InfoBarInstance.servicelist
		if servicelist:
			servicelist.setMode()


# construction of the channel list
class ServiceList(HTMLComponent, GUIComponent):
	PiconPaths = ('/usr/share/enigma2/picon/', '/media/cf/picon/', '/media/usb/picon/', '/media/ba/picon/', '/media/hdd/picon/', '/picon/')
	MODE_NORMAL = 0
	MODE_FAVOURITES = 1

	def __init__(self):
		GUIComponent.__init__(self)
		self.picFolder = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/folder.png"))
		self.picMarker = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/marker.png"))
		self.picDVB_S = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/ico_dvb_s-fs8.png"))
		self.picDVB_T = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/ico_dvb_t-fs8.png"))
		self.picDVB_C = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, 'ico_dvb_c-fs8.png'))
		self.picServiceGroup = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, 'ico_service_group-fs8.png'))

		# variations with pictures for bar from plugin options
		self.picBar = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog9.png"))
		self.picBar1 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog1.png"))
		self.picBar2 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog2.png"))
		self.picBar3 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog3.png"))
		self.picBar4 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog4.png"))
		self.picBar5 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog5.png"))
		self.picBar6 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog6.png"))
		self.picBar7 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog7.png"))
		self.picBar8 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog8.png"))
		self.picBar9 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog9.png"))
		self.picBar10 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog10.png"))
		self.picBar11 = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, "SystemPlugins/ExtraChannelSelection/images/bar_prog11.png"))

		# declare colors for marked and markedselected with Dec value use
		# or you can use the value None, if you are sure that they are in the skin
		self.markedForeground = 15774720
		self.markedBackground = 624318628
		self.markedForegroundSelected = 9437216
		self.markedBackgroundSelected = 624318628

		# or take these colors from the skin, if exists
		try:
			for path, skin in dom_skins:
				for windowstyle in skin.findall('windowstyle'):
					get_attr = windowstyle.attrib.get
					windowstyle_id = get_attr('id')
					windowstyle_typed = get_attr('type')
					if windowstyle_id == '0' and windowstyle_typed == 'skinned':
						for color in windowstyle.findall('color'):
							get_attr = color.attrib.get
							colorType = get_attr('name')
							if colorType == 'ListboxMarkedForeground':
								self.markedForeground = parseColor(get_attr('color')).argb()
							elif colorType == 'ListboxMarkedBackground':
								self.markedBackground = parseColor(get_attr('color')).argb()
							elif colorType == 'ListboxMarkedAndSelectedForeground':
								self.markedForegroundSelected = parseColor(get_attr('color')).argb()
							elif colorType == 'ListboxMarkedAndSelectedBackground':
								self.markedBackgroundSelected = parseColor(get_attr('color')).argb()
						break
		except:
			pass

		# declare other colors with Dec value use, and declare pixmap for bar
		self.serviceNotAvail = 6710886
		self.eventForeground = 10519808
		self.eventForegroundSelected = 65535
		self.serviceNameForeground = 16777215
		self.serviceNameForegroundSelected = 16776960
		self.eventborderForeground = None
		self.serviceEventProgressbarColor = 5622089
		self.serviceEventProgressbarColorSelected = 4772300
		self.serviceEventProgressbarBorderColor = 6710886
		self.serviceEventProgressbarBorderColorSelected = 8421631

		self.l = eListboxPythonMultiContent() # will use this module from enigma for the construction new channel list
		self.l.setBuildFunc(self.buildServiceList) # building new channel list

		# declare fonts
		self.l.setFont(0, gFont('Regular', 22))
		self.l.setFont(1, gFont('Regular', 18))
		self.l.setFont(2, gFont('Regular', 22))
		self.ServiceNameFont = gFont('Regular', 22)
		self.l.setFont(3, gFont('Regular', 20))
		self.l.setFont(4, gFont('Regular', 22))
		self.l.setFont(5, gFont('Regular', 20))
		self.l.setFont(6, gFont('Regular', 20))
		self.l.setFont(10, gFont('Regular', 17))
		self.l.setFont(7, gFont('Regular', 28))
		self.l.setFont(8, gFont('Regular', 18))
		self.l.setFont(9, gFont('Regular', 8))
		# declare functions
		self.list = []
		self.size = 0
		self.service_center = eServiceCenter.getInstance()
		self.numberoffset = 0
		self.is_playable_ignore = eServiceReference()
		self.current_marked = False
		self.marked = []
		self.marker_list = []
		self.l.lookupService = self.lookupService
		self.root = None
		self.mode = self.MODE_NORMAL

		# show picon by the module ePicLoad when you select -show picons in plugin
		# assign the row height
		if DOUBLE:
			self.ItemHeight = 52
		else:
			self.ItemHeight = 32
		self.l.setItemHeight(self.ItemHeight)

		self.onSelectionChanged = []

	# find picons
	def findPicon(self, service = None):
		if config.plugins.ExtraChannelSelection.piconmode.value:
			if service is not None:
				service = service.toString()
				pos = service.rfind(':')
				if pos != -1:
					service = '_'.join(service.split(':', 10)[:10])
				for path in self.PiconPaths:
					pngname = path + service + ".png"
					if fileExists(pngname):
						return pngname 
	# construction new service list
	def buildServiceList(self, service, **args):
		
		if config.plugins.ExtraChannelSelection.piconmode.value:
			self.picon = ePicLoad()
			
		if config.plugins.ExtraChannelSelection.piconmode.value:
			picon = self.findPicon(service)

			# find default picon
			if picon is None:
				tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
				if fileExists(tmp):
					picon = tmp
				else:
					picon = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')

			# new sizes of picon
			if DOUBLE:
				piconWidth = 80
				piconHeight = 48
			else:
				piconWidth = 50
				piconHeight = 30
			self.picon.setPara((piconWidth, piconHeight, 1, 1, False, 1, '#000f0f0f')) # set new parameters (sizes &&) of picon
			self.picon.startDecode(picon, 0, 0, False) # resizing picon
			picon2 = self.picon.getData() # picon with new sizes

		width = self.l.getItemSize().width()
		selected = True
		try:
			selected = args['selected']
		except:
			pass
		res = [None]
		service_info = self.service_center.info(service)
		isMarker = service.flags & eServiceReference.isMarker
		isPlayable = not (service.flags & eServiceReference.isDirectory or isMarker)
		recording = False
		pixmap = None
		pixico = None
		fontnum = config.plugins.ExtraChannelSelection.fontnum.value
		fontperc = config.plugins.ExtraChannelSelection.fontperc.value
		fontname = config.plugins.ExtraChannelSelection.fontname.value
		fontevent = config.plugins.ExtraChannelSelection.fontevent.value
		fontend = config.plugins.ExtraChannelSelection.fontend.value
		fontrem = config.plugins.ExtraChannelSelection.fontrem.value
		fonttxt = config.plugins.ExtraChannelSelection.fonttxt.value
		fontsat = config.plugins.ExtraChannelSelection.fontsat.value
		self.sizedict = {
					'1':17,
					'2':18,
					'3':19,
					'4':20,
					'5':21,
					'6':22,
					'7':23,
					'8':24,
					'9':25,
					'10':26,
				}
		if fontnum in self.sizedict:
			self.l.setFont(0, gFont('Regular', self.sizedict[fontnum]))
		else:
			self.l.setFont(0, gFont('Regular', 22))
		if fontperc in self.sizedict:
			self.l.setFont(1, gFont('Regular', self.sizedict[fontperc]))
		else:
			self.l.setFont(1, gFont('Regular', 18))
		if fontname in self.sizedict:
			self.l.setFont(2, gFont('Regular', self.sizedict[fontname]))
			self.ServiceNameFont = gFont('Regular', self.sizedict[fontname])
		else:
			self.l.setFont(2, gFont('Regular', 22))
			self.ServiceNameFont = gFont('Regular', 22)
		if fontevent in self.sizedict:
			self.l.setFont(3, gFont('Regular', self.sizedict[fontevent]))
		else:
			self.l.setFont(3, gFont('Regular', 20))
		if fontend in self.sizedict:
			self.l.setFont(4, gFont('Regular', self.sizedict[fontend]))
		else:
			self.l.setFont(4, gFont('Regular', 22))
		if fontrem in self.sizedict:
			self.l.setFont(5, gFont('Regular', self.sizedict[fontrem]))
		else:
			self.l.setFont(5, gFont('Regular', 20))
		if fonttxt in self.sizedict:
			self.l.setFont(6, gFont('Regular', self.sizedict[fonttxt]))
		else:
			self.l.setFont(6, gFont('Regular', 20))
		if fontsat in self.sizedict:
			self.l.setFont(10, gFont('Regular', self.sizedict[fontsat]))
		else:
			self.l.setFont(10, gFont('Regular', 17))
		usagemode = config.usage.show_event_progress_in_servicelist.value # working only for openpli
		iconmode = config.usage.servicetype_icon_mode.value
		barmode = config.plugins.ExtraChannelSelection.barmode.value
		percmode = config.plugins.ExtraChannelSelection.percmode.value
		barpercmode = config.plugins.ExtraChannelSelection.barpercmode.value
		percpos = config.plugins.ExtraChannelSelection.percpos.value
		coltext = config.plugins.ExtraChannelSelection.coltext.value
		colnum = config.plugins.ExtraChannelSelection.colnum.value
		colselnum = config.plugins.ExtraChannelSelection.colselnum.value
		colend = config.plugins.ExtraChannelSelection.colend.value
		colselend = config.plugins.ExtraChannelSelection.colselend.value
		colremain = config.plugins.ExtraChannelSelection.colremain.value
		colselremain = config.plugins.ExtraChannelSelection.colselremain.value
		colsat = config.plugins.ExtraChannelSelection.colsat.value
		colselsat = config.plugins.ExtraChannelSelection.colselsat.value
		colbar = config.plugins.ExtraChannelSelection.colbar.value
		colbarsel = config.plugins.ExtraChannelSelection.colbarsel.value
		picbar = config.plugins.ExtraChannelSelection.picbar.value
		colborder = config.plugins.ExtraChannelSelection.colborder.value
		colbordersel = config.plugins.ExtraChannelSelection.colbordersel.value
		colname = config.plugins.ExtraChannelSelection.colname.value
		colnamesel = config.plugins.ExtraChannelSelection.colnamesel.value
		colperc = config.plugins.ExtraChannelSelection.colperc.value
		colpercsel = config.plugins.ExtraChannelSelection.colpercsel.value
		colevent = config.plugins.ExtraChannelSelection.colevent.value
		coleventsel = config.plugins.ExtraChannelSelection.coleventsel.value
		self.colordict = {
					'1':16753920,
					'2':1401021,
					'3':8421504,
					'4':3100495,
					'5':32896,
					'6':65535,
					'7':1644912,
					'8':4620980,
					'9':65280,
					'10':12632256,
					'11':36080,
					'12':16776960,
					'13':16711680,
					'14':16711935,
					'15':16777215,
					'16':255,
					'17':9127187,
					'18':14423100,
					'19':6908265,
					'20':13808780,
					'21':3050327,
					'22':16761035,
					'23':12211667,
					'24':13458524,
					'25':16444375,
					'26':65407,
					'27':4915330,
					'28':25600,
					'29':5597999,
					'31':0,
					'32':4144959,
					'33':10329501,
					'34':8947848,
					'35':15774720,
				}
		self.picdict = {
					'1':self.picBar,
					'2':self.picBar11,
					'3':self.picBar1,
					'4':self.picBar2,
					'5':self.picBar3,
					'6':self.picBar4,
					'7':self.picBar5,
					'8':self.picBar6,
					'9':self.picBar7,
					'10':self.picBar8,
					'11':self.picBar9,
					'12':self.picBar10,
				}
		if config.plugins.ExtraChannelSelection.text.value:
			if coltext in self.colordict:
				txtColor = self.colordict[coltext]
			else:
				txtColor = self.markedForeground
		else:
			pass
		if barmode == '1':
			if colbar in self.colordict:
				barColor = self.colordict[colbar]
			else:
				barColor = self.serviceEventProgressbarColor
			if colbarsel in self.colordict:
				barColorSel = self.colordict[colbarsel]
			else:
				barColorSel = self.serviceEventProgressbarColorSelected
		elif barmode == '2':
			if picbar in self.picdict:
				pixbar = self.picdict[picbar]
			if colbordersel in self.colordict:
				borderColorSel = self.colordict[colbordersel]
			else:
				borderColorSel = self.serviceEventProgressbarBorderColorSelected
		if colborder in self.colordict:
			borderColor = self.colordict[colborder]
		else:
			borderColor = self.serviceEventProgressbarBorderColor
		if colsat in self.colordict:
			satColor = self.colordict[colsat]
		else:
			satColor = 16444375
		if colselsat in self.colordict:
			satColorSel = self.colordict[colselsat]
		else:
			satColorSel = 16444375
		if not config.plugins.ExtraChannelSelection.colormode.value:
			if colnum in self.colordict:
				numColor = self.colordict[colnum]
			else:
				numColor = self.eventForeground
			if colselnum in self.colordict:
				numColorSel = self.colordict[colselnum]
			else:
				numColorSel = self.eventForegroundSelected
			if colname in self.colordict:
				nameColor = self.colordict[colname]
			else:
				nameColor = self.serviceNameForeground
			if colnamesel in self.colordict:
				nameColorSel = self.colordict[colnamesel]
			else:
				nameColorSel = self.serviceNameForegroundSelected
			if colperc in self.colordict:
				percColor = self.colordict[colperc]
			else:
				percColor = self.eventForeground
			if colpercsel in self.colordict:
				percColorSel = self.colordict[colpercsel]
			else:
				percColorSel = self.eventForegroundSelected
			if colevent in self.colordict:
				eventColor = self.colordict[colevent]
			else:
				eventColor = self.eventForeground
			if coleventsel in self.colordict:
				eventColorSel = self.colordict[coleventsel]
			else:
				eventColorSel = self.eventForegroundSelected
			if config.plugins.ExtraChannelSelection.listmode.value:
				if colend in self.colordict:
					endColor = self.colordict[colend]
				else:
					endColor = self.eventForeground
				if colselend in self.colordict:
					endColorSel = self.colordict[colselend]
				else:
					endColorSel = self.eventForegroundSelected
				if colremain in self.colordict:
					remColor = self.colordict[colremain]
				else:
					remColor = self.markedForeground
				if colselremain in self.colordict:
					remColorSel = self.colordict[colselremain]
				else:
					remColorSel = self.markedForegroundSelected
		else:
			numColor = self.eventForeground
			numColorSel = self.eventForegroundSelected
			endColor = self.eventForeground
			endColorSel = self.eventForegroundSelected
			remColor = self.markedForeground
			remColorSel = self.markedForegroundSelected
			nameColor = self.serviceNameForeground
			nameColorSel = self.serviceNameForegroundSelected
			percColor = self.eventForeground
			percColorSel = self.eventForegroundSelected
			eventColor = self.eventForeground
			eventColorSel = self.eventForegroundSelected
		notChannelMode = False
		if service.flags & eServiceReference.isMarker:
			pixmap = self.picMarker
			notChannelMode = True
			selected = False
		elif service.flags & eServiceReference.isGroup:
			pixmap = self.picServiceGroup
			notChannelMode = True
		elif service.flags & eServiceReference.isDirectory:
			pixmap = self.picFolder
			notChannelMode = True
		else:
			orbpos = service.getUnsignedData(4) >> 16
			if orbpos == 65535:
				pixico = self.picDVB_C
			elif orbpos == 61166:
				pixico = self.picDVB_T
			elif orbpos == 0:
				pixico = self.picDVB_T
			else:
				pixico = self.picDVB_S
		height = self.l.getItemSize().height()
		yDouble = height / 2
		marked = 0
		if self.current_marked and selected:
			marked = 2
		elif self.isMarked(service):
			if selected:
				marked = 2
			else:
				marked = 1
		if marked == 1:
			backgroundColor = backgroundColorSel = None
		elif marked == 2:
			numColorSel = nameColorSel = percColorSel = eventColorSel = endColorSel = remColorSel = foregroundColorSel = self.markedForegroundSelected
			backgroundColorSel = self.markedBackgroundSelected
			foregroundColor = serviceDescriptionColor = backgroundColor = None
		else:
			backgroundColor = backgroundColorSel = None
		if marked == 0 and isPlayable and service_info and self.is_playable_ignore.valid() and not service_info.isPlayable(service, self.is_playable_ignore):
			numColor = numColorSel = nameColor = nameColorSel = percColor = percColorSel = eventColor = eventColorSel = endColor = endColorSel = remColor = remColorSel = txtColor = self.serviceNotAvail
		if marked > 0:
			res.append((eListboxPythonMultiContent.TYPE_TEXT,
			 0,
			 0,
			 width,
			 height,
			 1,
			 RT_HALIGN_RIGHT,
			 '',
			 foregroundColor,
			 foregroundColorSel,
			 backgroundColor,
			 backgroundColorSel))
		info = self.service_center.info(service)
		serviceName = info.getName(service) or ServiceReference(service).getServiceName() or ''
		event = info.getEvent(service)
		index = self.getCurrentIndex()
		xPos = 4
		if pixmap is not None:
			pixmap_size = self.picMarker.size()
			yPos = (height - pixmap_size.height()) / 2
			pix_width = pixmap_size.width()
			res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
			 xPos,
			 yPos,
			 pix_width,
			 height,
			 pixmap))
			xPos += pix_width + 5
		if pixico is not None:
			if iconmode == '1':
				pixmap_size = self.picMarker.size()
				yPos = (height - pixmap_size.height()) / 2
				pix_width = pixmap_size.width()
				res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
				 xPos,
				 yPos,
				 pix_width,
				 height,
				 pixico))
				xPos += pix_width + 5
			else:
				pass
		if not config.usage.show_channel_numbers_in_servicelist.value: # working only for openpli
			pass
		elif self.mode != self.MODE_NORMAL:
			if not service.flags & eServiceReference.isMarker:
				markers_before = 0
				for markers in self.marker_list:
					if index > markers:
						markers_before += 1
					else:
						break
				num = '%d' % (self.numberoffset + index + 1 - markers_before)
				if DOUBLE:
					res.append((eListboxPythonMultiContent.TYPE_TEXT,
					 xPos,
					 0,
					 60,
					 52,
					 7,
					 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
					 num,
					 numColor,
					 numColorSel,
					 backgroundColor,
					 backgroundColorSel))
					xPos += 63
				else:
					res.append((eListboxPythonMultiContent.TYPE_TEXT,
					 xPos,
					 0,
					 45,
					 height,
					 0,
					 RT_HALIGN_RIGHT | RT_VALIGN_CENTER,
					 num,
					 numColor,
					 numColorSel,
					 backgroundColor,
					 backgroundColorSel))
					xPos += 50
		if not notChannelMode:
			bar = 0
			perc = ''
			if event and isPlayable:
				i = 100 * (int(time()) - event.getBeginTime()) / event.getDuration()
				if i < 101:
					bar = i
					if percmode == '2':
						perc = str(i) + '%'
					elif percmode == '3':
						perc = '(' + str(i) + '%' + ')'
			if DOUBLE:
				if config.plugins.ExtraChannelSelection.piconmode.value:
					picomode = config.plugins.ExtraChannelSelection.picomode.value
					pixpic = picon2
					if picomode == '1':
						res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
						 xPos,
						 2,
						 80,
						 48,
						 pixpic))
						xPos += 90
					else:
						res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
						 width - 81,
						 2,
						 80,
						 48,
						 pixpic))
				remain = ''
				remmode = config.plugins.ExtraChannelSelection.remmode.value
				if event and isPlayable:
					if remmode == '1':
						r = (event.getBeginTime() + event.getDuration()) / 60 - int(time() / 60)
						remain = '(' + '+' + str(r) + (' ') + _('min') + ')'
					if remmode == '2':
						r = ((event.getBeginTime() + event.getDuration()) / 60) - int(time() / 60)
						rh = r / 60
						rm = r - (rh * 60)
						remain = '(' + '+' + str(rh) + _('h') + str(rm) + _('min') + ')'
				if barmode == '1':
					res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
					 xPos,
					 9,
					 52,
					 8,
					 bar,
					 1,
					 barColor,
					 barColorSel,
					 backgroundColor,
					 backgroundColorSel))
					res.append((eListboxPythonMultiContent.TYPE_TEXT,
					 xPos,
					 9,
					 52,
					 8,
					 9,
					 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
					 '',
					 None,
					 barColorSel,
					 None,
					 None,
					 1,
					 borderColor,
					 backgroundColor,
					 backgroundColorSel))
				else:
					res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
					 xPos,
					 9,
					 52,
					 8,
					 bar,
					 pixbar,
					 1,
					 borderColor,
					 borderColorSel))
				if remmode == '1' or remmode == '2':
					res.append((eListboxPythonMultiContent.TYPE_TEXT,
					 xPos ,
					 yDouble,
					 110,
					 yDouble,
					 5,
					 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
					 remain,
					 remColor,
					 remColorSel))
				res.append((eListboxPythonMultiContent.TYPE_TEXT,
				 xPos + 57,
				 0,
				 60,
				 26,
				 1,
				 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
				 perc,
				 percColor,
				 percColorSel,
				 backgroundColor,
				 backgroundColorSel))
			else:
				if config.plugins.ExtraChannelSelection.piconmode.value:
					picomode = config.plugins.ExtraChannelSelection.picomode.value
					pixpic = picon2
					if picomode == '1':
						res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
						 xPos,
						 1,
						 50,
						 30,
						 pixpic))
						xPos += 60
						if usagemode == 'no':
							pass
						# its all working only for openpli
						elif barmode == '1' and usagemode != 'barright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
								 xPos,
								 12,
								 52,
								 8,
								 bar,
								 1,
								 barColor,
								 barColorSel,
								 backgroundColor,
								 backgroundColorSel))
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos,
								 12,
								 52,
								 8,
								 9,
								 RT_HALIGN_CENTER | RT_VALIGN_TOP,
								 '',
								 None,
								 barColorSel,
								 None,
								 None,
								 1,
								 borderColor,
								 backgroundColor,
								 backgroundColorSel))
								xPos += 57
							else:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
								 xPos,
								 22,
								 52,
								 8,
								 bar,
								 1,
								 barColor,
								 barColorSel,
								 backgroundColor,
								 backgroundColorSel))
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos,
								 22,
								 52,
								 8,
								 9,
								 RT_HALIGN_CENTER | RT_VALIGN_TOP,
								 '',
								 None,
								 barColorSel,
								 None,
								 None,
								 1,
								 borderColor,
								 backgroundColor,
								 backgroundColorSel))
						elif barmode == '1' and usagemode == 'barright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
								 width - 55,
								 12,
								 52,
								 8,
								 bar,
								 1,
								 barColor,
								 barColorSel,
								 backgroundColor,
								 backgroundColorSel))
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 width - 55,
								 12,
								 52,
								 8,
								 9,
								 RT_HALIGN_CENTER | RT_VALIGN_TOP,
								 '',
								 None,
								 barColorSel,
								 None,
								 None,
								 1,
								 borderColor,
								 backgroundColor,
								 backgroundColorSel))
							else:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
								 width - 55,
								 22,
								 52,
								 8,
								 bar,
								 1,
								 barColor,
								 barColorSel,
								 backgroundColor,
								 backgroundColorSel))
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 width - 55,
								 22,
								 52,
								 8,
								 9,
								 RT_HALIGN_CENTER | RT_VALIGN_TOP,
								 '',
								 None,
								 barColorSel,
								 None,
								 None,
								 1,
								 borderColor,
								 backgroundColor,
								 backgroundColorSel))
						elif barmode == '2' and usagemode != 'barright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
								 xPos,
								 12,
								 52,
								 8,
								 bar,
								 pixbar,
								 1,
								 borderColor,
								 borderColorSel))
								xPos += 57
							else:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
								 xPos,
								 22,
								 52,
								 8,
								 bar,
								 pixbar,
								 1,
								 borderColor,
								 borderColorSel))
						elif barmode == '2' and usagemode == 'barright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
								 width - 55,
								 12,
								 52,
								 8,
								 bar,
								 pixbar,
								 1,
								 borderColor,
								 borderColorSel))
							else:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
								 width - 55,
								 22,
								 52,
								 8,
								 bar,
								 pixbar,
								 1,
								 borderColor,
								 borderColorSel))
						if percmode == '1':
							pass
						elif usagemode != 'percright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos,
								 0,
								 55,
								 height,
								 1,
								 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
								 perc,
								 percColor,
								 percColorSel,
								 backgroundColor,
								 backgroundColorSel))
								xPos += 60
							else:
								if percpos == '1':
									res.append((eListboxPythonMultiContent.TYPE_TEXT,
									 xPos,
									 2,
									 55,
									 18,
									 8,
									 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
									 perc,
									 percColor,
									 percColorSel,
									 backgroundColor,
									 backgroundColorSel))
									xPos += 60
								else:
									res.append((eListboxPythonMultiContent.TYPE_TEXT,
									 width - 60,
									 2,
									 55,
									 18,
									 8,
									 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
									 perc,
									 percColor,
									 percColorSel,
									 backgroundColor,
									 backgroundColorSel))
						elif usagemode == 'percright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 width - 60,
								 0,
								 55,
								 height,
								 1,
								 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
								 perc,
								 percColor,
								 percColorSel,
								 backgroundColor,
								 backgroundColorSel))
							else:
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 width - 60,
								 2,
								 55,
								 18,
								 8,
								 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
								 perc,
								 percColor,
								 percColorSel,
								 backgroundColor,
								 backgroundColorSel))
					else:
						res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
						 width - 47,
						 2,
						 50,
						 30,
						 pixpic))
						if usagemode == 'no':
							pass

						# its all working only for openpli
						elif barmode == '1' and usagemode != 'barright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
								 xPos,
								 12,
								 52,
								 8,
								 bar,
								 1,
								 barColor,
								 barColorSel,
								 backgroundColor,
								 backgroundColorSel))
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos,
								 12,
								 52,
								 8,
								 9,
								 RT_HALIGN_CENTER | RT_VALIGN_TOP,
								 '',
								 None,
								 barColorSel,
								 None,
								 None,
								 1,
								 borderColor,
								 backgroundColor,
								 backgroundColorSel))
								xPos += 57
							else:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
								 xPos,
								 22,
								 52,
								 8,
								 bar,
								 1,
								 barColor,
								 barColorSel,
								 backgroundColor,
								 backgroundColorSel))
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos,
								 22,
								 52,
								 8,
								 9,
								 RT_HALIGN_CENTER | RT_VALIGN_TOP,
								 '',
								 None,
								 barColorSel,
								 None,
								 None,
								 1,
								 borderColor,
								 backgroundColor,
								 backgroundColorSel))
						elif barmode == '1' and usagemode == 'barright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
								 width - 110,
								 12,
								 52,
								 8,
								 bar,
								 1,
								 barColor,
								 barColorSel,
								 backgroundColor,
								 backgroundColorSel))
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 width - 110,
								 12,
								 52,
								 8,
								 9,
								 RT_HALIGN_CENTER | RT_VALIGN_TOP,
								 '',
								 None,
								 barColorSel,
								 None,
								 None,
								 1,
								 borderColor,
								 backgroundColor,
								 backgroundColorSel))
							else:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
								 width - 110,
								 22,
								 52,
								 8,
								 bar,
								 1,
								 barColor,
								 barColorSel,
								 backgroundColor,
								 backgroundColorSel))
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 width - 110,
								 22,
								 52,
								 8,
								 9,
								 RT_HALIGN_CENTER | RT_VALIGN_TOP,
								 '',
								 None,
								 barColorSel,
								 None,
								 None,
								 1,
								 borderColor,
								 backgroundColor,
								 backgroundColorSel))
						elif barmode == '2' and usagemode != 'barright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
								 xPos,
								 12,
								 52,
								 8,
								 bar,
								 pixbar,
								 1,
								 borderColor,
								 borderColorSel))
								xPos += 57
							else:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
								 xPos,
								 22,
								 52,
								 8,
								 bar,
								 pixbar,
								 1,
								 borderColor,
								 borderColorSel))
						elif barmode == '2' and usagemode == 'barright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
								 width - 110,
								 12,
								 52,
								 8,
								 bar,
								 pixbar,
								 1,
								 borderColor,
								 borderColorSel))
							else:
								res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
								 width - 110,
								 22,
								 52,
								 8,
								 bar,
								 pixbar,
								 1,
								 borderColor,
								 borderColorSel))
						if percmode == '1':
							pass
						elif usagemode != 'percright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos,
								 0,
								 55,
								 height,
								 1,
								 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
								 perc,
								 percColor,
								 percColorSel,
								 backgroundColor,
								 backgroundColorSel))
								xPos += 60
							else:
								if percpos == '1':
									res.append((eListboxPythonMultiContent.TYPE_TEXT,
									 xPos,
									 2,
									 55,
									 18,
									 8,
									 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
									 perc,
									 percColor,
									 percColorSel,
									 backgroundColor,
									 backgroundColorSel))
									xPos += 60
								else:
									res.append((eListboxPythonMultiContent.TYPE_TEXT,
									 width - 115,
									 2,
									 55,
									 18,
									 8,
									 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
									 perc,
									 percColor,
									 percColorSel,
									 backgroundColor,
									 backgroundColorSel))
						elif usagemode == 'percright':
							if not barpercmode:
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 width - 115,
								 0,
								 55,
								 height,
								 1,
								 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
								 perc,
								 percColor,
								 percColorSel,
								 backgroundColor,
								 backgroundColorSel))
							else:
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 width - 115,
								 2,
								 55,
								 18,
								 8,
								 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
								 perc,
								 percColor,
								 percColorSel,
								 backgroundColor,
								 backgroundColorSel))
				else:
					if usagemode == 'no':
						pass

					# its all working only for openpli
					elif barmode == '1' and usagemode != 'barright':
						if not barpercmode:
							res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
							 xPos,
							 12,
							 52,
							 8,
							 bar,
							 1,
							 barColor,
							 barColorSel,
							 backgroundColor,
							 backgroundColorSel))
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos,
							 12,
							 52,
							 8,
							 9,
							 RT_HALIGN_CENTER | RT_VALIGN_TOP,
							 '',
							 None,
							 barColorSel,
							 None,
							 None,
							 1,
							 borderColor,
							 backgroundColor,
							 backgroundColorSel))
							xPos += 57
						else:
							res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
							 xPos,
							 22,
							 52,
							 8,
							 bar,
							 1,
							 barColor,
							 barColorSel,
							 backgroundColor,
							 backgroundColorSel))
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos,
							 22,
							 52,
							 8,
							 9,
							 RT_HALIGN_CENTER | RT_VALIGN_TOP,
							 '',
							 None,
							 barColorSel,
							 None,
							 None,
							 1,
							 borderColor,
							 backgroundColor,
							 backgroundColorSel))
					elif barmode == '1' and usagemode == 'barright':
						if not barpercmode:
							res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
							 width - 55,
							 12,
							 52,
							 8,
							 bar,
							 1,
							 barColor,
							 barColorSel,
							 backgroundColor,
							 backgroundColorSel))
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 width - 55,
							 12,
							 52,
							 8,
							 9,
							 RT_HALIGN_CENTER | RT_VALIGN_TOP,
							 '',
							 None,
							 barColorSel,
							 None,
							 None,
							 1,
							 borderColor,
							 backgroundColor,
							 backgroundColorSel))
						else:
							res.append((eListboxPythonMultiContent.TYPE_PROGRESS,
							 width - 55,
							 22,
							 52,
							 8,
							 bar,
							 1,
							 barColor,
							 barColorSel,
							 backgroundColor,
							 backgroundColorSel))
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 width - 55,
							 22,
							 52,
							 8,
							 9,
							 RT_HALIGN_CENTER | RT_VALIGN_TOP,
							 '',
							 None,
							 barColorSel,
							 None,
							 None,
							 1,
							 borderColor,
							 backgroundColor,
							 backgroundColorSel))
					elif barmode == '2' and usagemode != 'barright':
						if not barpercmode:
							res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
							 xPos,
							 12,
							 52,
							 8,
							 bar,
							 pixbar,
							 1,
							 borderColor,
							 borderColorSel))
							xPos += 57
						else:
							res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
							 xPos,
							 22,
							 52,
							 8,
							 bar,
							 pixbar,
							 1,
							 borderColor,
							 borderColorSel))
					elif barmode == '2' and usagemode == 'barright':
						if not barpercmode:
							res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
							 width - 55,
							 12,
							 52,
							 8,
							 bar,
							 pixbar,
							 1,
							 borderColor,
							 borderColorSel))
						else:
							res.append((eListboxPythonMultiContent.TYPE_PROGRESS_PIXMAP,
							 width - 55,
							 22,
							 52,
							 8,
							 bar,
							 pixbar,
							 1,
							 borderColor,
							 borderColorSel))
					if percmode == '1':
						pass
					elif usagemode != 'percright':
						if not barpercmode:
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos,
							 0,
							 55,
							 height,
							 1,
							 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
							 perc,
							 percColor,
							 percColorSel,
							 backgroundColor,
							 backgroundColorSel))
							xPos += 60
						else:
							if percpos == '1':
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos,
								 2,
								 55,
								 18,
								 8,
								 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
								 perc,
								 percColor,
								 percColorSel,
								 backgroundColor,
								 backgroundColorSel))
								xPos += 60
							else:
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 width - 60,
								 2,
								 55,
								 18,
								 8,
								 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
								 perc,
								 percColor,
								 percColorSel,
								 backgroundColor,
								 backgroundColorSel))
					elif usagemode == 'percright':
						if not barpercmode:
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 width - 60,
							 0,
							 55,
							 height,
							 1,
							 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
							 perc,
							 percColor,
							 percColorSel,
							 backgroundColor,
							 backgroundColorSel))
						else:
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 width - 60,
							 2,
							 55,
							 18,
							 8,
							 RT_HALIGN_CENTER | RT_VALIGN_CENTER,
							 perc,
							 percColor,
							 percColorSel,
							 backgroundColor,
							 backgroundColorSel))
		if event and isPlayable:
			self.renderLabel.setFont(self.ServiceNameFont)
			self.renderLabel.setText(serviceName)
			length = self.renderLabel.calculateSize().width() + 10
			begin = localtime(event.getBeginTime())
			end = localtime(event.getBeginTime() + event.getDuration())
			eventmode = config.plugins.ExtraChannelSelection.eventmode.value
			picomode = config.plugins.ExtraChannelSelection.picomode.value
			if eventmode == '1':
				eventname = '%s' % event.getEventName()
			elif eventmode == '2':
				eventname = '(%s)' % event.getEventName()
			elif eventmode == '3':
				eventname = '-%s' % event.getEventName()
			if DOUBLE:
				res.append((eListboxPythonMultiContent.TYPE_TEXT,
				 xPos + 122,
				 0,
				 length,
				 yDouble,
				 2,
				 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
				 serviceName,
				 nameColor,
				 nameColorSel,
				 backgroundColor,
				 backgroundColorSel))
				endmode = config.plugins.ExtraChannelSelection.endmode.value
				if config.plugins.ExtraChannelSelection.piconmode.value:
					if picomode == '1':
						if endmode:
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos + 127 + length ,
							 0,
							 width - xPos - length - 132,
							 yDouble,
							 4,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 "%02d.%02d - %02d.%02d" % (begin[3],begin[4],end[3],end[4]),
							 endColor,
							 endColorSel,
							 backgroundColor,
							 backgroundColorSel))
						if remmode == '1' or remmode == '2':
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos + 115,
							 yDouble,
							 width - xPos - 120,
							 yDouble,
							 3,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 eventname,
							 eventColor,
							 eventColorSel,
							 backgroundColor,
							 backgroundColorSel))
						else:
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos,
							 yDouble,
							 width - xPos - 5,
							 yDouble,
							 3,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 eventname,
							 eventColor,
							 eventColorSel,
							 backgroundColor,
							 backgroundColorSel))
					else:
						if endmode:
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos + 127 + length,
							 0,
							 width - xPos - length - 222,
							 yDouble,
							 4,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 "%02d.%02d - %02d.%02d" % (begin[3],begin[4],end[3],end[4]),
							 endColor,
							 endColorSel,
							 backgroundColor,
							 backgroundColorSel))
						if remmode == '1' or remmode == '2':
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos + 115,
							 yDouble,
							 width - xPos - 210,
							 yDouble,
							 3,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 eventname,
							 eventColor,
							 eventColorSel,
							 backgroundColor,
							 backgroundColorSel))
						else:
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos,
							 yDouble,
							 width - xPos - 95,
							 yDouble,
							 3,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 eventname,
							 eventColor,
							 eventColorSel,
							 backgroundColor,
							 backgroundColorSel))
				else:
					if endmode:
						res.append((eListboxPythonMultiContent.TYPE_TEXT,
						 xPos + 127 + length,
						 0,
						 width - xPos - length - 132,
						 yDouble,
						 4,
						 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
						 "%02d.%02d - %02d.%02d" % (begin[3],begin[4],end[3],end[4]),
						 endColor,
						 endColorSel,
						 backgroundColor,
						 backgroundColorSel))
					if remmode == '1' or remmode == '2':
						res.append((eListboxPythonMultiContent.TYPE_TEXT,
						 xPos + 115,
						 yDouble,
						 width - xPos - 120,
						 yDouble,
						 3,
						 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
						 eventname,
						 eventColor,
						 eventColorSel,
						 backgroundColor,
						 backgroundColorSel))
					else:
						res.append((eListboxPythonMultiContent.TYPE_TEXT,
						 xPos,
						 yDouble,
						 width - xPos - 5,
						 yDouble,
						 3,
						 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
						 eventname,
						 eventColor,
						 eventColorSel,
						 backgroundColor,
						 backgroundColorSel))
			else:
				res.append((eListboxPythonMultiContent.TYPE_TEXT,
				 xPos + 4,
				 0,
				 length,
				 height,
				 2,
				 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
				 serviceName,
				 nameColor,
				 nameColorSel,
				 backgroundColor,
				 backgroundColorSel))
				xPos += length
				if pixico is not None:
					if iconmode == '2':
						pixmap_size = self.picMarker.size()
						yPos = (height - pixmap_size.height()) / 2
						pix_width = pixmap_size.width()
						res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
						 xPos,
						 yPos,
						 pix_width,
						 height,
						 pixico))
						xPos += pix_width + 5
					else:
						pass
				if usagemode != 'barright' and usagemode != 'percright':
					if config.plugins.ExtraChannelSelection.piconmode.value:
						if picomode == '1':
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos,
							 0,
							 width - xPos - 5,
							 height,
							 3,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 eventname,
							 eventColor,
							 eventColorSel,
							 backgroundColor,
							 backgroundColorSel))
						else:
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos,
							 0,
							 width - xPos - 57,
							 height,
							 3,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 eventname,
							 eventColor,
							 eventColorSel,
							 backgroundColor,
							 backgroundColorSel))
					else:
						res.append((eListboxPythonMultiContent.TYPE_TEXT,
						 xPos,
						 0,
						 width - xPos - 5,
						 height,
						 3,
						 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
						 eventname,
						 eventColor,
						 eventColorSel,
						 backgroundColor,
						 backgroundColorSel))
				elif usagemode == 'barright' or usagemode == 'percright':
					if config.plugins.ExtraChannelSelection.piconmode.value:
						if picomode == '1':
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos,
							 0,
							 width - xPos - 63,
							 height,
							 3,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 eventname,
							 eventColor,
							 eventColorSel,
							 backgroundColor,
							 backgroundColorSel))
						else:
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos,
							 0,
							 width - xPos - 115,
							 height,
							 3,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 eventname,
							 eventColor,
							 eventColorSel,
							 backgroundColor,
							 backgroundColorSel))
					else:
						res.append((eListboxPythonMultiContent.TYPE_TEXT,
						 xPos,
						 0,
						 width - xPos - 63,
						 height,
						 3,
						 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
						 eventname,
						 eventColor,
						 eventColorSel,
						 backgroundColor,
						 backgroundColorSel))
		elif DOUBLE:
			notEpg = _('No EPG data available')
			if notChannelMode:
				res.append((eListboxPythonMultiContent.TYPE_TEXT,
				 xPos + 5,
				 0,
				 width - xPos - 10,
				 52,
				 10,
				 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
				 serviceName,
				 satColor,
				 satColorSel,
				 backgroundColor,
				 backgroundColorSel))
			else:
				res.append((eListboxPythonMultiContent.TYPE_TEXT,
				 xPos + 125,
				 0,
				 width - xPos - 130,
				 yDouble,
				 2,
				 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
				 serviceName,
				 nameColor,
				 nameColorSel,
				 backgroundColor,
				 backgroundColorSel))
				if config.plugins.ExtraChannelSelection.text.value:
					res.append((eListboxPythonMultiContent.TYPE_TEXT,
					 xPos + 20,
					 yDouble,
					 width - xPos - 80,
					 yDouble,
					 6,
					 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
					 notEpg,
					 txtColor,
					 16444375,
					 backgroundColor,
					 backgroundColorSel))
		else:
			self.renderLabel.setFont(self.ServiceNameFont)
			self.renderLabel.setText(serviceName)
			length = self.renderLabel.calculateSize().width() + 10
			if notChannelMode:
				res.append((eListboxPythonMultiContent.TYPE_TEXT,
				 xPos + 5,
				 0,
				 width - xPos - 10,
				 height,
				 10,
				 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
				 serviceName,
				 satColor,
				 satColorSel,
				 backgroundColor,
				 backgroundColorSel))
			else:
				res.append((eListboxPythonMultiContent.TYPE_TEXT,
				 xPos + 5,
				 0,
				 length,
				 height,
				 2,
				 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
				 serviceName,
				 nameColor,
				 nameColorSel,
				 backgroundColor,
				 backgroundColorSel))
				if pixico is not None:
					if iconmode == '2':
						pixmap_size = self.picMarker.size()
						yPos = (height - pixmap_size.height()) / 2
						pix_width = pixmap_size.width()
						res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
						 xPos + length + 5,
						 yPos,
						 pix_width,
						 height,
						 pixico))
						xPos += pix_width + 5
					else:
						pass
				notEpg = _('No EPG data available')
				if config.plugins.ExtraChannelSelection.piconmode.value:
					picomode = config.plugins.ExtraChannelSelection.picomode.value
					if picomode == '1':
						if config.plugins.ExtraChannelSelection.text.value:
							if usagemode != 'barright' and usagemode != 'percright':
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos + length + 10,
								 0,
								 width - xPos - length - 15,
								 height,
								 6,
								 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
								 notEpg,
								 txtColor,
								 16444375,
								 backgroundColor,
								 backgroundColorSel))
							elif usagemode == 'barright' or usagemode == 'percright':
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos + length + 10,
								 0,
								 width - xPos - length - 75,
								 height,
								 6,
								 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
								 notEpg,
								 txtColor,
								 16444375,
								 backgroundColor,
								 backgroundColorSel))
					else:
						if config.plugins.ExtraChannelSelection.text.value:
							if usagemode != 'barright' and usagemode != 'percright':
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos + length + 10,
								 0,
								 width - xPos - length - 70,
								 height,
								 6,
								 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
								 notEpg,
								 txtColor,
								 16444375,
								 backgroundColor,
								 backgroundColorSel))
							elif usagemode == 'barright' or usagemode == 'percright':
								res.append((eListboxPythonMultiContent.TYPE_TEXT,
								 xPos + length + 10,
								 0,
								 width - xPos - length - 135,
								 height,
								 6,
								 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
								 notEpg,
								 txtColor,
								 16444375,
								 backgroundColor,
								 backgroundColorSel))
				else:
					if config.plugins.ExtraChannelSelection.text.value:
						if usagemode != 'barright' and usagemode != 'percright':
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos + length + 10,
							 0,
							 width - xPos - length - 15,
							 height,
							 6,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 notEpg,
							 txtColor,
							 16444375,
							 backgroundColor,
							 backgroundColorSel))
						elif usagemode == 'barright' or usagemode == 'percright':
							res.append((eListboxPythonMultiContent.TYPE_TEXT,
							 xPos + length + 10,
							 0,
							 width - xPos - length - 75,
							 height,
							 6,
							 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
							 notEpg,
							 txtColor,
							 16444375,
							 backgroundColor,
							 backgroundColorSel))
		return res

	def applySkin(self, desktop, parent):
		attribs = []
		if self.skinAttributes is not None:
			attribs = []
			for (attrib, value) in self.skinAttributes:
				if attrib == 'foregroundColorMarked':
					self.markedForeground = parseColor(value).argb()
				elif attrib == 'foregroundColorMarkedSelected':
					self.markedForegroundSelected = parseColor(value).argb()
				elif attrib == 'backgroundColorMarked':
					self.markedBackground = parseColor(value).argb()
				elif attrib == 'backgroundColorMarkedSelected':
					self.markedBackgroundSelected = parseColor(value).argb()
				elif attrib == 'foregroundColorServiceNotAvail':
					self.serviceNotAvail = parseColor(value).argb()
				elif attrib == "foregroundColorEvent" or attrib == "colorServiceDescription":
					self.eventForeground = parseColor(value).argb()
				elif attrib == "foregroundColorEventSelected" or attrib == "colorServiceDescriptionSelected":
					self.eventForegroundSelected = parseColor(value).argb()
				elif attrib == "foregroundColorEventborder":
					pass
				elif attrib == 'colorEventProgressbar':
					self.serviceEventProgressbarColor = parseColor(value).argb()
				elif attrib == 'colorEventProgressbarSelected':
					self.serviceEventProgressbarColorSelected = parseColor(value).argb()
				elif attrib == "colorEventProgressbarBorder":
					self.serviceEventProgressbarBorderColor = parseColor(value).argb()
				elif attrib == "colorEventProgressbarBorderSelected":
					self.serviceEventProgressbarBorderColorSelected = parseColor(value).argb()
				elif attrib == 'picServiceEventProgressbar':
					self.picBar = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, value))
				elif attrib == 'serviceItemHeight':
					if DOUBLE:
						self.ItemHeight = 52
					else:
						self.ItemHeight = int(value)
				elif attrib == 'serviceNameFont':
					fontname = config.plugins.ExtraChannelSelection.fontname.value
					fontend = config.plugins.ExtraChannelSelection.fontend.value
					if fontname == '11':
						self.l.setFont(2, parseFont(value, ((1, 1), (1, 1))))
						self.ServiceNameFont = parseFont(value, ((1, 1), (1, 1)))
					else:
						pass
					if fontend == '11':
						self.l.setFont(4, parseFont(value, ((1, 1), (1, 1))))
					else:
						pass
				elif attrib == 'serviceInfoFont':
					fontevent = config.plugins.ExtraChannelSelection.fontevent.value
					fontrem = config.plugins.ExtraChannelSelection.fontrem.value
					fonttxt = config.plugins.ExtraChannelSelection.fonttxt.value
					if fontevent == '11':
						self.l.setFont(3, parseFont(value, ((1, 1), (1, 1))))
					else:
						pass
					if fontrem == '11':
						self.l.setFont(5, parseFont(value, ((1, 1), (1, 1))))
					else:
						pass
					if fonttxt == '11':
						self.l.setFont(6, parseFont(value, ((1, 1), (1, 1))))
					else:
						pass
				elif attrib == 'serviceNumberFont':
					fontnum = config.plugins.ExtraChannelSelection.fontnum.value
					fontperc = config.plugins.ExtraChannelSelection.fontperc.value
					if fontnum == '11':
						self.l.setFont(0, parseFont(value, ((1, 1), (1, 1))))
					else:
						pass
					if fontperc == '11':
						self.l.setFont(1, parseFont(value, ((1, 1), (1, 1))))
					else:
						pass
				else:
					attribs.append((attrib, value))
			self.skinAttributes = attribs
		return GUIComponent.applySkin(self, desktop, parent)

	def connectSelChanged(self, fnc):
		if not fnc in self.onSelectionChanged:
			self.onSelectionChanged.append(fnc)

	def disconnectSelChanged(self, fnc):
		if fnc in self.onSelectionChanged:
			self.onSelectionChanged.remove(fnc)

	def selectionChanged(self):
		for i in self.onSelectionChanged:
			i()

	def setCurrent(self, ref):
		index = 0
		x = 0
		for i in self.list:
			if i[0] == ref:
				index = x
				break
			x += 1
		self.instance.moveSelectionTo(index)

	def getCurrent(self):
		r = eServiceReference()
		cur = self.l.getCurrentSelection()
		return cur and cur[0] or r

	def atBegin(self):
		if self.list:
			return self.instance.atBegin()
		else:
			return True

	def atEnd(self):
		if self.list:
			return self.instance.atEnd()
		else:
			return True

	def servicePageUp(self):
		cur = None
		if self.current_marked:
			cur = self.l.getCurrentSelection()
		self.instance.moveSelection(self.instance.pageUp)
		if self.current_marked:
			self.changePage(cur)

	def servicePageDown(self):
		cur = None
		if self.current_marked:
			cur = self.l.getCurrentSelection()
		self.instance.moveSelection(self.instance.pageDown)
		if self.current_marked:
			self.changePage(cur)

	def changePage(self, cur):
		if cur and cur[0]:
			index = self.getCurrentIndex()
			self.list.remove(cur)
			self.list.insert(index, cur)
			self.buildMarkerList()
			self.l.invalidate()

	def moveUp(self):
		if self.current_marked:
			cur = self.l.getCurrentSelection()
			if cur and cur[0]:
				index = self.list.index(cur)
				newindex = index - 1
				if newindex < 0:
					self.list.remove(cur)
					self.list.append(cur)
					self.buildMarkerList()
				else:
					self.updateList(index, newindex)
		self.instance.moveSelection(self.instance.moveUp)

	def moveDown(self):
		if self.current_marked:
			cur = self.l.getCurrentSelection()
			if cur and cur[0]:
				index = self.list.index(cur)
				newindex = index + 1
				list_size = len(self.list) - 1
				if newindex > list_size:
					self.list.remove(cur)
					self.list.insert(0, cur)
					self.buildMarkerList()
				else:
					self.updateList(index, newindex)
		self.instance.moveSelection(self.instance.moveDown)

	def updateList(self, index, newindex):
		service1 = self.list[index][0]
		service2 = self.list[newindex][0]
		tmp = self.list[index]
		self.list[index] = self.list[newindex]
		self.list[newindex] = tmp
		if service1.flags & eServiceReference.isMarker or service2.flags & eServiceReference.isMarker:
			self.buildMarkerList()

	def getNextBeginningWithChar(self, char):
		found = False
		index = 0
		for i in self.list:
			service = i[0]
			info = self.service_center.info(service)
			serviceName = info.getName(service) or ServiceReference(service).getServiceName() or ''
			if serviceName != '':
				idx = 0
				length = len(serviceName) - 1
				while idx <= length:
					sn = serviceName[idx]
					if ord(sn) >= 33 and ord(sn) < 127:
						if sn == char:
							found = True
						break
					idx += 1
			if found:
				break
			else:
				index += 1
		return index

	def moveToChar(self, char):
		print "Next char: "
		index = self.getNextBeginningWithChar(char)
		indexup = self.getNextBeginningWithChar(char.upper())
		if indexup != 0:
			if (index > indexup or index == 0):
				index = indexup
		self.instance.moveSelectionTo(index)
		print "Moving to character " + str(char)

	def moveToNextMarker(self):
		index = self.getCurrentIndex()
		idx = self.size - 1
		for marker in self.marker_list:
			if index < marker:
				idx = marker
				break
		self.instance.moveSelectionTo(idx)

	def moveToPrevMarker(self):
		index = self.getCurrentIndex()
		idx = 0
		for marker in reversed(self.marker_list):
			if index > marker:
				idx = marker
				break
		self.instance.moveSelectionTo(idx)

	def moveToIndex(self, index):
		self.instance.moveSelectionTo(index)

	def getCurrentIndex(self):
		return self.instance.getCurrentIndex()

	GUI_WIDGET = eListbox

	def postWidgetCreate(self, instance):
		instance.setWrapAround(True)
		instance.setContent(self.l)
		instance.selectionChanged.get().append(self.selectionChanged)
		self.setMode(self.mode)
		self.renderLabel = eLabel(self.instance)
		self.renderLabel.resize(eSize(450, 0))
		self.renderLabel.hide()

	def preWidgetRemove(self, instance):
		instance.setContent(None)
		instance.selectionChanged.get().remove(self.selectionChanged)

	def getRoot(self):
		return self.root

	def getRootServices(self):
		serviceHandler = eServiceCenter.getInstance()
		list = serviceHandler.list(self.root)
		dest = []
		if list is not None:
			while 1:
				y = list.getNext()
				if y.valid():
					dest.append(y.toString())
				else:
					break
		return dest

	def setNumberOffset(self, offset):
		self.numberoffset = offset

	def setPlayableIgnoreService(self, ref):
		self.is_playable_ignore = ref

	def setRoot(self, root, justSet=False):
		self.root = root
		self.list = []
		if justSet:
			self.l.setList(self.list)
			self.size = 0
			return
		serviceref = root.toString()
		self.marker_list = []
		list = self.service_center.list(self.root)
		list = list.getContent('R', True)
		index = 0
		for i in list:
			self.list.append((i,))
			if i.flags & eServiceReference.isMarker:
				self.marker_list.append(index)
			index += 1

		self.finishFill(sort=False)
		self.selectionChanged()

	# function only for openpli
	def resetRoot(self):
		self.s = eListboxServiceContent()
		index = self.instance.getCurrentIndex()
		self.s.setRoot(self.root, False)
		self.s.sort()
		self.instance.moveSelectionTo(index)

	def removeCurrent(self):
		if self.list:
			cur = self.l.getCurrentSelection()
			if cur and cur[0]:
				self.list.remove(cur)
				self.size -= 1
				self.buildMarkerList()
				self.l.invalidate()

	def buildMarkerList(self):
		index = 0
		self.marker_list = []
		for service in self.list:
			if service[0].flags & eServiceReference.isMarker:
				self.marker_list.append(index)
			index += 1

	def addService(self, service, beforeCurrent=False):
		if beforeCurrent and self.size:
			index = self.getCurrentIndex()
			self.list.insert(index, (service,))
		else:
			self.list.append((service,))
		self.buildMarkerList()
		self.size += 1
		self.l.invalidate()

	def finishFill(self, sort = True):
		self.renderLabel.setFont(self.ServiceNameFont)
		self.size = len(self.list)
		if sort:
			self.list.sort(self.sortList)
		self.l.setList(self.list)
		self.instance.moveSelectionTo(0)

	def sortList(self, a, b):
		return cmp(a[0].getUnsignedData(4), b[0].getUnsignedData(4))

	def clearMarks(self):
		self.marked = []

	def isMarked(self, ref):
		try:
			index = self.marked.index(ref)
			return True
		except ValueError:
			return False

	def addMarked(self, ref):
		self.marked.append(ref)
		self.l.invalidateEntry(self.getCurrentIndex())

	def removeMarked(self, ref):
		self.marked.remove(ref)
		self.l.invalidateEntry(self.getCurrentIndex())

	def getMarked(self):
		return [ marks.toString() for marks in self.marked ]

	def lookupService(self, ref):
		index = 0
		for i in self.list:
			if i[0] == ref:
				return index
			index += 1
		return index

	def setCurrentMarked(self, state):
		prev = self.current_marked
		self.current_marked = state
		if state != prev:
			if not state:
				list = self.service_center.list(self.root)
				if list is not None:
					mutableList = list.startEdit()
					if mutableList:
						position = self.getCurrentIndex()
						cur = self.l.getCurrentSelection()
						if cur and cur[0]:
							mutableList.moveService(cur[0], position)
			self.l.invalidateEntry(self.getCurrentIndex())

	def setMode(self, mode):
		self.mode = mode
		self.l.setItemHeight(self.ItemHeight)

