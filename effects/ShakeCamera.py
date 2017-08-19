# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.effects.ShakeCamera
from panda3d.core import Camera
from otp.ai.MagicWordGlobal import *
import random

class ShakeCamera:

    def __init__(self, intensity, duration = 0.5, rate = 30.0):
        self.intensity = intensity
        self.duration = duration
        self.rate = rate
        self.elapsed = 0.0

    def uniqueName(self, name):
        return 'ShakeCamera-%s-%s' % (id(self), name)

    def start(self):
        self.stop()
        taskMgr.add(self.__shake, 'shakeCamera')

    def stop(self):
        base.cam.setPos(0, 0, 0)
        taskMgr.remove('shakeCamera')

    def getRandomCoord(self):
        return random.random() * 2 - 1

    def __shake(self, task):
        x, z = self.getRandomCoord(), self.getRandomCoord()
        life = self.elapsed / self.duration
        if life > 1.0:
            base.cam.setPos(0, 0, 0)
            return task.done
        displacement = (1 - life) * self.intensity
        base.cam.setPos(x * displacement, 0, z * displacement)
        task.delayTime = 1.0 / self.rate
        self.elapsed += task.delayTime
        return task.again


@magicWord(category=CATEGORY_PROGRAMMER, types=[float, float, float])
def shakeCamera(intensity, duration = 0.5, rate = 30.0):
    ShakeCamera(intensity, duration, rate).start()