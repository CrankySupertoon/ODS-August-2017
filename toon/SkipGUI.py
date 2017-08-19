# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.SkipGUI
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from otp.otpbase import OTPLocalizer
from toontown.toonbase import ToontownGlobals, TTLocalizer, ToontownBattleGlobals
from toontown.toontowngui.NumberCounter import NumberCounter
from toontown.toontowngui import TTDialog
from toontown.toon.InventoryNew import InventoryNew
from toontown.quest import Quests
from toontown.hood import ZoneUtil
import math

class HoodGUI(DirectFrame):

    def __init__(self, hood):
        DirectFrame.__init__(self, relief=None, geom_color=ToontownGlobals.GlobalDialogColor, geom=DGG.getDefaultDialogGeom(), geom_scale=(1.85, 1, 1.4), text=TTLocalizer.SkipToTitle % self.getText(hood), text_scale=0.09, text_pos=(0, 0.6))
        self.initialiseoptions(HoodGUI)
        self.hood = hood
        self.info = ToontownGlobals.SkippableTiers[hood]
        self.label = DirectLabel(self, relief=None, text='', text_scale=0.055, pos=(0, 0, 0.42), text_wordwrap=26)
        self.inv = InventoryNew(base.localAvatar, base.localAvatar.inventory.invString)
        self.inv.setActivateMode('book')
        self.inv.updateGUI()
        self.inv.invFrame.reparentTo(self)
        self.inv.invFrame.setPos(0.2, 0, 0.16)
        self.inv.invFrame.setScale(0.81)
        self.inv.detailFrame.removeNode()
        self.counters = []
        self.tracks = []
        self.maxPoints = self.getMaximumPoints()
        self.maxGags = self.info['gagTracks']
        self.zone = self.info['zone']
        for i in xrange(len(ToontownBattleGlobals.Tracks)):
            minimum = 1 if i in (4, 5) else 0
            self.tracks.append(minimum)
            counter = NumberCounter(minimum, minimum, 'updateHoodGUI', 10)
            counter.reparentTo(self)
            counter.setPos(-0.68, 0, 0.16 - i * 0.1)
            self.counters.append(counter)
            for j in xrange(len(ToontownBattleGlobals.Levels[i])):
                self.inv.buttons[i][j]['text'] = ''

        self.__updateAll()
        self.cancelButton = DirectButton(self, relief=None, image=Preloaded['closeButton'], pos=(-0.2, 0, -0.55), text=OTPLocalizer.lCancel, text_scale=0.06, text_pos=(0, -0.1), command=self.__cancel)
        self.okButton = DirectButton(self, relief=None, image=Preloaded['okButton'], pos=(0.2, 0, -0.55), text=TTLocalizer.SkipButton, text_scale=0.06, text_pos=(0, -0.1), command=self.__verify)
        self.accept('updateHoodGUI', self.__updateAll)
        self.dialog = None
        return

    def destroy(self):
        DirectFrame.destroy(self)
        if not hasattr(self, 'label'):
            return
        self.label.destroy()
        self.inv.destroy()
        for counter in self.counters:
            counter.destroy()

        self.cancelButton.destroy()
        self.okButton.destroy()
        self.destroyDialog()
        del self.label
        del self.inv
        del self.counters
        del self.cancelButton
        del self.okButton

    def destroyDialog(self):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        return

    def __cancel(self, *args):
        messenger.send('exitHoodGUI')
        self.destroy()

    def __closeDialog(self, *args):
        self.destroyDialog()

    def __acknowledgeDialog(self, choice):
        if choice > 0:
            base.localAvatar.d_skipToTier(self.hood, self.tracks)
            messenger.send('exitSkipGUI')
            self.destroy()
            base.cr.playGame.getPlace().fsm.request('teleportOut', [{'loader': ZoneUtil.getLoaderName(self.zone),
              'where': ZoneUtil.getWhereName(self.zone, 1),
              'how': 'teleportIn',
              'hoodId': self.zone,
              'zoneId': self.zone,
              'shardId': None,
              'avId': -1}])
        else:
            self.destroyDialog()
        return

    def showDialog(self, message):
        self.destroyDialog()
        self.dialog = TTDialog.TTDialog(style=TTDialog.Acknowledge, text=message, text_wordwrap=20, command=self.__closeDialog)
        self.dialog.show()

    def __verify(self, *args):
        if self.getPointsLeft() > 0:
            self.showDialog(TTLocalizer.SkipReallocateMessage)
            return
        if self.getUsedGags() != self.maxGags:
            self.showDialog(TTLocalizer.SkipGagTrackMessage % self.maxGags)
            return
        self.destroyDialog()
        self.dialog = TTDialog.TTDialog(style=TTDialog.TwoChoice, text=TTLocalizer.SkipConfirmMessage, text_wordwrap=20, command=self.__acknowledgeDialog)
        self.dialog.show()

    def getMaximumPoints(self):
        return max(self.info['points'], base.localAvatar.getTotalExperience())

    def getPointsLeft(self):
        points = self.getMaximumPoints()
        for counter in self.counters:
            points -= counter.current

        return max(points, 0)

    def getMaxPointsFor(self, counter, pointsLeft):
        return min(counter.current, pointsLeft)

    def getUsedGags(self):
        used = 0
        for i, counter in enumerate(self.counters):
            if counter.current:
                used += 1

        return used

    def __updateAll(self, *args):
        pointsLeft = self.getPointsLeft()
        used = self.getUsedGags()
        for i, counter in enumerate(self.counters):
            if pointsLeft and (counter.current > 0 or used < self.maxGags):
                counter.maximum = self.maxPoints
            else:
                counter.maximum = counter.current
            counter.increment = min(10, max(pointsLeft, 1))
            counter.updateCounter(0)
            bar = self.inv.trackBars[i]
            if counter.current:
                nextExp = counter.current
                for amount in ToontownBattleGlobals.Levels[i]:
                    if counter.current < amount:
                        nextExp = amount
                        break

                bar['text'] = TTLocalizer.InventoryTrackExp % {'curExp': counter.current,
                 'nextExp': nextExp}
                bar['range'] = nextExp
                bar['value'] = counter.current
                bar.show()
            else:
                bar.hide()
            for j in xrange(len(ToontownBattleGlobals.Levels[i])):
                if counter.current != 0 and counter.current >= ToontownBattleGlobals.Levels[i][j]:
                    self.inv.buttons[i][j].show()
                else:
                    self.inv.buttons[i][j].hide()

            self.tracks[i] = counter.current

        self.label['text'] = TTLocalizer.SkipToDescription % pointsLeft

    def getText(self, hood):
        if hood == Quests.DD_TIER:
            return TTLocalizer.lDonaldsDock
        if hood == Quests.DG_TIER:
            return TTLocalizer.lDaisyGardens


class SkipGUI(DirectObject):

    def __init__(self, pos = (0, 0, 0)):
        self.loaded = False
        self.pos = pos

    def load(self):
        if self.loaded:
            return
        else:
            self.frame = DirectFrame(relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(0.9, 1, 0.6), pos=self.pos)
            self.dockButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(0, 0.5, 1, 1), text=TTLocalizer.SkipToName % TTLocalizer.lDonaldsDock, text_scale=0.07, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, 0.12), command=self.__chooseTier, extraArgs=[Quests.DD_TIER])
            self.gardenButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(0, 0.5, 1, 1), text=TTLocalizer.SkipToName % TTLocalizer.lDaisyGardens, text_scale=0.07, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, 0), command=self.__chooseTier, extraArgs=[Quests.DG_TIER])
            self.cancelButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(1, 0, 0, 1), text=TTLocalizer.lCancel, text_scale=0.07, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, -0.12), command=self.cancel)
            self.gui = None
            self.loaded = True
            return

    def destroy(self):
        if self.gui:
            self.gui.destroy()
            self.gui = None
        if not self.loaded:
            return
        else:
            self.frame.destroy()
            del self.frame
            del self.dockButton
            del self.gardenButton
            del self.cancelButton
            self.loaded = False
            return

    def enter(self):
        self.setButtonState(self.dockButton, base.localAvatar.rewardTier < Quests.DD_TIER)
        self.setButtonState(self.gardenButton, base.localAvatar.rewardTier < Quests.DG_TIER)

    def setButtonState(self, button, state):
        state = DGG.NORMAL if state else DGG.DISABLED
        button['geom_color'] = (0, 0.5, 1, 1) if state == DGG.NORMAL else (0.5, 0.5, 0.5, 1)
        button['state'] = state

    def cancel(self, *args):
        messenger.send('exitSkip')
        self.destroy()

    def __chooseTier(self, tier):
        self.frame.hide()
        self.gui = HoodGUI(tier)
        self.acceptOnce('exitHoodGUI', self.__exitHoodGUI)
        self.acceptOnce('exitSkipGUI', self.cancel)

    def __exitHoodGUI(self):
        if hasattr(self, 'frame'):
            self.frame.show()
        else:
            messenger.send('exitSkip')