# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.chat.ChatLog
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from otp.nametag.NametagConstants import NAMETAG_COLORS
from otp.otpbase import OTPLocalizer
from toontown.shtiker.OptionsPage import speedChatStyles
from toontown.toonbase import ToontownGlobals, TTLocalizer

class ChatLog(DirectFrame):

    def __init__(self, **kwargs):
        args = {'parent': base.a2dTopLeft,
         'relief': None,
         'geom': Preloaded['squareBox'],
         'geom_scale': (1, 1, 0.55),
         'pos': (0.5, 0, -0.3)}
        kwargs.update(args)
        DirectFrame.__init__(self, **kwargs)
        self.initialiseoptions(ChatLog)
        self.log = []
        self.realLog = []
        self.current = 0
        self.text = TextNode('text')
        self.text.setShadow(0.05, 0.05)
        self.text.setShadowColor(0, 0, 0, 1)
        self.text.setWordwrap(21.5)
        self.text.setAlign(TextNode.ALeft)
        self.text.setTextColor(1, 1, 1, 1)
        self.text.setFont(ToontownGlobals.getToonFont())
        self.textNode = self.attachNewNode(self.text, 0)
        self.textNode.setPos(-0.435, 0, 0.175)
        self.textNode.setScale(0.04)
        self.exitButton = DirectButton(self, relief=None, geom=Preloaded['squareBox'], geom_color=(1, 0, 0, 1), geom_scale=(1, 1, 0.1), pos=(0, 0, -0.3), pressEffect=False, text=TTLocalizer.FishingExit, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.06, text_pos=(0, -0.0175), command=self.__exit)
        self.autoScroll = True
        self.accept('addChatHistory', self.__addChatHistory)
        self.accept('SpeedChatStyleChange', self.__updateSpeedChatStyle)
        return

    def removeNode(self):
        self.destroy()

    def destroy(self):
        DirectFrame.destroy(self)
        if not hasattr(self, 'log'):
            return
        self.textNode.removeNode()
        self.exitButton.destroy()
        del self.log
        del self.text
        del self.textNode
        del self.exitButton
        self.ignoreAll()

    def show(self):
        DirectFrame.show(self)
        self.__updateSpeedChatStyle()
        self.computeRealLog()
        self.accept('wheel_up-up', self.__wheel, [-1])
        self.accept('wheel_down-up', self.__wheel, [1])

    def hide(self):
        DirectFrame.hide(self)
        self.ignore('wheel_up-up')
        self.ignore('wheel_down-up')

    def scrollToCurrent(self):
        minimum = max(0, self.current - 10)
        self.text.setText('\n'.join(self.realLog[minimum:self.current]))

    def computeRealLog(self):
        oldText = self.text.getText()
        self.text.setText('\n'.join(self.log))
        self.realLog = self.text.getWordwrappedText().split('\n')
        if self.autoScroll:
            self.current = len(self.realLog)
            self.scrollToCurrent()
        else:
            self.text.setText(oldText)

    def __updateSpeedChatStyle(self):
        r, g, b = speedChatStyles[base.localAvatar.speedChatStyleIndex][2]
        self['geom_color'] = (r,
         g,
         b,
         1)

    def __exit(self):
        base.localAvatar.chatMgr.fsm.request('mainMenu')

    def __addChatHistory(self, name, font, speechFont, colorCode, chat):
        if font:
            color = NAMETAG_COLORS[colorCode][0][0]
            self.log.append('\x01%s\x01\x01%s\x01%s:\x02\x02 \x01%s\x01%s\x02' % (OTPLocalizer.getPropertiesForFont(font),
             OTPLocalizer.getPropertiesForColor(color),
             name,
             OTPLocalizer.getPropertiesForFont(speechFont),
             chat))
        else:
            self.log.append('\x01amber\x01%s: %s\x02' % (name, chat))
        if len(self.log) == 250:
            del self.log[0]
        if not self.isHidden():
            self.computeRealLog()

    def __wheel(self, amount):
        oldCurrent = self.current
        minimum = min(10, len(self.realLog))
        self.current += amount
        self.autoScroll = self.current >= len(self.realLog)
        if self.autoScroll:
            self.current = len(self.realLog)
        if self.current < minimum:
            self.current = minimum
        if oldCurrent != self.current:
            self.scrollToCurrent()