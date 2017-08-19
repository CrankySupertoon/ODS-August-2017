# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.DistributedNPCPainter
from direct.interval.IntervalGlobal import *
from otp.nametag.NametagConstants import CFSpeech, CFTimeout
from toontown.toonbase import TTLocalizer, ToontownGlobals
from DistributedNPCToonBase import DistributedNPCToonBase
from PaintShopGUI import PaintShopGUI
import time

class DistributedNPCPainter(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.lastCollision = 0
        self.sequence = None
        self.dialog = None
        return

    def disable(self):
        if self.sequence:
            self.sequence.finish()
            self.sequence = None
        self.ignoreAll()
        self.destroyDialog()
        DistributedNPCToonBase.disable(self)
        return

    def destroyDialog(self):
        self.clearChat()
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        return

    def freeAvatar(self):
        base.cr.playGame.getPlace().fsm.request('walk')
        base.setCellsAvailable(base.bottomCells, 1)

    def getCollSphereRadius(self):
        return 4.0

    def handleCollisionSphereEnter(self, collEntry):
        if self.lastCollision > time.time():
            return
        self.lastCollision = time.time() + ToontownGlobals.NPCCollisionDelay
        if base.localAvatar.getBankMoney() < ToontownGlobals.PaintCost:
            self.setChatAbsolute(TTLocalizer.PaintMoreMoneyMessage % ToontownGlobals.PaintCost, CFSpeech | CFTimeout)
            return
        base.cr.playGame.getPlace().fsm.request('stopped')
        base.setCellsAvailable(base.bottomCells, 0)
        self.setChatAbsolute(TTLocalizer.PaintPickColorMessage, CFSpeech)
        self.sequence = Sequence(camera.posHprInterval(1.5, (-2.8, 11, base.localAvatar.getHeight() + 3.5), (-180, -20, 0), other=base.localAvatar, blendType='easeIn'), Func(self.createDialog))
        self.sequence.start()

    def createDialog(self):
        self.destroyDialog()
        self.sequence = None
        self.dialog = PaintShopGUI(self.__paintShopDone)
        self.dialog.load()
        self.dialog.show()
        return

    def __paintShopDone(self, mode, dna):
        if mode == ToontownGlobals.NPC_TIMER:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
        elif mode == ToontownGlobals.NPC_EXIT:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)
        elif mode == ToontownGlobals.NPC_DONE:
            self.sendUpdate('requestPaint', [dna])
        self.freeAvatar()
        self.dialog = None
        return

    def paintResult(self, avId, status):
        if status == ToontownGlobals.NPC_NO_MONEY:
            self.setChatAbsolute(TTLocalizer.PaintNoMoneyMessage, CFSpeech | CFTimeout)
        elif status == ToontownGlobals.PAINT_INVALID_COLOR:
            self.setChatAbsolute(TTLocalizer.PaintInvalidColorMessage, CFSpeech | CFTimeout)
        elif status == ToontownGlobals.NPC_DONE:
            self.setChatAbsolute(TTLocalizer.PaintSuccessMessage, CFSpeech | CFTimeout)
            av = self.cr.doId2do.get(avId)
            if av:
                av.getDustCloud().start()