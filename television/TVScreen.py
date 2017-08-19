# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.television.TVScreen
from panda3d.core import Buffer, Camera, Texture, TextureStage
from TVScenes import *
from TVEffects import *
from TVChatGUI import *

class TVScreen:

    def __init__(self, screen, hasChatGui = False):
        self.screen = screen
        self.scene = None
        self.scenes = {}
        self.buffer = base.win.makeTextureBuffer('tv-screen', 960, 540)
        self.buffer.setSort(-1)
        self.camera = base.makeCamera(self.buffer)
        self.textureStage = TextureStage('tv-screen')
        if hasChatGui:
            self.chatGui = TVChatGUI(self)
            self.chatGui.hide()
        else:
            self.chatGui = None
        self.registerScene('gray', ColorScene((0.3, 0.3, 0.3, 1)))
        self.registerScene('static', TwoDScene('phase_3.5/maps/screen_static.jpg', [SoundEffect('phase_3.5/audio/sfx/tv_static.ogg'), ConfuseGUIEffect((0.5, 0.5, 0.5, 1))]))
        self.showScene('gray')
        self.loaded = True
        return

    def delete(self):
        if not self.loaded:
            return
        else:
            if self.camera:
                self.camera.removeNode()
                self.camera = None
            if self.buffer:
                base.graphicsEngine.removeWindow(self.buffer)
                self.buffer = None
            for obj in self.scenes.values() + [self.chatGui]:
                if obj:
                    obj.delete()

            self.scenes = []
            self.scene = None
            self.screen = None
            self.chatGui = None
            self.loaded = False
            return

    def hasChatGui(self):
        return self.chatGui != None

    def getScene(self, name):
        return self.scenes.get(name)

    def getScreen(self):
        return self.screen

    def getBuffer(self):
        return self.buffer

    def getCamera(self):
        return self.camera

    def getTextureStage(self):
        return self.textureStage

    def getChatGui(self):
        return self.chatGui

    def setTexScale(self, x, y):
        self.screen.setTexScale(self.getTextureStage(), x, y)

    def setTexture(self, texture, scale):
        if self.chatGui:
            self.chatGui.setTexture(texture, scale)
        self.screen.setTexture(self.getTextureStage(), texture, scale)

    def registerScene(self, name, scene):
        if name in self.scenes:
            return
        self.scenes[name] = scene
        scene.setScreen(self)

    def showScene(self, name, temporary = False):
        if name not in self.scenes:
            return
        if self.scene and not temporary:
            self.scene.exitEffects()
        self.scene = self.scenes[name]
        self.scene.show()