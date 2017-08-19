# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.PaintShopGUI
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals, TTLocalizer, ToontownTimer
from toontown.toontowngui.IntuitiveColorPicker import IntuitiveColorPicker
from toontown.toon import ToonDNA
import NPCToons
EMPTY_DNA = (0, 0, 0, 0)
All = 0
Head = 1
Body = 2
Legs = 3

class PaintShopGUI:

    def __init__(self, callback):
        self.callback = callback
        self.loaded = False
        self.shown = False

    def load(self):
        if self.loaded:
            return
        else:
            dna = base.localAvatar.style
            self.lastDNA = [dna.headColor, dna.armColor, dna.legColor]
            self.newDNA = [EMPTY_DNA] * len(self.lastDNA)
            self.frame = aspect2d.attachNewNode('PaintShop')
            self.frame.hide()
            self.timer = ToontownTimer.ToontownTimer()
            self.timer.reparentTo(self.frame)
            self.timer.posInTopRightCorner()
            self.title = DirectLabel(self.frame, relief=None, text=TTLocalizer.PaintGUITitle, text_fg=(0, 1, 0, 1), text_scale=0.15, text_font=ToontownGlobals.getSignFont(), pos=(0, 0, 0.8), text_shadow=(1, 1, 1, 1))
            self.notice = DirectLabel(self.title, relief=None, text='', text_fg=(1, 0, 0, 1), text_scale=0.11, text_font=ToontownGlobals.getSignFont(), pos=(0, 0, -0.2), text_shadow=(1, 1, 1, 1))
            self.buyButton = DirectButton(self.frame, relief=None, image=Preloaded['blueButton'], text=TTLocalizer.PaintGUIBuy, text_scale=0.11, text_pos=(0, -0.02), pos=(0.6, 0, -0.68), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), command=self.__exit, extraArgs=[ToontownGlobals.NPC_DONE])
            self.cancelButton = DirectButton(self.frame, relief=None, image=Preloaded['blueButton'], text=TTLocalizer.lCancel, text_scale=0.11, text_pos=(0, -0.02), pos=(1.4, 0, -0.68), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), command=self.__exit)
            self.colorPicker = IntuitiveColorPicker(self.frame, ToontownGlobals.COLOR_SATURATION_MIN, ToontownGlobals.COLOR_SATURATION_MAX, ToontownGlobals.COLOR_VALUE_MIN, ToontownGlobals.COLOR_VALUE_MAX, self.__colorPicked, ToonDNA.matColorsList, (1, 0, 0))
            self.colorPicker.setPartButtons([(All, TTLocalizer.ColorAll),
             (Head, TTLocalizer.BodyShopHead),
             (Body, TTLocalizer.BodyShopBody),
             (Legs, TTLocalizer.BodyShopLegs)], xStart=-0.29, xIncrement=0.2)
            self.updateJellybeans()
            self.loaded = True
            return

    def show(self):
        if not self.loaded or self.shown:
            return
        self.frame.show()
        self.timer.countdown(NPCToons.CLERK_COUNTDOWN_TIME, self.__exit, [ToontownGlobals.NPC_TIMER])
        base.applyMinAspectRatio(ToontownGlobals.RepaintDialogAspectRatio)
        self.shown = True

    def hide(self):
        if not self.loaded or not self.shown:
            return
        self.frame.hide()
        self.timer.reset()
        base.unapplyMinAspectRatio()
        self.shown = False

    def destroy(self):
        if not self.loaded:
            return
        self.timer.destroy()
        self.colorPicker.destroy()
        self.frame.removeNode()
        del self.lastDNA
        del self.frame
        del self.timer
        del self.title
        del self.notice
        del self.buyButton
        del self.cancelButton
        del self.colorPicker
        self.loaded = False

    def getNumEdits(self):
        return len([ x for x in self.newDNA if x != EMPTY_DNA ])

    def updateJellybeans(self):
        cost = ToontownGlobals.PaintCost * self.getNumEdits()
        available = base.localAvatar.getBankMoney() < cost
        self.notice['text'] = (TTLocalizer.PaintGUINoticeIns if available else TTLocalizer.PaintGUINotice) % cost
        self.buyButton['state'] = DGG.DISABLED if available else DGG.NORMAL

    def __exit(self, mode = ToontownGlobals.NPC_EXIT):
        if mode == ToontownGlobals.NPC_DONE and self.newDNA == [EMPTY_DNA] * len(self.lastDNA):
            mode = ToontownGlobals.NPC_EXIT
        dna = base.localAvatar.style
        dna.headColor, dna.armColor, dna.legColor = self.lastDNA
        base.localAvatar.swapToonColor(dna)
        self.hide()
        self.destroy()
        self.callback(mode, self.newDNA)
        del self.newDNA

    def __colorPicked(self, rgb):
        dna = base.localAvatar.getStyle()
        if self.colorPicker.isPartChosen(Head):
            dna.headColor = rgb
        if self.colorPicker.isPartChosen(Body):
            dna.armColor = rgb
        if self.colorPicker.isPartChosen(Legs):
            dna.legColor = rgb
        if self.colorPicker.isPartChosen(All):
            self.newDNA = [rgb] * len(self.newDNA)
        else:
            self.newDNA[self.colorPicker.part - 1] = rgb
        base.localAvatar.swapToonColor(dna)
        self.updateJellybeans()