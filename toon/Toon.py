# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.Toon
from panda3d.direct import HideInterval, ShowInterval
from panda3d.core import CollideMask, ColorBlendAttrib, GeomNode, NodePath, PartBundle, Plane, Point3, Texture, VBase3, VBase4, Vec3, headsUp
from direct.actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
import random
import types
import math
import AccessoryGlobals
import Motion
import TTEmote
import ToonDNA
import LaffMeter
from ToonHead import *
from otp.ai.MagicWordGlobal import *
from otp.avatar import Avatar
from otp.avatar import Emote
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from toontown.battle import SuitBattleGlobals
from otp.nametag.NametagConstants import *
from toontown.distributed import DelayDelete
from toontown.effects import DustCloud
from toontown.effects import Wake
from toontown.hood import ZoneUtil
from otp.nametag.NametagGroup import *
from toontown.suit import SuitDNA
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
AllAnims = ['angry',
 'applause',
 'bad-putt',
 'badloop-putt',
 'bank',
 'battlecast',
 'book',
 'bored',
 'bow',
 'callPet',
 'cast',
 'castlong',
 'catch-eatneutral',
 'catch-eatnrun',
 'catch-intro-throw',
 'catch-neutral',
 'catch-run',
 'climb',
 'confused',
 'conked',
 'cringe',
 'curtsy',
 'down',
 'duck',
 'feedPet',
 'firehose',
 'fish-again',
 'fish-end',
 'fish-neutral',
 'give-props',
 'give-props-start',
 'good-putt',
 'happy-dance',
 'headdown-putt',
 'hold-bottle',
 'hold-magnet',
 'hypnotize',
 'into-putt',
 'juggle',
 'jump',
 'jump-idle',
 'jump-land',
 'jump-squat',
 'left',
 'left-point',
 'leverNeutral',
 'leverPull',
 'leverReach',
 'look-putt',
 'lookloop-putt',
 'loop-dig',
 'loop-putt',
 'lose',
 'melt',
 'neutral',
 'periscope',
 'pet-end',
 'pet-loop',
 'pet-start',
 'phoneBack',
 'phoneNeutral',
 'pole',
 'pole-neutral',
 'push',
 'pushbutton',
 'reel',
 'reel-H',
 'reel-neutral',
 'right',
 'right-hand',
 'right-hand-start',
 'right-point',
 'right-point-start',
 'rotateL-putt',
 'rotateR-putt',
 'run',
 'running-jump',
 'running-jump-idle',
 'running-jump-land',
 'running-jump-squat',
 'sad-neutral',
 'sad-walk',
 'scientistEmcee',
 'scientistGame',
 'scientistJealous',
 'scientistWork',
 'shrug',
 'sidestep-left',
 'sidestep-right',
 'sit',
 'sit-start',
 'slip-backward',
 'slip-forward',
 'smooch',
 'sound',
 'spit',
 'sprinkle-dust',
 'start-dig',
 'struggle',
 'swim',
 'swing',
 'swing-putt',
 'takePhone',
 'taunt',
 'teleport',
 'think',
 'throw',
 'tickle',
 'toss',
 'tug-o-war',
 'up',
 'victory',
 'walk',
 'water',
 'water-gun',
 'wave']
LegDict = {'s': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_',
 'm': 'phase_3.5/models/char/tt_a_chr_dgm_shorts_legs_',
 'l': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_'}
TorsoDict = {'ss': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_',
 'ms': 'phase_3.5/models/char/tt_a_chr_dgm_shorts_torso_',
 'ls': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_',
 'sd': 'phase_3.5/models/char/tt_a_chr_dgs_skirt_torso_',
 'md': 'phase_3.5/models/char/tt_a_chr_dgm_skirt_torso_',
 'ld': 'phase_3.5/models/char/tt_a_chr_dgl_skirt_torso_'}
LegsAnimDict = {}
TorsoAnimDict = {}
HeadAnimDict = {}
DialogueTypes = ('short',
 'med',
 'long',
 'question',
 'exclaim',
 'howl')
DialogueDict = {}
for i, pair in enumerate([(HeadDict, HeadAnimDict), (TorsoDict, TorsoAnimDict), (LegDict, LegsAnimDict)]):
    sourceDict, targetDict = pair
    for key, value in sourceDict.iteritems():
        if i != 0 or 'd' in key:
            targetDict[key] = {anim:value + anim for anim in AllAnims}

DialogueDict = {species:[ loader.loadSfx('phase_3.5/audio/dial/AV_%s_%s.ogg' % (speciesName, dialogue)) for dialogue in DialogueTypes ] for species, speciesName in ToonDNA.toonSpeciesNames.iteritems()}

def reconsiderAllToonsUnderstandable():
    for av in Avatar.Avatar.ActiveAvatars:
        if isinstance(av, Toon) and not av.isDisguised:
            av.considerUnderstandable()


class Toon(Avatar.Avatar, ToonHead):
    notify = DirectNotifyGlobal.directNotify.newCategory('Toon')
    afkTimeout = config.GetInt('afk-timeout', 600)

    def __init__(self):
        Avatar.Avatar.__init__(self)
        ToonHead.__init__(self)
        self.forwardSpeed = 0.0
        self.rotateSpeed = 0.0
        self.avatarType = 'toon'
        self.motion = Motion.Motion(self)
        self.standWalkRunReverse = None
        self.playingAnim = None
        self.soundTeleport = None
        self.cheesyEffect = ToontownGlobals.CENormal
        self.effectTrack = None
        self.emoteTrack = None
        self.emote = None
        self.stunTrack = None
        self.__bookActor = None
        self.__holeActor = None
        self.wake = None
        self.lastWakeTime = 0
        self.forceJumpIdle = False
        self.numPies = 0
        self.pieType = 0
        self.pieThrowType = ToontownGlobals.PieThrowArc
        self.pieModel = None
        self.__pieModelType = None
        self.pieScale = 1.0
        self.hatNodes = []
        self.glassesNodes = []
        self.backpackNodes = []
        self.isStunned = 0
        self.isDisguised = 0
        self.defaultColorScale = None
        self.jar = None
        self.headMeter = None
        self.gmIcon = None
        self.partyHat = None
        self.lookAtSeq = None
        self.style = None
        self.setTag('pieCode', str(ToontownGlobals.PieCodeToon))
        self.setFont(ToontownGlobals.getToonFont())
        self.nametag.setSpeechFont(ToontownGlobals.getToonFont())
        self.soundChatBubble = loader.loadSfx('phase_3/audio/sfx/GUI_balloon_popup.ogg')
        self.swimRunSfx = loader.loadSfx('phase_4/audio/sfx/AV_footstep_runloop_water.ogg')
        self.animFSM = ClassicFSM('Toon', [State('off', self.enterOff, self.exitOff),
         State('neutral', self.enterNeutral, self.exitNeutral),
         State('victory', self.enterVictory, self.exitVictory),
         State('Happy', self.enterHappy, self.exitHappy),
         State('Sad', self.enterSad, self.exitSad),
         State('Catching', self.enterCatching, self.exitCatching),
         State('CatchEating', self.enterCatchEating, self.exitCatchEating),
         State('Sleep', self.enterSleep, self.exitSleep),
         State('walk', self.enterWalk, self.exitWalk),
         State('jumpSquat', self.enterJumpSquat, self.exitJumpSquat),
         State('jump', self.enterJump, self.exitJump),
         State('jumpAirborne', self.enterJumpAirborne, self.exitJumpAirborne),
         State('jumpLand', self.enterJumpLand, self.exitJumpLand),
         State('run', self.enterRun, self.exitRun),
         State('swim', self.enterSwim, self.exitSwim),
         State('swimhold', self.enterSwimHold, self.exitSwimHold),
         State('dive', self.enterDive, self.exitDive),
         State('cringe', self.enterCringe, self.exitCringe),
         State('OpenBook', self.enterOpenBook, self.exitOpenBook, ['ReadBook', 'CloseBook']),
         State('ReadBook', self.enterReadBook, self.exitReadBook),
         State('CloseBook', self.enterCloseBook, self.exitCloseBook),
         State('TeleportOut', self.enterTeleportOut, self.exitTeleportOut),
         State('Died', self.enterDied, self.exitDied),
         State('TeleportedOut', self.enterTeleportedOut, self.exitTeleportedOut),
         State('TeleportIn', self.enterTeleportIn, self.exitTeleportIn),
         State('Emote', self.enterEmote, self.exitEmote),
         State('SitStart', self.enterSitStart, self.exitSitStart),
         State('Sit', self.enterSit, self.exitSit),
         State('Push', self.enterPush, self.exitPush),
         State('Squish', self.enterSquish, self.exitSquish),
         State('FallDown', self.enterFallDown, self.exitFallDown),
         State('GolfPuttLoop', self.enterGolfPuttLoop, self.exitGolfPuttLoop),
         State('GolfRotateLeft', self.enterGolfRotateLeft, self.exitGolfRotateLeft),
         State('GolfRotateRight', self.enterGolfRotateRight, self.exitGolfRotateRight),
         State('GolfPuttSwing', self.enterGolfPuttSwing, self.exitGolfPuttSwing),
         State('GolfGoodPutt', self.enterGolfGoodPutt, self.exitGolfGoodPutt),
         State('GolfBadPutt', self.enterGolfBadPutt, self.exitGolfBadPutt),
         State('Flattened', self.enterFlattened, self.exitFlattened),
         State('CogThiefRunning', self.enterCogThiefRunning, self.exitCogThiefRunning),
         State('ScientistJealous', self.enterScientistJealous, self.exitScientistJealous),
         State('ScientistEmcee', self.enterScientistEmcee, self.exitScientistEmcee),
         State('ScientistWork', self.enterScientistWork, self.exitScientistWork),
         State('ScientistLessWork', self.enterScientistLessWork, self.exitScientistLessWork),
         State('ScientistPlay', self.enterScientistPlay, self.enterScientistPlay)], 'off', 'off')
        animStateList = self.animFSM.getStates()
        self.animFSM.enterInitialState()
        return

    def uniqueName(self, name):
        return '%s-%s' % (name, id(self))

    def stopAnimations(self):
        if hasattr(self, 'animFSM'):
            if not self.animFSM.isInternalStateInFlux():
                self.animFSM.request('off')
            else:
                self.notify.warning('animFSM in flux, state=%s, not requesting off' % self.animFSM.getCurrentState().getName())
        else:
            self.notify.warning('animFSM has been deleted')
        if self.effectTrack != None:
            self.effectTrack.finish()
            self.effectTrack = None
        if self.emoteTrack != None:
            self.emoteTrack.finish()
            self.emoteTrack = None
        if self.stunTrack != None:
            self.stunTrack.finish()
            self.stunTrack = None
        if self.wake:
            self.wake.stop()
            self.wake.destroy()
            self.wake = None
        self.cleanupPieModel()
        return

    def delete(self):
        try:
            self.Toon_deleted
        except:
            self.Toon_deleted = 1
            self.stopAnimations()
            self.rightHand = None
            self.leftHand = None
            self.headParts = None
            self.torsoParts = None
            self.hipsParts = None
            self.legsParts = None
            del self.animFSM
            if self.__bookActor:
                self.__bookActor.cleanup()
            del self.__bookActor
            if self.__holeActor:
                self.__holeActor.cleanup()
            del self.__holeActor
            self.soundTeleport = None
            self.motion.delete()
            self.motion = None
            self.stopPermanentLookAt()
            self.removeHeadMeter()
            self.removeGMIcon()
            self.removePartyHat()
            Avatar.Avatar.delete(self)
            ToonHead.delete(self)

        return

    def updateToonDNA(self, newDNA, fForce = 0):
        self.style.gender = newDNA.getGender()
        oldDNA = self.style
        if fForce or newDNA.head != oldDNA.head:
            self.swapToonHead(newDNA.head)
        if fForce or newDNA.torso != oldDNA.torso:
            self.swapToonTorso(newDNA.torso, genClothes=0)
            self.loop('neutral')
        if fForce or newDNA.legs != oldDNA.legs:
            self.swapToonLegs(newDNA.legs)
        if fForce or newDNA.hat != oldDNA.hat:
            self.generateHat(newDNA.hat)
        if fForce or newDNA.glasses != oldDNA.glasses:
            self.generateGlasses(newDNA.glasses)
        if fForce or newDNA.backpack != oldDNA.backpack:
            self.generateBackpack(newDNA.backpack)
        if fForce or newDNA.shoes != oldDNA.shoes:
            self.generateShoes(newDNA.shoes)
        self.swapToonColor(newDNA)
        self.__swapToonClothes(newDNA)

    def setDNAString(self, dnaString):
        newDNA = ToonDNA.ToonDNA()
        newDNA.makeFromNetString(dnaString)
        if len(newDNA.torso) < 2:
            self.sendLogSuspiciousEvent('nakedToonDNA %s was requested' % newDNA.torso)
            newDNA.torso = newDNA.torso + 's'
        self.setDNA(newDNA)
        if hasattr(self, 'laffMeter'):
            self.laffMeter.updateColor()

    def setDNA(self, dna):
        if hasattr(self, 'isDisguised'):
            if self.isDisguised:
                return
        if self.style:
            self.updateToonDNA(dna)
            if settings['smoothAnimations']:
                self.setBlend(frameBlend=True)
        else:
            self.style = dna
            self.generateToon()
            self.initializeDropShadow()
            self.initializeNametag3d()

    def parentToonParts(self):
        if not self.getPart('torso').find('**/def_head').isEmpty():
            self.attach('head', 'torso', 'def_head')
        else:
            self.attach('head', 'torso', 'joint_head')
        self.attach('torso', 'legs', 'joint_hips')

    def unparentToonParts(self):
        for part in ('head', 'torso', 'legs'):
            self.getPart(part).reparentTo(self.getGeomNode())

    def generateToon(self):
        self.generateToonLegs()
        self.generateToonHead()
        self.generateToonTorso()
        self.generateToonColor()
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        self.setupToonNodes()
        self.generateToonAccessories()

    def setupToonNodes(self):
        torso = self.getPart('torso')
        if not torso.find('**/def_joint_right_hold').isEmpty():
            self.rightHand = torso.find('**/def_joint_right_hold')
            self.leftHand = torso.find('**/def_joint_left_hold')
        else:
            self.rightHand = torso.find('**/joint_Rhold')
            self.leftHand = torso.find('**/joint_Lhold')
        self.headParts = self.findAllMatches('**/__Actor_head')
        self.legsParts = self.findAllMatches('**/__Actor_legs')
        self.hipsParts = self.legsParts.findAllMatches('**/joint_hips')
        self.torsoParts = self.hipsParts.findAllMatches('**/__Actor_torso')
        if settings['smoothAnimations']:
            self.setBlend(frameBlend=True)

    def initializeBodyCollisions(self, collIdStr):
        Avatar.Avatar.initializeBodyCollisions(self, collIdStr)
        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)

    def getBookActor(self):
        if not self.__bookActor:
            self.__bookActor = Actor.Actor('phase_3.5/models/props/book-mod', {'book': 'phase_3.5/models/props/book-chan'})
            self.__bookActor.reparentTo(self.rightHand)
            self.__bookActor.hide()
        return self.__bookActor

    def getHoleActor(self):
        if not self.__holeActor:
            self.__holeActor = Actor.Actor('phase_3.5/models/props/portal-mod', {'hole': 'phase_3.5/models/props/portal-chan'})
        return self.__holeActor

    def rescaleToon(self):
        animalStyle = self.style.getAnimal()
        bodyScale = ToontownGlobals.toonBodyScales[animalStyle]
        headScale = ToontownGlobals.toonHeadScales[animalStyle]
        self.setAvatarScale(bodyScale)
        self.getPart('head').setScale(headScale)

    def getBodyScale(self):
        animalStyle = self.style.getAnimal()
        bodyScale = ToontownGlobals.toonBodyScales[animalStyle]
        return bodyScale

    def resetHeight(self):
        if hasattr(self, 'style') and self.style:
            animal = self.style.getAnimal()
            bodyScale = ToontownGlobals.toonBodyScales[animal]
            headScale = ToontownGlobals.toonHeadScales[animal][2]
            shoulderHeight = ToontownGlobals.legHeightDict[self.style.legs] * bodyScale + ToontownGlobals.torsoHeightDict[self.style.torso] * bodyScale
            height = shoulderHeight + ToontownGlobals.headHeightDict[self.style.head] * headScale
            self.shoulderHeight = shoulderHeight
            if self.cheesyEffect == ToontownGlobals.CEBigToon or self.cheesyEffect == ToontownGlobals.CEBigWhite:
                height *= ToontownGlobals.BigToonScale
            elif self.cheesyEffect == ToontownGlobals.CESmallToon:
                height *= ToontownGlobals.SmallToonScale
            self.setHeight(height)

    def generateToonLegs(self):
        legStyle = self.style.legs
        filePrefix = LegDict.get(legStyle)
        if filePrefix is None:
            self.notify.error('unknown leg style: %s' % legStyle)
        self.loadModel(loader.loadModel(filePrefix + '1000', customOptions={'flatten': 'medium'}), 'legs')
        self.loadAnims(LegsAnimDict[legStyle], 'legs')
        self.findAllMatches('**/boots_short').stash()
        self.findAllMatches('**/boots_long').stash()
        self.findAllMatches('**/shoes').stash()
        return

    def swapToonLegs(self, legStyle):
        self.unparentToonParts()
        self.removePart('legs')
        if 'legs' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['legs']
        self.style.legs = legStyle
        self.generateToonLegs()
        self.generateToonColor()
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        self.initializeDropShadow()
        self.initializeNametag3d()
        self.generateShoes()

    def generateToonTorso(self, genClothes = 1):
        torsoStyle = self.style.torso
        filePrefix = TorsoDict.get(torsoStyle)
        if filePrefix is None:
            self.notify.error('unknown torso style: %s' % torsoStyle)
        self.loadModel(loader.loadModel(filePrefix + '1000', customOptions={'flatten': 'medium'}), 'torso')
        self.loadAnims(TorsoAnimDict[torsoStyle], 'torso')
        if genClothes == 1 and not len(torsoStyle) == 1:
            self.generateToonClothes()
        return

    def swapToonTorso(self, torsoStyle, genClothes = 1):
        self.unparentToonParts()
        self.removePart('torso')
        if 'torso' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['torso']
        self.style.torso = torsoStyle
        self.generateToonTorso(genClothes)
        self.generateToonColor()
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        self.setupToonNodes()
        self.generateBackpack()

    def generateToonHead(self):
        ToonHead.generateToonHead(self, self.style)
        if self.style.getAnimal() == 'dog':
            self.loadAnims(HeadAnimDict[self.style.head], 'head')

    def swapToonHead(self, headStyle = -1):
        self.stopLookAroundNow()
        self.eyelids.request('open')
        self.unparentToonParts()
        self.removePart('head')
        if 'head' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['head']
        if headStyle > -1:
            self.style.head = headStyle
        self.generateToonHead()
        self.generateToonColor()
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        self.eyelids.request('open')
        self.startLookAround()
        self.generateHat()
        self.generateGlasses()

    def generateToonColor(self):
        ToonHead.generateToonColor(self, self.style)
        armColor = self.style.getArmColor()
        gloveColor = self.style.getGloveColor()
        legColor = self.style.getLegColor()
        torso = self.getPart('torso')
        legs = self.getPart('legs')
        if len(self.style.torso) == 1:
            torso.findAllMatches('**/torso*').setColor(*armColor)
        for pieceName in ('arms', 'neck'):
            torso.find('**/' + pieceName).setColor(*armColor)

        for pieceName in ('legs', 'feet'):
            legs.find('**/%s;+s' % pieceName).setColor(*legColor)

        torso.find('**/hands').setColor(*gloveColor)
        if self.cheesyEffect == ToontownGlobals.CEGreenToon:
            self.reapplyCheesyEffect()

    def swapToonColor(self, dna):
        self.setStyle(dna)
        self.generateToonColor()

    def __swapToonClothes(self, dna):
        self.setStyle(dna)
        self.generateToonClothes(fromNet=1)

    def sendLogSuspiciousEvent(self, msg):
        pass

    def generateToonClothes(self, fromNet = 0):
        swappedTorso = 0
        if self.style.getGender() == 'f' and fromNet == 0:
            try:
                bottomPair = ToonDNA.GirlBottoms[self.style.botTex]
            except:
                bottomPair = ToonDNA.GirlBottoms[0]

            if len(self.style.torso) < 2:
                self.sendLogSuspiciousEvent('nakedToonDNA %s was requested' % self.style.torso)
                return 0
            if self.style.torso[1] == 's' and bottomPair[1] == ToonDNA.SKIRT:
                self.swapToonTorso(self.style.torso[0] + 'd', genClothes=0)
                swappedTorso = 1
            elif self.style.torso[1] == 'd' and bottomPair[1] == ToonDNA.SHORTS:
                self.swapToonTorso(self.style.torso[0] + 's', genClothes=0)
                swappedTorso = 1
        try:
            texName = ToonDNA.Shirts[self.style.topTex]
        except:
            texName = ToonDNA.Shirts[0]

        shirtTex = loader.loadTexture(texName, okMissing=True)
        if shirtTex is None:
            self.sendLogSuspiciousEvent('failed to load texture %s' % texName)
            shirtTex = loader.loadTexture(ToonDNA.Shirts[0])
        shirtTex.setMinfilter(Texture.FTLinearMipmapLinear)
        shirtTex.setMagfilter(Texture.FTLinear)
        try:
            texName = ToonDNA.Sleeves[self.style.sleeveTex]
        except:
            texName = ToonDNA.Sleeves[0]

        sleeveTex = loader.loadTexture(texName, okMissing=True)
        if sleeveTex is None:
            self.sendLogSuspiciousEvent('failed to load texture %s' % texName)
            sleeveTex = loader.loadTexture(ToonDNA.Sleeves[0])
        sleeveTex.setMinfilter(Texture.FTLinearMipmapLinear)
        sleeveTex.setMagfilter(Texture.FTLinear)
        if self.style.getGender() == 'm':
            try:
                texName = ToonDNA.BoyShorts[self.style.botTex]
            except:
                texName = ToonDNA.BoyShorts[0]

        else:
            try:
                texName = ToonDNA.GirlBottoms[self.style.botTex][0]
            except:
                texName = ToonDNA.GirlBottoms[0][0]

        bottomTex = loader.loadTexture(texName, okMissing=True)
        if bottomTex is None:
            self.sendLogSuspiciousEvent('failed to load texture %s' % texName)
            if self.style.getGender() == 'm':
                bottomTex = loader.loadTexture(ToonDNA.BoyShorts[0])
            else:
                bottomTex = loader.loadTexture(ToonDNA.GirlBottoms[0][0])
        bottomTex.setMinfilter(Texture.FTLinearMipmapLinear)
        bottomTex.setMagfilter(Texture.FTLinear)
        bottomColor = VBase4(self.style.botTexColor)
        darkBottomColor = bottomColor * 0.5
        darkBottomColor.setW(1.0)
        torso = self.getPart('torso')
        top = torso.find('**/torso-top')
        top.setTexture(shirtTex, 1)
        top.setColor(*self.style.topTexColor)
        sleeves = torso.find('**/sleeves')
        sleeves.setTexture(sleeveTex, 1)
        sleeves.setColor(*self.style.sleeveTexColor)
        bottoms = torso.findAllMatches('**/torso-bot')
        for bottomNum in xrange(0, bottoms.getNumPaths()):
            bottom = bottoms.getPath(bottomNum)
            bottom.setTexture(bottomTex, 1)
            bottom.setColor(bottomColor)

        caps = torso.findAllMatches('**/torso-bot-cap')
        caps.setColor(darkBottomColor)
        return swappedTorso

    def generateHat(self, hat = None):
        if not hat:
            hat = self.style.getHat()
        hatType, hatTex = hat
        if hatType >= len(ToonDNA.HatModels) or hatTex >= len(ToonDNA.HatTextures):
            return
        else:
            if self.hatNodes:
                for hatNode in self.hatNodes:
                    hatNode.removeNode()

                self.hatNodes = []
            self.showEars()
            if not hatType:
                return
            hatGeom = loader.loadModel(ToonDNA.HatModels[hatType], okMissing=True)
            if not hatGeom:
                return
            if hatType == 54:
                self.hideEars()
            if hatTex:
                texture = loader.loadTexture(ToonDNA.HatTextures[hatTex], okMissing=True)
                if texture:
                    texture.setMinfilter(Texture.FTLinearMipmapLinear)
                    texture.setMagfilter(Texture.FTLinear)
                    hatGeom.setTexture(texture, 1)
            transOffset = None
            headType = self.style.head[:2]
            if hatType in AccessoryGlobals.ExtendedHatTransTable:
                transOffset = AccessoryGlobals.ExtendedHatTransTable[hatType].get(headType)
            if not transOffset:
                transOffset = AccessoryGlobals.HatTransTable.get(headType)
                if not transOffset:
                    return
            hatGeom.setPosHprScale(*transOffset)
            for headNode in self.headParts:
                hatNode = headNode.attachNewNode('hatNode')
                self.hatNodes.append(hatNode)
                hatGeom.instanceTo(hatNode)

            return

    def generateGlasses(self, glasses = None):
        if not glasses:
            glasses = self.style.getGlasses()
        glassesType, glassesTex = glasses
        if glassesType >= len(ToonDNA.GlassesModels) or glassesTex >= len(ToonDNA.GlassesTextures):
            return
        else:
            if self.glassesNodes:
                for glassesNode in self.glassesNodes:
                    glassesNode.removeNode()

                self.glassesNodes = []
            self.showEyelashes()
            if not glassesType:
                return
            glassesGeom = loader.loadModel(ToonDNA.GlassesModels[glassesType], okMissing=True)
            if not glassesGeom:
                return
            if glassesType in (15, 16):
                self.hideEyelashes()
            if glassesTex:
                texture = loader.loadTexture(ToonDNA.GlassesTextures[glassesTex], okMissing=True)
                if texture:
                    texture.setMinfilter(Texture.FTLinearMipmapLinear)
                    texture.setMagfilter(Texture.FTLinear)
                    glassesGeom.setTexture(texture, 1)
            transOffset = None
            headType = self.style.head[:2]
            if glassesType in AccessoryGlobals.ExtendedGlassesTransTable:
                transOffset = AccessoryGlobals.ExtendedGlassesTransTable[glassesType].get(headType)
            if not transOffset:
                transOffset = AccessoryGlobals.GlassesTransTable.get(headType)
                if not transOffset:
                    return
            glassesGeom.setPosHprScale(*transOffset)
            for headNode in self.headParts:
                glassesNode = headNode.attachNewNode('glassesNode')
                self.glassesNodes.append(glassesNode)
                glassesGeom.instanceTo(glassesNode)

            return

    def generateBackpack(self, backpack = None):
        if not backpack:
            backpack = self.style.getBackpack()
        backpackType, backpackTex = backpack
        if backpackType >= len(ToonDNA.BackpackModels) or backpackTex >= len(ToonDNA.BackpackTextures):
            return
        else:
            if self.backpackNodes:
                for backpackNode in self.backpackNodes:
                    backpackNode.removeNode()

                self.backpackNodes = []
            if not backpackType:
                return
            backpackGeom = loader.loadModel(ToonDNA.BackpackModels[backpackType], okMissing=True)
            if not backpackGeom:
                return
            if backpackTex:
                texture = loader.loadTexture(ToonDNA.BackpackTextures[backpackTex], okMissing=True)
                if texture:
                    texture.setMinfilter(Texture.FTLinearMipmapLinear)
                    texture.setMagfilter(Texture.FTLinear)
                    backpackGeom.setTexture(texture, 1)
            transOffset = None
            torsoType = self.style.torso[:1]
            if backpackType in AccessoryGlobals.ExtendedBackpackTransTable:
                transOffset = AccessoryGlobals.ExtendedBackpackTransTable[backpackType].get(torsoType)
            if not transOffset:
                transOffset = AccessoryGlobals.BackpackTransTable.get(torsoType)
                if not transOffset:
                    return
            backpackGeom.setPosHprScale(*transOffset)
            for torsoNode in self.findAllMatches('**/def_joint_attachFlower'):
                backpackNode = torsoNode.attachNewNode('backpackNode')
                self.backpackNodes.append(backpackNode)
                backpackGeom.instanceTo(backpackNode)

            return

    def generateShoes(self, shoes = None):
        if not shoes:
            shoes = self.style.getShoes()
        shoesType, shoesTex = shoes
        self.findAllMatches('**/boots_short;+s').stash()
        self.findAllMatches('**/boots_long;+s').stash()
        self.findAllMatches('**/shoes;+s').stash()
        self.findAllMatches('**/feet;+s').unstash()
        if shoesType >= len(ToonDNA.ShoesModels) or shoesTex >= len(ToonDNA.ShoesTextures) or not shoesType:
            return
        modelPath = ToonDNA.ShoesModels[shoesType]
        geoms = self.findAllMatches('**/%s;+s' % modelPath)
        textureName = ToonDNA.ShoesTextures[shoesTex]
        if self.style.legs == 'l' and shoesType == 3:
            textureName = textureName[:-4] + 'LL.jpg'
        texture = loader.loadTexture(textureName, okMissing=True)
        if not texture:
            return
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        for geom in geoms:
            geom.unstash()
            geom.setTexture(texture, 1)

        self.findAllMatches('**/feet;+s').stash()

    def generateToonAccessories(self):
        self.generateHat()
        self.generateGlasses()
        self.generateBackpack()
        self.generateShoes()

    def getDialogueArray(self):
        if base.cr.newsManager and base.cr.newsManager.isHolidayRunning(ToontownGlobals.APRIL_TOONS_WEEK):
            return random.choice(DialogueDict.values())
        else:
            return DialogueDict[self.style.head[0]]

    def getShadowJoint(self):
        return self.getPart('legs').find('**/joint_shadow')

    def getNametagJoints(self):
        return [self.getPartBundle('legs').findChild('joint_nameTag')]

    def getRightHand(self):
        return self.rightHand

    def getLeftHand(self):
        return self.leftHand

    def getHeadParts(self):
        return self.headParts

    def getHipsParts(self):
        return self.hipsParts

    def getTorsoParts(self):
        return self.torsoParts

    def getLegsParts(self):
        return self.legsParts

    def findSomethingToLookAt(self):
        if self.randGen.random() < 0.1 or not hasattr(self, 'cr'):
            x = self.randGen.choice((-0.8, -0.5, 0, 0.5, 0.8))
            y = self.randGen.choice((-0.5, 0, 0.5, 0.8))
            self.lerpLookAt(Point3(x, 1.5, y), blink=1)
            return
        nodePathList = []
        for id, obj in self.cr.doId2do.items():
            if hasattr(obj, 'getStareAtNodeAndOffset') and obj != self:
                node, offset = obj.getStareAtNodeAndOffset()
                if node.getY(self) > 0.0:
                    nodePathList.append((node, offset))

        if nodePathList:
            nodePathList.sort(lambda x, y: cmp(x[0].getDistance(self), y[0].getDistance(self)))
            if len(nodePathList) >= 2:
                if self.randGen.random() < 0.9:
                    chosenNodePath = nodePathList[0]
                else:
                    chosenNodePath = nodePathList[1]
            else:
                chosenNodePath = nodePathList[0]
            self.lerpLookAt(chosenNodePath[0].getPos(self), blink=1)
        else:
            ToonHead.findSomethingToLookAt(self)

    def setForceJumpIdle(self, value):
        self.forceJumpIdle = value

    def getWake(self):
        if not self.wake:
            self.wake = Wake.Wake(render, self)
        return self.wake

    def getJar(self):
        if not self.jar:
            self.jar = loader.loadModel('phase_5.5/models/estate/jellybeanJar')
            self.jar.setP(290.0)
            self.jar.setY(0.5)
            self.jar.setZ(0.5)
            self.jar.setScale(0.0)
        return self.jar

    def removeJar(self):
        if self.jar:
            self.jar.removeNode()
            self.jar = None
        return

    def setSpeed(self, forwardSpeed, rotateSpeed):
        self.forwardSpeed = forwardSpeed
        self.rotateSpeed = rotateSpeed
        action = None
        if self.standWalkRunReverse != None:
            if forwardSpeed >= ToontownGlobals.RunCutOff:
                action = OTPGlobals.RUN_INDEX
            elif forwardSpeed > ToontownGlobals.WalkCutOff:
                action = OTPGlobals.WALK_INDEX
            elif forwardSpeed < -ToontownGlobals.WalkCutOff:
                action = OTPGlobals.REVERSE_INDEX
            elif rotateSpeed != 0.0:
                action = OTPGlobals.WALK_INDEX
            else:
                action = OTPGlobals.STAND_INDEX
            anim, rate = self.standWalkRunReverse[action]
            self.motion.enter()
            self.motion.setState(anim, rate)
            if anim != self.playingAnim:
                self.playingAnim = anim
                self.playingRate = rate
                self.stop()
                self.loop(anim)
                self.setPlayRate(rate, anim)
                if self.isDisguised:
                    rightHand = self.suit.rightHand
                    numChildren = rightHand.getNumChildren()
                    if numChildren > 0:
                        anim = 'tray-' + anim
                        if anim == 'tray-run':
                            anim = 'tray-walk'
                    elif anim == 'run':
                        anim = 'walk'
                    self.suit.stop()
                    self.suit.loop(anim)
                    self.suit.setPlayRate(rate, anim)
            elif rate != self.playingRate:
                self.playingRate = rate
                if not self.isDisguised:
                    self.setPlayRate(rate, anim)
                else:
                    self.suit.setPlayRate(rate, anim)
            showWake, wakeWaterHeight = ZoneUtil.getWakeInfo()
            if showWake and self.getZ(render) < wakeWaterHeight and abs(forwardSpeed) > ToontownGlobals.WalkCutOff:
                currT = globalClock.getFrameTime()
                deltaT = currT - self.lastWakeTime
                if action == OTPGlobals.RUN_INDEX and deltaT > ToontownGlobals.WakeRunDelta or deltaT > ToontownGlobals.WakeWalkDelta:
                    self.getWake().createRipple(wakeWaterHeight, rate=1, startFrame=4)
                    if not self.swimRunSfx.status() == self.swimRunSfx.PLAYING:
                        base.playSfx(self.swimRunSfx, node=self)
                    self.lastWakeTime = currT
        return action

    def enterOff(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.setActiveShadow(0)
        self.playingAnim = None
        return

    def exitOff(self):
        pass

    def enterNeutral(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        anim = 'neutral'
        self.pose(anim, int(self.getNumFrames(anim) * self.randGen.random()))
        self.loop(anim, restart=0)
        self.setPlayRate(animMultiplier, anim)
        self.playingAnim = anim
        self.setActiveShadow(1)

    def exitNeutral(self):
        self.stop()

    def enterVictory(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        anim = 'victory'
        frame = int(ts * self.getFrameRate(anim) * animMultiplier)
        self.pose(anim, frame)
        self.loop('victory', restart=0)
        self.setPlayRate(animMultiplier, 'victory')
        self.playingAnim = anim
        self.setActiveShadow(0)

    def exitVictory(self):
        self.stop()

    def enterHappy(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (('neutral', 1.0),
         ('walk', 1.0),
         ('run', 1.0),
         ('walk', -1.0))
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(1)
        return

    def exitHappy(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()
        return

    def enterSad(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.playingAnim = 'sad'
        self.playingRate = None
        self.standWalkRunReverse = (('sad-neutral', 1.0),
         ('sad-walk', 1.2),
         ('sad-walk', 1.2),
         ('sad-walk', -1.0))
        self.setSpeed(0, 0)
        Emote.globalEmote.disableBody(self, 'toon, enterSad')
        self.setActiveShadow(1)
        if self.isLocal():
            self.controlManager.disableAvatarJump()
        return

    def exitSad(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()
        Emote.globalEmote.releaseBody(self, 'toon, exitSad')
        if self.isLocal():
            self.controlManager.enableAvatarJump()
        return

    def enterCatching(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (('catch-neutral', 1.0),
         ('catch-run', 1.0),
         ('catch-run', 1.0),
         ('catch-run', -1.0))
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(1)
        return

    def exitCatching(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()
        return

    def enterCatchEating(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (('catch-eatneutral', 1.0),
         ('catch-eatnrun', 1.0),
         ('catch-eatnrun', 1.0),
         ('catch-eatnrun', -1.0))
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(0)
        return

    def exitCatchEating(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()
        return

    def enterWalk(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('walk')
        self.setPlayRate(animMultiplier, 'walk')
        self.setActiveShadow(1)

    def exitWalk(self):
        self.stop()

    def getJumpDuration(self):
        if self.playingAnim == 'neutral':
            return self.getDuration('jump', 'legs')
        else:
            return self.getDuration('running-jump', 'legs')

    def enterJump(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        if not self.isDisguised:
            if self.playingAnim == 'neutral':
                anim = 'jump'
            else:
                anim = 'running-jump'
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            self.play(anim)
        self.setActiveShadow(1)
        Emote.globalEmote.disableBody(self, 'toon, enterJump')

    def exitJump(self):
        self.stop()
        self.playingAnim = 'neutral'
        Emote.globalEmote.releaseBody(self, 'toon, exitJump')

    def enterJumpSquat(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        if not self.isDisguised:
            if self.playingAnim == 'neutral':
                anim = 'jump-squat'
            else:
                anim = 'running-jump-squat'
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            self.play(anim)
        self.setActiveShadow(1)
        Emote.globalEmote.disableBody(self, 'toon, enterJumpSquat')

    def exitJumpSquat(self):
        self.stop()
        self.playingAnim = 'neutral'
        Emote.globalEmote.releaseBody(self, 'toon, exitJumpSquat')

    def enterJumpAirborne(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        if not self.isDisguised:
            if self.playingAnim == 'neutral' or self.forceJumpIdle:
                anim = 'jump-idle'
            else:
                anim = 'running-jump-idle'
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            self.loop(anim)
        self.setActiveShadow(1)
        Emote.globalEmote.disableBody(self, 'toon, enterJumpAirborne')

    def exitJumpAirborne(self):
        self.stop()
        self.playingAnim = 'neutral'
        Emote.globalEmote.releaseBody(self, 'toon, exitJumpAirborne')

    def enterJumpLand(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        if not self.isDisguised:
            if self.playingAnim == 'running-jump-idle':
                anim = 'running-jump-land'
                skipStart = 0.2
            else:
                anim = 'jump-land'
                skipStart = 0.0
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            self.play(anim)
        self.setActiveShadow(1)
        Emote.globalEmote.disableBody(self, 'toon, enterJumpLand')

    def exitJumpLand(self):
        self.stop()
        self.playingAnim = 'neutral'
        Emote.globalEmote.releaseBody(self, 'toon, exitJumpLand')

    def enterRun(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('run')
        self.setPlayRate(animMultiplier, 'run')
        Emote.globalEmote.disableBody(self, 'toon, enterRun')
        self.setActiveShadow(1)

    def exitRun(self):
        self.stop()
        Emote.globalEmote.releaseBody(self, 'toon, exitRun')

    def enterSwim(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        Emote.globalEmote.disableAll(self, 'enterSwim')
        self.playingAnim = 'swim'
        self.loop('swim')
        self.setPlayRate(animMultiplier, 'swim')
        self.getGeomNode().setP(-89.0)
        self.dropShadow.hide()
        if self.isLocal():
            self.book.obscureButton(1)
            self.useSwimControls()
        self.nametag3d.setPos(0, -2, 1)
        self.startBobSwimTask()
        self.setActiveShadow(0)

    def enterCringe(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('cringe')
        self.getGeomNode().setPos(0, 0, -2)
        self.setPlayRate(animMultiplier, 'swim')

    def exitCringe(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.stop()
        self.getGeomNode().setPos(0, 0, 0)
        self.playingAnim = 'neutral'
        self.setPlayRate(animMultiplier, 'swim')

    def enterDive(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('swim')
        if hasattr(self.getGeomNode(), 'setPos'):
            self.getGeomNode().setPos(0, 0, -2)
            self.setPlayRate(animMultiplier, 'swim')
            self.setActiveShadow(0)
            self.dropShadow.hide()
            self.nametag3d.setPos(0, -2, 1)

    def exitDive(self):
        self.stop()
        self.getGeomNode().setPos(0, 0, 0)
        self.playingAnim = 'neutral'
        self.dropShadow.show()
        self.nametag3d.setPos(0, 0, self.height + 0.5)

    def enterSwimHold(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.getGeomNode().setPos(0, 0, -2)
        self.nametag3d.setPos(0, -2, 1)
        self.pose('swim', 55)

    def exitSwimHold(self):
        self.stop()
        self.getGeomNode().setPos(0, 0, 0)
        self.playingAnim = 'neutral'
        self.dropShadow.show()
        self.nametag3d.setPos(0, 0, self.height + 0.5)

    def exitSwim(self):
        self.stop()
        self.playingAnim = 'neutral'
        self.stopBobSwimTask()
        self.getGeomNode().setPosHpr(0, 0, 0, 0, 0, 0)
        self.dropShadow.show()
        if self.isLocal():
            self.useWalkControls()
            if hasattr(self, 'book'):
                self.book.obscureButton(False)
        self.nametag3d.setPos(0, 0, self.height + 0.5)
        Emote.globalEmote.releaseAll(self, 'exitSwim')

    def startBobSwimTask(self):
        if getattr(self, 'swimBob', None):
            self.swimBob.finish()
            self.swimBob = None
        self.nametag3d.setZ(5.0)
        geomNode = self.getGeomNode()
        geomNode.setZ(4.0)
        self.swimBob = Sequence(geomNode.posInterval(1, Point3(0, -3, 3), startPos=Point3(0, -3, 4), blendType='easeInOut'), geomNode.posInterval(1, Point3(0, -3, 4), startPos=Point3(0, -3, 3), blendType='easeInOut'))
        self.swimBob.loop()
        return

    def stopBobSwimTask(self):
        swimBob = getattr(self, 'swimBob', None)
        if swimBob:
            swimBob.finish()
        self.getGeomNode().setPos(0, 0, 0)
        self.nametag3d.setZ(1.0)
        return

    def enterOpenBook(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        Emote.globalEmote.disableAll(self, 'enterOpenBook')
        self.playingAnim = 'openBook'
        self.stopLookAround()
        self.lerpLookAt(Point3(0, 1, -2))
        book = self.getBookActor()
        bookTrack = Parallel(ActorInterval(book, 'book', startTime=1.2, endTime=1.5), ActorInterval(self, 'book', startTime=1.2, endTime=1.5))
        self.track = Sequence(Func(book.show), bookTrack, Wait(0.1), name=self.uniqueName('openBook'))
        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)
        self.track.start(ts)
        self.setActiveShadow(0)

    def exitOpenBook(self):
        self.playingAnim = 'neutralob'
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        self.getBookActor().hide()
        self.startLookAround()
        Emote.globalEmote.releaseAll(self, 'exitOpenBook')
        return

    def enterReadBook(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        Emote.globalEmote.disableBody(self, 'enterReadBook')
        self.playingAnim = 'readBook'
        self.stopLookAround()
        self.lerpLookAt(Point3(0, 1, -2))
        book = self.getBookActor()
        book.show()
        for actor in (self, book):
            actor.pingpong('book', fromFrame=38, toFrame=118)

        self.setActiveShadow(0)

    def exitReadBook(self):
        self.playingAnim = 'neutralrb'
        book = self.getBookActor()
        book.hide()
        book.stop()
        self.startLookAround()
        Emote.globalEmote.releaseBody(self, 'exitReadBook')

    def enterCloseBook(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        Emote.globalEmote.disableAll(self, 'enterCloseBook')
        self.playingAnim = 'closeBook'
        book = self.getBookActor()
        bookTrack = Parallel(ActorInterval(book, 'book', startTime=4.96, endTime=6.5), ActorInterval(self, 'book', startTime=4.96, endTime=6.5))
        self.track = Sequence(Func(book.show), bookTrack, Func(book.hide), name=self.uniqueName('closeBook'))
        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)
        self.track.start(ts)
        self.setActiveShadow(0)

    def exitCloseBook(self):
        self.playingAnim = 'neutralcb'
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseAll(self, 'exitCloseBook')
        return

    def getSoundTeleport(self):
        if not self.soundTeleport:
            self.soundTeleport = loader.loadSfx('phase_3.5/audio/sfx/AV_teleport.ogg')
        return self.soundTeleport

    def getTeleportOutTrack(self, autoFinishTrack = 1):
        hole = self.getHoleActor()
        holeTrack = Track((0.0, Func(hole.reparentTo, self.getRightHand())), (0.5, SoundInterval(self.getSoundTeleport(), node=self)), (1.708, Sequence(Func(hole.reparentTo, self), Func(hole.setBin, 'shadow', 0), Func(hole.setDepthTest, False), Func(hole.setDepthWrite, False))), (2.9, Func(self.dropShadow.hide)), (3.3, Sequence(Func(self.nametag3d.hide), Func(self.getGeomNode().hide), Func(hole.detachNode), Func(hole.clearBin), Func(hole.clearDepthTest), Func(hole.clearDepthWrite))))
        track = Parallel(holeTrack, name=self.uniqueName('teleportOut'), autoFinish=autoFinishTrack)
        track.append(ActorInterval(hole, 'hole', duration=3.4))
        track.append(ActorInterval(self, 'teleport', duration=3.4))
        return track

    def enterTeleportOut(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        name = self.name
        if hasattr(self, 'doId'):
            name += '-' + str(self.doId)
        self.notify.debug('enterTeleportOut %s' % name)
        if self.ghostMode or self.isDisguised:
            if callback:
                callback(*extraArgs)
            return
        self.playingAnim = 'teleport'
        Emote.globalEmote.disableAll(self, 'enterTeleportOut')
        if self.isLocal():
            autoFinishTrack = 0
        else:
            autoFinishTrack = 1
        self.track = self.getTeleportOutTrack(autoFinishTrack)
        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getName(), self.finishTeleportOut, [callback, extraArgs])
        self.nametag3d.setPos(0, 0, 1)
        self.nametag3d.setScale(*[ min(x + 1, 1.4) for x in self.nametag3d.find('**/nametag_contents').getScale() ])
        self.nametag3d.reparentTo(self.getHeadParts()[0])
        avHeight = min(self.getHeight(), 3)
        if hasattr(base, 'localAvatar') and self == base.localAvatar and settings['tpTransition']:
            holePos = Vec3(0, 2.1, 1.5)
            holeAbovePos = holePos + Vec3(0, -1, base.localAvatar.getHeight() + 3)
            Sequence(Parallel(ProjectileInterval(camera, duration=2, startPos=camera.getPos(), endPos=holeAbovePos, gravityMult=0.25), camera.hprInterval(2, Vec3(camera.getH(), -75, camera.getR()), blendType='easeInOut')), Parallel(ProjectileInterval(camera, duration=0.8, startPos=holeAbovePos, endPos=holePos, gravityMult=0.25), camera.hprInterval(0.8, Vec3(camera.getH(), -90, camera.getR()), blendType='easeInOut')), Func(base.transitions.fadeOut, 0)).start()
        self.track.start(ts)
        self.setActiveShadow(0)

    def finishTeleportOut(self, callback = None, extraArgs = []):
        name = self.name
        if hasattr(self, 'doId'):
            name += '-' + str(self.doId)
        self.notify.debug('finishTeleportOut %s' % name)
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if hasattr(self, 'animFSM'):
            self.animFSM.request('TeleportedOut')
        if callback:
            callback(*extraArgs)
        return

    def exitTeleportOut(self):
        name = self.name
        if hasattr(self, 'doId'):
            name += '-' + str(self.doId)
        self.notify.debug('exitTeleportOut %s' % name)
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            self.track = None
        geomNode = self.getGeomNode()
        if geomNode and not geomNode.isEmpty():
            self.getGeomNode().clearClipPlane()
        if self.nametag3d and not self.nametag3d.isEmpty():
            self.nametag3d.reparentTo(self)
            self.nametag3d.setScale(1)
            self.adjustNametag3d()
        Emote.globalEmote.releaseAll(self, 'exitTeleportOut')
        if self and not self.isEmpty():
            self.show()
        return

    def enterTeleportedOut(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.setActiveShadow(0)

    def exitTeleportedOut(self):
        pass

    def getDiedInterval(self, autoFinishTrack = 1):
        sound = loader.loadSfx('phase_5/audio/sfx/ENC_Lose.ogg')
        ival = Sequence(Func(Emote.globalEmote.disableBody, self), Func(self.sadEyes), Func(self.blinkEyes), Track((0, ActorInterval(self, 'lose')), (2, SoundInterval(sound, node=self)), (5.333, self.scaleInterval(1.5, VBase3(0.01, 0.01, 0.01), blendType='easeInOut'))), Func(self.detachNode), Func(self.setScale, 1, 1, 1), Func(self.normalEyes), Func(self.blinkEyes), Func(Emote.globalEmote.releaseBody, self), Func(messenger.send, self.uniqueName('died')), name=self.uniqueName('died'), autoFinish=autoFinishTrack)
        return ival

    def enterDied(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        if self.ghostMode:
            if callback:
                callback(*extraArgs)
            return
        else:
            if self.isDisguised:
                self.takeOffSuit()
            self.playingAnim = 'lose'
            Emote.globalEmote.disableAll(self, 'enterDied')
            if self.isLocal():
                autoFinishTrack = 0
            else:
                autoFinishTrack = 1
            if hasattr(self, 'jumpLandAnimFixTask') and self.jumpLandAnimFixTask:
                self.jumpLandAnimFixTask.remove()
                self.jumpLandAnimFixTask = None
            self.track = self.getDiedInterval(autoFinishTrack)
            if callback:
                self.track = Sequence(self.track, Func(callback, *extraArgs), autoFinish=autoFinishTrack)
            self.track.start(ts)
            self.setActiveShadow(0)
            return

    def finishDied(self, callback = None, extraArgs = []):
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if hasattr(self, 'animFSM'):
            self.animFSM.request('TeleportedOut')
        if callback:
            callback(*extraArgs)
        return

    def exitDied(self):
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseAll(self, 'exitDied')
        self.show()
        return

    def getTeleportInTrack(self):
        hole = self.getHoleActor()
        hole.setBin('shadow', 0)
        hole.setDepthTest(0)
        hole.setDepthWrite(0)
        holeTrack = Sequence()
        holeTrack.append(Func(hole.reparentTo, self))
        pos = Point3(0, -2.4, 0)
        holeTrack.append(Func(hole.setPos, self, pos))
        holeTrack.append(ActorInterval(hole, 'hole', startTime=3.4, endTime=3.1))
        holeTrack.append(Wait(0.6))
        holeTrack.append(ActorInterval(hole, 'hole', startTime=3.1, endTime=3.4))

        def restoreHole(hole):
            hole.setPos(0, 0, 0)
            hole.detachNode()
            hole.clearBin()
            hole.clearDepthTest()
            hole.clearDepthWrite()

        holeTrack.append(Func(restoreHole, hole))
        toonTrack = Sequence(Wait(0.3), Func(self.getGeomNode().show), Func(self.nametag3d.show), ActorInterval(self, 'jump', startTime=0.45))
        return Parallel(holeTrack, toonTrack, name=self.uniqueName('teleportIn'))

    def enterTeleportIn(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        if self.ghostMode or self.isDisguised:
            if callback:
                callback(*extraArgs)
            return
        self.show()
        self.playingAnim = 'teleport'
        Emote.globalEmote.disableAll(self, 'enterTeleportIn')
        self.pose('teleport', self.getNumFrames('teleport') - 1)
        self.getGeomNode().hide()
        self.nametag3d.hide()
        self.dropShadow.show()
        self.track = Sequence(self.getTeleportInTrack(), Func(self.loop, 'neutral'))
        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)
        self.track.start(ts)
        self.setActiveShadow(0)

    def exitTeleportIn(self):
        self.playingAnim = None
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if not self.ghostMode and not self.isDisguised:
            self.getGeomNode().show()
            self.nametag3d.show()
        Emote.globalEmote.releaseAll(self, 'exitTeleportIn')
        return

    def enterSitStart(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        Emote.globalEmote.disableBody(self)
        self.playingAnim = 'sit-start'
        if self.isLocal():
            self.track = Sequence(ActorInterval(self, 'sit-start'), Func(self.b_setAnimState, 'Sit', animMultiplier))
        else:
            self.track = Sequence(ActorInterval(self, 'sit-start'))
        self.track.start(ts)
        self.setActiveShadow(0)

    def exitSitStart(self):
        self.playingAnim = 'neutral'
        if self.track != None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseBody(self)
        return

    def enterSit(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        Emote.globalEmote.disableBody(self)
        self.playingAnim = 'sit'
        self.loop('sit')
        self.setActiveShadow(0)

    def exitSit(self):
        self.playingAnim = 'neutral'
        Emote.globalEmote.releaseBody(self)

    def enterSleep(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.stopLookAround()
        self.stopBlink()
        self.closeEyes()
        self.lerpLookAt(Point3(0, 1, -4))
        self.loop('neutral')
        self.setPlayRate(animMultiplier * 0.4, 'neutral')
        self.setChatAbsolute(TTLocalizer.ToonSleepString, CFThought)
        if self == base.localAvatar:
            self.notify.debug('Adding timeout task to Toon.')
            taskMgr.doMethodLater(self.afkTimeout, self.__handleAfkTimeout, self.uniqueName('afkTimeout'))
        self.setActiveShadow(0)

    def __handleAfkTimeout(self, task):
        self.notify.debug('Handling timeout task on Toon.')
        self.ignore('wakeup')
        self.takeOffSuit()
        base.cr.playGame.getPlace().fsm.request('final')
        self.b_setAnimState('TeleportOut', 1, self.__handleAfkExitTeleport, [0])
        return Task.done

    def __handleAfkExitTeleport(self, requestStatus):
        self.notify.info('closing shard...')
        base.cr.gameFSM.request('closeShard', ['afkTimeout'])

    def exitSleep(self):
        taskMgr.remove(self.uniqueName('afkTimeout'))
        self.startLookAround()
        self.openEyes()
        self.startBlink()
        if self.nametag.getChat() == TTLocalizer.ToonSleepString:
            self.clearChat()
        self.lerpLookAt(Point3(0, 1, 0), time=0.25)
        self.stop()

    def enterPush(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        Emote.globalEmote.disableBody(self)
        self.playingAnim = 'push'
        self.track = Sequence(ActorInterval(self, 'push'))
        self.track.loop()
        self.setActiveShadow(1)

    def exitPush(self):
        self.playingAnim = 'neutral'
        if self.track != None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseBody(self)
        return

    def enterEmote(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        if len(extraArgs) > 0:
            emoteIndex = extraArgs[0]
        else:
            return
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (('neutral', 1.0),
         ('walk', 1.0),
         ('run', 1.0),
         ('walk', -1.0))
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        if self.isLocal() and emoteIndex != Emote.globalEmote.EmoteSleepIndex:
            if self.sleepFlag:
                self.b_setAnimState('Happy', self.animMultiplier)
            self.wakeUp()
        duration = 0
        self.emoteTrack, duration = Emote.globalEmote.doEmote(self, emoteIndex, ts)
        self.setActiveShadow(1)
        return

    def doEmote(self, emoteIndex, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        if not self.isLocal():
            if hasattr(base, 'localAvatar') and base.localAvatar.isIgnored(self.doId):
                return
        duration = 0
        if self.isLocal():
            self.wakeUp()
            if self.hasTrackAnimToSpeed():
                self.trackAnimToSpeed(None)
        self.emoteTrack, duration = Emote.globalEmote.doEmote(self, emoteIndex, ts)
        return

    def __returnToLastAnim(self, task):
        if self.playingAnim:
            self.loop(self.playingAnim)
        elif self.hp > 0:
            self.loop('neutral')
        else:
            self.loop('sad-neutral')
        return Task.done

    def __finishEmote(self, task):
        if self.isLocal():
            if self.hp > 0:
                self.b_setAnimState('Happy')
            else:
                self.b_setAnimState('Sad')
        return Task.done

    def exitEmote(self):
        self.stop()
        if self.emoteTrack != None:
            self.emoteTrack.finish()
            self.emoteTrack = None
        taskMgr.remove(self.taskName('finishEmote'))
        return

    def enterSquish(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        Emote.globalEmote.disableAll(self)
        sound = loader.loadSfx('phase_9/audio/sfx/toon_decompress.ogg')
        lerpTime = 0.1
        node = self.getGeomNode().getChild(0)
        origScale = node.getScale()
        self.track = Sequence(LerpScaleInterval(node, lerpTime, VBase3(2, 2, 0.025), blendType='easeInOut'), Wait(1.0), Parallel(Sequence(Wait(0.4), LerpScaleInterval(node, lerpTime, VBase3(1.4, 1.4, 1.4), blendType='easeInOut'), LerpScaleInterval(node, lerpTime / 2.0, VBase3(0.8, 0.8, 0.8), blendType='easeInOut'), LerpScaleInterval(node, lerpTime / 3.0, origScale, blendType='easeInOut')), ActorInterval(self, 'jump', startTime=0.2), SoundInterval(sound)))
        self.track.start(ts)
        self.setActiveShadow(1)

    def exitSquish(self):
        self.playingAnim = 'neutral'
        if self.track != None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseAll(self)
        return

    def enterFallDown(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.playingAnim = 'fallDown'
        Emote.globalEmote.disableAll(self)
        self.track = Sequence(ActorInterval(self, 'slip-backward'), name='fallTrack')
        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)
        self.track.start(ts)

    def exitFallDown(self):
        self.playingAnim = 'neutral'
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseAll(self)
        return

    def stunToon(self, ts = 0, callback = None, knockdown = 0):
        if not self.isStunned:
            if self.stunTrack:
                self.stunTrack.finish()
                self.stunTrack = None

            def setStunned(stunned):
                self.isStunned = stunned
                if self == base.localAvatar:
                    messenger.send('toonStunned-' + str(self.doId), [self.isStunned])

            node = self.getGeomNode()
            lerpTime = 0.5
            down = self.doToonColorScale(VBase4(1, 1, 1, 0.6), lerpTime)
            up = self.doToonColorScale(VBase4(1, 1, 1, 0.9), lerpTime)
            clear = self.doToonColorScale(self.defaultColorScale, lerpTime)
            track = Sequence(Func(setStunned, 1), down, up, down, up, down, up, down, clear, Func(self.restoreDefaultColorScale), Func(setStunned, 0))
            if knockdown:
                self.stunTrack = Parallel(ActorInterval(self, animName='slip-backward'), track)
            else:
                self.stunTrack = track
            self.stunTrack.start()
        return

    def getPieces(self, *pieces):
        results = []
        for partName, pieceNames in pieces:
            part = self.getPart(partName)
            if part:
                if type(pieceNames) == types.StringType:
                    pieceNames = (pieceNames,)
                for pieceName in pieceNames:
                    npc = part.findAllMatches('**/%s;+s' % pieceName)
                    for i in xrange(npc.getNumPaths()):
                        results.append(npc[i])

        return results

    def applyCheesyEffect(self, effect, lerpTime = 0):
        if self.effectTrack != None:
            self.effectTrack.finish()
            self.effectTrack = None
        if self.cheesyEffect != effect:
            oldEffect = self.cheesyEffect
            self.cheesyEffect = effect
            if oldEffect == ToontownGlobals.CENormal:
                self.effectTrack = self.__doCheesyEffect(effect, lerpTime)
            elif effect == ToontownGlobals.CENormal:
                self.effectTrack = self.__undoCheesyEffect(oldEffect, lerpTime)
            else:
                self.effectTrack = Sequence(self.__undoCheesyEffect(oldEffect, lerpTime / 2.0), self.__doCheesyEffect(effect, lerpTime / 2.0))
            self.effectTrack.start()
        return

    def reapplyCheesyEffect(self, lerpTime = 0):
        if self.effectTrack != None:
            self.effectTrack.finish()
            self.effectTrack = None
        effect = self.cheesyEffect
        self.effectTrack = Sequence(self.__undoCheesyEffect(effect, 0), self.__doCheesyEffect(effect, lerpTime))
        self.effectTrack.start()
        return

    def clearCheesyEffect(self, lerpTime = 0):
        self.applyCheesyEffect(ToontownGlobals.CENormal, lerpTime=lerpTime)
        if self.effectTrack != None:
            self.effectTrack.finish()
            self.effectTrack = None
        return

    def __doHeadScale(self, scale, lerpTime):
        if scale == None:
            scale = ToontownGlobals.toonHeadScales[self.style.getAnimal()]
        track = Parallel()
        for hi in xrange(self.headParts.getNumPaths()):
            head = self.headParts[hi]
            track.append(LerpScaleInterval(head, lerpTime, scale, blendType='easeInOut'))

        return track

    def doHeadScale(self, scale):
        if scale == None:
            scale = ToontownGlobals.toonHeadScales[self.style.getAnimal()]
        for hi in xrange(self.headParts.getNumPaths()):
            self.headParts[hi].setScale(scale)

        return

    def __doLegsScale(self, scale, lerpTime):
        if scale == None:
            scale = 1
            invScale = 1
        else:
            invScale = 1.0 / scale
        track = Parallel()
        for li in xrange(self.legsParts.getNumPaths()):
            legs = self.legsParts[li]
            torso = self.torsoParts[li]
            track.append(LerpScaleInterval(legs, lerpTime, scale, blendType='easeInOut'))
            track.append(LerpScaleInterval(torso, lerpTime, invScale, blendType='easeInOut'))

        return track

    def __doToonScale(self, scale, lerpTime):
        if scale == None:
            scale = 1
        node = self.getGeomNode()
        track = Sequence(Parallel(LerpHprInterval(node, lerpTime, Vec3(0.0, 0.0, 0.0), blendType='easeInOut'), LerpScaleInterval(node, lerpTime, scale, blendType='easeInOut')), Func(self.resetHeight))
        return track

    def doToonColorScale(self, scale, lerpTime, keepDefault = 0):
        if keepDefault:
            self.defaultColorScale = scale
        if scale == None:
            scale = VBase4(1, 1, 1, 1)
        node = self.getGeomNode()
        caps = self.getPieces(('torso', 'torso-bot-cap'))
        track = Sequence()
        track.append(Func(node.setTransparency, 1))
        if scale[3] != 1:
            for cap in caps:
                track.append(HideInterval(cap))

        track.append(LerpColorScaleInterval(node, lerpTime, scale, blendType='easeInOut'))
        if scale[3] == 1:
            track.append(Func(node.clearTransparency))
            for cap in caps:
                track.append(ShowInterval(cap))

        elif scale[3] == 0:
            track.append(Func(node.clearTransparency))
        return track

    def __doPumpkinHeadSwitch(self, lerpTime, toPumpkin):
        node = self.getGeomNode()
        dust = self.getDustCloud(0.0)
        track = Sequence()
        if toPumpkin:
            track.append(Func(self.stopBlink))
            track.append(Func(self.closeEyes))
            if lerpTime > 0.0:
                track.append(Func(dust.start))
                track.append(Wait(0.5))
            else:
                dust.finish()
            track.append(Func(self.enablePumpkins, True))
        else:
            if lerpTime > 0.0:
                track.append(Func(dust.start))
                track.append(Wait(0.5))
            else:
                dust.finish()
            track.append(Func(self.enablePumpkins, False))
            track.append(Func(self.startBlink))
        return track

    def __doSnowManHeadSwitch(self, lerpTime, toSnowMan):
        node = self.getGeomNode()
        dust = self.getDustCloud(0.0)
        track = Sequence()
        if toSnowMan:
            track.append(Func(self.stopBlink))
            track.append(Func(self.closeEyes))
            if lerpTime > 0.0:
                track.append(Func(dust.start))
                track.append(Wait(0.5))
            else:
                dust.finish()
            track.append(Func(self.enableSnowman, True))
        else:
            if lerpTime > 0.0:
                track.append(Func(dust.start))
                track.append(Wait(0.5))
            else:
                dust.finish()
            track.append(Func(self.enableSnowman, False))
            track.append(Func(self.startBlink))
        return track

    def __doGreenToon(self, lerpTime, toGreen):
        track = Sequence()
        greenTrack = Parallel()
        if lerpTime > 0.0:
            dust = self.getDustCloud(0.0)
            track.append(Func(dust.start))
            track.append(Wait(0.5))
        if toGreen:
            skinGreen = VBase4(76 / 255.0, 240 / 255.0, 84 / 255.0, 1)
            muzzleGreen = VBase4(4 / 255.0, 205 / 255.0, 90 / 255.0, 1)
            gloveGreen = VBase4(14 / 255.0, 173 / 255.0, 40 / 255.0, 1)
            greenTrack.append(self.__colorToonSkin(skinGreen, lerpTime))
            greenTrack.append(self.__colorToonEars(skinGreen, muzzleGreen, lerpTime))
            greenTrack.append(self.__colorScaleToonMuzzle(muzzleGreen, lerpTime))
            greenTrack.append(self.__colorToonGloves(gloveGreen, lerpTime))
        else:
            greenTrack.append(self.__colorToonSkin(None, lerpTime))
            greenTrack.append(self.__colorToonEars(None, None, lerpTime))
            greenTrack.append(self.__colorScaleToonMuzzle(None, lerpTime))
            greenTrack.append(self.__colorToonGloves(None, lerpTime))
        track.append(greenTrack)
        return track

    def __colorToonSkin(self, color, lerpTime):
        colorTrack = Parallel()
        torsoPieces = self.getPieces(('torso', ('arms', 'neck')))
        legPieces = self.getPieces(('legs', ('legs', 'feet')))
        headPieces = self.getPieces(('head', '*head*'))
        if color == None:
            armColor = self.style.getArmColor()
            legColor = self.style.getLegColor()
            headColor = self.style.getHeadColor()
        else:
            armColor = color
            legColor = color
            headColor = color
        for piece in torsoPieces:
            colorTrack.append(Func(piece.setColor, *armColor))

        for piece in legPieces:
            colorTrack.append(Func(piece.setColor, *legColor))

        for piece in headPieces:
            if 'hatNode' not in str(piece) and 'glassesNode' not in str(piece):
                colorTrack.append(Func(piece.setColor, *headColor))

        return colorTrack

    def __colorToonEars(self, color, colorScale, lerpTime):
        track = Sequence()
        earPieces = self.getPieces(('head', '*ear*'))
        if len(earPieces) == 0:
            return track
        else:
            colorTrack = Parallel()
            if earPieces[0].hasColor():
                if color == None:
                    headColor = self.style.getHeadColor()
                else:
                    headColor = color
                for piece in earPieces:
                    colorTrack.append(Func(piece.setColor, *headColor))

            else:
                if colorScale == None:
                    colorScale = VBase4(1, 1, 1, 1)
                for piece in earPieces:
                    colorTrack.append(Func(piece.setColorScale, *colorScale))

            track.append(colorTrack)
            return track

    def __colorScaleToonMuzzle(self, scale, lerpTime):
        colorTrack = Parallel()
        if scale == None:
            scale = 1
        for piece in self.getPieces(('head', '*muzzle*')):
            colorTrack.append(Func(piece.setColorScale, scale))

        return colorTrack

    def __colorToonGloves(self, color, lerpTime):
        colorTrack = Parallel()
        if color == None:
            color = self.style.getGloveColor()
        for piece in self.getPieces(('torso', '*hands*')):
            colorTrack.append(Func(piece.setColor, color))

        return colorTrack

    def __doBigAndWhite(self, color, scale, lerpTime):
        return Parallel(self.__doToonColor(color, lerpTime), self.__doToonScale(scale, lerpTime))

    def __doVirtual(self):
        for parts in (self.getHeadParts(),
         self.getTorsoParts(),
         self.getHipsParts(),
         self.getLegsParts()):
            self.setPartsAdd(parts)

        return self.__doToonColor(VBase4(0.25, 0.25, 1.0, 1), 0.0)

    def __doUnVirtual(self):
        for parts in (self.getHeadParts(),
         self.getTorsoParts(),
         self.getHipsParts(),
         self.getLegsParts()):
            self.setPartsNormal(parts)

        return self.__doToonColor(None, 0.0)

    def setPartsAdd(self, parts):
        for i in xrange(0, parts.getNumPaths()):
            part = parts[i]
            if part.getName() not in ('joint_attachMeter', 'joint_nameTag'):
                part.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
                part.setDepthWrite(False)
                self.setBin('fixed', 1)

    def setPartsNormal(self, parts):
        for i in xrange(0, parts.getNumPaths()):
            part = parts[i]
            if part.getName() not in ('joint_attachMeter', 'joint_nameTag'):
                part.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
                part.setDepthWrite(True)
                self.clearBin()

    def doToonGhostColorScale(self, scale, lerpTime, keepDefault = 0):
        if keepDefault:
            self.defaultColorScale = scale
        if scale == None:
            scale = VBase4(1, 1, 1, 1)
        node = self.getGeomNode()
        caps = self.getPieces(('torso', 'torso-bot-cap'))
        track = Sequence()
        track.append(Func(node.setTransparency, 1))
        track.append(ShowInterval(node))
        if scale[3] != 1:
            for cap in caps:
                track.append(HideInterval(cap))

        track.append(LerpColorScaleInterval(node, lerpTime, scale, blendType='easeInOut'))
        if scale[3] == 1:
            track.append(Func(node.clearTransparency))
            for cap in caps:
                track.append(ShowInterval(cap))

        elif scale[3] == 0:
            track.append(Func(node.clearTransparency))
            track.append(HideInterval(node))
        return track

    def restoreDefaultColorScale(self):
        node = self.getGeomNode()
        if node:
            if self.defaultColorScale:
                node.setColorScale(self.defaultColorScale)
                if self.defaultColorScale[3] != 1:
                    node.setTransparency(1)
                else:
                    node.clearTransparency()
            else:
                node.clearColorScale()
                node.clearTransparency()

    def __doToonColor(self, color, lerpTime):
        node = self.getGeomNode()
        if color == None:
            return Func(node.clearColor)
        else:
            return Func(node.setColor, color, 1)
            return

    def __doPartsColorScale(self, scale, lerpTime):
        if scale == None:
            scale = VBase4(1, 1, 1, 1)
        node = self.getGeomNode()
        pieces = self.getPieces(('torso', ('arms', 'neck')), ('legs', ('legs', 'feet')), ('head', '+GeomNode'))
        track = Sequence()
        track.append(Func(node.setTransparency, 1))
        for piece in pieces:
            if piece.getName()[:7] == 'muzzle-' and piece.getName()[-8:] != '-neutral':
                continue
            track.append(ShowInterval(piece))

        p1 = Parallel()
        for piece in pieces:
            if piece.getName()[:7] == 'muzzle-' and piece.getName()[-8:] != '-neutral':
                continue
            p1.append(LerpColorScaleInterval(piece, lerpTime, scale, blendType='easeInOut'))

        track.append(p1)
        if scale[3] == 1:
            track.append(Func(node.clearTransparency))
        elif scale[3] == 0:
            track.append(Func(node.clearTransparency))
            for piece in pieces:
                if piece.getName()[:7] == 'muzzle-' and piece.getName()[-8:] != '-neutral':
                    continue
                track.append(HideInterval(piece))

        self.generateHat()
        self.generateGlasses()
        return track

    def __doCheesyEffect(self, effect, lerpTime):
        if effect == ToontownGlobals.CEBigHead:
            return self.__doHeadScale(2.5, lerpTime)
        if effect == ToontownGlobals.CESmallHead:
            return self.__doHeadScale(0.5, lerpTime)
        if effect == ToontownGlobals.CEBigLegs:
            return self.__doLegsScale(1.4, lerpTime)
        if effect == ToontownGlobals.CESmallLegs:
            return self.__doLegsScale(0.6, lerpTime)
        if effect == ToontownGlobals.CEBigToon:
            return self.__doToonScale(ToontownGlobals.BigToonScale, lerpTime)
        if effect == ToontownGlobals.CESmallToon:
            return self.__doToonScale(ToontownGlobals.SmallToonScale, lerpTime)
        if effect == ToontownGlobals.CEFlatPortrait:
            return self.__doToonScale(VBase3(1, 0.05, 1), lerpTime)
        if effect == ToontownGlobals.CEFlatProfile:
            return self.__doToonScale(VBase3(0.05, 1, 1), lerpTime)
        if effect == ToontownGlobals.CETransparent:
            return self.doToonColorScale(VBase4(1, 1, 1, 0.6), lerpTime, keepDefault=1)
        if effect == ToontownGlobals.CENoColor:
            return self.__doToonColor(VBase4(1, 1, 1, 1), lerpTime)
        if effect == ToontownGlobals.CEInvisible:
            return self.__doPartsColorScale(VBase4(1, 1, 1, 0), lerpTime)
        if effect == ToontownGlobals.CEPumpkin:
            return self.__doPumpkinHeadSwitch(lerpTime, toPumpkin=True)
        if effect == ToontownGlobals.CEBigWhite:
            return self.__doBigAndWhite(VBase4(1, 1, 1, 1), ToontownGlobals.BigToonScale, lerpTime)
        if effect == ToontownGlobals.CESnowMan:
            return self.__doSnowManHeadSwitch(lerpTime, toSnowMan=True)
        if effect == ToontownGlobals.CEGreenToon:
            return self.__doGreenToon(lerpTime, toGreen=True)
        if effect == ToontownGlobals.CEVirtual:
            return self.__doVirtual()
        if effect == ToontownGlobals.CEGhost:
            alpha = 0.25
            if base.localAvatar.getAdminAccess() < self.adminAccess:
                alpha = 0
            return Sequence(self.doToonGhostColorScale(VBase4(1, 1, 1, alpha), lerpTime, keepDefault=1), Func(self.nametag3d.hide))
        return Sequence()

    def __undoCheesyEffect(self, effect, lerpTime):
        if effect == ToontownGlobals.CEBigHead:
            return self.__doHeadScale(None, lerpTime)
        elif effect == ToontownGlobals.CESmallHead:
            return self.__doHeadScale(None, lerpTime)
        elif effect == ToontownGlobals.CEBigLegs:
            return self.__doLegsScale(None, lerpTime)
        elif effect == ToontownGlobals.CESmallLegs:
            return self.__doLegsScale(None, lerpTime)
        elif effect == ToontownGlobals.CEBigToon:
            return self.__doToonScale(None, lerpTime)
        elif effect == ToontownGlobals.CESmallToon:
            return self.__doToonScale(None, lerpTime)
        elif effect == ToontownGlobals.CEFlatPortrait:
            return self.__doToonScale(None, lerpTime)
        elif effect == ToontownGlobals.CEFlatProfile:
            return self.__doToonScale(None, lerpTime)
        elif effect == ToontownGlobals.CETransparent:
            return self.doToonColorScale(None, lerpTime, keepDefault=1)
        elif effect == ToontownGlobals.CENoColor:
            return self.__doToonColor(None, lerpTime)
        elif effect == ToontownGlobals.CEInvisible:
            return self.__doPartsColorScale(None, lerpTime)
        elif effect == ToontownGlobals.CEPumpkin:
            return self.__doPumpkinHeadSwitch(lerpTime, toPumpkin=False)
        elif effect == ToontownGlobals.CEBigWhite:
            return self.__doBigAndWhite(None, None, lerpTime)
        elif effect == ToontownGlobals.CESnowMan:
            return self.__doSnowManHeadSwitch(lerpTime, toSnowMan=False)
        elif effect == ToontownGlobals.CEGreenToon:
            return self.__doGreenToon(lerpTime, toGreen=False)
        elif effect == ToontownGlobals.CEVirtual:
            return self.__doUnVirtual()
        elif effect == ToontownGlobals.CEGhost:
            return Sequence(Func(self.nametag3d.show), self.doToonGhostColorScale(None, lerpTime, keepDefault=1))
        else:
            return Sequence()

    def putOnSuit(self, suitType, setDisplayName = True, rental = False):
        if self.isDisguised:
            self.takeOffSuit()
        from toontown.suit import Suit
        deptIndex = suitType
        suit = Suit.Suit()
        dna = SuitDNA.SuitDNA()
        if rental == True:
            if SuitDNA.suitDepts[deptIndex] == 's':
                suitType = 'cc'
            elif SuitDNA.suitDepts[deptIndex] == 'm':
                suitType = 'sc'
            elif SuitDNA.suitDepts[deptIndex] == 'l':
                suitType = 'bf'
            elif SuitDNA.suitDepts[deptIndex] == 'c':
                suitType = 'f'
            else:
                self.notify.warning('Suspicious: Incorrect rental suit department requested')
                suitType = 'cc'
        dna.newSuit(suitType)
        suit.setStyle(dna)
        suit.isDisguised = 1
        suit.generateSuit()
        suit.initializeDropShadow()
        suit.setPos(self.getPos())
        suit.setHpr(self.getHpr())
        suit.destroyNametag3d()
        for part in suit.getHeadParts():
            part.hide()

        suitHeadNull = suit.find('**/joint_head')
        toonHead = self.getPart('head')
        Emote.globalEmote.disableAll(self)
        toonGeom = self.getGeomNode()
        toonGeom.hide()
        worldScale = toonHead.getScale(render)
        self.headOrigScale = toonHead.getScale()
        headPosNode = hidden.attachNewNode('headPos')
        toonHead.reparentTo(headPosNode)
        toonHead.setPos(0, 0, 0.2)
        headPosNode.reparentTo(suitHeadNull)
        headPosNode.setScale(render, worldScale)
        suitGeom = suit.getGeomNode()
        suitGeom.reparentTo(self)
        if rental == True:
            suit.makeRentalSuit(SuitDNA.suitDepts[deptIndex])
        self.suit = suit
        self.suitGeom = suitGeom
        self.setHeight(suit.getHeight())
        self.nametag3d.setPos(0, 0, self.height + 1.3)
        if self.isLocal():
            if hasattr(self, 'book'):
                self.book.obscureButton(1)
            self.oldForward = ToontownGlobals.ToonForwardSpeed
            self.oldReverse = ToontownGlobals.ToonReverseSpeed
            self.oldRotate = ToontownGlobals.ToonRotateSpeed
            ToontownGlobals.ToonForwardSpeed = ToontownGlobals.SuitWalkSpeed
            ToontownGlobals.ToonReverseSpeed = ToontownGlobals.SuitWalkSpeed
            ToontownGlobals.ToonRotateSpeed = ToontownGlobals.ToonRotateSlowSpeed
            if self.hasTrackAnimToSpeed():
                self.stopTrackAnimToSpeed()
                self.startTrackAnimToSpeed()
            self.controlManager.disableAvatarJump()
            indices = range(OTPLocalizer.SCMenuCommonCogIndices[0], OTPLocalizer.SCMenuCommonCogIndices[1] + 1)
            customIndices = OTPLocalizer.SCMenuCustomCogIndices[suitType]
            indices += range(customIndices[0], customIndices[1] + 1)
            self.chatMgr.chatInputSpeedChat.addCogMenu(indices)
        self.suit.loop('neutral')
        self.isDisguised = 1
        self.setFont(ToontownGlobals.getSuitFont())
        self.nametag.setSpeechFont(ToontownGlobals.getSuitFont())
        if setDisplayName:
            if hasattr(base, 'idTags') and base.idTags:
                name = self.getAvIdName()
            else:
                name = self.getName()
            suitDept = SuitDNA.suitDepts.index(SuitDNA.getSuitDept(suitType))
            suitName = SuitBattleGlobals.SuitAttributes[suitType]['name']
            self.nametag.setDisplayName(TTLocalizer.SuitBaseNameWithLevel % {'name': name,
             'dept': suitName,
             'level': self.cogLevels[suitDept] + 1})
            self.nametag.setWordwrap(9.0)

    def takeOffSuit(self):
        if not self.isDisguised:
            return
        else:
            suitType = self.suit.style.name
            torso = self.getPart('torso')
            toonHeadNull = torso.find('**/def_head')
            if not toonHeadNull:
                toonHeadNull = torso.find('**/joint_head')
            toonHead = self.getPart('head')
            toonHead.reparentTo(toonHeadNull)
            toonHead.setScale(self.headOrigScale)
            toonHead.setPos(0, 0, 0)
            headPosNode = self.suitGeom.find('**/headPos')
            headPosNode.removeNode()
            self.suitGeom.reparentTo(self.suit)
            self.resetHeight()
            self.nametag3d.setPos(0, 0, self.height + 0.5)
            toonGeom = self.getGeomNode()
            toonGeom.show()
            Emote.globalEmote.releaseAll(self)
            self.isDisguised = 0
            self.setFont(ToontownGlobals.getToonFont())
            self.nametag.setSpeechFont(ToontownGlobals.getToonFont())
            self.nametag.setWordwrap(None)
            if hasattr(base, 'idTags') and base.idTags:
                name = self.getAvIdName()
            else:
                name = self.getName()
            self.setDisplayName(name)
            if self.isLocal():
                if hasattr(self, 'book'):
                    self.book.obscureButton(0)
                ToontownGlobals.ToonForwardSpeed = self.oldForward
                ToontownGlobals.ToonReverseSpeed = self.oldReverse
                ToontownGlobals.ToonRotateSpeed = self.oldRotate
                if self.hasTrackAnimToSpeed():
                    self.stopTrackAnimToSpeed()
                    self.startTrackAnimToSpeed()
                del self.oldForward
                del self.oldReverse
                del self.oldRotate
                self.controlManager.enableAvatarJump()
                self.chatMgr.chatInputSpeedChat.removeCogMenu()
            self.suit.delete()
            del self.suit
            del self.suitGeom
            return

    def makeWaiter(self):
        if not self.isDisguised:
            return
        self.suit.makeWaiter(self.suitGeom)

    def getPieModel(self):
        from toontown.toonbase import ToontownBattleGlobals
        from toontown.battle import BattleProps
        if self.pieModel != None and self.__pieModelType != self.pieType:
            self.pieModel.detachNode()
            self.pieModel = None
        pieName = ToontownBattleGlobals.pieNames[self.pieType]
        if self.pieModel == None:
            self.__pieModelType = self.pieType
            self.pieModel = BattleProps.globalPropPool.getProp(pieName)
            self.pieScale = self.pieModel.getScale()
            self.pieThrowType = ToontownGlobals.PieThrowArc
        if pieName == 'snowball':
            self.pieModel.setTexture(loader.loadTexture('phase_3/maps/snowball.jpg'), 1)
            self.pieModel.setScale(0.25)
            self.pieScale = 0.25
            self.pieThrowType = ToontownGlobals.PieThrowLinear
        return self.pieModel

    def getPresentPieInterval(self, x, y, z, h):
        from toontown.toonbase import ToontownBattleGlobals
        from toontown.battle import BattleProps
        from toontown.battle import MovieUtil
        pie = self.getPieModel()
        pieName = ToontownBattleGlobals.pieNames[self.pieType]
        pieType = BattleProps.globalPropPool.getPropType(pieName)
        animPie = Sequence()
        pingpongPie = Sequence()
        if pieType == 'actor':
            animPie = ActorInterval(pie, pieName, startFrame=0, endFrame=31)
            pingpongPie = Func(pie.pingpong, pieName, fromFrame=32, toFrame=47)
        partName = None if self.playingAnim == 'neutral' else 'torso'
        track = Sequence(Func(self.setPosHpr, x, y, z, h, 0, 0), Func(pie.reparentTo, self.rightHand), Func(pie.setPosHpr, 0, 0, 0, 0, 0, 0), Parallel(pie.scaleInterval(1, self.pieScale, startScale=MovieUtil.PNT3_NEARZERO), ActorInterval(self, 'throw', startFrame=0, endFrame=31, partName=partName), animPie), Func(self.pingpong, 'throw', fromFrame=32, toFrame=45, partName=partName), pingpongPie)
        return track

    def getTossPieInterval(self, x, y, z, h, power, throwType, beginFlyIval = Sequence()):
        from toontown.toonbase import ToontownBattleGlobals
        from toontown.battle import BattleProps
        pie = self.getPieModel()
        flyPie = pie.copyTo(NodePath('a'))
        pieName = ToontownBattleGlobals.pieNames[self.pieType]
        pieType = BattleProps.globalPropPool.getPropType(pieName)
        animPie = Sequence()
        if pieType == 'actor':
            animPie = ActorInterval(pie, pieName, startFrame=48)
        sound = loader.loadSfx('phase_3.5/audio/sfx/AA_pie_throw_only.ogg')
        if throwType == ToontownGlobals.PieThrowArc:
            t = power / 100.0
            dist = 100 - 70 * t
            time = 1 + 0.5 * t
            proj = ProjectileInterval(None, startPos=Point3(0, 0, 0), endPos=Point3(0, dist, 0), duration=time)
            relVel = proj.startVel
        elif throwType == ToontownGlobals.PieThrowLinear:
            magnitude = power / 2.0 + 25
            relVel = Vec3(0, 1, 0.25)
            relVel.normalize()
            relVel *= magnitude

        def getVelocity(toon = self, relVel = relVel):
            return render.getRelativeVector(toon, relVel)

        partName = None if self.playingAnim == 'neutral' else 'torso'

        def matchRunningAnim(toon = self):
            toon.playingAnim = None
            toon.setSpeed(self.forwardSpeed, self.rotateSpeed)
            return

        if not pie:
            return (Sequence(), Sequence(), flyPie)
        else:
            toss = Track((0, Sequence(Func(self.setPosHpr, x, y, z, h, 0, 0), Func(pie.reparentTo, self.rightHand), Func(pie.setPosHpr, 0, 0, 0, 0, 0, 0), Parallel(ActorInterval(self, 'throw', startFrame=46, partName=partName), animPie), Func(matchRunningAnim))), (16.0 / 24.0, Func(pie.detachNode)))
            fly = Track((14.0 / 24.0, SoundInterval(sound, node=self)), (16.0 / 24.0, Sequence(Func(flyPie.reparentTo, render), Func(flyPie.setScale, self.pieScale), Func(flyPie.setPosHpr, self, 0.52, 0.97, 2.24, 89.42, -10.56, 87.94), beginFlyIval, ProjectileInterval(flyPie, startVel=getVelocity, duration=3), Func(flyPie.detachNode))))
            return (toss, fly, flyPie)

    def getPieSplatInterval(self, x, y, z, pieCode):
        from toontown.toonbase import ToontownBattleGlobals
        from toontown.battle import BattleProps
        pieName = ToontownBattleGlobals.pieNames[self.pieType]
        splatName = 'splat-%s' % pieName
        if pieName == 'lawbook':
            splatName = 'dust'
        splat = BattleProps.globalPropPool.getProp(splatName)
        splat.setBillboardPointWorld(2)
        color = ToontownGlobals.PieCodeColors.get(pieCode)
        if color:
            splat.setColor(*color)
        vol = 1.0
        if pieName == 'lawbook':
            sound = loader.loadSfx('phase_11/audio/sfx/LB_evidence_miss.ogg')
            vol = 0.25
        else:
            sound = loader.loadSfx('phase_4/audio/sfx/AA_wholepie_only.ogg')
        ival = Parallel(Func(splat.reparentTo, render), Func(splat.setPos, x, y, z), SoundInterval(sound, node=splat, volume=vol), Sequence(ActorInterval(splat, splatName), Func(splat.detachNode)))
        return ival

    def cleanupPieModel(self):
        if self.pieModel != None:
            self.pieModel.detachNode()
            self.pieModel = None
        return

    def getFeedPetIval(self):
        return Sequence(ActorInterval(self, 'feedPet'), Func(self.animFSM.request, 'neutral'))

    def getScratchPetIval(self):
        return Sequence(ActorInterval(self, 'pet-start'), ActorInterval(self, 'pet-loop'), ActorInterval(self, 'pet-end'))

    def getCallPetIval(self):
        return ActorInterval(self, 'callPet')

    def enterGolfPuttLoop(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('loop-putt')

    def exitGolfPuttLoop(self):
        self.stop()

    def enterGolfRotateLeft(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('rotateL-putt')

    def exitGolfRotateLeft(self):
        self.stop()

    def enterGolfRotateRight(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('rotateR-putt')

    def exitGolfRotateRight(self):
        self.stop()

    def enterGolfPuttSwing(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('swing-putt')

    def exitGolfPuttSwing(self):
        self.stop()

    def enterGolfGoodPutt(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('good-putt', restart=0)

    def exitGolfGoodPutt(self):
        self.stop()

    def enterGolfBadPutt(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('badloop-putt', restart=0)

    def exitGolfBadPutt(self):
        self.stop()

    def enterFlattened(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        Emote.globalEmote.disableAll(self)
        sound = loader.loadSfx('phase_9/audio/sfx/toon_decompress.ogg')
        lerpTime = 0.1
        node = self.getGeomNode().getChild(0)
        self.origScale = node.getScale()
        self.track = Sequence(LerpScaleInterval(node, lerpTime, VBase3(2, 2, 0.025), blendType='easeInOut'))
        self.track.start(ts)
        self.setActiveShadow(1)

    def exitFlattened(self):
        self.playingAnim = 'neutral'
        if self.track != None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        node = self.getGeomNode().getChild(0)
        node.setScale(self.origScale)
        Emote.globalEmote.releaseAll(self)
        return

    def enterCogThiefRunning(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (('neutral', 1.0),
         ('run', 1.0),
         ('run', 1.0),
         ('run', -1.0))
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(1)
        return

    def exitCogThiefRunning(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()
        return

    def enterScientistJealous(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('scientistJealous')

    def exitScientistJealous(self):
        self.stop()

    def enterScientistEmcee(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('scientistEmcee')

    def exitScientistEmcee(self):
        self.stop()

    def enterScientistWork(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('scientistWork')

    def exitScientistWork(self):
        self.stop()

    def enterScientistLessWork(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('scientistWork', fromFrame=319, toFrame=619)

    def exitScientistLessWork(self):
        self.stop()

    def enterScientistPlay(self, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.loop('scientistGame')

    def exitScientistPlay(self):
        self.stop()

    def getDustCloud(self, delay = 0.5, color = None):
        dustCloud = DustCloud.DustCloud(fBillboard=0, wantSound=1)
        dustCloud.setBillboardAxis(2.0)
        dustCloud.setZ(3)
        dustCloud.setScale(0.4)
        dustCloud.createTrack()
        sequence = Sequence(Wait(delay), Func(dustCloud.reparentTo, self), dustCloud.track, Func(dustCloud.destroy), name='dustCloudIval')
        if color is not None and hasattr(self, 'laffMeter'):
            self.laffMeter.color = color
            sequence.append(Func(self.laffMeter.adjustFace, self.hp, self.maxHp))
        return sequence

    def createHeadMeter(self):
        if self.headMeter:
            return
        nodePath = NodePath(self.nametag.getNameIcon())
        if nodePath.isEmpty():
            return
        self.headMeter = LaffMeter.LaffMeter(self.style, self.getHp(), self.getMaxHp())
        self.headMeter.av = self
        self.headMeter.reparentTo(nodePath)
        self.headMeter.setScale(1)
        self.headMeter.setBin('fixed', 40)
        self.headMeter.setDepthWrite(False)
        self.headMeter.start()
        self.setHeadPositions()

    def removeHeadMeter(self):
        if not self.headMeter:
            return
        else:
            self.headMeter.destroy()
            self.headMeter = None
            self.setHeadPositions()
            return

    def setGMIcon(self, access):
        if self.gmIcon:
            return
        icons = loader.loadModel('phase_3/models/props/gm_icons')
        self.gmIcon = icons.find('**/access_level_%s' % access)
        np = NodePath(self.nametag.getNameIcon())
        if np.isEmpty() or not self.gmIcon:
            return
        self.gmIcon.flattenStrong()
        self.gmIcon.reparentTo(np)
        self.gmIcon.setScale(1.6)
        self.gmIconInterval = LerpHprInterval(self.gmIcon, 3.0, Point3(0, 0, 0), Point3(-360, 0, 0))
        self.gmIconInterval.loop()
        self.setHeadPositions()

    def removeGMIcon(self):
        if not self.gmIcon:
            return
        else:
            self.gmIconInterval.finish()
            self.gmIcon.detachNode()
            del self.gmIconInterval
            self.gmIcon = None
            self.setHeadPositions()
            return

    def setPartyHat(self):
        if self.partyHat:
            return
        nodePath = NodePath(self.nametag.getNameIcon())
        if nodePath.isEmpty():
            return
        model = loader.loadModel('phase_4/models/parties/partyStickerbook')
        self.partyHat = model.find('**/Stickerbook_PartyIcon')
        self.partyHat.setHpr(0.0, 0.0, -50.0)
        self.partyHat.setScale(4)
        self.partyHat.setBillboardAxis()
        self.partyHat.reparentTo(nodePath)
        model.removeNode()
        self.setHeadPositions()

    def removePartyHat(self):
        if not self.partyHat:
            return
        else:
            self.partyHat.detachNode()
            self.partyHat = None
            self.setHeadPositions()
            return

    def setHeadPositions(self):
        position = 2.5
        if self.gmIcon:
            self.gmIcon.setZ(position)
            position += 2.5 if self.trophyStar else 2.7
        if self.trophyStar:
            self.trophyStar.setZ(position)
            position += 2.7
        if self.headMeter:
            self.headMeter.setZ(position)
            position += 3.3
        if self.partyHat:
            self.partyHat.setZ(position)

    def permanentLookAt(self, where):
        self.stopPermanentLookAt()
        taskMgr.add(lambda task: self.__permanentLookAt(where), self.uniqueName('permanentLookAt'))

    def __permanentLookAt(self, where):
        if not where or where.isEmpty():
            return Task.done
        posHpr = self.getHpr()
        self.headsUp(where)
        if (not self.lookAtSeq or not self.lookAtSeq.isPlaying()) and self.getHpr() != posHpr:
            self.lookAtSeq = Sequence(ActorInterval(self, 'walk', startFrame=0, endFrame=5), Func(self.loop, 'neutral'))
            self.lookAtSeq.start()
        return Task.cont

    def stopPermanentLookAt(self):
        taskMgr.remove(self.uniqueName('permanentLookAt'))


@magicWord(category=CATEGORY_PROGRAMMER, types=[int])
def headMeter(create = True):
    for av in base.cr.doId2do.values():
        if isinstance(av, Toon):
            av.createHeadMeter() if create else av.removeHeadMeter()


@magicWord(category=CATEGORY_PROGRAMMER, types=[int])
def partyHat(create = True):
    for av in base.cr.doId2do.values():
        if isinstance(av, Toon):
            av.setPartyHat() if create else av.removePartyHat()