ACLOCAL_AMFLAGS = -I m4

SUBDIRS = \
	alternativesoftcammanager \
	automaticvolumeadjustment \
	autovolume \
	dreamexplorer \
	duckba \
	empanel \
	epanel \
	extrachannelselection \
	hddmanager \
	hdmicec \
	imagemanager \
	libgisclub \
	mgcamd \
	mediaplayer2 \
	networkbrowser \
	oscam \
	osdadjustment \
	quicksignal \
	rucam \
	settings36 \
	settings36_4 \
	settings4 \
	simplesatscan \
	shootyourscreen \
	shoutcast \
	softcamsetup \
	spzzaphistory \
	timeronoff \
	wicardd \
	vfdmax \
	vfdmin

metadir = $(datadir)/meta
meta_DATA = index-enigma2-plugins.xml
CLEANFILES = index-enigma2-plugins.xml

index-enigma2-plugins.xml: $(top_srcdir)/genmetaindex.py $(top_srcdir)/*/meta/plugin_*.xml
	$(AM_V_GEN)$(PYTHON) $^ > $@
