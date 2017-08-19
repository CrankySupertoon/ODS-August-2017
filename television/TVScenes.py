# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.television.TVScenes
from panda3d.core import Buffer, Camera, NodePath, Texture

class TVScene:

    def __init__(self, effects = []):
        self.screen = None
        self.effects = effects
        for effect in self.effects:
            effect.setScene(self)

        return

    def delete(self):
        for effect in self.effects:
            effect.delete()

        self.effects = []

    def setScreen(self, screen):
        self.screen = screen

    def getScreen(self):
        return self.screen

    def hasEffect(self, effectClass):
        return any((isinstance(effect, effectClass) for effect in self.effects))

    def exitEffects(self):
        for effect in self.effects:
            effect.exit()

    def show(self):
        for effect in self.effects:
            effect.enter()

        self.screen.getScreen().setColor(1, 1, 1, 1)

    def startTask(self):
        pass

    def stopTask(self):
        pass


class ColorScene(TVScene):

    def __init__(self, color, effects = []):
        TVScene.__init__(self, effects)
        self.color = color

    def getColor(self):
        return self.color

    def show(self):
        if not self.screen:
            return
        TVScene.show(self)
        screen = self.screen.getScreen()
        screen.clearTexture()
        screen.setColor(*self.color)


class TwoDScene(TVScene):

    def __init__(self, texture, effects = []):
        TVScene.__init__(self, effects)
        self.texture = loader.loadTexture(texture)
        self.texture.setMinfilter(Texture.FTLinearMipmapLinear)
        self.texture.setMagfilter(Texture.FTLinear)

    def delete(self):
        if self.texture:
            self.texture.clear()
            self.texture = None
        TVScene.delete(self)
        return

    def getTexture(self):
        return self.texture

    def show(self):
        if not self.screen:
            return
        self.screen.setTexScale(1.0, 1.0)
        self.screen.setTexture(self.texture, 1)
        TVScene.show(self)


class ThreeDScene(TVScene, NodePath):
    CameraPos = [(0, 0, 0, 0, 0, 0)]

    def __init__(self, name, effects = []):
        TVScene.__init__(self, effects)
        NodePath.__init__(self, name)
        self.setCameraPosHprIndex(0)

    def delete(self):
        NodePath.removeNode(self)
        TVScene.delete(self)

    def setCameraPosHprIndex(self, index):
        if index < 0 or index >= len(self.CameraPos):
            return
        self.setCameraPosHpr(*self.CameraPos[index])

    def setCameraPosHpr(self, x, y, z, h, p, r):
        self.cameraPosHpr = (x,
         y,
         z,
         h,
         p,
         r)
        if self.screen:
            self.screen.getCamera().setPosHpr(*self.cameraPosHpr)

    def getCameraPosHpr(self):
        return self.cameraPosHpr

    def show(self):
        if not self.screen:
            return
        camera = self.screen.getCamera()
        camera.reparentTo(self)
        camera.setPosHpr(*self.cameraPosHpr)
        self.screen.setTexScale(0.95, 0.67)
        self.screen.setTexture(self.screen.getBuffer().getTexture(), 1)
        TVScene.show(self)