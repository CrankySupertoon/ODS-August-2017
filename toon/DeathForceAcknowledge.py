# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.DeathForceAcknowledge
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from direct.showbase import Transitions
from direct.gui.DirectGui import *
import LaffMeter

class DeathForceAcknowledge:

    def __init__(self, doneEvent):
        fadeModel = loader.loadModel('phase_3/models/misc/fade')
        if fadeModel:
            self.fade = DirectFrame(parent=aspect2dp, relief=None, image=fadeModel, image_color=(0, 0, 0, 0.4), image_scale=4.0, state=DGG.NORMAL)
            self.fade.reparentTo(aspect2d, FADE_SORT_INDEX)
            fadeModel.removeNode()
        else:
            print 'Problem loading fadeModel.'
            self.fade = None
        if base.localAvatar.getHardcoreModeEnabled():
            text = TTLocalizer.PlaygroundHardcoreAckMessage
        else:
            text = TTLocalizer.PlaygroundDeathAckMessage
        self.dialog = TTDialog.TTGlobalDialog(message=text, doneEvent=doneEvent, style=TTDialog.Acknowledge, suppressKeys=True)
        if base.localAvatar.getHardcoreModeEnabled():
            self.greened = DirectFrame(self.dialog, relief=None, image='phase_3/maps/melody_greened.png', scale=0.075, hpr=(0, 0, -20), pos=(0.5, 0, -0.375))
            self.greened.setTransparency(True)
        else:
            self.greened = None
        self.dialog['text_pos'] = (-0.26, 0.1)
        scale = self.dialog.component('image0').getScale()
        scale.setX(scale[0] * 1.3)
        self.dialog.component('image0').setScale(scale)
        av = base.localAvatar
        self.laffMeter = LaffMeter.LaffMeter(av.style, av.hp, av.maxHp)
        self.laffMeter.reparentTo(self.dialog)
        if av.style.getAnimal() == 'monkey':
            self.laffMeter.setPos(-0.46, 0, -0.035)
            self.laffMeter.setScale(0.085)
        else:
            self.laffMeter.setPos(-0.48, 0, -0.035)
            self.laffMeter.setScale(0.1)
        self.laffMeter.start()
        self.dialog.show()
        return

    def cleanup(self):
        if self.fade:
            self.fade.destroy()
        if self.laffMeter:
            self.laffMeter.destroy()
            del self.laffMeter
        if self.greened:
            self.greened.destroy()
            del self.greened
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        return