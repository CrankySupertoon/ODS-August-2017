# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.television.TVEffects
from direct.task.Task import Task
from otp.otpbase import OTPGlobals
import random

class TVEffect:

    def __init__(self):
        self.deleted = False
        self.entered = False
        self.scene = None
        return

    def uniqueName(self, name):
        return 'TVEffect-%s-%s' % (id(self), name)

    def setScene(self, scene):
        self.scene = scene

    def getScene(self):
        return self.scene

    def getScreen(self):
        return self.scene.screen

    def delete(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass


class SoundEffect(TVEffect):

    def __init__(self, sfx, looping = False):
        TVEffect.__init__(self)
        self.sfx = loader.loadSfx(sfx)
        self.looping = looping

    def delete(self):
        if self.deleted:
            return
        else:
            self.sfx.stop()
            self.sfx = None
            self.deleted = True
            return

    def enter(self):
        if self.entered or self.deleted:
            return
        base.playSfx(self.sfx, looping=self.looping, volume=0.9)
        self.entered = True

    def exit(self):
        if self.deleted or not self.entered:
            return
        self.sfx.stop()
        self.entered = False


class FlickerEffect(TVEffect):

    def __init__(self, origScene, nextScene, endTriggers):
        TVEffect.__init__(self)
        self.origScene = origScene
        self.nextScene = nextScene
        self.endTriggers = endTriggers
        self.taskName = self.uniqueName('flickerTask')
        self.trigger = 0

    def enter(self):
        if self.entered:
            return
        taskMgr.remove(self.taskName)
        taskMgr.doMethodLater(2.5, self.__checkTrigger, self.taskName)
        self.entered = True

    def exit(self):
        taskMgr.remove(self.taskName)
        self.trigger = 0
        self.entered = False

    def __checkTrigger(self, task = None):
        if self.trigger:
            return
        if not random.random() > 0.6:
            return Task.again
        self.endTrigger = random.randint(*self.endTriggers) * 2 + 2
        self.__nextTrigger()
        taskMgr.doMethodLater(0.25, self.__nextTrigger, self.taskName)

    def __nextTrigger(self, task = None):
        if self.trigger == self.endTrigger:
            self.trigger = 0
            taskMgr.doMethodLater(2.5, self.__checkTrigger, self.taskName)
            return
        if self.trigger % 2 == 0:
            self.getScreen().showScene(self.nextScene, True)
        else:
            self.getScreen().showScene(self.origScene)
        self.trigger += 1
        return Task.again


class ConfuseGUIEffect(TVEffect):

    def __init__(self, confuseColor):
        TVEffect.__init__(self)
        self.confuseColor = confuseColor

    def enter(self):
        if self.entered:
            return
        self.entered = True
        screen = self.getScreen()
        if not screen.hasChatGui():
            return
        chatGui = screen.getChatGui()
        chatGui.fakeBubble['geom_color'] = self.confuseColor
        chatGui.setFakeBubble(True)

    def exit(self):
        if not self.entered:
            return
        self.entered = False
        screen = self.getScreen()
        if screen.hasChatGui():
            screen.getChatGui().setFakeBubble(False)


class FontEffect(TVEffect):

    def __init__(self, font, shadow = (0, 0, 0, 0)):
        TVEffect.__init__(self)
        self.font = font
        self.shadow = shadow

    def switchFont(self, font, shadow):
        screen = self.getScreen()
        if screen.hasChatGui():
            screen.getChatGui().switchFont(font, shadow)

    def enter(self):
        if self.entered:
            return
        self.switchFont(self.font, self.shadow)
        self.entered = True

    def exit(self):
        if not self.entered:
            return
        self.switchFont(OTPGlobals.getInterfaceFont(), (0, 0, 0, 0))
        self.entered = False