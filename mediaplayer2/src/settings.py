from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.FileList import FileList
from Components.MediaPlayer import PlayList
from Components.Sources.StaticText import StaticText
from Components.config import config, getConfigListEntry, ConfigSubsection, \
    configfile, ConfigText, ConfigYesNo, ConfigDirectory
from Screens.HelpMenu import HelpableScreen
from Screens.Screen import Screen


config.plugins.mediaplayer2 = ConfigSubsection()
config.plugins.mediaplayer2.repeat = ConfigYesNo(default=False)
config.plugins.mediaplayer2.savePlaylistOnExit = ConfigYesNo(default=True)
config.plugins.mediaplayer2.saveDirOnExit = ConfigYesNo(default=False)
config.plugins.mediaplayer2.defaultDir = ConfigDirectory()
config.plugins.mediaplayer2.useAlternateUserAgent = ConfigYesNo(default=False)
config.plugins.mediaplayer2.alternateUserAgent = ConfigText(default="")
config.plugins.mediaplayer2.sortPlaylists = ConfigYesNo(default=False)
config.plugins.mediaplayer2.extensionsMenu = ConfigYesNo(default=False)
config.plugins.mediaplayer2.mainMenu = ConfigYesNo(default=False)

class DirectoryBrowser(Screen, HelpableScreen):

    def __init__(self, session, currDir):
        Screen.__init__(self, session)
        # for the skin: first try MediaPlayerDirectoryBrowser, then FileBrowser, this allows individual skinning
        self.skinName = ["MediaPlayerDirectoryBrowser", "FileBrowser" ]

        HelpableScreen.__init__(self)

        self["key_red"] = StaticText(_("Cancel"))
        self["key_green"] = StaticText(_("Use"))

        self.filelist = FileList(currDir, matchingPattern="")
        self["filelist"] = self.filelist

        self["FilelistActions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "green": self.use,
                "red": self.exit,
                "ok": self.ok,
                "cancel": self.exit
            })
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(_("Directory browser"))

    def ok(self):
        if self.filelist.canDescent():
            self.filelist.descent()

    def use(self):
        if self["filelist"].getCurrentDirectory() is not None:
            if self.filelist.canDescent() and self["filelist"].getFilename() and len(self["filelist"].getFilename()) > len(self["filelist"].getCurrentDirectory()):
                self.filelist.descent()
                self.close(self["filelist"].getCurrentDirectory())
        else:
                self.close(self["filelist"].getFilename())

    def exit(self):
        self.close(False)

class MediaPlayerSettings(Screen,ConfigListScreen):

    def __init__(self, session, parent):
        Screen.__init__(self, session)
        # for the skin: first try MediaPlayerSettings, then Setup, this allows individual skinning
        self.skinName = ["MediaPlayerSettings", "Setup" ]
        self.setup_title = _("Edit settings")
        self.onChangedEntry = [ ]

        self["key_red"] = StaticText(_("Cancel"))
        self["key_green"] = StaticText(_("Save"))

        ConfigListScreen.__init__(self, [], session = session, on_change = self.changedEntry)
        self.parent = parent
        self.initConfigList()
        config.plugins.mediaplayer2.saveDirOnExit.addNotifier(self.initConfigList)

        self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
        {
            "green": self.save,
            "red": self.cancel,
            "cancel": self.cancel,
            "ok": self.ok,
        }, -2)

    def layoutFinished(self):
        self.setTitle(self.setup_title)

    def initConfigList(self, element=None):
        print "[initConfigList]", element
        try:
            self.list = []
            self.list.append(getConfigListEntry(_("repeat playlist"), config.plugins.mediaplayer2.repeat))
            self.list.append(getConfigListEntry(_("save playlist on exit"), config.plugins.mediaplayer2.savePlaylistOnExit))
            self.list.append(getConfigListEntry(_("save last directory on exit"), config.plugins.mediaplayer2.saveDirOnExit))
            if not config.plugins.mediaplayer2.saveDirOnExit.getValue():
                self.list.append(getConfigListEntry(_("start directory"), config.plugins.mediaplayer2.defaultDir))
            self.list.append(getConfigListEntry(_("sorting of playlists"), config.plugins.mediaplayer2.sortPlaylists))
            self.list.append(getConfigListEntry(_("show in extensions menu"), config.plugins.mediaplayer2.extensionsMenu))
            self.list.append(getConfigListEntry(_("replace default MediaPlayer in main menu"), config.plugins.mediaplayer2.mainMenu))
            self["config"].setList(self.list)
        except KeyError:
            print "keyError"

    def changedConfigList(self):
        self.initConfigList()

    def ok(self):
        if self["config"].getCurrent()[1] == config.plugins.mediaplayer2.defaultDir:
            self.session.openWithCallback(self.DirectoryBrowserClosed, DirectoryBrowser, self.parent.filelist.getCurrentDirectory())

    def DirectoryBrowserClosed(self, path):
        print "PathBrowserClosed:" + str(path)
        if path != False:
            config.plugins.mediaplayer2.defaultDir.setValue(path)

    def save(self):
        for x in self["config"].list:
            x[1].save()
        self.close()

    def cancel(self):
        self.close()

    # for summary:
    def changedEntry(self):
        for x in self.onChangedEntry:
            x()

    def getCurrentEntry(self):
        return self["config"].getCurrent()[0]

    def getCurrentValue(self):
        return str(self["config"].getCurrent()[1].getText())

    def createSummary(self):
        from Screens.Setup import SetupSummary
        return SetupSummary
