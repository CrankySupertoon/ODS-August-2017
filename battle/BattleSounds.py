# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.battle.BattleSounds
from panda3d.core import AudioManager, DSearchPath, Filename
from direct.directnotify import DirectNotifyGlobal

class BattleSounds:
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleSounds')

    def __init__(self):
        self.mgr = AudioManager.createAudioManager()
        self.isValid = 0
        if self.mgr != None and self.mgr.isValid():
            self.isValid = 1
            limit = config.GetInt('battle-sound-cache-size', 15)
            self.mgr.setCacheLimit(limit)
            base.addSfxManager(self.mgr)
            self.setupSearchPath()
        return

    def setupSearchPath(self):
        self.sfxSearchPath = DSearchPath()
        self.sfxSearchPath.appendDirectory(Filename('../resources/phase_3/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('../resources/phase_3.5/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('../resources/phase_4/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('../resources/phase_5/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('/phase_3/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('/phase_3.5/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('/phase_4/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('/phase_5/audio/sfx'))

    def clear(self):
        if self.isValid:
            self.mgr.clearCache()

    def getSound(self, name):
        if self.isValid:
            filename = Filename(name)
            found = vfs.resolveFilename(filename, self.sfxSearchPath)
            if not found:
                self.setupSearchPath()
                found = vfs.resolveFilename(filename, self.sfxSearchPath)
            if not found:
                self.notify.warning('%s not found on: %s' % (name, self.sfxSearchPath))
            else:
                return self.mgr.getSound(filename.getFullpath())
        return self.mgr.getNullSound()


globalBattleSoundCache = BattleSounds()