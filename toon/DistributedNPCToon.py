# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.DistributedNPCToon
from panda3d.core import Camera
from direct.interval.IntervalGlobal import *
import time
from DistributedNPCToonBase import *
from toontown.hood import ZoneUtil
from otp.nametag.NametagConstants import *
from toontown.quest import QuestChoiceGui
from toontown.quest import TrackChoiceGui
from toontown.toonbase import TTLocalizer
from toontown.minigame import ClerkPurchase
ChoiceTimeout = 20

class DistributedNPCToon(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.curQuestMovie = None
        self.questChoiceGui = None
        self.trackChoiceGui = None
        self.purchaseGui = None
        self.cameraLerp = None
        return

    def allowedToTalk(self):
        return True

    def delayDelete(self):
        DistributedNPCToonBase.delayDelete(self)
        if self.curQuestMovie:
            curQuestMovie = self.curQuestMovie
            self.curQuestMovie = None
            curQuestMovie.timeout(fFinish=1)
            curQuestMovie.cleanup()
        return

    def disable(self):
        self.cleanupMovie()
        DistributedNPCToonBase.disable(self)

    def cleanupMovie(self):
        self.clearChat()
        self.ignore('chooseQuest')
        if self.questChoiceGui:
            self.questChoiceGui.destroy()
            self.questChoiceGui = None
        self.ignore(self.uniqueName('doneChatPage'))
        if self.curQuestMovie:
            self.curQuestMovie.timeout(fFinish=1)
            self.curQuestMovie.cleanup()
            self.curQuestMovie = None
        if self.trackChoiceGui:
            self.trackChoiceGui.destroy()
            self.trackChoiceGui = None
        if self.purchaseGui:
            self.purchaseGui.exit()
            self.purchaseGui.unload()
            self.purchaseGui = None
        if self.cameraLerp:
            self.cameraLerp.pause()
            self.cameraLerp = None
        return

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('quest', [self])
        self.sendUpdate('avatarEnter', [])
        self.nametag3d.setDepthTest(0)
        self.nametag3d.setBin('fixed', 0)

    def finishMovie(self, av, isLocalToon, elapsedTime = None):
        self.cleanupMovie()
        av.startLookAround()
        self.startLookAround()
        self.detectAvatars()
        if isLocalToon:
            self.showNametag2d()
            self.neutralizeCamera()
            self.sendUpdate('setMovieDone', [])
            self.nametag3d.clearDepthTest()
            self.nametag3d.clearBin()

    def neutralizeCamera(self):
        avHeight = max(base.localAvatar.getHeight(), 3.0)
        scaleFactor = avHeight * 0.33
        Sequence(Func(camera.wrtReparentTo, base.localAvatar), camera.posQuatInterval(1, (0, -9 * scaleFactor, avHeight), (0, 0, 0), other=base.localAvatar, blendType='easeOut'), Func(base.cr.playGame.getPlace().setState, 'walk')).start()

    def setupCamera(self, mode):
        camera.wrtReparentTo(render)
        if mode == NPCToons.QUEST_MOVIE_QUEST_CHOICE or mode == NPCToons.QUEST_MOVIE_TRACK_CHOICE:
            camera.posQuatInterval(1, (5, 9, self.getHeight() - 0.5), (155, -2, 0), other=self, blendType='easeOut').start()
        else:
            camera.posQuatInterval(1, (-5, 9, self.getHeight() - 0.5), (-150, -2, 0), other=self, blendType='easeOut').start()

    def setMovie(self, mode, npcId, avId, quests, timestamp):
        isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.QUEST_MOVIE_CLEAR:
            self.cleanupMovie()
            if isLocalToon:
                self.neutralizeCamera()
            return
        elif mode == NPCToons.QUEST_MOVIE_TIMEOUT:
            self.cleanupMovie()
            if isLocalToon:
                self.neutralizeCamera()
            self.setPageNumber(0, -1)
            self.clearChat()
            self.startLookAround()
            self.detectAvatars()
            return
        else:
            av = base.cr.doId2do.get(avId)
            if av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            elif mode == NPCToons.QUEST_MOVIE_REJECT:
                rejectString = Quests.chooseQuestDialogReject()
                rejectString = Quests.fillInQuestNames(rejectString, avName=av.name)
                self.setChatAbsolute(rejectString, CFSpeech | CFTimeout)
                if isLocalToon:
                    base.cr.playGame.getPlace().setState('walk')
                return
            elif mode == NPCToons.QUEST_MOVIE_TIER_NOT_DONE:
                rejectString = Quests.chooseQuestDialogTierNotDone()
                rejectString = Quests.fillInQuestNames(rejectString, avName=av.name)
                self.setChatAbsolute(rejectString, CFSpeech | CFTimeout)
                if isLocalToon:
                    self.neutralizeCamera()
                return
            self.setupAvatars(av)
            fullString = ''
            toNpcId = None
            if isLocalToon:
                self.hideNametag2d()
            if mode == NPCToons.QUEST_MOVIE_COMPLETE:
                questId, rewardId, toNpcId = quests
                if isLocalToon:
                    self.setupCamera(mode)
                greetingString = Quests.chooseQuestDialog(questId, Quests.GREETING)
                if greetingString:
                    fullString += greetingString + '\x07'
                fullString += Quests.chooseQuestDialog(questId, Quests.COMPLETE) + '\x07'
                if rewardId:
                    fullString += Quests.getReward(rewardId).getString()
                leavingString = Quests.chooseQuestDialog(questId, Quests.LEAVING)
                if leavingString:
                    fullString += '\x07' + leavingString
            elif mode == NPCToons.QUEST_MOVIE_QUEST_CHOICE_CANCEL:
                fullString = TTLocalizer.QuestMovieQuestChoiceCancel
            elif mode == NPCToons.QUEST_MOVIE_TRACK_CHOICE_CANCEL:
                fullString = TTLocalizer.QuestMovieTrackChoiceCancel
            elif mode == NPCToons.QUEST_MOVIE_INCOMPLETE:
                questId, completeStatus, toNpcId = quests
                if isLocalToon:
                    self.setupCamera(mode)
                greetingString = Quests.chooseQuestDialog(questId, Quests.GREETING)
                if greetingString:
                    fullString += greetingString + '\x07'
                fullString += Quests.chooseQuestDialog(questId, completeStatus)
                leavingString = Quests.chooseQuestDialog(questId, Quests.LEAVING)
                if leavingString:
                    fullString += '\x07' + leavingString
            elif mode == NPCToons.QUEST_MOVIE_ASSIGN:
                questId, rewardId, toNpcId = quests
                if isLocalToon:
                    self.setupCamera(mode)
                fullString += Quests.chooseQuestDialog(questId, Quests.QUEST)
                leavingString = Quests.chooseQuestDialog(questId, Quests.LEAVING)
                if leavingString:
                    fullString += '\x07' + leavingString
            else:
                if mode == NPCToons.QUEST_MOVIE_QUEST_CHOICE:
                    if isLocalToon:
                        self.setupCamera(mode)
                    self.setChatAbsolute(TTLocalizer.QuestMovieQuestChoice, CFSpeech)
                    if isLocalToon:
                        self.acceptOnce('chooseQuest', self.sendChooseQuest)
                        self.questChoiceGui = QuestChoiceGui.QuestChoiceGui()
                        self.questChoiceGui.setQuests(quests, npcId, ChoiceTimeout)
                    return
                if mode == NPCToons.QUEST_MOVIE_TRACK_CHOICE:
                    if isLocalToon:
                        self.setupCamera(mode)
                    self.setChatAbsolute(TTLocalizer.QuestMovieTrackChoice, CFSpeech)
                    if isLocalToon:
                        self.acceptOnce('chooseTrack', self.sendChooseTrack)
                        self.trackChoiceGui = TrackChoiceGui.TrackChoiceGui(ChoiceTimeout)
                    return
                if mode == NPCToons.QUEST_MOVIE_RESCUED:
                    if isLocalToon:
                        self.cameraLerp = Sequence(Func(camera.wrtReparentTo, render), camera.posQuatInterval(1, (-5, 9, self.getHeight() - 0.5), (-150, -2, 0), other=self, blendType='easeOut'), Func(self.popupPurchaseGUI))
                        self.cameraLerp.start()
                    self.setChatAbsolute(TTLocalizer.STOREOWNER_RESCUED, CFSpeech)
                    return
            fullString = Quests.fillInQuestNames(fullString, avName=av.name, fromNpcId=npcId, toNpcId=toNpcId)
            self.acceptOnce(self.uniqueName('doneChatPage'), self.finishMovie, extraArgs=[av, isLocalToon])
            self.clearChat()
            self.setPageChat(avId, 0, fullString, 1)
            return

    def sendChooseQuest(self, questId):
        if self.questChoiceGui:
            self.questChoiceGui.destroy()
            self.questChoiceGui = None
        self.sendUpdate('chooseQuest', [questId])
        return

    def sendChooseTrack(self, trackId):
        if self.trackChoiceGui:
            self.trackChoiceGui.destroy()
            self.trackChoiceGui = None
        self.sendUpdate('chooseTrack', [trackId])
        return

    def d_setInventory(self, inventory, money):
        self.sendUpdate('setInventory', [inventory, money])

    def popupPurchaseGUI(self):
        self.acceptOnce('purchaseClerkDone', self.__handlePurchaseDone)
        self.purchaseGui = ClerkPurchase.ClerkPurchase(base.localAvatar, NPCToons.CLERK_COUNTDOWN_TIME, 'purchaseClerkDone')
        self.purchaseGui.load()
        self.purchaseGui.enter()

    def __handlePurchaseDone(self, state):
        self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)
        self.d_setInventory(base.localAvatar.inventory.makeNetString(), base.localAvatar.getMoney())
        self.finishMovie(base.localAvatar, True)