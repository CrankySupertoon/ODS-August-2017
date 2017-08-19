# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toontowngui.SleepScreen
from direct.gui.DirectGui import *
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import ToontownGlobals, TTLocalizer

class SleepScreen(DirectFrame):

    def __init__(self, parent = None, **kw):
        optiondefs = (('name', '???', self.updateName),
         ('command', self.destroy, self.updateCommand),
         ('frameColor', (0.1, 0.1, 0.1, 1), None),
         ('frameSize', (-10, 10, -10, 10), None),
         ('dnaString', None, self.updateToon))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.bed = loader.loadModel('phase_5.5/models/estate/regular_bed')
        self.bed.reparentTo(self)
        self.bed.find('**/pCube2').removeNode()
        self.bed.setScale(0.1)
        self.bed.setPos(-0.325, 0, -0.175)
        self.bed.setH(90)
        self.toon = None
        self.header = DirectLabel(self, relief=None, text_scale=0.1, text='', text_font=ToontownGlobals.getJiggeryPokeryFont(), text_fg=(1, 1, 1, 1), pos=(0, 0, 0.85))
        self.footer = DirectLabel(self, relief=None, text_scale=0.1, text=TTLocalizer.SleepScreenText, text_font=ToontownGlobals.getJiggeryPokeryFont(), text_fg=(1, 1, 1, 1), pos=(0, 0, -0.65))
        self.button = DirectButton(self, relief=None, image=Preloaded['blueButton'], image_color=(0.5, 0.5, 0.5, 1), text=TTLocalizer.lOK, text_scale=0.11, text_pos=(0, -0.02), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), pos=(0, 0, -0.85), scale=0.75)
        base.playMusic(self.getMusic(), looping=True, volume=0.8)
        self.initialiseoptions(SleepScreen)
        return

    def destroy(self):
        DirectFrame.destroy(self)
        if not hasattr(self, 'header'):
            return
        if self.toon:
            self.toon.delete()
        self.getMusic().stop()
        self.header.destroy()
        self.footer.destroy()
        self.button.destroy()
        del self.toon
        del self.header
        del self.footer
        del self.button

    def getMusic(self):
        return loader.loadMusic('phase_3/audio/bgm/lullaby.ogg')

    def updateName(self):
        self.header['text'] = TTLocalizer.SleepScreenName % {'name': self['name']}

    def updateCommand(self):
        self.button['command'] = self['command']

    def updateToon(self):
        if self.toon:
            self.toon.delete()
        dnaString = self['dnaString']
        if not dnaString:
            return
        dna = ToonDNA(dnaString)
        dna.removeAccessories()
        self.toon = Toon()
        self.toon.reparentTo(self.bed)
        self.toon.setDNAString(dna.makeNetString())
        self.toon.dropShadow.removeNode()
        self.toon.setPosHpr(0, -0.945 - self.toon.getHeight(), 2.3, 270, 90, 270)
        self.toon.setPlayRate(0.4, 'neutral')
        self.toon.loop('neutral')
        self.toon.setDepthWrite(True)
        self.toon.setDepthTest(True)
        self.toon.closeEyes()