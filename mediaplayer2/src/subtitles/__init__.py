# -*- coding: utf-8 -*-

import gettext
import os

from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE

def getPluginDir():
    absPath = os.path.dirname(__file__)
    pluginDir = absPath[len(os.path.join(resolveFilename(SCOPE_PLUGINS),'Extensions/')):]
    pluginDir = pluginDir.split('/')[0]
    return pluginDir

pluginDir = getPluginDir()
print 'pluginDir',pluginDir

def _(txt):
    t = gettext.dgettext(pluginDir, txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t

from subtitles import SubsSupport
