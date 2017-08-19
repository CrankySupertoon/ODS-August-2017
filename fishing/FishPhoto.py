# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.fishing.FishPhoto
from panda3d.core import Buffer, Camera, CardMaker, DisplayRegion, Lens, NodePath, Texture
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
import FishGlobals

class DirectRegion(NodePath):

    def __init__(self, parent = aspect2d):
        NodePath.__init__(self, 'DirectRegion')
        self.reparentTo(parent)
        self.loaded = False
        self.color = None
        return

    def destroy(self):
        self.unload()

    def setBounds(self, bounds):
        self.bounds = bounds

    def setColor(self, color):
        self.color = color

    def load(self):
        if self.loaded:
            return self.scene
        self.buffer = base.win.makeTextureBuffer('DirectRegion-%s' % id(self), 1024, 1024)
        self.buffer.setSort(-1)
        self.camera = base.makeCamera(self.buffer)
        self.camera.node().getLens().setFov(40, 40)
        cardMaker = CardMaker('card')
        cardMaker.setFrame(*self.bounds)
        self.card = self.attachNewNode(cardMaker.generate())
        self.card.setTexture(self.buffer.getTexture())
        self.scene = NodePath('scene')
        if self.color:
            cardMaker.setFrame(-1, 1, -1, 1)
            card = self.scene.attachNewNode(cardMaker.generate())
            card.setPos(0, 10, 0)
            card.setColor(*self.color)
            card.setScale(30)
        self.camera.reparentTo(self.scene)
        self.loaded = True
        return self.scene

    def unload(self):
        if not self.loaded:
            return
        base.graphicsEngine.removeWindow(self.buffer)
        base.win.removeDisplayRegion(self.camera.node().getDisplayRegion(0))
        self.camera.removeNode()
        del self.buffer
        del self.camera
        self.card.removeNode()
        del self.card
        self.scene.removeNode()
        del self.scene
        self.loaded = False


class FishPhoto(NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory('FishPhoto')

    def __init__(self, fish = None, parent = aspect2d):
        NodePath.__init__(self)
        self.assign(parent.attachNewNode('FishPhoto'))
        self.fish = fish
        self.actor = None
        self.sound = None
        self.soundTrack = None
        self.track = None
        self.fishFrame = None
        self.swimColor = None
        return

    def destroy(self):
        self.hide()
        if hasattr(self, 'background'):
            del self.background
        self.fish = None
        del self.soundTrack
        del self.track
        return

    def update(self, fish):
        self.fish = fish

    def setSwimBounds(self, *bounds):
        self.swimBounds = bounds

    def setSwimColor(self, *color):
        self.swimColor = color

    def load(self):
        pass

    def makeFishFrame(self, actor):
        actor.setDepthTest(1)
        actor.setDepthWrite(1)
        if not hasattr(self, 'fishDisplayRegion'):
            self.fishDisplayRegion = DirectRegion(parent=self)
            self.fishDisplayRegion.setBounds(self.swimBounds)
            self.fishDisplayRegion.setColor(self.swimColor)
        frame = self.fishDisplayRegion.load()
        pitch = frame.attachNewNode('pitch')
        rotate = pitch.attachNewNode('rotate')
        scale = rotate.attachNewNode('scale')
        actor.reparentTo(scale)
        bMin, bMax = actor.getTightBounds()
        center = (bMin + bMax) / 2.0
        actor.setPos(-center[0], -center[1], -center[2])
        genus = self.fish.getGenus()
        fishInfo = FishGlobals.FishFileDict.get(genus, FishGlobals.FishFileDict[-1])
        fishPos = fishInfo[5]
        if fishPos:
            actor.setPos(fishPos[0], fishPos[1], fishPos[2])
        scale.setScale(fishInfo[6])
        rotate.setH(fishInfo[7])
        pitch.setP(fishInfo[8])
        pitch.setY(2)
        return frame

    def show(self, showBackground = 0):
        messenger.send('wakeup')
        if self.fishFrame:
            self.actor.cleanup()
            if hasattr(self, 'fishDisplayRegion'):
                self.fishDisplayRegion.unload()
            self.hide()
        self.actor = self.fish.getActor()
        self.actor.setTwoSided(1)
        self.fishFrame = self.makeFishFrame(self.actor)
        if showBackground:
            if not hasattr(self, 'background'):
                background = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
                background = background.find('**/Fish_BG')
                self.background = background
            self.background.setPos(0, 15, 0)
            self.background.setScale(11)
            self.background.reparentTo(self.fishFrame)
        self.sound, loop, delay, playRate = self.fish.getSound()
        if playRate is not None:
            self.actor.setPlayRate(playRate, 'intro')
            self.actor.setPlayRate(playRate, 'swim')
        introDuration = self.actor.getDuration('intro')
        track = Parallel(Sequence(Func(self.actor.play, 'intro'), Wait(introDuration), Func(self.actor.loop, 'swim')))
        if self.sound:
            soundTrack = Sequence(Wait(delay), Func(self.sound.play))
            if loop:
                duration = max(introDuration, self.sound.length())
                soundTrack.append(Wait(duration - delay))
                track.append(Func(soundTrack.loop))
                self.soundTrack = soundTrack
            else:
                track.append(soundTrack)
        self.track = track
        self.track.start()
        return

    def hide(self):
        if hasattr(self, 'fishDisplayRegion'):
            self.fishDisplayRegion.unload()
        if self.actor:
            self.actor.stop()
        if self.sound:
            self.sound.stop()
            self.sound = None
        if self.soundTrack:
            self.soundTrack.pause()
            self.soundTrack = None
        if self.track:
            self.track.pause()
            self.track = None
        return