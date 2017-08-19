# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.DistributedNPCLaffRestock
from otp.nametag.NametagConstants import CFSpeech, CFTimeout
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toon import NPCToons
from DistributedNPCToonBase import DistributedNPCToonBase
import LaffRestockGlobals, LaffShopGui, time

class DistributedNPCLaffRestock(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.lastCollision = 0
        self.laffDialog = None
        return

    def disable(self):
        self.ignoreAll()
        self.destroyDialog()
        DistributedNPCToonBase.disable(self)

    def destroyDialog(self):
        self.clearChat()
        if self.laffDialog:
            self.laffDialog.destroy()
            self.laffDialog = None
        return

    def postToonStateInit(self):
        self.putOnSuit(ToontownGlobals.cogHQZoneId2deptIndex(self.zoneId), rental=True)

    def getCollSphereRadius(self):
        return 1.25

    def handleCollisionSphereEnter(self, collEntry):
        if self.lastCollision > time.time():
            return
        self.lastCollision = time.time() + ToontownGlobals.NPCCollisionDelay
        if base.localAvatar.getHp() >= base.localAvatar.getMaxHp():
            self.setChatAbsolute(TTLocalizer.RestockFullLaffMessage, CFSpeech | CFTimeout)
            return
        base.cr.playGame.getPlace().fsm.request('stopped')
        base.setCellsAvailable(base.bottomCells, 0)
        self.destroyDialog()
        self.acceptOnce('laffShopDone', self.__laffShopDone)
        self.laffDialog = LaffShopGui.LaffShopGui()

    def freeAvatar(self):
        base.cr.playGame.getPlace().fsm.request('walk')
        base.setCellsAvailable(base.bottomCells, 1)

    def __laffShopDone(self, state, laff):
        self.freeAvatar()
        if state == LaffRestockGlobals.TIMER_END:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
        elif state == LaffRestockGlobals.USER_CANCEL:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)
        elif state == LaffRestockGlobals.RESTOCK:
            self.sendUpdate('restock', [laff])

    def restockResult(self, state):
        if state in LaffRestockGlobals.RestockMessages:
            self.setChatAbsolute(LaffRestockGlobals.RestockMessages[state], CFSpeech | CFTimeout)