AC_INIT([enigma2-plugins],[3.2.0],[enigma2-devel@lists.elitedvb.net])
AM_INIT_AUTOMAKE([dist-bzip2 foreign no-define tar-pax])
AC_CONFIG_HEADERS([enigma2-plugins-config.h])

# Silent rules are available since 1.11, but older versions
# are still in use. So don't use them unconditionally.
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

AC_USE_SYSTEM_EXTENSIONS
AC_SYS_LARGEFILE

AC_PROG_CC
AC_PROG_CXX
m4_ifdef([LT_INIT], [LT_INIT], [AC_PROG_LIBTOOL])
AC_CONFIG_MACRO_DIR([m4])

AC_PATH_PROG(MSGFMT, msgfmt, AC_MSG_ERROR(Could not find msgfmt))

AM_PATH_PYTHON
AX_PYTHON_DEVEL
AX_PTHREAD

TUXBOX_APPS_DVB

PKG_CHECK_MODULES(ENIGMA2, enigma2)
AC_ARG_ENABLE(libeplayer3,
	[  --enable-libeplayer3          enable TDT libeplayer3 as player engine supportt],
	[AC_DEFINE(ENABLE_LIBEPLAYER3,1,[enable TDT libeplayer3 as player engine support])])

if ! test "$enable_libeplayer3" = "yes"; then
PKG_CHECK_MODULES(GSTREAMER, gstreamer-0.10 gstreamer-pbutils-0.10)
fi
PKG_CHECK_MODULES(LIBCRYPTO, libcrypto)
PKG_CHECK_MODULES(SIGC,sigc++-1.2)

AC_ARG_WITH(tpm,
	AS_HELP_STRING([--with-tpm], [enable plugins that require a TPM]),
	[with_tpm="$withval"],[with_tpm="no"])
if test "$with_tpm" = "yes"; then
	AC_DEFINE([HAVE_TPM],[1],[Define to 1 to enable plugins that require a TPM])
fi
AM_CONDITIONAL(TPM, test "$with_tpm" = "yes")

AC_ARG_WITH(debug,
	AS_HELP_STRING([--without-debug],[disable debugging code]),
	[with_debug="$withval"],[with_debug="yes"])
if test "$with_debug" = "yes"; then
	DEBUG_CFLAGS="-ggdb3"
	AC_DEFINE([DEBUG],[1],[Define to 1 to enable debugging code])
fi
AC_SUBST(DEBUG_CFLAGS)

AC_ARG_WITH(po,
	AS_HELP_STRING([--with-po],[enable updating of po files]),
	[with_po="$withval"],[with_po="no"])
if test "$with_po" = "yes"; then
	AC_PATH_PROG(MSGINIT, msginit)
	AC_PATH_PROG(MSGMERGE, msgmerge)
	AC_PATH_PROG(MSGUNIQ, msguniq)
	AC_PATH_PROG(XGETTEXT, xgettext)
	if test -z "$MSGINIT" -o -z "$MSGMERGE" -o -z "$MSGUNIQ" -o -z "$XGETTEXT"; then
		AC_MSG_ERROR([Could not find required gettext tools])
	fi
fi
AM_CONDITIONAL(UPDATE_PO, test "$with_po" = "yes")

AC_CONFIG_FILES([
Makefile

alternativesoftcammanager/Makefile
alternativesoftcammanager/meta/Makefile
alternativesoftcammanager/po/Makefile
alternativesoftcammanager/src/Makefile
alternativesoftcammanager/src/images/Makefile

automaticvolumeadjustment/Makefile
automaticvolumeadjustment/meta/Makefile
automaticvolumeadjustment/po/Makefile
automaticvolumeadjustment/src/Makefile

autovolume/Makefile
autovolume/meta/Makefile
autovolume/src/Makefile

dreamexplorer/Makefile
dreamexplorer/meta/Makefile
dreamexplorer/src/Makefile
dreamexplorer/src/res/Makefile

duckba/Makefile
duckba/src/Makefile
duckba/src/bin/Makefile
duckba/src/icons/Makefile

empanel/Makefile
empanel/meta/Makefile
empanel/po/Makefile
empanel/src/Makefile
empanel/src/images/Makefile
empanel/script/Makefile

epanel/Makefile
epanel/meta/Makefile
epanel/po/Makefile
epanel/src/Makefile
epanel/src/images/Makefile
epanel/src/script/Makefile

extrachannelselection/Makefile
extrachannelselection/meta/Makefile
extrachannelselection/po/Makefile
extrachannelselection/Components/Makefile
extrachannelselection/Screens/Makefile
extrachannelselection/src/Makefile
extrachannelselection/src/backup/Makefile
extrachannelselection/src/images/Makefile
extrachannelselection/src/script/Makefile

hddmanager/Makefile
hddmanager/meta/Makefile
hddmanager/po/Makefile
hddmanager/src/Makefile

hdmicec/Makefile
hdmicec/meta/Makefile
hdmicec/Components/Makefile
hdmicec/Plugin/Makefile

imagemanager/Makefile
imagemanager/po/Makefile
imagemanager/src/Makefile
imagemanager/src/bin/Makefile
imagemanager/src/icon/Makefile
imagemanager/src/lib/Makefile

libgisclub/Makefile
libgisclub/meta/Makefile
libgisclub/src/Makefile
libgisclub/src/Converter/Makefile
libgisclub/src/Renderer/Makefile
libgisclub/src/bitratecalc/Makefile

mgcamd/Makefile
mgcamd/meta/Makefile
mgcamd/src/Makefile
mgcamd/src/bin/Makefile
mgcamd/src/init/Makefile
mgcamd/src/keys/Makefile

mediaplayer2/Makefile
mediaplayer2/meta/Makefile
mediaplayer2/po/Makefile
mediaplayer2/src/Makefile
mediaplayer2/src/subtitles/Makefile
mediaplayer2/src/subtitles/fonts/Makefile
mediaplayer2/src/subtitles/parsers/Makefile

networkbrowser/Makefile
networkbrowser/meta/Makefile
networkbrowser/po/Makefile
networkbrowser/src/Makefile
networkbrowser/src/icons/Makefile
networkbrowser/src/lib/Makefile

oscam/Makefile
oscam/bin/Makefile
oscam/config/Makefile
oscam/init/Makefile
oscam/keys/Makefile
oscam/meta/Makefile

osdadjustment/Makefile
osdadjustment/meta/Makefile
osdadjustment/src/Makefile

quicksignal/Makefile
quicksignal/src/Makefile
quicksignal/src/Converter/Makefile
quicksignal/src/Renderer/Makefile
quicksignal/src/plugin/Makefile
quicksignal/src/plugin/icons_quick/Makefile

rucam/Makefile
rucam/meta/Makefile
rucam/src/Makefile
rucam/src/bin/Makefile
rucam/src/init/Makefile

settings36/Makefile
settings36/meta/Makefile
settings36/src/Makefile

settings36_4/Makefile
settings36_4/meta/Makefile
settings36_4/src/Makefile

settings4/Makefile
settings4/meta/Makefile
settings4/src/Makefile

simplesatscan/Makefile
simplesatscan/meta/Makefile
simplesatscan/po/Makefile
simplesatscan/src/Makefile

shootyourscreen/Makefile
shootyourscreen/meta/Makefile
shootyourscreen/po/Makefile
shootyourscreen/src/Makefile
shootyourscreen/src/pic/Makefile

shoutcast/Makefile
shoutcast/meta/Makefile
shoutcast/po/Makefile
shoutcast/src/Makefile

softcamsetup/Makefile
softcamsetup/meta/Makefile
softcamsetup/po/Makefile
softcamsetup/src/Makefile
softcamsetup/src/images/Makefile

spzzaphistory/Makefile
spzzaphistory/meta/Makefile
spzzaphistory/po/Makefile
spzzaphistory/src/Makefile
spzzaphistory/src/res/Makefile

timeronoff/Makefile
timeronoff/meta/Makefile
timeronoff/po/Makefile
timeronoff/src/Makefile
timeronoff/src/images/Makefile

wicardd/Makefile
wicardd/meta/Makefile
wicardd/src/Makefile
wicardd/src/bin/Makefile
wicardd/src/config/Makefile
wicardd/src/init/Makefile
wicardd/src/keys/Makefile
wicardd/src/script/Makefile

vfd_max/Makefile
vfd_max/meta/Makefile
vfd_max/src/Makefile
vfd_max/src/images/Makefile

vfd_min/Makefile
vfd_min/meta/Makefile
vfd_min/src/Makefile


])
AC_OUTPUT
