# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.coghq.DistributedBattleFactory
from panda3d.core import Filename
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleBase import *
from toontown.coghq import DistributedLevelBattle
from direct.directnotify import DirectNotifyGlobal
from toontown.toon import TTEmote
from otp.avatar import Emote
from toontown.battle import SuitBattleGlobals
from toontown.suit import SuitDNA
from direct.fsm import State
from direct.fsm import ClassicFSM, State
from toontown.toonbase import ToontownGlobals
from otp.nametag.NametagConstants import *
from otp.nametag import NametagGlobals

class DistributedBattleFactory(DistributedLevelBattle.DistributedLevelBattle):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleFactory')

    def __init__(self, cr):
        DistributedLevelBattle.DistributedLevelBattle.__init__(self, cr)
        self.fsm.addState(State.State('FactoryReward', self.enterFactoryReward, self.exitFactoryReward, ['Resume']))
        offState = self.fsm.getStateNamed('Off')
        offState.addTransition('FactoryReward')
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('FactoryReward')
        self.battleMusic = loader.loadMusic(self.getBattleMusicFilename())

    def getBattleMusicFilename(self):
        return 'phase_9/audio/bgm/encntr_general_FACT_bg.ogg'

    def getBattleMusic(self):
        return self.battleMusic

    def enterFaceOff(self, ts):
        base.cr.playGame.place.loader.battleMusic = self.getBattleMusic()
        base.cr.playGame.place.loader.battleMusic.play()
        DistributedLevelBattle.DistributedLevelBattle.enterFaceOff(self, ts)

    def enterFactoryReward(self, ts):
        self.disableCollision()
        self.delayDeleteMembers()
        if self.hasLocalToon():
            NametagGlobals.setMasterArrowsOn(0)
            if self.bossBattle:
                messenger.send('localToonConfrontedForeman')
        self.movie.playReward(ts, self.uniqueName('building-reward'), self.__handleFactoryRewardDone, noSkip=True)

    def __handleFactoryRewardDone(self):
        if self.hasLocalToon():
            self.d_rewardDone()
        self.movie.resetReward()
        self.fsm.request('Resume')

    def exitFactoryReward(self):
        self.movie.resetReward(finish=1)
        self._removeMembersKeep()
        NametagGlobals.setMasterArrowsOn(1)