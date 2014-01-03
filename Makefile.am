ACLOCAL_AMFLAGS = -I m4

SUBDIRS = \
	alternativesoftcammanager \
	autovolume \
	dreamexplorer \
	hddmanager \
	libgisclub \
	networkbrowser \
	osdadjustment \
	rucam \
	settings36 \
	wicardd
#	antiscrollbar \
#	audiosync \
#	automaticcleanup \
#	automaticvolumeadjustment \
#	autoresolution \
#	autotimer \
#	babelzapper \
#	bitrateviewer \
#	bonjour \
#	cdinfo \
#	curlytx \
#	dreamirc \
#	dreammediathek \
#	dyndns \
#	easyinfo \
#	easymedia \
#	ecasa \
#	eibox \
#	elektro \
#	emailclient \
#	emission \
#	epgrefresh \
#	epgsearch \
#	eurotictv \
#	extrachannelselection \
#	filebrowser \
#	fritzcall \
#	fstabeditor \
#	ftpbrowser \
#	googlemaps \
#	growlee \
#	httpproxy \
#	imdb \
#	infobartunerstate \
#	kiddytimer \
#	lastfm \
#	letterbox \
#	logomanager \
#	mediadownloader \
#	merlinepg \
#	merlinepgcenter \
#	meteoitalia \
#	mosaic \
#	moviecut \
#	movieretitle \
#	moviesearch \
#	movieselectionquickbutton \
#	movietagger \
#	mphelp \
#	multiquickbutton \
#	multirc \
#	ncidclient \
#	netcaster \
#	ofdb \
#	orfat \
#	orfteletext \
#	partnerbox \
#	permanentclock \
#	permanenttimeshift \
#	pipservicerelation \
#	pipzap \
#	pluginhider \
#	pluginsort \
#	podcast \
#	porncenter \
#	quickbutton \
#	quickepg \
#	reconstructapsc \
#	remotetimer \
#	rsdownloader \
#	sambaserver \
#	seekbar \
#	serienfilm \
#	setpasswd \
#	shoutcast \
#	showclock \
#	simplerss \
#	startupservice \
#	startuptostandby \
#	subsdownloader2 \
#	svdrp \
#	tageditor \
#	trafficinfo \
#	tvcharts \
#	toolkit \
#	unwetterinfo \
#	valixdcontrol \
#	vfd_min \
#	virtualzap \
#	vlcplayer \
#	vps \
#	weatherplugin \
#	webcamviewer \
#	webbouqueteditor \
#	werbezapper \
#	youtubeplayer \
#	zaphistorybrowser \
#	zapstatistic \
#	zdfmediathek \
#	mytube \
#	yttrailer \
#	webinterface

metadir = $(datadir)/meta
meta_DATA = index-enigma2-plugins.xml
CLEANFILES = index-enigma2-plugins.xml

index-enigma2-plugins.xml: $(top_srcdir)/genmetaindex.py $(top_srcdir)/*/meta/plugin_*.xml
	$(AM_V_GEN)$(PYTHON) $^ > $@
