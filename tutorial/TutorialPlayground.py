# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.TutorialPlayground
from panda3d.core import CardMaker, Vec3, headsUp
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
from otp.avatar import Emote
from otp.nametag import NametagGlobals
from toontown.battle.BattleProps import globalPropPool
from toontown.battle.MovieSuitAttacks import getSoundTrack
from toontown.catalog import CatalogFurnitureItem
from toontown.toon import NPCToons, TTEmote
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.hood import ZoneUtil
from TutorialTVScreen import TutorialTVScreen
from TutorialUtil import *
import random
TvFurnitureItem = 1532
TutorialObjects = [('tv', 'phase_5.5/models/estate/bugRoomTV_100inch', (-111, -88.5, 2.48, 224, 0, 0))]
StaticCogs = [('holly',
  'mh',
  RegularSuit,
  True,
  True,
  'neutral',
  (-121, -78, 2.5, 225, 0, 0)), ('raider',
  'cr',
  RegularSuit,
  True,
  True,
  'neutral',
  (-116, -61, 2.5, 150, 0, 0))]
EscapingCogPositions = [(-75.5, -2.1, 1.4, 335, 0, 0), (-60.5, -5.5, 0.14, 300, 0, 0)]
EscapingToonPositions = [(-66.5, 15.5, -0.01, 335, 0, 0), (-40.5, 3.8, -0.01, 300, 0, 0)]
EscapingToonFinalPositions = [(-57.5, 34, -0.01, 335, 0, 0), (-21.5, 15, -0.01, 300, 0, 0)]
FlyInBasePosition = (2.55, 37, -0.01)
FlyInGridXNum = 4
FlyInGridYNum = 3
FlyInGridXDifference = -10.5
FlyInGridYDifference = -10.5

class TutorialPlayground(DirectObject):

    def __init__(self, playground):
        self.playground = playground
        self.loaded = False
        self.entered = False
        self.initializeLoad()
        self.initialize()

    def uniqueName(self, name):
        return 'TutorialPlayground-%s-%s' % (id(self), name)

    def getHollywood(self):
        return self.models.get('holly')

    def getRaider(self):
        return self.models.get('raider')

    def getPlayground(self):
        return self.playground

    def getGeom(self):
        return self.playground.loader.geom

    def initializeLoad(self):
        self.tvScreen = None
        self.models = {}
        return

    def initialize(self):
        self.introSequence = None
        self.chopper = None
        self.escapingCogs = []
        self.escapingToons = []
        self.flyingInCogs = []
        return

    def load(self):
        if self.loaded:
            return
        geom = self.getGeom()
        for crates in ('**/group1', '**/group2'):
            geom.find(crates).removeNode()

        self.initializeLoad()
        self.initialize()
        for object in TutorialObjects:
            name, path, transform = object
            model = loader.loadModel(path)
            model.reparentTo(geom)
            model.setPosHpr(*transform)
            self.models[name] = model

        for object in StaticCogs:
            name, suitName, type, hasNametag, nametagActive, anim, transform = object
            self.models[name] = createSuit(self, suitName, transform, hasNametag=hasNametag, active=nametagActive, type=type, parent=geom, anim=anim)

        tv = self.models['tv']
        tv.find('**/toonTownBugTV_screen').removeNode()
        pos, scale = CatalogFurnitureItem.TvToPosScale[TvFurnitureItem]
        screen = model.attachNewNode(CardMaker('tv-screen').generate())
        screen.setPos(*pos)
        screen.setScale(*scale)
        self.tvScreen = TutorialTVScreen(screen)
        self.loaded = True

    def unloadLoad(self):
        if self.introSequence and self.introSequence.isPlaying():
            self.introSequence.pause()
        for actor in self.escapingCogs + self.escapingToons + self.flyingInCogs + [self.chopper]:
            cleanupActor(actor)

    def unload(self):
        if not self.loaded:
            return
        for model in self.models.values() + [self.tvScreen]:
            if model:
                if hasattr(model, 'delete'):
                    model.delete()
                else:
                    model.removeNode()

        self.unloadLoad()
        self.initializeLoad()
        self.initialize()
        self.ignoreAll()
        self.loaded = False

    def enter(self):
        if self.entered:
            return
        self.initialize()
        self.entered = True
        self.acceptOnce('enterWalk', self.__delayedEnter)

    def exit(self):
        if not self.entered:
            return
        self.unloadLoad()
        self.initialize()
        self.ignoreAll()
        self.entered = False

    def __makeEvilEyeMovies(self, cog, targetPosHpr):
        eye = globalPropPool.getProp('evil-eye')
        if cog.style.name == 'cr':
            eyePosHpr = (-0.46, 4.85, 5.28, -155.0, -20.0, 0.0)
        else:
            eyePosHpr = (-0.4, 3.65, 5.01, -155.0, -20.0, 0.0)
        soundTrack = getSoundTrack('SA_evil_eye.ogg', delay=1.3, node=cog)
        eyeTrack = Sequence(Wait(1.06), Func(eye.reparentTo, cog), Func(eye.setPosHpr, *eyePosHpr), eye.scaleInterval(0.63, 11), Wait(0.33), eye.hprInterval(0.02, (205, 40, 0)), Wait(0.77), Func(eye.wrtReparentTo, self.getGeom()), Parallel(eye.hprInterval(1.1, (0, 0, -180)), eye.posInterval(1.1, Vec3(targetPosHpr[:3]) + Vec3(0, 0, 2.5))), Func(eye.removeNode))
        suitTrack = Sequence(cog.actorInterval('glower', endFrame=32), Wait(1.1), cog.actorInterval('glower', startFrame=32), Func(cog.loop, 'neutral'))
        return (soundTrack, eyeTrack, suitTrack)

    def __makeEscapingToonMovie(self, index):
        cog = self.escapingCogs[index]
        toon = self.escapingToons[index]
        targetPosHpr = EscapingToonFinalPositions[index]
        soundTrack, eyeTrack, suitTrack = self.__makeEvilEyeMovies(cog, targetPosHpr)
        toonTrack = Sequence(Func(toon.animFSM.request, 'run'), toon.posHprInterval(3.91, targetPosHpr[:3], targetPosHpr[3:]), Func(toon.animFSM.request, 'Died'))
        self.acceptOnce(toon.uniqueName('died'), lambda : cleanupActor(toon))
        return Sequence(Wait(0.5 * index), Parallel(eyeTrack, suitTrack, toonTrack, soundTrack))

    def __makeEscapingToonMovies(self):
        return Parallel(*[ self.__makeEscapingToonMovie(i) for i in xrange(len(self.escapingToons)) ])

    def __makeCogFlyInMovie(self, spawnTime):
        cogNum = len(self.flyingInCogs)
        cogIds = range(cogNum)
        spawnOneTime = spawnTime / cogNum
        sequences = []
        random.shuffle(cogIds)
        for i, id in enumerate(cogIds):
            cog = self.flyingInCogs[id]
            flySeq = cog.beginSupaFlyMove(cog.finalPosition, True, 'fromSky', False, True)
            sequences.append(Sequence(Wait(spawnOneTime * i), Func(cog.show), Parallel(flySeq, cog.hprInterval(flySeq.getDuration() * 0.6, (cog.getH(), 0, 0))), Wait(0.3), Func(cog.pingpong, 'effort', fromFrame=90, toFrame=125)))

        return Parallel(*sequences)

    def __deleteChopper(self):
        cleanupActor(self.chopper)
        self.chopper = None
        return

    def __delayedEnter(self):
        self.playground.fsm.request('stopped')
        base.localAvatar.laffMeter.obscure(True)
        base.localAvatar.setPreventSleepWatch(True)
        NametagGlobals.setMasterArrowsOn(False)
        geom = self.getGeom()
        self.escapingCogs = [ createSuit(self, 'tf', EscapingCogPositions[i], hasNametag=True, parent=geom) for i in xrange(len(EscapingCogPositions)) ]
        self.escapingToons = [ NPCToons.createRandomNPC() for i in xrange(len(EscapingToonPositions)) ]
        self.flyingInCogs = []
        for i, toon in enumerate(self.escapingToons):
            toon.reparentTo(geom)
            toon.setPosHpr(*EscapingToonPositions[i])

        for xG in xrange(FlyInGridXNum):
            for yG in xrange(FlyInGridYNum):
                x, y, z = FlyInBasePosition
                x += FlyInGridXDifference * xG
                y += FlyInGridYDifference * yG
                suit = createSuit(self, None, (x,
                 y + 100,
                 z,
                 180,
                 45,
                 0), hasNametag=True, type=DistributedSuit, parent=geom)
                suit.finalPosition = Vec3(x, y, z)
                suit.flattenStrong()
                suit.hide()
                self.flyingInCogs.append(suit)

        self.chopper = Actor('phase_4/models/char/cogChopper_ctc_zero', {'fly': 'phase_4/models/char/cogChopper_ctc_fly'})
        self.chopper.reparentTo(geom)
        self.chopper.setHpr(270, 0, 0)
        self.startIntroSequence()
        return

    def startIntroSequence(self):
        self.introSequence = Sequence(Func(camera.wrtReparentTo, self.getGeom()), Func(self.chopper.pingpong, 'fly', fromFrame=0, toFrame=200), camera.posHprInterval(2, (-146, -98, 9), (-56, 0, 0), blendType='easeInOut'), Wait(2), Parallel(camera.posHprInterval(2, (-105.5, -42.5, 18.5), (-40, -12.5, 0), blendType='easeInOut'), Sequence(Wait(0.7), self.__makeEscapingToonMovies())), Wait(1.5), Parallel(camera.posHprInterval(2, (-106.5, -43.5, 18.5), (-46, 7.5, 0), blendType='easeInOut'), self.__makeCogFlyInMovie(2.0), Sequence(Wait(2.5), self.chopper.actorInterval('fly', startFrame=200, endFrame=395), Func(self.__deleteChopper))), camera.posHprInterval(3, (-146, -98, 9), (-56, 0, 0), blendType='easeInOut'), Wait(1), Func(self.__talkSuit, self.getHollywood(), TTLocalizer.TutorialHollywoodMessage1, self.__doneIntroScene1))
        self.introSequence.start()

    def __talkSuit(self, suit, message, callback):
        self.tvScreen.chatGui.setButtonState(False)
        suit.setLocalPageChat(message, 0)
        self.acceptOnce(suit.uniqueName('doneChatPage'), callback)

    def __switchSceneSequence(self, nextScene, message, sound):
        chatGui = self.tvScreen.chatGui
        chatGui.setButtonState(False)
        self.introSequence = Sequence(Wait(0.5), Func(self.tvScreen.showScene, 'static'), Func(chatGui.show), Wait(0.5), Func(self.tvScreen.showScene, nextScene), Func(self.__playTextChat, message, sound))
        self.introSequence.start()

    def __playTextChat(self, chat, sound):
        chatGui = self.tvScreen.chatGui
        chatGui.setButtonState(True)
        chatGui.playTextSound(chat, sound)
        self.acceptOnce(chatGui.getCallbackEvent(), self.__doneChatGui)

    def __doneChatGui(self, stage):
        if stage == 1:
            self.__playTextChat(TTLocalizer.TutorialChairmanMessage2, 'question')
        elif stage == 2:
            self.__talkSuit(self.getHollywood(), TTLocalizer.TutorialHollywoodMessage3, lambda _: self.__playTextChat(TTLocalizer.TutorialChairmanMessage3, 'statement'))
        elif stage == 3:
            self.__playTextChat(TTLocalizer.TutorialChairmanMessage4, 'statement')
        elif stage == 4:
            self.__playTextChat(TTLocalizer.TutorialChairmanMessage5, 'exclaim')
        elif stage == 5:
            self.__playTextChat(TTLocalizer.TutorialChairmanMessage6, 'statement')
        elif stage == 6:
            self.__playTextChat(TTLocalizer.TutorialChairmanMessage7, 'statement')
        elif stage == 7:
            hollywood = self.getHollywood()
            self.__talkSuit(hollywood, TTLocalizer.TutorialHollywoodMessage4, self.__doneIntroScene3)
            self.accept(hollywood.uniqueName('nextChatPage'), self.__nextIntroScene3)
        elif stage == 8:
            self.__playTextChat(TTLocalizer.TutorialCEOMessage2, 'statement')
        elif stage == 9:
            self.__talkSuit(self.getHollywood(), TTLocalizer.TutorialHollywoodMessage5, lambda _: self.__playTextChat(TTLocalizer.TutorialCEOMessage3, 'statement'))
        elif stage == 10:
            self.__switchSceneSequence('scientist', TTLocalizer.TutorialScientistMessage1, 'duck_question')
        elif stage == 11:
            self.tvScreen.scene.startTask()
            self.__playTextChat(TTLocalizer.TutorialScientistMessage2, ['duck_exclaim', 'furious'])
        elif stage == 12:
            self.__playTextChat(TTLocalizer.TutorialScientistMessage3, 'duck_exclaim')
        elif stage == 13:
            self.tvScreen.scene.stopTask()
            self.__switchSceneSequence('ceo', TTLocalizer.TutorialCEOMessage4, 'question')
        elif stage == 14:
            self.__talkSuit(self.getHollywood(), TTLocalizer.TutorialHollywoodMessage6, lambda _: self.__playTextChat(TTLocalizer.TutorialCEOMessage5, 'statement'))
        elif stage == 15:
            self.__playTextChat(TTLocalizer.TutorialCEOMessage6, 'question')
        elif stage == 16:
            self.__talkSuit(self.getRaider(), TTLocalizer.TutorialRaiderMessage2, lambda _: self.__playTextChat(TTLocalizer.TutorialCEOMessage7, 'statement'))
        elif stage == 17:
            self.__talkSuit(self.getRaider(), TTLocalizer.TutorialRaiderMessage3, self.__doneIntroScene4)
        elif stage == 18:
            self.__playTextChat(TTLocalizer.TutorialCEOMessage9, 'exclaim')
        elif stage == 19:
            self.__playTextChat(TTLocalizer.TutorialCEOMessage10, 'exclaim')
        elif stage == 20:
            self.__talkSuit(self.getRaider(), TTLocalizer.TutorialRaiderMessage4, self.__doneIntroAftermatch)

    def __doneIntroScene1(self, elapsed):
        self.__talkSuit(self.getRaider(), TTLocalizer.TutorialRaiderMessage1, self.__doneIntroScene2)

    def __doneIntroScene2(self, elapsed):
        self.__talkSuit(self.getHollywood(), TTLocalizer.TutorialHollywoodMessage2, lambda _: self.__switchSceneSequence('gyro', TTLocalizer.TutorialChairmanMessage1, 'question'))

    def __nextIntroScene3(self, pageNumber, elapsed):
        if pageNumber == 1:
            self.tvScreen.chatGui.hide()
            self.tvScreen.showScene('gray')

    def __doneIntroScene3(self, elapsed):
        hollywood = self.getHollywood()
        self.ignore(hollywood.uniqueName('nextChatPage'))
        self.__switchSceneSequence('ceo', TTLocalizer.TutorialCEOMessage1, 'question')

    def __doneIntroScene4(self, elapsed):
        hollywood = self.getHollywood()
        hollywood.loop('walk')
        self.tvScreen.chatGui.hide()
        self.introSequence = Parallel(Sequence(hollywood.hprInterval(1.5, getHeadsUpHpr(hollywood.getPos(), base.localAvatar.getPos())), Func(hollywood.loop, 'neutral'), Func(self.__talkSuit, hollywood, TTLocalizer.TutorialHollywoodMessage7, self.__doneIntroScene5)), camera.posInterval(1.5, base.localAvatar.getPos() + Vec3(-5, -2, base.localAvatar.getHeight())))
        self.introSequence.start()

    def __doneIntroScene5(self, elapsed):
        base.localAvatar.laffMeter.obscure(False)
        base.cr.tutorialManager.d_requestStage('introFight')

    def startIntroAftermatch(self):
        NametagGlobals.setMasterArrowsOn(False)
        camera.wrtReparentTo(self.getGeom())
        base.localAvatar.laffMeter.obscure(True)
        self.tvScreen.showScene('ceo')
        self.introSequence = Sequence(camera.posHprInterval(3, (-146, -98, 9), (304, 0, 0), blendType='easeInOut'), Func(self.playground.fsm.request, 'walk'), Func(self.playground.fsm.request, 'stopped'), Func(base.localAvatar.laffMeter.obscure, True), Func(camera.reparentTo, self.getGeom()), Func(camera.setPosHpr, -146, -98, 9, 304, 0, 0), Emote.globalEmote.doEmote(base.localAvatar, TTEmote.Emotes.index('laugh'), 0, start=False)[0], Wait(2), Func(self.tvScreen.chatGui.show), Func(self.__playTextChat, TTLocalizer.TutorialCEOMessage8, []))
        self.introSequence.start()

    def __doneIntroAftermatch(self, elapsed):
        raider = self.getRaider()
        raider.headsUp(base.localAvatar)
        self.tvScreen.chatGui.hide()
        soundTrack, eyeTrack, suitTrack = self.__makeEvilEyeMovies(raider, tuple(base.localAvatar.getPos()))
        toonTrack = Sequence(Wait(3.91), Func(base.localAvatar.animFSM.request, 'Died'))
        self.acceptOnce(base.localAvatar.uniqueName('died'), self.__doneIntroDeath)
        self.introSequence = Parallel(eyeTrack, suitTrack, toonTrack, soundTrack)
        self.introSequence.start()

    def __doneIntroDeath(self):
        self.playground.doRequestLeave({'loader': 'townLoader',
         'where': 'street',
         'how': 'teleportIn',
         'hoodId': ToontownGlobals.CogtownCentral,
         'zoneId': ZoneUtil.tutorialDict['exteriors'][1],
         'shardId': None,
         'avId': -1,
         'tutorial': 1,
         'battle': True})
        return