# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.ai.DistributedBlackCatMgr
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from toontown.toonbase import ToontownGlobals
from toontown.toon import ToonDNA

class DistributedBlackCatMgr(DistributedObject):
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackCatMgr')

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        base.cr.blackCatMgr = self

    def delete(self):
        base.cr.blackCatMgr = None
        DistributedObject.delete(self)
        return

    def requestBlackCatTransformation(self):
        if not base.cr.newsManager.isHolidayRunning(ToontownGlobals.BLACK_CAT_DAY):
            return
        self.sendUpdate('requestBlackCatTransformation')

    def doBlackCatTransformation(self):
        base.localAvatar.getDustCloud(0.0, color=ToonDNA.getBlackColor()).start()