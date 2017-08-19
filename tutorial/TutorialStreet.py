# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.TutorialStreet
from panda3d.core import Texture
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from otp.nametag.NametagConstants import CFSpeech
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui import GUIUtils
from toontown.suit.Suit import Suit
from toontown.suit.SuitDNA import SuitDNA
from toontown.hood import ZoneUtil
from CreditScreen import CreditScreen
from TutorialUtil import *
SuitNewPos = [(-35, 5, 0), (-35, -5, 0), (-30, 0, 0)]

class TutorialStreet(DirectObject):

    def __init__(self, street):
        self.street = street
        self.loaded = False
        self.entered = False
        self.movieDone = False

    def uniqueName(self, name):
        return 'TutorialStreet-%s-%s' % (id(self), name)

    def getStreet(self):
        return self.street

    def getGeom(self):
        return self.street.loader.geom

    def isEnding(self):
        return hasattr(self, 'suits')

    def getStatic(self):
        return loader.loadMusic('phase_4/videos/static.mp4')

    def load(self):
        if self.loaded:
            return
        self.suit = createSuit(self, 'cr', (188.5, 24.5, -0.475, 250, 0, 0), active=True, type=DistributedSuit)
        self.interior = loader.loadModel('phase_4/models/modules/toon_outpost_interior')
        self.interior.setColorScale(0.8, 0.8, 0.8, 1)
        self.suits = []
        for suit in (['ss', (-25, 15, 0), 135], ['kc', (-25, -15, 0), 45], ['ru', (-15, 0, 0), 90]):
            suitName, pos, h = suit
            dna = SuitDNA()
            dna.newSuit(suitName)
            suit = Suit()
            suit.reparentTo(self.interior)
            suit.setDNA(dna)
            suit.setPos(*pos)
            suit.setH(h)
            suit.loop('neutral')
            suit.setDisplayLevel()
            self.suits.append(suit)

        self.static = GUIUtils.loadTextureModel(loader.loadTexture('phase_3.5/maps/screen_static.jpg'), transparency=True)
        self.static.setScale(30, 1, 3)
        self.static.setColorScale(1, 1, 1, 0.3)
        self.credits = CreditScreen()
        self.loaded = True

    def unload(self):
        if not self.loaded:
            return
        else:
            cleanupActor(self.suit)
            if self.text:
                self.text.destroy()
                self.text = None
            if self.credits:
                self.credits.removeNode()
                self.credits = None
            self.interior.removeNode()
            for suit in self.suits:
                suit.delete()

            self.static.removeNode()
            self.suit = None
            self.interior = None
            self.suits = None
            self.static = None
            self.loaded = False
            return

    def enter(self):
        if self.entered:
            return
        else:
            self.entered = True
            self.movie = None
            if not self.movieDone:
                base.cr.tutorialManager.d_requestStage('ending')
                self.acceptOnce('enterWalk', self.startMovie)
                self.movieDone = True
            taskMgr.doMethodLater(0.2, self.__watchPos, self.uniqueName('watchPos'))
            return

    def exit(self):
        if not self.entered:
            return
        else:
            if self.movie and self.movie.isPlaying():
                self.movie.pause()
            self.movie = None
            self.entered = False
            taskMgr.remove(self.uniqueName('watchPos'))
            taskMgr.remove(self.uniqueName('goAway'))
            return

    def startMovie(self):
        self.street.fsm.request('stopped')
        self.oldCamPos = camera.getPos(self.getGeom())
        self.oldCamHpr = camera.getHpr(self.getGeom())
        base.localAvatar.setPreventSleepWatch(True)
        self.movie = Sequence(Func(camera.wrtReparentTo, self.getGeom()), camera.posHprInterval(2, (207.5, 17.5, 4.85), (70, 0, 0), blendType='easeInOut'), Func(self.suit.setLocalPageChat, TTLocalizer.TutorialRaiderTalk, 0))
        self.acceptOnce(self.suit.uniqueName('doneChatPage'), self.__endTalk)
        self.movie.start()

    def cleanupSuit(self):
        cleanupActor(self.suit)
        self.suit = None
        return

    def __endTalk(self, elapsed):
        self.suit.removeActive()
        self.movie = Parallel(Sequence(self.suit.beginSupaFlyMove(self.suit.getPos(), False, 'toSky', False), Func(self.cleanupSuit)), Sequence(Wait(2), camera.posHprInterval(2, self.oldCamPos, self.oldCamHpr, blendType='easeInOut'), Func(self.street.fsm.request, 'walk'), Func(base.localAvatar.laffMeter.obscure, False), Func(base.localAvatar.setPreventSleepWatch, False)))
        self.movie.start()

    def __watchPos(self, task):
        if localAvatar.getX(self.getGeom()) < 45.0:
            self.__startEnding()
            return task.done
        return task.again

    def getSuitWalkSequences(self):
        parallel = Parallel()
        for i, suit in enumerate(self.suits):
            parallel.append(Sequence(Wait(i * 0.5), Func(suit.loop, 'walk'), suit.posInterval(1.5, SuitNewPos[i]), Func(suit.loop, 'neutral'), Func(suit.setChatAbsolute, TTLocalizer.TutorialEndSuitTalk[i], CFSpeech)))

        return parallel

    def __startEnding(self):
        self.text = DirectLabel(aspect2dp, relief=None, text=TTLocalizer.TutorialBloodyText, text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.1, text_fg=(1, 0, 0, 1), text_shadow=(0, 0, 0, 1), pos=(0, 0, 0.1))
        Sequence(Func(base.localAvatar.setPreventSleepWatch, True), Func(base.transitions.fadeOut, 1), self.text.colorScaleInterval(1, (1, 0, 0, 1), (1, 0, 0, 0)), Func(self.street.loader.music.stop), Func(self.street.loader.thunderSfx.stop), Func(self.street.fsm.request, 'stopped'), Func(base.localAvatar.laffMeter.hide), Func(camera.reparentTo, self.interior), Func(camera.setPosHpr, -56, 0.36, 18.7, 270, -30, 0), Wait(3.5), self.text.colorScaleInterval(1, (1, 0, 0, 0), (1, 0, 0, 1)), Func(base.transitions.fadeIn, 1), Func(self.static.reparentTo, aspect2d), Func(base.playMusic, self.getStatic(), looping=True, volume=0.35), Wait(4.5), Func(base.localAvatar.reparentTo, self.interior), Func(base.localAvatar.setH, 270), Func(base.localAvatar.loop, 'walk'), base.localAvatar.posInterval(1, (-40, 0, 0), (-45, 0, 0)), Func(base.localAvatar.loop, 'neutral'), Parallel(Sequence(Wait(1), Func(base.localAvatar.sadEyes), Func(base.localAvatar.blinkEyes), Func(base.localAvatar.loop, 'walk'), base.localAvatar.hprInterval(2, (90, 0, 0), (270, 0, 0)), Func(base.localAvatar.loop, 'run'), base.localAvatar.posInterval(1, (-45, 0, 0))), self.getSuitWalkSequences()), Func(base.localAvatar.normalEyes), Func(base.localAvatar.blinkEyes), Func(base.localAvatar.reparentTo, render), Func(camera.reparentTo, base.localAvatar), Func(base.transitions.fadeOut, 0), Func(base.transitions.fade.setColor, 0, 0, 0, 1), Func(self.getStatic().stop), Wait(2.5), Parallel(Parallel(base.transitions.fade.colorInterval(2, (0, 0.75, 1, 1), (0, 0, 0, 1)), SoundInterval(loader.loadSfx('phase_4/audio/sfx/avatar_emotion_very_sad.ogg'), volume=1.4)), Sequence(Wait(2.5), Parallel(base.transitions.fade.colorInterval(2.6, (1, 0, 0, 1), (0, 0.75, 1, 1)), SoundInterval(loader.loadSfx('phase_5/audio/sfx/ENC_Lose.ogg'), volume=1.4)))), Func(base.transitions.fade.setColor, 0.2, 0.2, 0.2, 1), Wait(4), Func(render.setColorScale, 1, 1, 1, 1), Func(self.credits.fadeOut), Func(self.credits.start)).start()
        self.accept('creditsOver', self.__creditsOver)
        return

    def __creditsOver(self):
        base.localAvatar.cantLeaveGame = 0
        base.localAvatar.setPreventSleepWatch(False)
        base.cr.tutorialManager.d_allDone()
        ZoneUtil.overrideOff()
        self.credits.removeNode()
        self.credits = None
        taskMgr.doMethodLater(1, self.__goAway, self.uniqueName('goAway'))
        return

    def __goAway(self, task = None):
        base.localAvatar.experience.zeroOutExp()
        base.localAvatar.inventory.updateGUI()
        self.unload()
        self.street.doRequestLeave({'loader': 'safeZoneLoader',
         'where': 'playground',
         'how': 'teleportIn',
         'hoodId': ToontownGlobals.ToontownCentral,
         'zoneId': ToontownGlobals.ToontownCentral,
         'shardId': -1,
         'avId': -1})