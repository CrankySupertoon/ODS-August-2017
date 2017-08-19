# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.minigame.DistributedMinigame
from panda3d.core import VBase4
from toontown.toonbase.ToonBaseGlobal import *
from direct.gui.DirectGui import *
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import MinigameRulesPanel
from direct.task.Task import Task
from toontown.toon import Toon
from direct.showbase import RandomNumGen
from toontown.toonbase import TTLocalizer
import random
import MinigameGlobals
from direct.showbase import PythonUtil
from toontown.toon import TTEmote
from otp.avatar import Emote
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs
from otp.ai.MagicWordGlobal import *

class DistributedMinigame(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMinigame')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.waitingStartLabel = DirectLabel(text=TTLocalizer.MinigameWaitingForOtherToons, text_fg=VBase4(1, 1, 1, 1), relief=None, pos=(-0.6, 0, -0.75), scale=0.075)
        self.waitingStartLabel.hide()
        self.avIdList = []
        self.remoteAvIdList = []
        self.localAvId = base.localAvatar.doId
        self.frameworkFSM = ClassicFSM.ClassicFSM('DistributedMinigame', [State.State('frameworkInit', self.enterFrameworkInit, self.exitFrameworkInit, ['frameworkRules', 'frameworkCleanup', 'frameworkAvatarExited']),
         State.State('frameworkRules', self.enterFrameworkRules, self.exitFrameworkRules, ['frameworkWaitServerStart', 'frameworkCleanup', 'frameworkAvatarExited']),
         State.State('frameworkWaitServerStart', self.enterFrameworkWaitServerStart, self.exitFrameworkWaitServerStart, ['frameworkGame', 'frameworkCleanup', 'frameworkAvatarExited']),
         State.State('frameworkGame', self.enterFrameworkGame, self.exitFrameworkGame, ['frameworkWaitServerFinish', 'frameworkCleanup', 'frameworkAvatarExited']),
         State.State('frameworkWaitServerFinish', self.enterFrameworkWaitServerFinish, self.exitFrameworkWaitServerFinish, ['frameworkCleanup']),
         State.State('frameworkAvatarExited', self.enterFrameworkAvatarExited, self.exitFrameworkAvatarExited, ['frameworkCleanup']),
         State.State('frameworkCleanup', self.enterFrameworkCleanup, self.exitFrameworkCleanup, [])], 'frameworkInit', 'frameworkCleanup')
        hoodMinigameState = self.cr.playGame.hood.fsm.getStateNamed('minigame')
        hoodMinigameState.addChild(self.frameworkFSM)
        self.rulesDoneEvent = 'rulesDone'
        self.acceptOnce('minigameAbort', self.d_requestExit)
        self.acceptOnce('minigameSkip', self.requestSkip)
        base.curMinigame = self
        self.cleanupActions = []
        self.usesSmoothing = 0
        self.usesLookAround = 0
        self.difficultyOverride = None
        self.trolleyZoneOverride = None
        self.hasLocalToon = 0
        self.frameworkFSM.enterInitialState()
        self._telemLimiter = None
        return

    def addChildGameFSM(self, gameFSM):
        self.frameworkFSM.getStateNamed('frameworkGame').addChild(gameFSM)

    def removeChildGameFSM(self, gameFSM):
        self.frameworkFSM.getStateNamed('frameworkGame').removeChild(gameFSM)

    def setUsesSmoothing(self):
        self.usesSmoothing = 1

    def setUsesLookAround(self):
        self.usesLookAround = 1

    def getTitle(self):
        return TTLocalizer.DefaultMinigameTitle

    def getInstructions(self):
        return TTLocalizer.DefaultMinigameInstructions

    def getMaxDuration(self):
        raise Exception('Minigame implementer: you must override getMaxDuration()')

    def __createRandomNumGen(self):
        self.notify.debug('BASE: self.doId=0x%08X' % self.doId)
        self.randomNumGen = RandomNumGen.RandomNumGen(self.doId)

        def destroy(self = self):
            self.notify.debug('BASE: destroying random num gen')
            del self.randomNumGen

        self.cleanupActions.append(destroy)

    def generate(self):
        self.notify.debug('BASE: generate, %s' % self.getTitle())
        DistributedObject.DistributedObject.generate(self)
        self.__createRandomNumGen()

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        if not self.hasLocalToon:
            return
        self.notify.debug('BASE: handleAnnounceGenerate: send setAvatarJoined')
        self.sendUpdate('setAvatarJoined', [])
        self.normalExit = 1
        loader.beginBulkLoad('minigame', TTLocalizer.HeadingToFactory % self.getTitle(), True, TTLocalizer.TIP_MINIGAME, 100 + self.minigameId)
        self.load()
        loader.endBulkLoad('minigame')
        globalClock.syncFrameTime()
        self.onstage()

        def cleanup(self = self):
            self.notify.debug('BASE: cleanup: normalExit=%s' % self.normalExit)
            self.offstage()
            base.cr.renderFrame()
            if self.normalExit:
                self.sendUpdate('setAvatarExited', [])

        self.cleanupActions.append(cleanup)
        self._telemLimiter = self.getTelemetryLimiter()
        self.frameworkFSM.request('frameworkRules')

    def disable(self):
        self.notify.debug('BASE: disable')
        if self._telemLimiter:
            self._telemLimiter.destroy()
            self._telemLimiter = None
        self.frameworkFSM.request('frameworkCleanup')
        taskMgr.remove(self.uniqueName('random-abort'))
        taskMgr.remove(self.uniqueName('random-disconnect'))
        taskMgr.remove(self.uniqueName('random-netplugpull'))
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        self.notify.debug('BASE: delete')
        if self.hasLocalToon:
            self.unload()
        self.ignoreAll()
        if self.cr.playGame.hood:
            hoodMinigameState = self.cr.playGame.hood.fsm.getStateNamed('minigame')
            hoodMinigameState.removeChild(self.frameworkFSM)
        self.waitingStartLabel.destroy()
        del self.waitingStartLabel
        del self.frameworkFSM
        DistributedObject.DistributedObject.delete(self)

    def getTelemetryLimiter(self):
        return TLGatherAllAvs('Minigame', RotationLimitToH)

    def load(self):
        self.notify.debug('BASE: load')

    def onstage(self):
        base.localAvatar.laffMeter.hide()

    def offstage(self):
        self.notify.debug('BASE: offstage')
        for avId in self.avIdList:
            av = self.getAvatar(avId)
            if av:
                av.detachNode()

        messenger.send('minigameOffstage')

    def unload(self):
        self.notify.debug('BASE: unload')
        if hasattr(base, 'curMinigame'):
            del base.curMinigame

    def setParticipants(self, avIds):
        self.avIdList = avIds
        self.numPlayers = len(self.avIdList)
        self.hasLocalToon = self.localAvId in self.avIdList
        if not self.hasLocalToon:
            self.notify.warning('localToon (%s) not in list of minigame players: %s' % (self.localAvId, self.avIdList))
            return
        self.notify.info('BASE: setParticipants: %s' % self.avIdList)
        self.remoteAvIdList = []
        for avId in self.avIdList:
            if avId != self.localAvId:
                self.remoteAvIdList.append(avId)

        self.setSkipCount(0)

    def setTrolleyZone(self, trolleyZone):
        if not self.hasLocalToon:
            return
        self.notify.debug('BASE: setTrolleyZone: %s' % trolleyZone)
        self.trolleyZone = trolleyZone

    def setMinigameId(self, minigameId):
        self.minigameId = minigameId

    def getMinigameId(self):
        return self.minigameId

    def setDifficultyOverrides(self, difficultyOverride, trolleyZoneOverride):
        if not self.hasLocalToon:
            return
        if difficultyOverride != MinigameGlobals.NoDifficultyOverride:
            self.difficultyOverride = difficultyOverride / float(MinigameGlobals.DifficultyOverrideMult)
        if trolleyZoneOverride != MinigameGlobals.NoTrolleyZoneOverride:
            self.trolleyZoneOverride = trolleyZoneOverride

    def setGameReady(self):
        if not self.hasLocalToon:
            return
        self.notify.debug('BASE: setGameReady: Ready for game with avatars: %s' % self.avIdList)
        self.notify.debug('  safezone: %s' % self.getSafezoneId())
        self.notify.debug('difficulty: %s' % self.getDifficulty())
        self.__serverFinished = 0
        for avId in self.remoteAvIdList:
            if avId not in self.cr.doId2do:
                self.notify.warning('BASE: toon %s already left or has not yet arrived; waiting for server to abort the game' % avId)
                return 1

        for avId in self.remoteAvIdList:
            avatar = self.cr.doId2do[avId]
            event = avatar.uniqueName('disable')
            self.acceptOnce(event, self.handleDisabledAvatar, [avId])

            def ignoreToonDisable(self = self, event = event):
                self.ignore(event)

            self.cleanupActions.append(ignoreToonDisable)

        for avId in self.avIdList:
            avatar = self.getAvatar(avId)
            if avatar:
                if not self.usesSmoothing:
                    avatar.stopSmooth()
                if not self.usesLookAround:
                    avatar.stopLookAround()

        def cleanupAvatars(self = self):
            for avId in self.avIdList:
                avatar = self.getAvatar(avId)
                if avatar:
                    avatar.stopSmooth()
                    avatar.startLookAround()

        self.cleanupActions.append(cleanupAvatars)
        return 0

    def setGameStart(self, timestamp):
        if not self.hasLocalToon:
            return
        self.notify.debug('BASE: setGameStart: Starting game')
        self.gameStartTime = globalClockDelta.networkToLocalTime(timestamp)
        self.frameworkFSM.request('frameworkGame')

    def setGameAbort(self):
        if not self.hasLocalToon:
            return
        self.notify.warning('BASE: setGameAbort: Aborting game')
        self.normalExit = 0
        self.frameworkFSM.request('frameworkCleanup')

    def gameOver(self):
        if not self.hasLocalToon:
            return
        self.notify.debug('BASE: gameOver')
        self.frameworkFSM.request('frameworkWaitServerFinish')

    def getAvatar(self, avId):
        if avId in self.cr.doId2do:
            return self.cr.doId2do[avId]
        else:
            self.notify.warning('BASE: getAvatar: No avatar in doId2do with id: ' + str(avId))
            return None
            return None

    def getAvatarName(self, avId):
        avatar = self.getAvatar(avId)
        if avatar:
            return avatar.getName()
        else:
            return 'Unknown'

    def isSinglePlayer(self):
        if self.numPlayers == 1:
            return 1
        else:
            return 0

    def handleDisabledAvatar(self, avId):
        self.notify.warning('BASE: handleDisabledAvatar: disabled avId: ' + str(avId))
        self.frameworkFSM.request('frameworkAvatarExited')

    def d_requestExit(self):
        self.notify.debug('BASE: Sending requestExit')
        self.sendUpdate('requestExit', [])

    def enterFrameworkInit(self):
        self.notify.debug('BASE: enterFrameworkInit')
        self.setEmotes()
        self.cleanupActions.append(self.unsetEmotes)

    def exitFrameworkInit(self):
        pass

    def enterFrameworkRules(self):
        self.notify.debug('BASE: enterFrameworkRules')
        self.accept(self.rulesDoneEvent, self.handleRulesDone)
        self.rulesPanel = MinigameRulesPanel.MinigameRulesPanel('MinigameRulesPanel', self.getTitle(), self.getInstructions(), self.rulesDoneEvent, playerCount=len(self.avIdList))
        self.rulesPanel.load()
        self.rulesPanel.enter()

    def exitFrameworkRules(self):
        self.ignore(self.rulesDoneEvent)
        self.rulesPanel.exit()
        self.rulesPanel.unload()
        del self.rulesPanel

    def handleRulesDone(self):
        self.notify.debug('BASE: handleRulesDone')
        self.sendUpdate('setAvatarReady', [])
        self.frameworkFSM.request('frameworkWaitServerStart')

    def setAvatarReady(self):
        messenger.send('disableMinigameSkip')

    def enterFrameworkWaitServerStart(self):
        self.notify.debug('BASE: enterFrameworkWaitServerStart')
        if self.numPlayers > 1:
            msg = TTLocalizer.MinigameWaitingForOtherToons
        else:
            msg = TTLocalizer.MinigamePleaseWait
        self.waitingStartLabel['text'] = msg
        self.waitingStartLabel.show()

    def exitFrameworkWaitServerStart(self):
        self.waitingStartLabel.hide()

    def enterFrameworkGame(self):
        self.notify.debug('BASE: enterFrameworkGame')

    def exitFrameworkGame(self):
        pass

    def enterFrameworkWaitServerFinish(self):
        self.notify.debug('BASE: enterFrameworkWaitServerFinish')
        if self.__serverFinished:
            self.frameworkFSM.request('frameworkCleanup')

    def setGameExit(self):
        if not self.hasLocalToon:
            return
        self.notify.debug('BASE: setGameExit -- it is now safe to exit the game.')
        if self.frameworkFSM.getCurrentState().getName() != 'frameworkWaitServerFinish':
            self.__serverFinished = 1
        else:
            self.notify.debug('Must wait for server to exit game: ask the framework to cleanup.')
            self.frameworkFSM.request('frameworkCleanup')

    def exitFrameworkWaitServerFinish(self):
        pass

    def enterFrameworkAvatarExited(self):
        self.notify.debug('BASE: enterFrameworkAvatarExited')

    def exitFrameworkAvatarExited(self):
        pass

    def enterFrameworkCleanup(self):
        self.notify.debug('BASE: enterFrameworkCleanup')
        for action in self.cleanupActions:
            action()

        self.cleanupActions = []
        self.ignoreAll()
        if self.hasLocalToon:
            messenger.send(self.cr.playGame.hood.minigameDoneEvent)

    def exitFrameworkCleanup(self):
        pass

    def local2GameTime(self, timestamp):
        return timestamp - self.gameStartTime

    def game2LocalTime(self, timestamp):
        return timestamp + self.gameStartTime

    def getCurrentGameTime(self):
        return self.local2GameTime(globalClock.getFrameTime())

    def getDifficulty(self):
        if self.difficultyOverride is not None:
            return self.difficultyOverride
        elif hasattr(base, 'minigameDifficulty'):
            return float(base.minigameDifficulty)
        else:
            return MinigameGlobals.getDifficulty(self.getSafezoneId())

    def getSafezoneId(self):
        if self.trolleyZoneOverride is not None:
            return self.trolleyZoneOverride
        elif hasattr(base, 'minigameSafezoneId'):
            return MinigameGlobals.getSafezoneId(base.minigameSafezoneId)
        else:
            return MinigameGlobals.getSafezoneId(self.trolleyZone)

    def setEmotes(self):
        Emote.globalEmote.disableAll(base.localAvatar)

    def unsetEmotes(self):
        Emote.globalEmote.releaseAll(base.localAvatar)

    def requestSkip(self):
        self.sendUpdate('requestSkip')

    def setSkipCount(self, count):
        messenger.send('gameSkipCountChange', [count, len(self.avIdList)])