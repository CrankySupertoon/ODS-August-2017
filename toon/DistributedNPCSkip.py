# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.DistributedNPCSkip
from panda3d.core import Camera, Point3
from direct.gui.DirectGui import *
from otp.nametag.NametagConstants import *
from otp.nametag import NametagGlobals
from toontown.toonbase import TTLocalizer
from DistributedNPCToonBase import *
from SkipGUI import SkipGUI
import NPCToons
import time

class DistributedNPCSkip(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.av = None
        self.gui = None
        self.nextCollision = 0
        return

    def disable(self):
        self.ignoreAll()
        self.destroyGui()
        self.av = None
        DistributedNPCToonBase.disable(self)
        return

    def destroyGui(self):
        if self.gui:
            self.gui.destroy()
            self.gui = None
        return

    def getCollSphereRadius(self):
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        self.currentTime = time.time()
        if self.nextCollision > self.currentTime:
            self.nextCollision = self.currentTime + 2
            return
        base.cr.playGame.getPlace().fsm.request('stopped')
        base.localAvatar.setPreventSleepWatch(True)
        self.d_setState(ToontownGlobals.CLERK_GREETING)
        self.nextCollision = self.currentTime + 2
        camera.wrtReparentTo(render)
        NametagGlobals.setMasterArrowsOn(False)
        self.cr.enableTransparentToons()
        Sequence(LerpPosQuatInterval(camera, 1, Point3(1, 8, self.getHeight()), Point3(180, -2, 0), other=self, blendType='easeInOut'), Func(self.popupGUI)).start()

    def popupGUI(self):
        self.gui = SkipGUI((-0.6, 0, 0))
        self.gui.load()
        self.gui.enter()
        self.acceptOnce('exitSkip', self.__exit)

    def __exit(self):
        NametagGlobals.setMasterArrowsOn(True)
        self.cr.disableTransparentToons()
        self.resetSkipToon()
        self.d_setState(ToontownGlobals.CLERK_GOODBYE)

    def setupAvatars(self, av):
        self.ignoreAvatars()
        av.stopLookAround()
        av.lerpLookAt(Point3(-0.5, 4, 0), time=0.5)
        self.stopLookAround()
        self.lerpLookAt(Point3(av.getPos(self)), time=0.5)

    def resetSkipToon(self):
        self.ignoreAll()
        self.destroyGui()
        self.show()
        self.startLookAround()
        self.detectAvatars()
        self.freeAvatar()
        base.localAvatar.setPreventSleepWatch(False)

    def d_setState(self, state):
        self.sendUpdate('setState', [0, state])

    def setState(self, avId, state):
        if self.gui and avId != base.localAvatar.doId:
            return
        av = base.cr.doId2do.get(avId)
        if not av:
            return
        if state == ToontownGlobals.CLERK_GOODBYE:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)
        elif state == ToontownGlobals.CLERK_GREETING:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GREETING_SKIP, CFSpeech)
        elif state == ToontownGlobals.CLERK_TOOKTOOLONG:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)