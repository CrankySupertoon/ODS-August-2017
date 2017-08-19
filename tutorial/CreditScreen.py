# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.CreditScreen
from panda3d.core import NodePath
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from toontown.toonbase import ToontownGlobals, TTLocalizer

class CreditScreen(NodePath, DirectObject):

    def __init__(self):
        NodePath.__init__(self, 'creditScreen')
        self.labels = []
        self.z = 0
        self.addLabel(DirectLabel(self, relief=None, text=TTLocalizer.CreditsThankYou, text_scale=0.1, text_font=ToontownGlobals.getToonFont(), text_fg=(1, 1, 1, 1), text_wordwrap=20))
        self.z -= 0.5
        for game in TTLocalizer.Credits:
            self.addGame(game)

        self.z -= 0.65
        self.sequence = None
        return

    def getMusic(self):
        return loader.loadMusic('phase_3/audio/bgm/credits.ogg')

    def addGame(self, game):
        logo, name, credits, afterCredits = game
        if logo:
            self.z -= 0.1
            logo = DirectLabel(self, relief=None, image=logo, image_scale=(1, 0, 0.5), pos=(0, 0, self.z))
            logo.setTransparency(True)
            self.addLabel(logo, True)
            self.z -= 0.15
        self.addLabel(DirectLabel(self, relief=None, text='\x01beigeShadow\x01%s\x02' % name, text_fg=(1, 1, 1, 1), text_scale=0.1, text_font=ToontownGlobals.getMinnieFont(), text_shadow=(0, 0, 0, 1)))
        for credit in credits:
            title, names = credit
            self.z -= 0.15
            self.addLabel(DirectLabel(self, relief=None, text=title, text_fg=(1, 1, 1, 1), text_scale=0.1, text_font=ToontownGlobals.getMinnieFont(), text_shadow=(0, 0, 0, 1), text_wordwrap=20))
            self.z -= 0.025
            self.addLabel(DirectLabel(self, relief=None, text='\n'.join(names), text_fg=(1, 1, 1, 1), text_scale=0.09, text_font=ToontownGlobals.getToonFont(), text_shadow=(0, 0, 0, 1)))

        self.z -= 0.15
        self.addLabel(DirectLabel(self, relief=None, text='\x01orangeShadow\x01%s\x02' % afterCredits, text_scale=0.1, text_font=ToontownGlobals.getToonFont(), text_fg=(1, 1, 1, 1), text_wordwrap=20, text_shadow=(0, 0, 0, 1)))
        self.z -= 0.35
        return

    def removeNode(self):
        if not hasattr(self, 'labels'):
            return
        for label in self.labels:
            label.destroy()

        del self.labels
        self.stop()
        self.ignoreAll()
        NodePath.removeNode(self)

    def fadeOut(self):
        base.transitions.fadeOut(0)
        base.transitions.fade.setColor(0.2, 0.2, 0.2, 1)
        self.reparentTo(aspect2dp)
        self.setPos(0, 0, -1.1)

    def start(self):
        if self.sequence:
            return
        base.playMusic(self.getMusic(), looping=True, volume=0.6)
        self.sequence = Sequence(self.posInterval(4 * -self.z, (0, 0, -self.z)), Func(self.stop))
        self.sequence.start()
        self.accept('wheel_up-up', self.__wheel, [-0.5])
        self.accept('wheel_down-up', self.__wheel, [0.5])
        self.accept('escape', self.stop)

    def __wheel(self, time):
        if self.sequence:
            self.sequence.setT(max(0, self.sequence.getT() + time))

    def stop(self):
        if not self.sequence:
            return
        else:
            base.fadeMusic(self.getMusic(), 3)
            self.sequence.pause()
            self.sequence = None
            messenger.send('creditsOver')
            self.removeNode()
            return

    def getLabelZ(self, label):
        label.resetFrameSize()
        left, right, down, up = label.node().getFrame()
        return abs(down) + abs(up)

    def addLabel(self, label, halve = False):
        label.setZ(self.z)
        self.labels.append(label)
        if halve:
            self.z -= self.getLabelZ(label) / 2
        else:
            self.z -= self.getLabelZ(label)