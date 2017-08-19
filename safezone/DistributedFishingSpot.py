# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.safezone.DistributedFishingSpot
from panda3d.core import BoundingSphere, CollideMask, CollisionNode, CollisionSphere, NodePath, Point3, TextNode, VBase3, Vec4, deg2Rad, rad2Deg
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.directtools.DirectGeometry import LineNodePath
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.fishing import FishGlobals
from toontown.shtiker import FishPage
from toontown.toonbase import TTLocalizer
from toontown.quest import Quests
from direct.actor import Actor
from direct.showutil import Rope
import math
from direct.task.Task import Task
import random
import sys
from toontown.fishing import FishingTargetGlobals
from toontown.fishing import FishBase
from toontown.fishing import FishPanel
from toontown.effects import Ripples
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownTimer
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.toontowngui.DirectHealthBar import DirectHealthBar

class DistributedFishingSpot(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFishingSpot')
    vZeroMax = 25.0
    angleMax = 30.0

    def __init__(self, cr):
        if hasattr(self, 'fishInit'):
            return
        else:
            self.fishInit = 1
            DistributedObject.DistributedObject.__init__(self, cr)
            self.lastAvId = 0
            self.lastFrame = 0
            self.avId = 0
            self.av = None
            self.placedAvatar = 0
            self.localToonFishing = 0
            self.nodePath = None
            self.collSphere = None
            self.collNode = None
            self.collNodePath = None
            self.castTrack = None
            self.pond = None
            self.guiTrack = None
            self.madeGui = 0
            self.castGui = None
            self.itemGui = None
            self.durabilityBar = None
            self.pole = None
            self.line = None
            self.poleNode = []
            self.ptop = None
            self.bob = None
            self.bobBobTask = None
            self.splashSounds = None
            self.ripples = None
            self.line = None
            self.lineSphere = None
            self.power = 0.0
            self.startAngleNP = 0
            self.firstCast = 1
            self.fishPanel = None
            self.baitDisabled = False
            self.fsm = ClassicFSM.ClassicFSM('DistributedFishingSpot', [State.State('off', self.enterOff, self.exitOff, ['waiting',
              'distCasting',
              'fishing',
              'reward',
              'failure',
              'leaving']),
             State.State('waiting', self.enterWaiting, self.exitWaiting, ['localAdjusting',
              'distCasting',
              'leaving',
              'sellFish']),
             State.State('localAdjusting', self.enterLocalAdjusting, self.exitLocalAdjusting, ['localCasting', 'leaving']),
             State.State('localCasting', self.enterLocalCasting, self.exitLocalCasting, ['localAdjusting', 'fishing', 'leaving']),
             State.State('distCasting', self.enterDistCasting, self.exitDistCasting, ['fishing',
              'leaving',
              'reward',
              'failure',
              'distCasting']),
             State.State('fishing', self.enterFishing, self.exitFishing, ['localAdjusting',
              'distCasting',
              'waitForAI',
              'reward',
              'failure',
              'leaving']),
             State.State('sellFish', self.enterSellFish, self.exitSellFish, ['waiting', 'leaving']),
             State.State('waitForAI', self.enterWaitForAI, self.exitWaitForAI, ['reward', 'failure', 'leaving']),
             State.State('reward', self.enterReward, self.exitReward, ['localAdjusting',
              'distCasting',
              'leaving',
              'sellFish']),
             State.State('failure', self.enterFailure, self.exitFailure, ['localAdjusting',
              'distCasting',
              'leaving',
              'sellFish']),
             State.State('leaving', self.enterLeaving, self.exitLeaving, [])], 'off', 'off')
            self.fsm.enterInitialState()
            return

    def disable(self):
        self.ignore(self.uniqueName('enterFishingSpotSphere'))
        self.setOccupied(0)
        self.avId = 0
        if self.castTrack != None:
            if self.castTrack.isPlaying():
                self.castTrack.finish()
            self.castTrack = None
        if self.guiTrack != None:
            if self.guiTrack.isPlaying():
                self.guiTrack.finish()
            self.guiTrack = None
        self.__hideBob()
        self.nodePath.detachNode()
        self.__unmakeGui()
        self.pond.stopCheckingTargets()
        self.pond = None
        for event in self.getAllAccepting():
            if event.startswith('generate-'):
                self.ignore(event)

        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        if hasattr(self, 'fishDeleted'):
            return
        self.fishDeleted = 1
        del self.pond
        del self.fsm
        if self.nodePath:
            self.nodePath.removeNode()
            del self.nodePath
        DistributedObject.DistributedObject.delete(self)
        if self.ripples:
            self.ripples.destroy()

    def generateInit(self):
        DistributedObject.DistributedObject.generateInit(self)
        self.nodePath = NodePath(self.uniqueName('FishingSpot'))
        self.angleNP = self.nodePath.attachNewNode(self.uniqueName('FishingSpotAngleNP'))
        self.collSphere = CollisionSphere(0, 0, 0, self.getSphereRadius())
        self.collSphere.setTangible(0)
        self.collNode = CollisionNode(self.uniqueName('FishingSpotSphere'))
        self.collNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.nodePath.attachNewNode(self.collNode)
        self.bobStartPos = Point3(0.0, 3.0, 8.5)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.nodePath.reparentTo(self.getParentNodePath())
        self.accept(self.uniqueName('enterFishingSpotSphere'), self.__handleEnterSphere)

    def setPondDoId(self, pondDoId):
        self.pondDoId = pondDoId
        if pondDoId in self.cr.doId2do:
            self.setPond(self.cr.doId2do[pondDoId])
        else:
            self.acceptOnce('generate-%d' % pondDoId, self.setPond)

    def setPond(self, pond):
        self.pond = pond
        self.area = self.pond.getArea()
        self.waterLevel = FishingTargetGlobals.getWaterLevel(self.area)

    def __handleEnterSphere(self, collEntry):
        if base.localAvatar.doId == self.lastAvId and globalClock.getFrameCount() <= self.lastFrame + 1:
            self.notify.debug('Ignoring duplicate entry for avatar.')
            return
        if base.localAvatar.hp > 0 and base.cr.playGame.getPlace().fsm.getCurrentState().getName() != 'fishing':
            self.cr.playGame.getPlace().detectedFishingCollision()
            self.d_requestEnter()

    def d_requestEnter(self):
        self.sendUpdate('requestEnter', [])

    def rejectEnter(self):
        self.cr.playGame.getPlace().setState('walk')

    def d_requestExit(self):
        self.sendUpdate('requestExit', [])

    def d_doCast(self, power, heading):
        self.sendUpdate('doCast', [power, heading])

    def getSphereRadius(self):
        return 1.5

    def getParentNodePath(self):
        return render

    def setPosHpr(self, x, y, z, h, p, r):
        self.nodePath.setPosHpr(x, y, z, h, p, r)
        self.angleNP.setH(render, self.nodePath.getH(render))

    def setOccupied(self, avId):
        if avId and avId not in self.cr.doId2do:

            def tryAgain(av):

                def reposition(task):
                    self.setOccupied(avId)
                    return task.done

                taskMgr.doMethodLater(0.1, reposition, self.uniqueName('reposition'))

            self.acceptOnce('generate-%d' % avId, tryAgain)
            return
        else:
            if self.av != None:
                if not self.av.isEmpty():
                    self.__dropPole()
                    self.av.loop('neutral')
                    self.av.setParent(ToontownGlobals.SPRender)
                    self.av.startSmooth()
                self.ignore(self.av.uniqueName('disable'))
                self.__hideBob()
                self.fsm.requestFinalState()
                self.__removePole()
                self.av = None
                self.placedAvatar = 0
                self.angleNP.setH(render, self.nodePath.getH(render))
            self.__hideLine()
            wasLocalToon = self.localToonFishing
            self.lastAvId = self.avId
            self.lastFrame = globalClock.getFrameCount()
            self.avId = avId
            self.localToonFishing = 0
            if self.avId == 0:
                self.collSphere.setTangible(0)
            else:
                self.collSphere.setTangible(1)
                if self.avId == base.localAvatar.doId:
                    base.setCellsAvailable(base.bottomCells, 0)
                    self.localToonFishing = 1
                    if base.wantBingo:
                        self.pond.setLocalToonSpot(self)
                self.av = self.cr.doId2do.get(self.avId)
                self.__loadStuff()
                self.placedAvatar = 0
                self.firstCast = 1
                self.acceptOnce(self.av.uniqueName('disable'), self.__avatarGone)
                self.av.stopSmooth()
                self.av.wrtReparentTo(self.angleNP)
                self.av.setAnimState('neutral', 1.0)
                self.createCastTrack()
            if wasLocalToon and not self.localToonFishing:
                self.__hideCastGui()
                if base.wantBingo:
                    self.pond.setLocalToonSpot()
                base.setCellsAvailable([base.bottomCells[1], base.bottomCells[2]], 1)
                base.setCellsAvailable(base.rightCells, 1)
                place = base.cr.playGame.getPlace()
                if place:
                    place.setState('walk')
            return

    def __avatarGone(self):
        self.setOccupied(0)

    def setMovie(self, mode, code, itemDesc1, itemDesc2, itemDesc3, power, h):
        if self.av == None:
            return
        else:
            if mode == FishGlobals.NoMovie:
                pass
            elif mode == FishGlobals.EnterMovie:
                self.fsm.request('waiting')
            elif mode == FishGlobals.ExitMovie:
                self.fsm.request('leaving')
            elif mode == FishGlobals.CastMovie:
                if not self.localToonFishing:
                    self.fsm.request('distCasting', [power, h])
            elif mode == FishGlobals.PullInMovie:
                self.fsm.request('reward', [code,
                 itemDesc1,
                 itemDesc2,
                 itemDesc3])
            elif mode == FishGlobals.FailureMovie:
                if not self.localToonFishing:
                    self.fsm.request('failure')
            return

    def getStareAtNodeAndOffset(self):
        return (self.nodePath, Point3())

    def __loadStuff(self):
        rodId = self.av.getFishingRod()
        rodPath = FishGlobals.RodFileDict.get(rodId)
        if not rodPath:
            self.notify.warning('Rod id: %s model not found' % rodId)
            rodPath = RodFileDict[0]
        self.pole = Actor.Actor()
        self.pole.loadModel(rodPath)
        self.pole.loadAnims({'cast': 'phase_4/models/props/fishing-pole-chan'})
        self.pole.pose('cast', 0)
        if settings['smoothAnimations']:
            self.pole.setBlend(frameBlend=True)
        self.ptop = self.pole.find('**/joint_attachBill')
        if self.line == None:
            self.line = Rope.Rope(self.uniqueName('Line'))
            self.line.setTransparency(1)
            self.lineSphere = BoundingSphere(Point3(-0.6, -2, -5), 5.5)
        if self.bob == None:
            self.bob = loader.loadModel('phase_4/models/props/fishing_bob')
            self.bob.setScale(1.5)
            self.ripples = Ripples.Ripples(self.nodePath)
            self.ripples.setScale(0.4)
            self.ripples.hide()
        r, g, b = FishGlobals.Lure2Color[self.av.getFishingLure()]
        self.line.setColor(r, g, b, 0.4)
        r, g, b, a = FishGlobals.Fish2Color[self.av.getFishingBait()]
        self.bob.setColor(r, g, b, 1)
        if self.splashSounds == None:
            self.splashSounds = (loader.loadSfx('phase_4/audio/sfx/TT_splash1.ogg'), loader.loadSfx('phase_4/audio/sfx/TT_splash2.ogg'))
        self.__setFishingRodDurability()
        return

    def __placeAvatar(self):
        if not self.placedAvatar:
            self.placedAvatar = 1
            self.__holdPole()
            self.av.setPosHpr(0, 0, 0, 0, 0, 0)

    def __holdPole(self):
        if self.poleNode != []:
            self.__dropPole()
        np = NodePath('pole-holder')
        self.poleNode.append(np.instanceTo(self.av.getRightHand()))
        self.pole.reparentTo(self.poleNode[0])

    def __dropPole(self):
        self.__hideBob()
        self.__hideLine()
        if self.pole != None:
            self.pole.clearMat()
            self.pole.detachNode()
        for pn in self.poleNode:
            pn.removeNode()

        self.poleNode = []
        return

    def __removePole(self):
        self.pole.cleanup()
        self.pole.removeNode()
        self.poleNode = []
        self.ptop.removeNode()
        self.pole = None
        self.ptop = None
        return

    def __showLineWaiting(self):
        self.line.setup(4, ((None, (0, 0, 0)),
         (None, (0, -2, -4)),
         (self.bob, (0, -1, 0)),
         (self.bob, (0, 0, 0))))
        self.line.ropeNode.setBounds(self.lineSphere)
        self.line.reparentTo(self.ptop)
        return

    def __showLineCasting(self):
        self.line.setup(2, ((None, (0, 0, 0)), (self.bob, (0, 0, 0))))
        self.line.ropeNode.setBounds(self.lineSphere)
        self.line.reparentTo(self.ptop)
        return

    def __showLineReeling(self):
        self.line.setup(2, ((None, (0, 0, 0)), (self.bob, (0, 0, 0))))
        self.line.ropeNode.setBounds(self.lineSphere)
        self.line.reparentTo(self.ptop)
        return

    def __hideLine(self):
        if self.line:
            self.line.detachNode()

    def __showBobFloat(self):
        self.__hideBob()
        self.bob.reparentTo(self.angleNP)
        self.ripples.reparentTo(self.angleNP)
        self.ripples.setPos(self.bob.getPos())
        self.ripples.setZ(self.waterLevel + 0.025)
        self.ripples.play()
        splashSound = random.choice(self.splashSounds)
        base.playSfx(splashSound, volume=0.8, node=self.bob)
        self.bobBobTask = taskMgr.add(self.__doBobBob, self.taskName('bob'))

    def __hideBob(self):
        if self.bob:
            self.bob.detachNode()
        if self.bobBobTask:
            taskMgr.remove(self.bobBobTask)
            self.bobBobTask = None
        if self.ripples:
            self.ripples.stop()
            self.ripples.detachNode()
        return

    def __doBobBob(self, task):
        z = math.sin(task.time * 1.8) * 0.08
        self.bob.setZ(self.waterLevel + z)
        return Task.cont

    def __userExit(self, event = None):
        if self.localToonFishing:
            self.fsm.request('leaving')
            self.d_requestExit()

    def __sellFish(self, result = None):
        if self.localToonFishing:
            if result == DGG.DIALOG_OK:
                self.sendUpdate('sellFish', [])
                for button in self.sellFishDialog.buttonList:
                    button['state'] = DGG.DISABLED

            else:
                self.fsm.request('leaving')
                self.d_requestExit()

    def __sellFishConfirm(self, result = None):
        if self.localToonFishing:
            self.fsm.request('waiting', [False])

    def __requestFishReel(self, _ = None):
        if self.fsm.getCurrentState().getName() != 'fishing':
            return
        if self.pond.currentTarget:
            messenger.send('hitFishingTarget')
        else:
            self.__showHowTo(TTLocalizer.FishingNoFish)
            self.fsm.request('failure')
            self.sendUpdate('handleFailure', [])

    def __showCastGui(self):
        self.__hideCastGui()
        self.__makeGui()
        self.castButton.show()
        self.arrow.hide()
        self.exitButton.show()
        self.timer.show()
        self.__updateFishTankGui()
        self.__refreshFishingBait()
        self.__setFishingRodDurability()
        self.castGui.reparentTo(aspect2d)
        self.castButton['state'] = DGG.NORMAL
        self.jar['text'] = str(self.av.getMoney())
        self.accept(localAvatar.uniqueName('moneyChange'), self.__moneyChange)
        self.accept(localAvatar.uniqueName('fishTankChange'), self.__updateFishTankGui)
        target = base.cr.doFind('DistributedTarget')
        if target:
            target.hideGui()
        if base.wantBingo:
            self.__setBingoCastGui()

        def requestLocalAdjusting(mouseEvent):
            if self.av.isFishTankFull() and self.__allowSellFish():
                self.fsm.request('sellFish')
            else:
                self.fsm.request('localAdjusting')

        def requestLocalCasting(mouseEvent):
            if self.fsm.getCurrentState().getName() == 'localAdjusting' and not (self.av.isFishTankFull() and self.__allowSellFish()):
                self.fsm.request('localCasting')

        self.castButton.bind(DGG.B1PRESS, requestLocalAdjusting)
        self.castButton.bind(DGG.B3PRESS, self.__requestFishReel)
        self.castButton.bind(DGG.B1RELEASE, requestLocalCasting)
        self.castButton.bind(DGG.B3RELEASE, requestLocalCasting)
        self.accept('touchDoubleTap', self.__requestFishReel)
        if self.firstCast and len(self.av.fishCollection) == 0 and len(self.av.fishTank) == 0:
            self.__showHowTo(TTLocalizer.FishingHowToFirstTime)
        elif base.wantBingo and self.pond.hasPondBingoManager() and not self.av.fishBingoTutorialDone:
            self.__showHowTo(TTLocalizer.FishBingoHelpMain)
            self.av.b_setFishBingoTutorialDone(True)

    def __moneyChange(self, money):
        self.jar['text'] = str(money)

    def __initCastGui(self):
        self.timer.countdown(FishGlobals.CastTimeout)

    def __showQuestItem(self, itemId):
        self.__makeGui()
        itemName = Quests.getItemName(itemId)
        self.itemLabel['text'] = itemName
        self.itemGui.reparentTo(aspect2d)
        self.itemPackage.show()
        self.itemJellybean.hide()
        self.itemBoot.hide()

    def __showBootItem(self):
        self.__makeGui()
        itemName = TTLocalizer.FishingBootItem
        self.itemLabel['text'] = itemName
        self.itemGui.reparentTo(aspect2d)
        self.itemBoot.show()
        self.itemJellybean.hide()
        self.itemPackage.hide()

    def __setItemLabel(self):
        if self.pond.hasPondBingoManager():
            self.itemLabel['text'] = str(itemName + '\n\n' + 'BINGO WILDCARD')
        else:
            self.itemLabel['text'] = itemName

    def __showJellybeanItem(self, amount):
        self.__makeGui()
        itemName = TTLocalizer.FishingJellybeanItem % amount
        self.itemLabel['text'] = itemName
        self.itemGui.reparentTo(aspect2d)
        self.jar['text'] = str(self.av.getMoney())
        self.itemJellybean.show()
        self.itemBoot.hide()
        self.itemPackage.hide()

    def __showFishItem(self, code, fish):
        self.fishPanel = FishPanel.FishPanel(fish)
        self.__setFishItemPos()
        self.fishPanel.setSwimBounds(-0.3, 0.3, -0.235, 0.25)
        self.fishPanel.setSwimColor(1.0, 1.0, 0.74901, 1.0)
        self.fishPanel.load(True)
        self.fishPanel.show(code)
        self.__updateFishTankGui()

    def __setFishItemPos(self):
        if base.wantBingo and self.pond.hasPondBingoManager():
            self.fishPanel.setPos(0.65, 0, 0.35)
        else:
            self.fishPanel.setPos(0, 0, 0.35)

    def __updateFishTankGui(self):
        fishTank = self.av.getFishTank()
        lenFishTank = len(fishTank)
        maxFishTank = self.av.getMaxFishTank()
        self.bucket['text'] = '%s/%s' % (lenFishTank, maxFishTank)

    def __showFailureReason(self, code):
        self.__makeGui()
        reason = ''
        if code == FishGlobals.OverTankLimit:
            reason = TTLocalizer.FishingOverTankLimit
        elif code == FishGlobals.RodBroken:
            reason = TTLocalizer.FishingRodBroken
        self.failureDialog.setMessage(reason)
        self.failureDialog.show()

    def __showSellFishDialog(self):
        self.__makeGui()
        self.sellFishDialog.show()

    def __hideSellFishDialog(self):
        self.__makeGui()
        self.sellFishDialog.hide()

    def __showSellFishConfirmDialog(self, numFishCaught):
        self.__makeGui()
        msg = TTLocalizer.STOREOWNER_TROPHY % (numFishCaught, FishGlobals.getTotalNumFish())
        self.sellFishConfirmDialog.setMessage(msg)
        self.sellFishConfirmDialog.show()

    def __hideSellFishConfirmDialog(self):
        self.__makeGui()
        self.sellFishConfirmDialog.hide()

    def __showBroke(self):
        self.__makeGui()
        self.brokeDialog.show()
        self.castButton['state'] = DGG.DISABLED

    def __showHowTo(self, message):
        self.__makeGui()
        self.howToLabel['text'] = message
        self.howToLabel.resetFrameSize()
        self.howToLabel.show()

    def __hideHowTo(self, event = None):
        self.__makeGui()
        self.howToLabel.hide()

    def __showFishTankFull(self):
        self.__makeGui()
        self.__showFailureReason(FishGlobals.OverTankLimit)
        self.castButton['state'] = DGG.DISABLED

    def __showFishingRodBroken(self):
        self.__makeGui()
        self.__showFailureReason(FishGlobals.RodBroken)
        self.castButton['state'] = DGG.DISABLED

    def __hideCastGui(self):
        target = base.cr.doFind('DistributedTarget')
        if target:
            target.showGui()
        if self.madeGui:
            self.timer.hide()
            self.castGui.detachNode()
            self.itemGui.detachNode()
            self.failureDialog.hide()
            self.sellFishDialog.hide()
            self.sellFishConfirmDialog.hide()
            self.brokeDialog.hide()
            self.howToLabel.hide()
            self.exitButton.hide()
            self.castButton.unbind(DGG.B1PRESS)
            self.castButton.unbind(DGG.B3PRESS)
            self.castButton.unbind(DGG.B1RELEASE)
            self.castButton.unbind(DGG.B3RELEASE)
            self.ignore('touchDoubleTap')
            self.ignore(localAvatar.uniqueName('moneyChange'))
            self.ignore(localAvatar.uniqueName('fishTankChange'))

    def __itemGuiClose(self):
        self.itemGui.detachNode()

    def __makeGui(self):
        if self.madeGui:
            return
        else:
            self.timer = ToontownTimer.ToontownTimer()
            self.timer.posInTopRightCorner()
            self.timer.hide()
            self.castGui = loader.loadModel('phase_4/models/gui/fishingGui')
            self.castGui.setBin('background', 10)
            self.castGui.setScale(0.67)
            self.castGui.setPos(0, 1, 0)
            for nodeName in ('bucket', 'jar', 'display_bucket', 'display_jar'):
                self.castGui.find('**/' + nodeName).reparentTo(self.castGui)

            self.exitButton = DirectButton(parent=base.a2dBottomRight, relief=None, text=('', TTLocalizer.FishingExit, TTLocalizer.FishingExit), text_align=TextNode.ACenter, text_scale=0.1, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(0.0, -0.12), pos=(-0.218, 0, 0.11), scale=0.8, textMayChange=0, image=(self.castGui.find('**/exit_buttonUp'), self.castGui.find('**/exit_buttonDown'), self.castGui.find('**/exit_buttonRollover')), command=self.__userExit)
            self.castGui.find('**/exitButton').removeNode()
            self.castButton = DirectButton(parent=self.castGui, relief=None, text=TTLocalizer.FishingCast, text_align=TextNode.ACenter, text_scale=(3, 2.25, 2.25), text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(0, -4), image=self.castGui.find('**/castButton'), image0_color=(1, 0, 0, 1), image1_color=(0, 1, 0, 1), image2_color=(1, 1, 0, 1), image3_color=(0.8, 0.5, 0.5, 1), pos=(0, -0.05, -0.666), scale=(0.036, 1, 0.048))
            self.castGui.find('**/castButton').removeNode()
            self.arrow = self.castGui.find('**/arrow')
            self.arrowTip = self.arrow.find('**/arrowTip')
            self.arrowTail = self.arrow.find('**/arrowTail')
            self.arrow.reparentTo(self.castGui)
            self.arrow.setColorScale(0.9, 0.9, 0.1, 0.7)
            self.arrow.hide()
            self.jar = DirectLabel(parent=self.castGui, relief=None, text=str(self.av.getMoney()), text_scale=0.16, text_fg=(0.95, 0.95, 0, 1), text_font=ToontownGlobals.getSignFont(), pos=(-1.12, 0, -1.3))
            self.bucket = DirectLabel(parent=self.castGui, relief=None, text='', text_scale=0.09, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), pos=(1.14, 0, -1.33))
            self.__updateFishTankGui()
            self.itemGui = NodePath('itemGui')
            self.itemFrame = DirectFrame(parent=self.itemGui, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(1, 1, 0.6), text=TTLocalizer.FishingItemFound, text_pos=(0, 0.2), text_scale=0.08, pos=(0, 0, 0.587))
            self.itemLabel = DirectLabel(parent=self.itemFrame, text='', text_scale=0.06, pos=(0, 0, -0.25))
            buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
            self.itemGuiCloseButton = DirectButton(parent=self.itemFrame, pos=(0.44, 0, -0.24), relief=None, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), image_scale=(0.7, 1, 0.7), command=self.__itemGuiClose)
            buttons.removeNode()
            jarGui = loader.loadModel('phase_3.5/models/gui/jar_gui')
            bootGui = loader.loadModel('phase_4/models/gui/fishing_boot')
            packageGui = loader.loadModel('phase_3.5/models/gui/stickerbook_gui').find('**/package')
            self.itemJellybean = DirectFrame(parent=self.itemFrame, relief=None, image=jarGui, scale=0.5)
            self.itemBoot = DirectFrame(parent=self.itemFrame, relief=None, image=bootGui, scale=0.2)
            self.itemPackage = DirectFrame(parent=self.itemFrame, relief=None, image=packageGui, scale=0.25)
            self.itemJellybean.hide()
            self.itemBoot.hide()
            self.itemPackage.hide()
            self.failureDialog = TTDialog.TTGlobalDialog(dialogName=self.uniqueName('failureDialog'), doneEvent=self.uniqueName('failureDialog'), command=self.__userExit, message=TTLocalizer.FishingFailure, style=TTDialog.CancelOnly, cancelButtonText=TTLocalizer.FishingExit, text_wordwrap=12)
            self.failureDialog.hide()
            self.sellFishDialog = TTDialog.TTGlobalDialog(dialogName=self.uniqueName('sellFishDialog'), doneEvent=self.uniqueName('sellFishDialog'), command=self.__sellFish, message=TTLocalizer.FishBingoOfferToSellFish, style=TTDialog.YesNo)
            self.sellFishDialog.hide()
            self.sellFishConfirmDialog = TTDialog.TTGlobalDialog(dialogName=self.uniqueName('sellFishConfirmDialog'), doneEvent=self.uniqueName('sellFishConfirmDialog'), command=self.__sellFishConfirm, message=TTLocalizer.STOREOWNER_TROPHY, style=TTDialog.Acknowledge)
            self.sellFishConfirmDialog.hide()
            self.brokeDialog = TTDialog.TTGlobalDialog(dialogName=self.uniqueName('brokeDialog'), doneEvent=self.uniqueName('brokeDialog'), command=self.__userExit, message=TTLocalizer.FishingBroke, style=TTDialog.CancelOnly, cancelButtonText=TTLocalizer.FishingExit)
            self.brokeDialog.hide()
            self.howToLabel = DirectButton(self.castGui, relief=None, text='', text_scale=0.09, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_wordwrap=25, pressEffect=0, pos=(0, 0, 1.15), command=self.__hideHowTo)
            self.durabilityBar = DirectHealthBar(self.castGui, relief=DGG.SUNKEN, frameSize=(-1.2, 1.2, -0.15, 0.15), borderWidth=(0.02, 0.02), scale=0.4, text='', text_scale=0.18, text_fg=(0, 0, 0, 1), text_align=TextNode.ALeft, text_pos=(-1.16, -0.05), pos=(0, 0, -1.325))
            self.baitFrame = DirectFrame(self.castGui, relief=DGG.SUNKEN, frameColor=(0.85, 0.95, 1, 1), borderWidth=(0.01, 0.01), frameSize=(-0.84, 0.84, -0.075, 0.075), text='', text_scale=0.09, text_font=ToontownGlobals.getMinnieFont(), text_fg=(0, 0.5, 1, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, -0.035), pos=(0, 0, 1.34), scale=1.194)
            self.baitLeftButton = DirectButton(self.baitFrame, state=DGG.NORMAL, relief=None, geom=Preloaded['yellowArrow'], pos=(-0.93, 0, 0), command=self.__updateBaitIndex, extraArgs=[-1])
            self.baitRightButton = DirectButton(self.baitFrame, state=DGG.NORMAL, relief=None, geom=Preloaded['yellowArrow'], pos=(0.93, 0, 0), hpr=(180, 0, 0), command=self.__updateBaitIndex, extraArgs=[1])
            self.madeGui = 1
            self.accept('setFishingRodDurability', self.__setFishingRodDurability)
            self.accept('refreshFishingBait', self.__refreshFishingBait)
            return

    def __setFishingRodDurability(self):
        if not self.madeGui:
            return
        rod = self.av.getFishingRod()
        maxDurability = FishGlobals.Rod2Durability[rod]
        durability = self.av.getFishingRodDurability()[rod]
        self.durabilityBar['range'] = maxDurability
        self.durabilityBar['value'] = durability
        self.durabilityBar['text'] = '%s/%s %s' % (durability, maxDurability, TTLocalizer.FishingRodDurability)
        self.durabilityBar.updateColor()

    def getBait(self):
        if self.baitIndex == -1:
            return -1
        return self.av.getFishingBaits().keys()[self.baitIndex]

    def __refreshFishingBait(self):
        if not self.av:
            return
        bait = self.av.getFishingBait()
        if bait == -1:
            self.baitIndex = -1
        elif self.av.doId == base.localAvatar.doId:
            self.baitIndex = self.av.getFishingBaits().keys().index(bait)
        self.updateFishingBait(bait)

    def updateFishingBait(self, bait):
        if not self.madeGui:
            return
        if self.bob:
            r, g, b, a = FishGlobals.Fish2Color[self.av.getFishingBait()]
            self.bob.setColor(r, g, b, 1)
        baits = self.av.getFishingBaits()
        if bait == -1:
            self.baitFrame['text'] = TTLocalizer.FishingNoBait
        else:
            self.baitFrame['text'] = '\x01small\x01\x01white\x01%s\x02\x02 %s' % (baits.values()[self.baitIndex], TTLocalizer.FishGenusNames[bait])
        if not self.baitDisabled:
            self.baitLeftButton['state'] = DGG.DISABLED if self.baitIndex <= -1 else DGG.NORMAL
            self.baitRightButton['state'] = DGG.DISABLED if self.baitIndex >= len(baits) - 1 else DGG.NORMAL

    def updateFishingBaitByIndex(self):
        if self.avId == base.localAvatar.doId:
            self.updateFishingBait(self.getBait())

    def __updateBaitIndex(self, delta):
        self.baitIndex += delta
        self.updateFishingBaitByIndex()
        taskMgr.remove(self.taskName('updateBait'))
        taskMgr.doMethodLater(1.0, self.__requestBait, self.taskName('updateBait'))

    def __requestBait(self, task):
        bait = self.getBait()
        if self.av.getFishingBait() != bait:
            self.av.requestFishingBait(bait)

    def __setBingoCastGui(self):
        if self.pond.hasPondBingoManager():
            self.notify.debug('__setBingoCastGui: Has PondBing Manager %s' % self.pond.getPondBingoManager().getDoId())
            bucket = self.castGui.find('**/bucket')
            self.castGui.find('**/display_bucket').reparentTo(bucket)
            self.bucket.reparentTo(bucket)
            jar = self.castGui.find('**/jar')
            self.castGui.find('**/display_jar').reparentTo(jar)
            self.jar.reparentTo(jar)
            base.setCellsAvailable(base.rightCells, 0)
            bucket.setScale(0.9)
            bucket.setX(-1.9)
            bucket.setZ(-0.11)
            jar.setScale(0.9)
            jar.setX(-0.375)
            jar.setZ(-0.135)
        else:
            self.notify.debug('__setItemFramePos: Has No Pond Bingo Manager')
            bucket = self.castGui.find('**/bucket')
            bucket.setScale(1)
            bucket.setPos(0, 0, 0)
            jar = self.castGui.find('**/jar')
            jar.setScale(1)
            jar.setPos(0, 0, 0)

    def resetCastGui(self):
        if not self.castGui:
            return
        self.notify.debug('resetCastGui: Bingo Night Ends - resetting Gui')
        bucket = self.castGui.find('**/bucket')
        jar = self.castGui.find('**/jar')
        bucketPosInt = bucket.posInterval(5.0, Point3(0, 0, 0), startPos=bucket.getPos(), blendType='easeInOut')
        bucketScaleInt = bucket.scaleInterval(5.0, VBase3(1.0, 1.0, 1.0), startScale=bucket.getScale(), blendType='easeInOut')
        bucketTrack = Parallel(bucketPosInt, bucketScaleInt)
        jarPosInt = jar.posInterval(5.0, Point3(0, 0, 0), startPos=jar.getPos(), blendType='easeInOut')
        jarScaleInt = jar.scaleInterval(5.0, VBase3(1.0, 1.0, 1.0), startScale=jar.getScale(), blendType='easeInOut')
        jarTrack = Parallel(jarPosInt, jarScaleInt)
        self.guiTrack = Parallel(bucketTrack, jarTrack)
        self.guiTrack.start()

    def setCastGui(self):
        self.notify.debug('setCastGui: Bingo Night Starts - setting Gui')
        bucket = self.castGui.find('**/bucket')
        self.castGui.find('**/display_bucket').reparentTo(bucket)
        self.bucket.reparentTo(bucket)
        jar = self.castGui.find('**/jar')
        self.castGui.find('**/display_jar').reparentTo(jar)
        self.jar.reparentTo(jar)
        bucketPosInt = bucket.posInterval(3.0, Point3(-1.9, 0, -0.11), startPos=bucket.getPos(), blendType='easeInOut')
        bucketScaleInt = bucket.scaleInterval(3.0, VBase3(0.9, 0.9, 0.9), startScale=bucket.getScale(), blendType='easeInOut')
        bucketTrack = Parallel(bucketPosInt, bucketScaleInt)
        jarPosInt = jar.posInterval(3.0, Point3(-0.375, 0, -0.135), startPos=jar.getPos(), blendType='easeInOut')
        jarScaleInt = jar.scaleInterval(3.0, VBase3(0.9, 0.9, 0.9), startScale=jar.getScale(), blendType='easeInOut')
        jarTrack = Parallel(jarPosInt, jarScaleInt)
        self.guiTrack = Parallel(bucketTrack, jarTrack)
        self.guiTrack.start()

    def setJarAmount(self, amount):
        if self.madeGui:
            money = int(self.jar['text']) + amount
            pocketMoney = min(money, self.av.getMaxMoney())
            self.jar.setProp('text', str(pocketMoney))

    def __unmakeGui(self):
        if not self.madeGui:
            return
        self.timer.destroy()
        del self.timer
        self.exitButton.destroy()
        self.castButton.destroy()
        self.jar.destroy()
        self.bucket.destroy()
        self.itemFrame.destroy()
        self.itemGui.removeNode()
        self.failureDialog.cleanup()
        self.sellFishDialog.cleanup()
        self.sellFishConfirmDialog.cleanup()
        self.brokeDialog.cleanup()
        self.howToLabel.destroy()
        self.durabilityBar.destroy()
        self.baitFrame.destroy()
        self.baitLeftButton.destroy()
        self.baitRightButton.destroy()
        self.castGui.removeNode()
        self.madeGui = 0
        self.ignore('setFishingRodDurability')

    def localAdjustingCastTask(self, state):
        self.getMouse()
        deltaX = self.mouseX - self.initMouseX
        deltaY = self.mouseY - self.initMouseY
        if deltaY >= 0:
            if self.power == 0:
                self.arrowTail.setScale(0.075, 0.075, 0)
                self.arrow.setR(0)
            self.castTrack.pause()
            return Task.cont
        dist = math.sqrt(deltaX * deltaX + deltaY * deltaY)
        delta = dist / 0.5
        self.power = max(min(abs(delta), 1.0), 0.0)
        self.castTrack.setT(0.2 + self.power * 0.7)
        angle = rad2Deg(math.atan(deltaX / deltaY))
        if self.power < 0.25:
            angle = angle * math.pow(self.power * 4, 3)
        if delta < 0:
            angle += 180
        minAngle = -FishGlobals.FishingAngleMax
        maxAngle = FishGlobals.FishingAngleMax
        if angle < minAngle:
            self.arrow.setColorScale(1, 0, 0, 1)
            angle = minAngle
        elif angle > maxAngle:
            self.arrow.setColorScale(1, 0, 0, 1)
            angle = maxAngle
        else:
            self.arrow.setColorScale(1, 1 - math.pow(self.power, 3), 0.1, 0.7)
        self.arrowTail.setScale(0.075, 0.075, self.power * 0.2)
        self.arrow.setR(angle)
        self.angleNP.setH(-angle)
        return Task.cont

    def getMouse(self):
        if base.mouseWatcherNode.hasMouse():
            self.mouseX = base.mouseWatcherNode.getMouseX()
            self.mouseY = base.mouseWatcherNode.getMouseY()
        else:
            self.mouseX = 0
            self.mouseY = 0

    def createCastTrack(self):
        self.castTrack = Sequence(ActorInterval(self.av, 'castlong', playRate=4), ActorInterval(self.av, 'cast', startFrame=20), Func(self.av.loop, 'fish-neutral'))

    def startMoveBobTask(self):
        self.__showBob()
        taskMgr.add(self.moveBobTask, self.taskName('moveBobTask'))

    def moveBobTask(self, task):
        g = 32.2
        t = task.time
        vZero = self.power * self.vZeroMax
        angle = deg2Rad(self.power * self.angleMax)
        deltaY = vZero * math.cos(angle) * t
        deltaZ = vZero * math.sin(angle) * t - g * t * t / 2.0
        deltaPos = Point3(0, deltaY, deltaZ)
        self.bobStartPos = Point3(0.0, 3.0, 8.5)
        pos = self.bobStartPos + deltaPos
        self.bob.setPos(pos)
        if pos[2] < self.waterLevel:
            self.fsm.request('fishing')
            return Task.done
        else:
            return Task.cont

    def __showBob(self):
        self.__hideBob()
        self.bob.reparentTo(self.angleNP)
        self.bob.setPos(self.ptop, 0, 0, 0)
        self.av.update(0)

    def hitTarget(self):
        self.fsm.request('waitForAI')

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterWaiting(self, doAnimation = True):
        self.av.stopLookAround()
        self.__hideLine()
        self.track = Parallel()
        if doAnimation:
            toonTrack = Sequence(Func(self.av.setPlayRate, 1.0, 'run'), Func(self.av.loop, 'run'), LerpPosHprInterval(self.av, 1.0, Point3(0, 0, 0), Point3(0, 0, 0)), Func(self.__placeAvatar), Parallel(ActorInterval(self.av, 'pole'), Func(self.pole.pose, 'cast', 0), LerpScaleInterval(self.pole, duration=0.5, scale=1.0, startScale=0.01)), Func(self.av.loop, 'pole-neutral'))
            if self.localToonFishing:
                camera.wrtReparentTo(render)
                self.track.append(LerpPosHprInterval(nodePath=camera, other=self.av, duration=1.5, pos=Point3(0, -12, 15), hpr=VBase3(0, -38, 0), blendType='easeInOut'))
                toonTrack.append(Func(self.__showCastGui))
                toonTrack.append(Func(self.__initCastGui))
                if base.wantBingo:
                    self.__appendBingoMethod(toonTrack, self.pond.showBingoGui)
            self.track.append(toonTrack)
        elif self.localToonFishing:
            self.__showCastGui()
        self.track.start()

    def __appendBingoMethod(self, interval, callback):
        interval.append(Func(callback))

    def exitWaiting(self):
        if self.track:
            self.track.finish()
            self.track = None
        return

    def enterLocalAdjusting(self, guiEvent = None):
        if self.track:
            self.track.pause()
        if self.castTrack:
            self.castTrack.pause()
        self.power = 0.0
        self.firstCast = 0
        self.castButton['image0_color'] = Vec4(0, 1, 0, 1)
        self.castButton['text'] = ''
        self.av.stopLookAround()
        self.__hideLine()
        self.__hideBob()
        self.howToLabel.hide()
        castCost = FishGlobals.getCastCost(self.av.getFishingRod())
        if self.av.getMoney() < castCost:
            self.__hideCastGui()
            self.__showBroke()
            self.av.loop('pole-neutral')
            return
        elif self.av.isFishTankFull():
            self.__hideCastGui()
            self.__showFishTankFull()
            self.av.loop('pole-neutral')
            return
        elif self.av.getFishingRodDurability()[self.av.getFishingRod()] == 0:
            self.__hideCastGui()
            self.__showFishingRodBroken()
            self.av.loop('pole-neutral')
            return
        else:
            self.arrow.show()
            self.arrow.setColorScale(1, 1, 0, 0.7)
            self.startAngleNP = self.angleNP.getH()
            self.getMouse()
            self.initMouseX = self.mouseX
            self.initMouseY = self.mouseY
            self.__hideBob()
            self.baitLeftButton['state'] = DGG.DISABLED
            self.baitRightButton['state'] = DGG.DISABLED
            self.baitDisabled = True
            if taskMgr.remove(self.taskName('updateBait')):
                self.__requestBait(None)
            taskMgr.add(self.localAdjustingCastTask, self.taskName('adjustCastTask'))
            if base.wantBingo:
                bingoMgr = self.pond.getPondBingoManager()
                if bingoMgr:
                    bingoMgr.castingStarted()
            return

    def exitLocalAdjusting(self):
        taskMgr.remove(self.taskName('adjustCastTask'))
        self.castButton['image0_color'] = Vec4(1, 0, 0, 1)
        self.castButton['text'] = TTLocalizer.FishingCast
        self.arrow.hide()

    def enterLocalCasting(self):
        if self.power == 0.0 and len(self.av.fishCollection) == 0:
            self.__showHowTo(TTLocalizer.FishingHowToFailed)
            if self.castTrack:
                self.castTrack.pause()
            self.av.loop('pole-neutral')
            self.track = None
            return
        else:
            castCost = FishGlobals.getCastCost(self.av.getFishingRod())
            self.jar['text'] = str(max(self.av.getMoney() - castCost, 0))
            if not self.castTrack:
                self.createCastTrack()
            self.castTrack.pause()
            startT = 0.7 + (1 - self.power) * 0.3
            speed = FishGlobals.Lure2Speed[self.av.getFishingLure()]
            self.castTrack.start(startT, playRate=speed)
            self.track = Sequence(Wait(1.2 - startT * speed), Func(self.startMoveBobTask), Func(self.__showLineCasting))
            self.track.start()
            heading = self.angleNP.getH()
            self.d_doCast(self.power, heading)
            self.timer.countdown(FishGlobals.CastTimeout)
            return

    def exitLocalCasting(self):
        taskMgr.remove(self.taskName('moveBobTask'))
        if self.track:
            self.track.pause()
            self.track = None
        if self.castTrack:
            self.castTrack.pause()
        self.__hideLine()
        self.__hideBob()
        return

    def enterDistCasting(self, power, h):
        self.av.stopLookAround()
        self.__placeAvatar()
        self.__hideLine()
        self.__hideBob()
        self.angleNP.setH(h)
        self.power = power
        self.track = Parallel(Sequence(ActorInterval(self.av, 'cast'), Func(self.pole.pose, 'cast', 0), Func(self.av.loop, 'fish-neutral')), Sequence(Wait(1.0), Func(self.startMoveBobTask), Func(self.__showLineCasting)))
        self.track.start(playRate=FishGlobals.Lure2Speed[self.av.getFishingLure()])

    def exitDistCasting(self):
        if self.track:
            self.track.finish()
            self.track = None
        taskMgr.remove(self.taskName('moveBobTask'))
        self.__hideLine()
        self.__hideBob()
        return

    def enterFishing(self):
        if self.localToonFishing:
            self.track = Sequence(ActorInterval(self.av, 'cast'), Func(self.pole.pose, 'cast', 0), Func(self.av.loop, 'fish-neutral'))
            self.track.start(self.castTrack.getT())
        else:
            self.track = None
            self.av.loop('fish-neutral')
        self.__showBobFloat()
        self.__showLineWaiting()
        if self.localToonFishing:
            self.castButton['text'] = TTLocalizer.FishingCastAndReel
            self.accept('updateFishingTarget', self.__updateFishingTarget)
            self.pond.startCheckingTargets(self, self.bob.getPos(render))
        return

    def exitFishing(self):
        if self.localToonFishing:
            self.pond.stopCheckingTargets()
            self.castButton['text'] = TTLocalizer.FishingCast
            self.ignore('updateFishingTarget')
        self.baitDisabled = False
        self.updateFishingBaitByIndex()
        if self.track:
            self.track.finish()
            self.track = None
        return

    def __updateFishingTarget(self):
        if self.pond.currentTarget:
            self.castButton['text'] = TTLocalizer.FishingCastAndReelNow
            self.__hideHowTo()
        else:
            self.castButton['text'] = TTLocalizer.FishingCastAndReel

    def enterWaitForAI(self):
        self.castButton['state'] = DGG.DISABLED

    def exitWaitForAI(self):
        self.castButton['state'] = DGG.NORMAL

    def enterFailure(self):
        self.__placeAvatar()
        self.__hideBob()
        self.__hideLine()
        self.castTrack.pause()
        self.track = Sequence(self.av.actorInterval('fish-again'), Func(self.av.loop, 'pole-neutral'))
        self.track.start()

    def exitFailure(self):
        if self.track:
            self.track.finish()
            self.track = None
        return

    def enterReward(self, code, itemDesc1, itemDesc2, itemDesc3):
        self.__placeAvatar()
        self.bob.reparentTo(self.angleNP)
        self.waterLevel = FishingTargetGlobals.getWaterLevel(self.area)
        self.bob.setZ(self.waterLevel)
        self.__showLineReeling()
        self.castTrack.pause()
        if self.localToonFishing:
            self.__showCastGui()
            if code == FishGlobals.QuestItem:
                self.__showQuestItem(itemDesc1)
            elif code in (FishGlobals.FishItem, FishGlobals.FishItemNewEntry, FishGlobals.FishItemNewRecord):
                genus, species, weight = itemDesc1, itemDesc2, itemDesc3
                fish = FishBase.FishBase(genus, species, weight)
                self.__showFishItem(code, fish)
                if base.wantBingo:
                    self.pond.handleBingoCatch((genus, species))
            elif code == FishGlobals.BootItem:
                self.__showBootItem()
                if base.wantBingo:
                    self.pond.handleBingoCatch(FishGlobals.BingoBoot)
            elif code == FishGlobals.JellybeanItem:
                amount = itemDesc1
                self.__showJellybeanItem(amount)
            elif code == FishGlobals.OverTankLimit:
                self.__hideCastGui()
            else:
                self.__showFailureReason(code)
        self.track = Sequence(Parallel(ActorInterval(self.av, 'reel'), ActorInterval(self.pole, 'cast', startFrame=63, endFrame=127)), ActorInterval(self.av, 'reel-neutral'), Func(self.__hideLine), Func(self.__hideBob), ActorInterval(self.av, 'fish-again'), Func(self.av.loop, 'pole-neutral'))
        self.track.start()

    def cleanupFishPanel(self):
        if self.fishPanel:
            self.fishPanel.hide()
            self.fishPanel.destroy()
            self.fishPanel = None
        return

    def hideBootPanel(self):
        if self.madeGui and self.itemBoot:
            self.__itemGuiClose()

    def exitReward(self):
        if self.localToonFishing:
            self.itemGui.detachNode()
            self.cleanupFishPanel()
        if self.track:
            self.track.finish()
            self.track = None
        return

    def enterLeaving(self):
        if self.localToonFishing:
            self.__hideCastGui()
            if base.wantBingo:
                self.pond.cleanupBingoMgr()
        self.av.stopLookAround()
        self.av.startLookAround()
        self.__placeAvatar()
        self.__hideLine()
        self.__hideBob()
        self.track = Sequence(Parallel(ActorInterval(self.av, 'fish-end'), Func(self.pole.pose, 'cast', 0), LerpScaleInterval(self.pole, duration=0.5, scale=0.01, startScale=1.0)), Func(self.__dropPole), Func(self.av.loop, 'neutral'))
        if self.localToonFishing:
            self.track.append(Func(self.fsm.requestFinalState))
        self.track.start()

    def exitLeaving(self):
        self.track.pause()
        self.track = None
        return

    def enterSellFish(self):
        self.castButton['state'] = DGG.DISABLED
        self.__showSellFishDialog()
        self.__hideHowTo()

    def exitSellFish(self):
        self.castButton['state'] = DGG.NORMAL
        self.__hideSellFishDialog()
        self.__hideSellFishConfirmDialog()

    def sellFishComplete(self, trophyResult, numFishCaught):
        for button in self.sellFishDialog.buttonList:
            button['state'] = DGG.NORMAL

        if self.localToonFishing:
            if trophyResult:
                self.__hideSellFishDialog()
                self.__showSellFishConfirmDialog(numFishCaught)
            else:
                self.fsm.request('waiting', [False])

    def __allowSellFish(self):
        return base.wantBingo and self.pond.hasPondBingoManager()