# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.battle.Movie
from panda3d.core import Point3, Vec3
import copy
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
import random
from BattleBase import *
import BattleExperience
import BattleParticles
import MovieDrop
import MovieFire
import MovieHeal
import MovieLure
import MovieNPCSOS
import MoviePetSOS
import MovieSOS
import MovieSound
import MovieSquirt
import MovieSuitAttacks
import MovieThrow
import MovieToonVictory
import MovieTrap
import MovieUtil
import PlayByPlayText
import RewardPanel
from SuitBattleGlobals import *
from toontown.distributed import DelayDelete
from toontown.toon import NPCToons
from toontown.toon import Toon
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownBattleGlobals import *
from toontown.toontowngui import TTDialog
from toontown.suit import SuitDNA
from otp.nametag.NametagConstants import *
from otp.nametag.NametagGroup import *
camPos = Point3(14, 0, 10)
camHpr = Vec3(89, -30, 0)
randomBattleTimestamp = config.GetBool('random-battle-timestamp', 0)

class Movie(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('Movie')

    def __init__(self, battle):
        self.battle = battle
        self.track = None
        self.rewardPanel = None
        self.rewardCallback = None
        self.playByPlayText = PlayByPlayText.PlayByPlayText()
        self.playByPlayText.hide()
        self.renderProps = []
        self.hasBeenReset = 0
        self.reset()
        self.rewardHasBeenReset = 0
        self.tutRewardDialog = None
        self.tutSequence = None
        self.resetReward()
        return

    def cleanup(self):
        self.reset()
        self.resetReward()
        self.battle = None
        if self.playByPlayText != None:
            self.playByPlayText.cleanup()
        self.playByPlayText = None
        if self.rewardPanel != None:
            self.rewardPanel.cleanup()
        self.cleanupTutRewardDialog()
        self.rewardPanel = None
        self.rewardCallback = None
        return

    def needRestoreColor(self):
        self.restoreColor = 1

    def clearRestoreColor(self):
        self.restoreColor = 0

    def needRestoreHips(self):
        self.restoreHips = 1

    def clearRestoreHips(self):
        self.restoreHips = 0

    def needRestoreHeadScale(self):
        self.restoreHeadScale = 1

    def clearRestoreHeadScale(self):
        self.restoreHeadScale = 0

    def needRestoreToonScale(self):
        self.restoreToonScale = 1

    def clearRestoreToonScale(self):
        self.restoreToonScale = 0

    def needRestoreParticleEffect(self, effect):
        self.specialParticleEffects.append(effect)

    def clearRestoreParticleEffect(self, effect):
        if effect in self.specialParticleEffects:
            self.specialParticleEffects.remove(effect)

    def needRestoreRenderProp(self, prop):
        self.renderProps.append(prop)

    def clearRenderProp(self, prop):
        if prop in self.renderProps:
            self.renderProps.remove(prop)

    def restore(self):
        return
        for toon in self.battle.activeToons:
            toon.loop('neutral')
            origPos, origHpr = self.battle.getActorPosHpr(toon)
            toon.setPosHpr(self.battle, origPos, origHpr)
            hands = [toon.getLeftHand(), toon.getRightHand()]
            for hand in hands:
                props = hand.getChildren()
                for prop in props:
                    if prop.getName() != 'book':
                        MovieUtil.removeProp(prop)

            if self.restoreColor == 1:
                headParts = toon.getHeadParts()
                torsoParts = toon.getTorsoParts()
                legsParts = toon.getLegsParts()
                partsList = [headParts, torsoParts, legsParts]
                for parts in partsList:
                    for partNum in xrange(0, parts.getNumPaths()):
                        nextPart = parts.getPath(partNum)
                        nextPart.clearColorScale()
                        nextPart.clearTransparency()

            if self.restoreHips == 1:
                parts = toon.getHipsParts()
                for partNum in xrange(0, parts.getNumPaths()):
                    nextPart = parts.getPath(partNum)
                    props = nextPart.getChildren()
                    for prop in props:
                        if prop.getName() == 'redtape-tube.egg':
                            MovieUtil.removeProp(prop)

            if self.restoreHeadScale == 1:
                headScale = ToontownGlobals.toonHeadScales[toon.style.getAnimal()]
                toon.getPart('head').setScale(headScale)
            if self.restoreToonScale == 1:
                toon.setScale(1)
            headParts = toon.getHeadParts()
            for partNum in xrange(0, headParts.getNumPaths()):
                part = headParts.getPath(partNum)
                part.setHpr(0, 0, 0)
                part.setPos(0, 0, 0)

            arms = toon.findAllMatches('**/arms')
            sleeves = toon.findAllMatches('**/sleeves')
            hands = toon.findAllMatches('**/hands')
            for partNum in xrange(0, arms.getNumPaths()):
                armPart = arms.getPath(partNum)
                sleevePart = sleeves.getPath(partNum)
                handsPart = hands.getPath(partNum)
                armPart.setHpr(0, 0, 0)
                sleevePart.setHpr(0, 0, 0)
                handsPart.setHpr(0, 0, 0)

        for suit in self.battle.activeSuits:
            if suit._Actor__animControlDict != None:
                suit.loop('neutral')
                suit.battleTrapIsFresh = 0
                origPos, origHpr = self.battle.getActorPosHpr(suit)
                suit.setPosHpr(self.battle, origPos, origHpr)
                hands = [suit.getRightHand(), suit.getLeftHand()]
                for hand in hands:
                    props = hand.getChildren()
                    for prop in props:
                        MovieUtil.removeProp(prop)

        for effect in self.specialParticleEffects:
            if effect != None:
                effect.cleanup()

        self.specialParticleEffects = []
        for prop in self.renderProps:
            MovieUtil.removeProp(prop)

        self.renderProps = []
        return

    def _deleteTrack(self):
        if self.track:
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        return

    def reset(self, finish = 0):
        if self.hasBeenReset == 1:
            return
        self.hasBeenReset = 1
        self.stop()
        self._deleteTrack()
        if finish == 1:
            self.restore()
        self.toonAttackDicts = []
        self.suitAttackDicts = []
        self.specialSuitAttackDicts = []
        self.restoreColor = 0
        self.restoreHips = 0
        self.restoreHeadScale = 0
        self.restoreToonScale = 0
        self.specialParticleEffects = []
        for prop in self.renderProps:
            MovieUtil.removeProp(prop)

        self.renderProps = []

    def resetReward(self, finish = 0):
        if self.rewardHasBeenReset == 1:
            return
        else:
            self.rewardHasBeenReset = 1
            self.stop()
            self._deleteTrack()
            if finish == 1:
                self.restore()
            self.toonRewardDicts = []
            if self.rewardPanel != None:
                self.rewardPanel.destroy()
            self.rewardPanel = None
            return

    def play(self, ts, callback):
        self.hasBeenReset = 0
        ptrack = Sequence()
        camtrack = Sequence()
        if random.random() > 0.5:
            MovieUtil.shotDirection = 'left'
        else:
            MovieUtil.shotDirection = 'right'
        for s in self.battle.activeSuits:
            s.battleTrapIsFresh = 0

        spattacks, spcam = self.__doSpecialSuitAttacks()
        if spattacks:
            ptrack.append(spattacks)
            camtrack.append(spcam)
        sattacks, scam = self.__doSuitAttacks(True)
        if sattacks:
            ptrack.append(sattacks)
            camtrack.append(scam)
        tattacks, tcam = self.__doToonAttacks()
        if tattacks:
            ptrack.append(tattacks)
            camtrack.append(tcam)
        sattacks, scam = self.__doSuitAttacks(False)
        if sattacks:
            ptrack.append(sattacks)
            camtrack.append(scam)
        ptrack.append(Func(callback))
        self._deleteTrack()
        self.track = Sequence(ptrack, name='movie-track-%d' % self.battle.doId)
        if self.battle.localToonPendingOrActive():
            self.track = Parallel(self.track, camtrack, name='movie-track-with-cam-%d' % self.battle.doId)
        if randomBattleTimestamp == 1:
            randNum = random.randint(0, 99)
            dur = self.track.getDuration()
            ts = float(randNum) / 100.0 * dur
        self.track.delayDeletes = []
        for suit in self.battle.suits:
            self.track.delayDeletes.append(DelayDelete.DelayDelete(suit, 'Movie.play'))

        for toon in self.battle.toons:
            self.track.delayDeletes.append(DelayDelete.DelayDelete(toon, 'Movie.play'))

        self.track.start(ts)
        return None

    def finish(self):
        self.track.finish()

    def playReward(self, ts, name, callback, noSkip = False):
        self.rewardHasBeenReset = 0
        ptrack = Sequence()
        camtrack = Sequence()
        self.rewardPanel = RewardPanel.RewardPanel(name)
        self.rewardPanel.hide()
        victory, camVictory, skipper = MovieToonVictory.doToonVictory(self.battle.localToonActive(), self.battle.activeToons, self.toonRewardIds, self.toonRewardDicts, self.deathList, self.rewardPanel, 1, self.uberList, self.helpfulToons, noSkip=noSkip)
        if victory:
            skipper.setIvals((ptrack, camtrack), ptrack.getDuration())
            ptrack.append(victory)
            camtrack.append(camVictory)
        ptrack.append(Func(callback))
        self._deleteTrack()
        self.track = Sequence(ptrack, name='movie-reward-track-%d' % self.battle.doId)
        if self.battle.localToonActive():
            self.track = Parallel(self.track, camtrack, name='movie-reward-track-with-cam-%d' % self.battle.doId)
        self.track.delayDeletes = []
        for t in self.battle.activeToons:
            self.track.delayDeletes.append(DelayDelete.DelayDelete(t, 'Movie.playReward'))

        skipper.setIvals((self.track,), 0.0)
        skipper.setBattle(self.battle)
        self.track.start(ts)

    def cleanupTutRewardDialog(self):
        if self.tutRewardDialog:
            self.tutRewardDialog.cleanup()
            self.tutRewardDialog = None
        if self.tutSequence:
            self.tutSequence.pause()
            self.tutSequence = None
        return

    def playTutorialReward(self, ts, name, callback):
        self.rewardHasBeenReset = 0
        self.rewardPanel = RewardPanel.RewardPanel(name)
        self.rewardCallback = callback
        camera.setPosHpr(0, 8, base.localAvatar.getHeight() * 0.66, 179, 15, 0)
        self.rewardPanel.initGagFrame(base.localAvatar, base.localAvatar.experience.experience, [0] * len(SuitDNA.suitDepts), noSkip=True)
        earnedExp = self.toonRewardDicts[0]['earnedExp']
        if all((not xp for xp in earnedExp)):
            self.playTutorialNoGagReward()
        else:
            self.playTutorialGagReward(None, earnedExp)
        return

    def playTutorialGagReward(self, dialog, earnedXp, tutTrack = 0):
        self.cleanupTutRewardDialog()
        if tutTrack >= len(earnedXp):
            self.rewardCallback()
            return
        else:
            xp = earnedXp[tutTrack]
            if xp:
                self.tutRewardDialog = TTDialog.TTDialog(text=TTLocalizer.MovieTutorialMessage % (xp, TTLocalizer.BattleGlobalTracks[tutTrack].capitalize()), command=self.playTutorialGagReward, extraArgs=[earnedXp, tutTrack + 1], style=TTDialog.Acknowledge, fadeScreen=None, pos=(0.65, 0, 0.5), scale=0.8)
                self.tutSequence = Sequence()
                self.tutSequence += self.rewardPanel.getTrackIntervalList(base.localAvatar, tutTrack, base.localAvatar.experience.getExp(tutTrack), xp, 0)
                self.tutSequence.start()
            else:
                self.playTutorialGagReward(None, earnedXp, tutTrack + 1)
            return

    def playTutorialNoGagReward(self):
        self.tutRewardDialog = TTDialog.TTDialog(text=TTLocalizer.MovieTutorialMessage2, command=self.__callbackAndCleanupTut, style=TTDialog.Acknowledge, fadeScreen=None, pos=(0.65, 0, 0.5), scale=0.8)
        return

    def __callbackAndCleanupTut(self, dialog = None):
        self.cleanupTutRewardDialog()
        self.rewardCallback()

    def stop(self):
        if self.track:
            self.track.finish()
            self._deleteTrack()
        if hasattr(self, 'track1'):
            self.track1.finish()
            self.track1 = None
        if hasattr(self, 'track2'):
            self.track2.finish()
            self.track2 = None
        if hasattr(self, 'track3'):
            self.track3.finish()
            self.track3 = None
        if self.rewardPanel:
            self.rewardPanel.hide()
        if self.playByPlayText:
            self.playByPlayText.hide()
        return

    def __doToonAttacks(self):
        if config.GetBool('want-toon-attack-anims', 1):
            track = Sequence(name='toon-attacks')
            camTrack = Sequence(name='toon-attacks-cam')
            ival, camIval = MovieFire.doFires(self.__findToonAttack(FIRE))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MovieSOS.doSOSs(self.__findToonAttack(SOS))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MovieNPCSOS.doNPCSOSs(self.__findToonAttack(NPCSOS))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MoviePetSOS.doPetSOSs(self.__findToonAttack(PETSOS))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MovieHeal.doHeals(self.__findToonAttack(HEAL), self.battle.getInteractivePropTrackBonus() == HEAL)
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MovieTrap.doTraps(self.__findToonAttack(TRAP))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MovieLure.doLures(self.__findToonAttack(LURE))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MovieSound.doSounds(self.__findToonAttack(SOUND))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MovieThrow.doThrows(self.__findToonAttack(THROW))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MovieSquirt.doSquirts(self.__findToonAttack(SQUIRT))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            ival, camIval = MovieDrop.doDrops(self.__findToonAttack(DROP))
            if ival:
                track.append(ival)
                camTrack.append(camIval)
            if len(track) == 0:
                return (None, None)
            else:
                return (track, camTrack)
        else:
            return (None, None)
        return None

    def genRewardDicts(self, battleExperience):
        experiences, self.deathList, self.uberList, self.helpfulToons = battleExperience
        self.toonRewardDicts = BattleExperience.genRewardDicts(experiences)
        self.toonRewardIds = [ experience[0] for experience in experiences ]

    def genAttackDicts(self, activeToons, activeSuits, toonAttacks, suitAttacks, specialSuitAttacks):
        if self.track and self.track.isPlaying():
            self.notify.warning('genAttackDicts() - track is playing!')
        self.__genToonAttackDicts(activeToons, activeSuits, toonAttacks)
        self.__genSuitAttackDicts(activeToons, activeSuits, suitAttacks)
        self.__genSpecialSuitAttackDicts(activeSuits, specialSuitAttacks)

    def __genToonAttackDicts(self, toons, suits, toonAttacks):
        for ta in toonAttacks:
            targetGone = 0
            track = ta[TOON_TRACK_COL]
            if track != NO_ATTACK:
                adict = {}
                toonIndex = ta[TOON_ID_COL]
                toonId = toons[toonIndex]
                toon = self.battle.findToon(toonId)
                if toon == None:
                    continue
                level = ta[TOON_LVL_COL]
                adict['toon'] = toon
                adict['track'] = track
                adict['level'] = level
                hps = ta[TOON_HP_COL]
                kbbonuses = ta[TOON_KBBONUS_COL]
                if track == NPCSOS:
                    adict['npcId'] = ta[TOON_TGT_COL]
                    toonId = ta[TOON_TGT_COL]
                    track, npc_level, npc_hp = NPCToons.getNPCTrackLevelHp(adict['npcId'])
                    if track == None:
                        track = NPCSOS
                    adict['track'] = track
                    adict['level'] = npc_level
                elif track == PETSOS:
                    petId = ta[TOON_TGT_COL]
                    adict['toonId'] = toonId
                    adict['petId'] = petId
                if track == SOS:
                    targetId = ta[TOON_TGT_COL]
                    if targetId == base.localAvatar.doId:
                        target = base.localAvatar
                        adict['targetType'] = 'callee'
                    elif toon == base.localAvatar:
                        target = base.cr.identifyAvatar(targetId)
                        adict['targetType'] = 'caller'
                    else:
                        target = None
                        adict['targetType'] = 'observer'
                    adict['target'] = target
                elif track in (NPCSOS,
                 PETSOS,
                 NPC_COGS_MISS,
                 NPC_TOONS_HIT,
                 NPC_COGS_POWER_DOWN,
                 NPC_TOONS_POWER_UP,
                 NPC_RESTOCK_GAGS):
                    adict['special'] = 1
                    toonHandles = []
                    for t in toons:
                        if t != -1:
                            target = self.battle.findToon(t)
                            if target == None:
                                continue
                            if (track == NPC_TOONS_HIT or track == NPC_TOONS_POWER_UP) and t == toonId:
                                continue
                            toonHandles.append(target)

                    adict['toons'] = toonHandles
                    suitHandles = []
                    for s in suits:
                        if s != -1:
                            target = self.battle.findSuit(s)
                            if target == None:
                                continue
                            suitHandles.append(target)

                    adict['suits'] = suitHandles
                    if track == PETSOS:
                        del adict['special']
                        targets = []
                        for t in toons:
                            if t != -1:
                                target = self.battle.findToon(t)
                                if target == None:
                                    continue
                                tdict = {}
                                tdict['toon'] = target
                                tdict['hp'] = hps[toons.index(t)]
                                self.notify.debug('PETSOS: toon: %d healed for hp: %d' % (target.doId, hps[toons.index(t)]))
                                targets.append(tdict)

                        if len(targets) > 0:
                            adict['target'] = targets
                elif track == HEAL:
                    if levelAffectsGroup(HEAL, level):
                        targets = []
                        for t in toons:
                            if t != toonId and t != -1:
                                target = self.battle.findToon(t)
                                if target == None:
                                    continue
                                tdict = {}
                                tdict['toon'] = target
                                tdict['hp'] = hps[toons.index(t)]
                                self.notify.debug('HEAL: toon: %d healed for hp: %d' % (target.doId, hps[toons.index(t)]))
                                targets.append(tdict)

                        if len(targets) > 0:
                            adict['target'] = targets
                        else:
                            targetGone = 1
                    else:
                        targetIndex = ta[TOON_TGT_COL]
                        if targetIndex < 0:
                            targetGone = 1
                        else:
                            targetId = toons[targetIndex]
                            target = self.battle.findToon(targetId)
                            if target != None:
                                tdict = {}
                                tdict['toon'] = target
                                tdict['hp'] = hps[targetIndex]
                                adict['target'] = tdict
                            else:
                                targetGone = 1
                elif attackAffectsGroup(track, level, ta[TOON_TRACK_COL]):
                    targets = []
                    for s in suits:
                        if s != -1:
                            target = self.battle.findSuit(s)
                            if ta[TOON_TRACK_COL] == NPCSOS:
                                if track == LURE and self.battle.isSuitLured(target):
                                    continue
                                elif track == TRAP and (self.battle.isSuitLured(target) or target.battleTrap != NO_TRAP):
                                    continue
                            targetIndex = suits.index(s)
                            sdict = {}
                            sdict['suit'] = target
                            sdict['hp'] = hps[targetIndex]
                            if ta[TOON_TRACK_COL] == NPCSOS and track == DROP and hps[targetIndex] == 0:
                                continue
                            sdict['kbbonus'] = kbbonuses[targetIndex]
                            sdict['died'] = ta[SUIT_DIED_COL] & 1 << targetIndex
                            sdict['revived'] = ta[SUIT_REVIVE_COL] & 1 << targetIndex
                            if sdict['died'] != 0:
                                pass
                            sdict['leftSuits'] = []
                            sdict['rightSuits'] = []
                            targets.append(sdict)

                    adict['target'] = targets
                else:
                    targetIndex = ta[TOON_TGT_COL]
                    if targetIndex < 0:
                        targetGone = 1
                    else:
                        targetId = suits[targetIndex]
                        target = self.battle.findSuit(targetId)
                        sdict = {}
                        sdict['suit'] = target
                        if target not in self.battle.activeSuits:
                            targetGone = 1
                            suitIndex = 0
                        else:
                            suitIndex = self.battle.activeSuits.index(target)
                        leftSuits = []
                        for si in xrange(0, suitIndex):
                            asuit = self.battle.activeSuits[si]
                            if not self.battle.isSuitLured(asuit):
                                leftSuits.append(asuit)

                        lenSuits = len(self.battle.activeSuits)
                        rightSuits = []
                        if lenSuits > suitIndex + 1:
                            for si in xrange(suitIndex + 1, lenSuits):
                                asuit = self.battle.activeSuits[si]
                                if not self.battle.isSuitLured(asuit):
                                    rightSuits.append(asuit)

                        sdict['leftSuits'] = leftSuits
                        sdict['rightSuits'] = rightSuits
                        sdict['hp'] = hps[targetIndex]
                        sdict['kbbonus'] = kbbonuses[targetIndex]
                        sdict['died'] = ta[SUIT_DIED_COL] & 1 << targetIndex
                        sdict['revived'] = ta[SUIT_REVIVE_COL] & 1 << targetIndex
                        if sdict['revived'] != 0:
                            pass
                        if sdict['died'] != 0:
                            pass
                        if track == DROP or track == TRAP:
                            adict['target'] = [sdict]
                        else:
                            adict['target'] = sdict
                adict['hpbonus'] = ta[TOON_HPBONUS_COL]
                adict['sidestep'] = ta[TOON_ACCBONUS_COL]
                if 'npcId' in adict:
                    adict['sidestep'] = 0
                adict['battle'] = self.battle
                adict['playByPlayText'] = self.playByPlayText
                if targetGone == 0:
                    self.toonAttackDicts.append(adict)
                else:
                    self.notify.warning('genToonAttackDicts() - target gone!')

        def compFunc(a, b):
            alevel = a['level']
            blevel = b['level']
            if alevel > blevel:
                return 1
            if alevel < blevel:
                return -1
            return 0

        self.toonAttackDicts.sort(compFunc)
        return

    def __findToonAttack(self, track):
        tp = []
        for ta in self.toonAttackDicts:
            if ta['track'] == track or track == NPCSOS and 'special' in ta:
                tp.append(ta)

        if track == TRAP:
            sortedTraps = []
            for attack in tp:
                if 'npcId' not in attack:
                    sortedTraps.append(attack)

            for attack in tp:
                if 'npcId' in attack:
                    sortedTraps.append(attack)

            tp = sortedTraps
        return tp

    def __genSpecialSuitAttackDicts(self, suits, suitAttacks):
        for sa in suitAttacks:
            attack = sa[SUIT_ATK_COL]
            if attack == NO_ATTACK:
                continue
            suitIndex = sa[SUIT_ID_COL]
            suitId = suits[suitIndex]
            suit = self.battle.findSuit(suitId)
            if not suit:
                continue
            atkDict = {}
            atkDict['id'] = attack
            atkDict['name'] = SuitAttacks.keys()[attack]
            atkDict['suit'] = suit
            atkDict['battle'] = self.battle
            atkDict['playByPlayText'] = self.playByPlayText
            atkDict['taunt'] = sa[SUIT_SPECIAL_TAUNT_COL]
            self.specialSuitAttackDicts.append(atkDict)

    def __genSuitAttackDicts(self, toons, suits, suitAttacks):
        for sa in suitAttacks:
            targetGone = 0
            attack = sa[SUIT_ATK_COL]
            if attack != NO_ATTACK:
                suitIndex = sa[SUIT_ID_COL]
                suitId = suits[suitIndex]
                suit = self.battle.findSuit(suitId)
                if suit == None:
                    self.notify.warning('suit: %d not in battle!' % suitId)
                    return
                adict = getSuitAttack(suit.getStyleName(), suit.getLevel(), attack)
                adict['suit'] = suit
                adict['battle'] = self.battle
                adict['playByPlayText'] = self.playByPlayText
                adict['taunt'] = sa[SUIT_TAUNT_COL]
                adict['beforeToons'] = sa[SUIT_BEFORE_TOONS_COL]
                hps = sa[SUIT_HP_COL]
                if adict['group'] == ATK_TGT_GROUP:
                    targets = []
                    for t in toons:
                        if t != -1:
                            target = self.battle.findToon(t)
                            if target == None:
                                continue
                            targetIndex = toons.index(t)
                            tdict = {}
                            tdict['toon'] = target
                            tdict['hp'] = hps[targetIndex]
                            self.notify.debug('DAMAGE: toon: %d hit for hp: %d' % (target.doId, hps[targetIndex]))
                            toonDied = sa[TOON_DIED_COL] & 1 << targetIndex
                            tdict['died'] = toonDied
                            targets.append(tdict)

                    if len(targets) > 0:
                        adict['target'] = targets
                    else:
                        targetGone = 1
                elif adict['group'] == ATK_TGT_SINGLE:
                    targetIndex = sa[SUIT_TGT_COL]
                    targetId = toons[targetIndex]
                    target = self.battle.findToon(targetId)
                    if target == None:
                        targetGone = 1
                        break
                    tdict = {}
                    tdict['toon'] = target
                    tdict['hp'] = hps[targetIndex]
                    self.notify.debug('DAMAGE: toon: %d hit for hp: %d' % (target.doId, hps[targetIndex]))
                    toonDied = sa[TOON_DIED_COL] & 1 << targetIndex
                    tdict['died'] = toonDied
                    toonIndex = self.battle.activeToons.index(target)
                    rightToons = []
                    for ti in xrange(0, toonIndex):
                        rightToons.append(self.battle.activeToons[ti])

                    lenToons = len(self.battle.activeToons)
                    leftToons = []
                    if lenToons > toonIndex + 1:
                        for ti in xrange(toonIndex + 1, lenToons):
                            leftToons.append(self.battle.activeToons[ti])

                    tdict['leftToons'] = leftToons
                    tdict['rightToons'] = rightToons
                    adict['target'] = tdict
                else:
                    self.notify.warning('got suit attack not group or single!')
                if targetGone == 0:
                    self.suitAttackDicts.append(adict)
                else:
                    self.notify.warning('genSuitAttackDicts() - target gone!')

        return

    def __doSpecialSuitAttacks(self):
        if not config.GetBool('want-suit-anims', 1):
            return (None, None)
        track = Sequence(name='special-suit-attacks')
        camTrack = Sequence(name='special-suit-attacks-cam')
        for attack in self.specialSuitAttackDicts:
            ival, camIval = MovieSuitAttacks.doSuitAttack(attack)
            if ival:
                taunt = getAttackTaunt(attack['name'], attack['taunt'])
                suit = attack['suit']
                ival = Sequence(Func(suit.setChatAbsolute, taunt, CFSpeech), ival, Func(suit.clearChat))
                track.append(ival)
                camTrack.append(camIval)

        if len(track) == 0:
            return (None, None)
        else:
            return (track, camTrack)

    def __doSuitAttacks(self, beforeToons = False):
        if config.GetBool('want-suit-anims', 1):
            track = Sequence(name='suit-attacks')
            camTrack = Sequence(name='suit-attacks-cam')
            isLocalToonSad = False
            for a in self.suitAttackDicts:
                if a['beforeToons'] != beforeToons:
                    continue
                ival, camIval = MovieSuitAttacks.doSuitAttack(a)
                if ival:
                    track.append(ival)
                    camTrack.append(camIval)
                targetField = a.get('target')
                if targetField is None:
                    continue
                if a['group'] == ATK_TGT_GROUP:
                    for target in targetField:
                        if target['died'] and target['toon'].doId == base.localAvatar.doId:
                            isLocalToonSad = True

                elif a['group'] == ATK_TGT_SINGLE:
                    if targetField['died'] and targetField['toon'].doId == base.localAvatar.doId:
                        isLocalToonSad = True
                if isLocalToonSad:
                    break

            if len(track) == 0:
                return (None, None)
            return (track, camTrack)
        else:
            return (None, None)
            return