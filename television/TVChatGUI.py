# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.television.TVChatGUI
from panda3d.core import Buffer, CardMaker, TextNode, Texture, TextureStage
from direct.gui.DirectGui import *
MinAspectRatio = 1.22

class TVChatGUI(DirectFrame):

    def __init__(self, screen, parent = aspect2d, **kw):
        optiondefs = (('relief', None, None),
         ('geom', Preloaded['cogdoChatBg'], None),
         ('geom_scale', 5.2, None),
         ('pos', (0.09, 0, -0.6), None))
        self.screen = screen
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(TVChatGUI)
        self.bubble = DirectLabel(self, relief=None, geom=Preloaded['cogdoChatBubble'], geom_scale=(6.5, 6.5, 7.3), pos=(0.18, 0, 0), text='', text_pos=(0, 0.05), text_scale=0.06, text_wordwrap=28, text_align=TextNode.ACenter)
        self.fakeBubble = DirectFrame(self, relief=None, geom=Preloaded['cogdoChatBubble'], geom_scale=(6.5, 6.5, 7.3), pos=(0.18, 0, 0))
        self.button = DirectButton(self.bubble, relief=None, state=DGG.NORMAL, geom=Preloaded['cogdoChatButton'], pos=(0.62, 0, -0.165), scale=4.2, command=self.__buttonPressed)
        self.textureStage = TextureStage('tv-chat-screen')
        self.screenCard = self.attachNewNode(CardMaker('tv-chat-screen').generate())
        self.screenCard.setPos(-1.05, 0, -0.16)
        self.screenCard.setScale(0.36, 1, 0.3)
        self.setBin('background', 1)
        self.screenCard.setBin('background', 2)
        self.bubble.setBin('background', 3)
        self.fakeBubble.setBin('background', 3)
        self.setFakeBubble(False)
        self.sounds = {}
        self.clickCounter = 0
        self.loaded = True
        return

    def delete(self):
        if not self.loaded:
            return
        for element in [self.button, self.bubble, self.fakeBubble]:
            element.destroy()

        for element in [self.screenCard]:
            element.removeNode()

        DirectFrame.destroy(self)
        del self.bubble
        del self.fakeBubble
        del self.button
        del self.textureStage
        del self.screenCard
        del self.sounds
        self.loaded = False

    def show(self):
        DirectFrame.show(self)
        base.applyMinAspectRatio(MinAspectRatio)

    def hide(self):
        DirectFrame.hide(self)
        base.unapplyMinAspectRatio()

    def getScreen(self):
        return self.screen

    def getClickCounter(self):
        return self.clickCounter

    def getCallbackEvent(self):
        return self.uniqueName('buttonClicked')

    def setFakeBubble(self, state):
        if state:
            self.bubble.hide()
            self.fakeBubble.show()
        else:
            self.bubble.show()
            self.fakeBubble.hide()

    def setTexture(self, texture, scale):
        if texture == self.getScreen().getBuffer().getTexture():
            self.screenCard.setTexScale(self.textureStage, 0.93, 0.52)
        else:
            self.screenCard.setTexScale(self.textureStage, 1, 1)
        self.screenCard.setTexture(self.textureStage, texture, scale)

    def setButtonState(self, enabled):
        self.button.show() if enabled else self.button.hide()

    def resetClickCounter(self):
        self.clickCounter = 0

    def registerSounds(self, *sounds):
        for soundTuple in sounds:
            name, filename = soundTuple
            self.sounds[name] = loader.loadSfx(filename)

    def switchFont(self, font, shadow):
        self.bubble['text_font'] = font
        self.bubble['text_shadow'] = shadow

    def playTextSound(self, text, sound):
        self.playText(text)
        if isinstance(sound, str):
            self.playSound(sound)
        else:
            for sfx in sound:
                self.playSound(sfx)

    def playText(self, text):
        self.bubble['text'] = text

    def playSound(self, sound):
        if sound in self.sounds:
            base.playSfx(self.sounds[sound], volume=0.9)

    def __buttonPressed(self):
        self.clickCounter += 1
        messenger.send(self.getCallbackEvent(), [self.clickCounter])