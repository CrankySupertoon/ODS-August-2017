# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.effects.VisualEffect
from panda3d.core import Light, Texture, TextureStage, lookAt

class VisualEffect:

    def __init__(self, parent = None, model = 'vfx_regular', texture = None, color = None, scale = 1.0, h = -90, uIncrement = 0.125, lookAt = True, depth = True):
        self.effect = loader.loadModel('phase_4/models/props/' + model)
        if parent:
            self.effect.reparentTo(parent)
        if texture:
            self.effect.setTexture(TextureStage.getDefault(), loader.loadTexture(texture), 1)
        if color:
            self.effect.setColor(color)
        if not depth:
            self.effect.setBin('fixed', 40)
        self.effect.setScale(scale)
        self.effect.setH(h)
        self.effect.setTwoSided(True)
        self.effect.setDepthWrite(depth)
        self.effect.setDepthTest(depth)
        self.effect.setLightOff()
        self.effect.flattenLight()
        self.effect.hide()
        self.uIncrement = uIncrement
        self.lookAt = lookAt

    def removeNode(self):
        if not self.effect:
            return
        else:
            self.effect.removeNode()
            taskMgr.remove(self.uniqueName('play'))
            self.effect = None
            return

    def uniqueName(self, name):
        return 'VisualEffect-%s-%s' % (id(self), name)

    def getWaitTime(self, speed):
        return (1 / 0.125 * (1 / self.uIncrement) + 1) * speed

    def loop(self, speed = 0.015):
        self.runTask(False, speed)

    def play(self, speed = 0.015):
        self.runTask(True, speed)

    def stop(self):
        taskMgr.remove(self.uniqueName('play'))
        self.effect.hide()

    def runTask(self, play, speed):
        self.effectU = -0.125
        self.effectV = 0
        taskMgr.doMethodLater(speed, lambda task: self.run(play, task), self.uniqueName('run'))

    def run(self, play, task):
        if not self.effect:
            return task.done
        else:
            self.effect.show()
            self.effectU += self.uIncrement
            if self.effectU >= 1.0:
                self.effectU = 0
                self.effectV -= 0.125
            if play and self.effectV <= -1:
                self.effect.removeNode()
                self.effect = None
                return task.done
            if self.lookAt:
                self.effect.lookAt(base.camera)
            self.effect.setTexOffset(TextureStage.getDefault(), self.effectU, self.effectV)
            return task.again


class P2PVisualEffect(VisualEffect):

    def __init__(self, parent = None, target = None, model = 'vfx_p2p', texture = None, color = None, scale = 1.0, h = 0, uIncrement = 0.5, lookAt = False, depth = True):
        VisualEffect.__init__(self, parent, model, texture, color, scale, h, uIncrement, lookAt, depth)
        self.parent = parent
        if parent and target:
            self.setTarget(target)

    def setTarget(self, target):
        oldHpr = self.parent.getHpr()
        self.parent.lookAt(target)
        self.effect.setHpr(self.parent.getHpr(target))
        self.effect.setH(self.effect, 90)
        self.parent.setHpr(oldHpr)
        self.effect.setScale(self.parent.getDistance(target), 1, 1)