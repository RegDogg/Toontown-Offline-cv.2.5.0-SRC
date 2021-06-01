# Embedded file name: toontown.toonbase.GameSettings
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import loadPrcFileData
from otp.otpbase.Settings import Settings

class GameSettings:
    notify = DirectNotifyGlobal.directNotify.newCategory('GameSettings')

    def __init__(self):
        self.settings = Settings()
        self.loadFromSettings()

    def loadFromSettings(self):
        electionEvent = self.settings.getBool('game', 'elections', False)
        loadPrcFileData('toonBase Settings Election Active', 'want-doomsday %s' % electionEvent)
        self.settings.updateSetting('game', 'elections', electionEvent)
        self.electionEvent = electionEvent
        retroMode = self.settings.getBool('game', 'retro', False)
        loadPrcFileData('toonBase Settings TTO Map Hover', 'want-map-hover %s' % retroMode)
        loadPrcFileData('toonBase Settings TTO Loading Screen', 'want-tto-loading-screen %s' % retroMode)
        loadPrcFileData('toonBase Settings TTO Localizers', 'want-tto-text %s' % retroMode)
        loadPrcFileData('toonBase Settings TTO Theme Song', 'want-tto-theme %s' % retroMode)
        loadPrcFileData('toonBase Settings TTO Catalog Screen', 'want-tto-catalog %s' % retroMode)
        loadPrcFileData('toonBase Settings TTO Fireworks', 'want-old-fireworks %s' % retroMode)
        loadPrcFileData('toonBase Settings TTO Run Sound', 'want-tto-runsound %s' % retroMode)
        self.settings.updateSetting('game', 'retro', retroMode)
        self.retroMode = retroMode
        miniServer = self.settings.getBool('game', 'mini-server', False)
        loadPrcFileData('toonBase Settings Mini-Servers', 'want-mini-server %s' % miniServer)
        self.settings.updateSetting('game', 'mini-server', miniServer)
        self.miniServer = miniServer
        randomInvasions = self.settings.getBool('game', 'random-invasions', True)
        loadPrcFileData('toonBase Settings Random Invasions', 'want-random-invasions %s' % randomInvasions)
        self.settings.updateSetting('game', 'random-invasions', randomInvasions)
        self.randomInvasions = randomInvasions
        nerfs = self.settings.getBool('game', 'nerfs', True)
        loadPrcFileData('toonBase Settings Nerfs', 'want-nerfs %s' % nerfs)
        self.settings.updateSetting('game', 'nerfs', nerfs)
        self.nerfs = nerfs