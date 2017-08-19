# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.makeatoon.ColorShop
from direct.fsm import StateData
from toontown.toon import ToonDNA
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui.IntuitiveColorPicker import IntuitiveColorPicker
from MakeAToonGlobals import *
All = 0
Head = 1
Body = 2
Legs = 3

class ColorShop(StateData.StateData):

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.toon = None
        self.frame = None
        return

    def enter(self, toon):
        self.toon = toon
        self.frame.show()
        self.acceptOnce('last', lambda : self.__handleDoneStatus('last'))
        self.acceptOnce('next', lambda : self.__handleDoneStatus('next'))

    def exit(self):
        self.ignoreAll()
        self.toon = None
        self.frame.hide()
        return

    def load(self):
        if self.frame:
            return
        self.frame = base.a2dBottomRight.attachNewNode('colorShop')
        self.frame.hide()
        self.colorPicker = IntuitiveColorPicker(self.frame, ToontownGlobals.COLOR_SATURATION_MIN, ToontownGlobals.COLOR_SATURATION_MAX, ToontownGlobals.COLOR_VALUE_MIN, ToontownGlobals.COLOR_VALUE_MAX, self.__colorPicked, ToonDNA.matColorsList, pos=(-0.5, 0, 1))
        self.colorPicker.setPartButtons([(All, TTLocalizer.ColorAll),
         (Head, TTLocalizer.BodyShopHead),
         (Body, TTLocalizer.BodyShopBody),
         (Legs, TTLocalizer.BodyShopLegs)], xStart=-0.29, xIncrement=0.2)

    def unload(self):
        if not self.frame:
            return
        else:
            self.frame.removeNode()
            self.colorPicker.removeNode()
            self.frame = None
            self.colorPicker = None
            return

    def __handleDoneStatus(self, doneStatus):
        self.doneStatus = doneStatus
        messenger.send(self.doneEvent)

    def __colorPicked(self, rgb):
        dna = self.toon.getStyle()
        if self.colorPicker.isPartChosen(Head):
            dna.headColor = rgb
        if self.colorPicker.isPartChosen(Body):
            dna.armColor = rgb
        if self.colorPicker.isPartChosen(Legs):
            dna.legColor = rgb
        self.toon.swapToonColor(dna)