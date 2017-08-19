# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.TutorialManager
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals

class TutorialManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        messenger.send('tmGenerate')
        self.cr.tutorialManager = self
        self.accept('requestTutorial', self.d_requestTutorial)
        self.accept('requestSkipTutorial', self.d_requestSkipTutorial)

    def disable(self):
        self.ignoreAll()
        ZoneUtil.overrideOff()
        DistributedObject.DistributedObject.disable(self)

    def d_requestTutorial(self):
        self.sendUpdate('requestTutorial', [])

    def d_requestSkipTutorial(self):
        self.sendUpdate('requestSkipTutorial', [])

    def skipTutorialDone(self):
        messenger.send('skipTutorialDone')

    def enterTutorial(self, exteriorZones, interiorZones):
        base.localAvatar.cantLeaveGame = 1
        ZoneUtil.overrideOn(exteriorList=exteriorZones, interiorList=interiorZones)
        messenger.send('startTutorial', [interiorZones[0]])
        self.acceptOnce('toonArrivedTutorial', self.d_toonArrived)

    def d_allDone(self):
        self.sendUpdate('allDone', [])

    def d_toonArrived(self):
        self.sendUpdate('toonArrived', [])

    def d_requestStage(self, stage):
        self.sendUpdate('requestStage', [stage])