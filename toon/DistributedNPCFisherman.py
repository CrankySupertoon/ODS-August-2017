# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.DistributedNPCFisherman
from panda3d.core import Camera, Point3
from direct.gui.DirectGui import *
from direct.interval.LerpInterval import LerpPosHprInterval
from direct.task.Task import Task
import time, random
from DistributedNPCToonBase import *
import NPCToons
from toontown.fishing import FishSellGUI
from toontown.toonbase import TTLocalizer, ToontownTimer
from toontown.fishing.FishermanGUI import FishermanGUI
from otp.nametag.NametagConstants import *
from otp.nametag import NametagGlobals

class DistributedNPCFisherman(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.av = None
        self.button = None
        self.popupInfo = None
        self.gui = None
        self.timer = None
        self.nextCollision = 0
        return

    def disable(self):
        self.ignoreAll()
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        self.destroyGui()
        self.av = None
        if self.isLocalToon:
            base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)
        return

    def destroyGui(self):
        if self.gui:
            self.gui.destroy()
            self.gui = None
        if self.timer:
            self.timer.destroy()
            self.timer = None
        return

    def getNpcOriginParent(self):
        return self.cr.playGame.hood.loader.geom

    def getNpcOrigin(self):
        return '**/npc_fisherman_origin_%s;+s'

    def getCollSphereRadius(self):
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        self.currentTime = time.time()
        if self.nextCollision > self.currentTime:
            self.nextCollision = self.currentTime + 2
        else:
            base.cr.playGame.getPlace().fsm.request('stopped')
            self.sendUpdate('avatarEnter', [])
            self.nextCollision = self.currentTime + 2

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None
        return

    def setupAvatars(self, av):
        self.ignoreAvatars()
        av.stopLookAround()
        av.lerpLookAt(Point3(-0.5, 4, 0), time=0.5)
        self.stopLookAround()
        self.lerpLookAt(Point3(av.getPos(self)), time=0.5)

    def resetFisherman(self):
        self.ignoreAll()
        self.destroyGui()
        self.show()
        self.startLookAround()
        self.detectAvatars()
        if self.isLocalToon:
            self.freeAvatar()
        return Task.done

    def getRandomString(self, list, seed):
        return random.Random(seed).choice(list)

    def setMovie(self, mode, npcId, avId, extraArgs, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.FISHERMAN_COUNTDOWN_TIME - timeStamp
        self.npcId = npcId
        self.isLocalToon = avId == base.localAvatar.doId
        if self.isLocalToon:
            NametagGlobals.setMasterArrowsOn(True)
            self.cr.disableTransparentToons()
        if mode == NPCToons.SELL_MOVIE_CLEAR:
            return
        else:
            if mode == NPCToons.SELL_MOVIE_TIMEOUT:
                if self.isLocalToon:
                    if self.popupInfo:
                        self.popupInfo.reparentTo(hidden)
                    self.destroyGui()
                self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_START:
                self.av = base.cr.doId2do.get(avId)
                if self.av is None:
                    self.notify.warning('Avatar %d not found in doId' % avId)
                    return
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
                self.setupAvatars(self.av)
                self.setChatAbsolute(self.getRandomString(TTLocalizer.FishermanHello, timestamp), CFSpeech)
                if self.isLocalToon:
                    camera.wrtReparentTo(render)
                    NametagGlobals.setMasterArrowsOn(False)
                    self.cr.enableTransparentToons()
                    Sequence(LerpPosQuatInterval(camera, 1, Point3(1, 8, self.getHeight()), Point3(180, -2, 0), other=self, blendType='easeInOut'), Func(self.popupGUI)).start()
            elif mode == NPCToons.SELL_MOVIE_COMPLETE:
                chatStr = TTLocalizer.STOREOWNER_THANKSFISH
                self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_DUMPEDFISH:
                self.setChatAbsolute(TTLocalizer.STOREOWNER_DUMPEDFISH, CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_TROPHY:
                self.av = base.cr.doId2do.get(avId)
                if self.av is None:
                    self.notify.warning('Avatar %d not found in doId' % avId)
                    return
                numFish, totalNumFish = extraArgs
                self.setChatAbsolute(TTLocalizer.STOREOWNER_TROPHY % (numFish, totalNumFish), CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_NOFISH:
                chatStr = TTLocalizer.STOREOWNER_NOFISH
                self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_REPAIRED:
                self.setChatAbsolute(TTLocalizer.STOREOWNER_REPAIRED, CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_NEWROD:
                self.setChatAbsolute(TTLocalizer.STOREOWNER_NEWROD % TTLocalizer.FishingRodNameDict[extraArgs[0]], CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_NEWTANK:
                self.setChatAbsolute(TTLocalizer.STOREOWNER_NEWTANK % extraArgs[0], CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_NEWLURE:
                self.setChatAbsolute(TTLocalizer.STOREOWNER_NEWLURE % TTLocalizer.FishingLureColors[extraArgs[0]], CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_BAIT:
                bait, count = extraArgs
                self.setChatAbsolute(TTLocalizer.STOREOWNER_BAIT % (count, TTLocalizer.FishGenusNames[bait]), CFSpeech | CFTimeout)
                self.resetFisherman()
            elif mode == NPCToons.SELL_MOVIE_NO_MONEY:
                self.notify.warning('SELL_MOVIE_NO_MONEY should not be called')
                self.resetFisherman()
            return

    def b_completeSale(self, sell):
        self.sendUpdate('completeSale', [sell])

    def b_requestRepair(self, durability):
        self.sendUpdate('requestRepair', [durability])

    def b_requestUpgrade(self, upgradeType):
        self.sendUpdate('requestUpgrade', [upgradeType])

    def b_buyBait(self, bait, count):
        self.sendUpdate('buyBait', [bait, count])

    def popupGUI(self):
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(aspect2d)
        self.timer.posInTopRightCorner()
        self.timer.countdown(self.remain)
        self.gui = FishermanGUI(self.b_completeSale, self.b_requestRepair, self.b_requestUpgrade, self.b_buyBait, (-0.45, 0, 0))
        self.gui.load()
        self.gui.enter()