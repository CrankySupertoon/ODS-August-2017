# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.DistributedTopToonsInterior
from panda3d.core import CollisionNode, CollisionSphere
from direct.distributed.DistributedObject import DistributedObject
from direct.actor.Actor import Actor
from toontown.safezone import SZUtil
from toontown.toptoons.PeriodPicker import PeriodPicker
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toon import NPCToons
from RandomBuilding import RandomBuilding

class DistributedTopToonsInterior(DistributedObject, RandomBuilding):

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.setup()

    def setup(self):
        randomGen = self.getRandomGen()
        colors = self.getColors()
        self.interior = loader.loadModel('phase_3.5/models/modules/toon_toptoons_int')
        self.interior.reparentTo(render)
        self.duck = loader.loadModel('phase_3.5/models/modules/tt_m_ara_int_scientistDuckFlat')
        self.duck.reparentTo(self.interior)
        self.duck.setPosHpr(-5.823, 21.19, 0.025, 70, 0, 0)
        collisions = CollisionNode('topToons')
        sphere = CollisionSphere(0, 0, -0.5, 3)
        sphere.setTangible(0)
        collisions.addSolid(sphere)
        self.duck.attachNewNode(collisions)
        self.accept('entertopToons', self.__enterTopToons)
        self.sky = loader.loadModel('phase_3.5/models/props/TT_sky')
        self.sky.setScale(0.15)
        self.sky.setPos(13, 0, -3)
        self.sky.setH(90)
        for i in xrange(1, 3):
            self.sky.find('**/cloud%s' % i).setScale(1.2)

        SZUtil.startClouds(self.sky, lambda task: SZUtil.cloudSkyTrack(task), self.interior, None)
        self.setupDoor(randomGen, colors, self.interior, -0.25)
        self.resetNPCs()
        self.gui = None
        self.toons = []
        self.positions = [(-9.775, 13.42, 2.335, 270, 0, 0),
         (-12.8792, 17.7304, 2.33506, 270, 0, 0),
         (-12.8572, 8.49616, 2.33506, 270, 0, 0),
         (-17.4662, 6.17828, 2.33506, 270, 0, 0),
         (-16.3713, 19.6819, 2.33506, 270, 0, 0)]
        return

    def disable(self):
        self.sky.removeNode()
        del self.sky
        self.duck.removeNode()
        del self.duck
        self.interior.removeNode()
        del self.interior
        if self.gui:
            self.gui.destroy()
            self.gui = None
        self.deleteToons()
        self.ignoreAll()
        DistributedObject.disable(self)
        return

    def deleteToons(self):
        for toon in self.toons:
            toon.delete()

        self.toons = []

    def __gotTopToons(self, topToons):
        if not topToons:
            self.gui = TTDialog.TTDialog(text=TTLocalizer.TopToonsEmpty, command=self.__stoppedAsleep, style=TTDialog.Acknowledge)
            self.gui.show()
            return
        self.deleteToons()
        for i, topToon in enumerate(topToons):
            name, dna, score = topToon
            realName = TTLocalizer.TopToonName % (i + 1, name, score)
            toon = NPCToons.createDataNPC(realName, dna, 'TeleportIn')
            toon.reparentTo(self.interior)
            toon.setPosHpr(*self.positions[i])
            toon.initializeBodyCollisions('topToonsBody')
            self.toons.append(toon)

        base.cr.playGame.place.fsm.request('walk')

    def __handleCatalogDialog(self, choice):
        self.cleanupCatalogDialog()
        base.cr.playGame.getPlace().setState('walk')
        if choice > 0:
            self.cleanupCatalogNotifyDialog()

    def __topToonsDone(self, period, category):
        base.cr.statisticsManager.d_requestToons(period, category)
        self.acceptOnce('gotTopToons', self.__gotTopToons)

    def __topToonsExit(self):
        base.cr.playGame.place.fsm.request('walk')
        self.ignore('stoppedAsleep')

    def __stoppedAsleep(self, *args):
        if self.gui:
            self.gui.destroy()
            self.gui = None
        self.__topToonsExit()
        return

    def __enterTopToons(self, col):
        base.cr.playGame.place.fsm.request('stopped')
        self.gui = PeriodPicker(self.__topToonsDone, self.__topToonsExit)
        self.acceptOnce('stoppedAsleep', self.__stoppedAsleep)