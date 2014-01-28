ACLOCAL_AMFLAGS = -I m4

SUBDIRS = \
	alternativesoftcammanager \
	automaticvolumeadjustment \
	autovolume \
	dreamexplorer \
	empanel \
	extrachannelselection \
	hddmanager \
	libgisclub \
	mgcamd \
	networkbrowser \
	oscam \
	osdadjustment \
	rucam \
	settings36 \
	settings36_4 \
	softcamsetup \
	wicardd \
	vfd_max \
	vfd_min

metadir = $(datadir)/meta
meta_DATA = index-enigma2-plugins.xml
CLEANFILES = index-enigma2-plugins.xml

index-enigma2-plugins.xml: $(top_srcdir)/genmetaindex.py $(top_srcdir)/*/meta/plugin_*.xml
	$(AM_V_GEN)$(PYTHON) $^ > $@
