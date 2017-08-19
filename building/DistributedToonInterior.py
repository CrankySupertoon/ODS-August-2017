# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.DistributedToonInterior
from panda3d.core import Light, Mat4, Point3, TextNode
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm import ClassicFSM, State
from toontown.toon import ToonDNA, ToonHead
from toontown.toonbase import ToontownGlobals
from RandomBuilding import RandomBuilding
SIGN_LEFT = -4
SIGN_RIGHT = 4
SIGN_BOTTOM = -3.5
SIGN_TOP = 1.5
FrameScale = 1.4

class DistributedToonInterior(DistributedObject, RandomBuilding):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.fsm = ClassicFSM.ClassicFSM('DistributedToonInterior', [State.State('toon', self.enterToon, self.exitToon, ['beingTakenOver']), State.State('beingTakenOver', self.enterBeingTakenOver, self.exitBeingTakenOver, []), State.State('off', self.enterOff, self.exitOff, [])], 'toon', 'off')
        self.fsm.enterInitialState()
        self.alarmSound = None
        self.takeOverSeq = None
        return

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.setup()

    def disable(self):
        self.interior.removeNode()
        del self.interior
        del self.fsm
        self.exitBeingTakenOver()
        DistributedObject.disable(self)

    def getModelType(self, zoneId):
        interior = self.randomDNAItem(self.getRandomGen(), 'TI_room', assetStorage.findNode)
        return str(interior.getName().split('.egg')[0])

    def setupSign(self):
        if self.block not in base.cr.playGame.signs:
            return
        sign = base.cr.playGame.signs[self.block]
        signOrigin = self.interior.find('**/sign_origin;+s')
        newSignNP = sign.copyTo(signOrigin)
        newSignNP.setDepthWrite(1, 1)
        mat = self.interior.getNetTransform().getMat()
        inv = Mat4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        inv.invertFrom(mat)
        newSignNP.setMat(inv)
        newSignNP.flattenLight()
        ll = Point3()
        ur = Point3()
        newSignNP.calcTightBounds(ll, ur)
        width = ur[0] - ll[0]
        height = ur[2] - ll[2]
        if width == 0 or height == 0:
            return
        xScale = (SIGN_RIGHT - SIGN_LEFT) / width
        zScale = (SIGN_TOP - SIGN_BOTTOM) / height
        scale = min(xScale, zScale)
        xCenter = (ur[0] + ll[0]) / 2.0
        zCenter = (ur[2] + ll[2]) / 2.0
        newSignNP.setPosHprScale((SIGN_RIGHT + SIGN_LEFT) / 2.0 - xCenter * scale, -0.1, (SIGN_TOP + SIGN_BOTTOM) / 2.0 - zCenter * scale, 0.0, 0.0, 0.0, scale, scale, scale)

    def setup(self):
        randomGen = self.getRandomGen()
        colors = self.getColors()
        self.interior = self.randomDNAItem(randomGen, 'TI_room', assetStorage.findNode).copyTo(render)
        self.replaceRandomInModel(randomGen, colors, self.interior)
        self.setupDoor(randomGen, colors, self.interior)
        self.setupSign()
        trophyOrigin = self.interior.find('**/trophy_origin')
        trophy = self.buildTrophy()
        if trophy:
            trophy.reparentTo(trophyOrigin)
        self.interior.flattenMedium()
        self.resetNPCs()

    def setToonData(self, savedBy):
        self.savedBy = savedBy

    def buildTrophy(self):
        if not self.savedBy:
            return
        numToons = len(self.savedBy)
        pos = 1.25 - 1.25 * numToons
        trophy = hidden.attachNewNode('trophy')
        for name, dna in self.savedBy:
            frame = self.buildFrame(name, dna)
            frame.reparentTo(trophy)
            frame.setPos(pos, 0, 0)
            pos += 2.5

        return trophy

    def buildFrame(self, name, dna):
        frame = loader.loadModel('phase_3.5/models/modules/trophy_frame')
        dna = ToonDNA.ToonDNA(dna)
        head = ToonHead.ToonHead()
        head.setupHead(dna)
        head.setPosHprScale(0, -0.05, -0.05, 180, 0, 0, 0.55, 0.02, 0.55)
        if dna.head[0] == 'r':
            head.setZ(-0.15)
        elif dna.head[0] == 'h':
            head.setZ(0.05)
        elif dna.head[0] == 'm':
            head.setScale(0.45, 0.02, 0.45)
        head.reparentTo(frame)
        nameText = TextNode('trophy')
        nameText.setFont(ToontownGlobals.getToonFont())
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0, 0, 0, 1)
        nameText.setWordwrap(5.36 * FrameScale)
        nameText.setText(name)
        namePath = frame.attachNewNode(nameText.generate())
        namePath.setPos(0, -0.03, -0.6)
        namePath.setScale(0.186 / FrameScale)
        frame.setScale(FrameScale, 1.0, FrameScale)
        return frame

    def setState(self, state, timestamp):
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterToon(self):
        pass

    def exitToon(self):
        pass

    def enterBeingTakenOver(self, ts):
        self.alarmSound = loader.loadSfx('phase_3.5/audio/sfx/alarm_warning.ogg')
        self.takeOverSeq = Sequence(render.colorScaleInterval(1.5, (0.5, 0, 0, 1)), render.colorScaleInterval(1.5, (1, 1, 1, 1)))
        base.playSfx(self.alarmSound, looping=1, volume=1.25)
        self.takeOverSeq.loop()
        taskMgr.doMethodLater(3.75, lambda task: messenger.send('clearOutToonInterior'), self.uniqueName('clearOutToonInterior'))

    def exitBeingTakenOver(self):
        if self.takeOverSeq:
            self.takeOverSeq.finish()
            self.takeOverSeq = None
        if self.alarmSound:
            self.alarmSound.stop()
            self.alarmSound = None
        taskMgr.remove(self.uniqueName('clearOutToonInterior'))
        return