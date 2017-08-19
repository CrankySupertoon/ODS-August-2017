# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.DistributedNPCToonBase
from panda3d.core import Camera, CollideMask, CollisionNode, CollisionTube, NodePath, Point3, headsUp, lookAt
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import ClockDelta
from direct.distributed import DistributedObject
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.interval.IntervalGlobal import *
import random
import DistributedToon
import NPCToons
from otp.nametag.NametagGroup import NametagGroup
from toontown.quest import QuestChoiceGui
from toontown.quest import Quests
from toontown.toonbase import ToontownGlobals

class DistributedNPCToonBase(DistributedToon.DistributedToon):

    def __init__(self, cr):
        try:
            self.DistributedNPCToon_initialized
        except:
            self.DistributedNPCToon_initialized = 1
            DistributedToon.DistributedToon.__init__(self, cr)
            self.deleteShadowPlacer()
            self.setPickable(0)
            self.setPlayerType(NametagGroup.CCNonPlayer)

    def disable(self):
        DistributedToon.DistributedToon.disable(self)
        self.ignoreAll()

    def delete(self):
        try:
            self.DistributedNPCToon_deleted
        except:
            self.DistributedNPCToon_deleted = 1
            self.__deleteCollisions()
            self.stopTalkSequence()
            DistributedToon.DistributedToon.delete(self)

    def isPlayerControlled(self):
        return False

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
        self.__bookActor = None
        self.__holeActor = None
        return

    def announceGenerate(self):
        self.initColls()
        self.initToonState()
        DistributedToon.DistributedToon.announceGenerate(self)

    def initColls(self):
        self.__initCollisions(self.attributes['collRadius'] if 'collRadius' in self.attributes else self.getCollSphereRadius())
        self.cSphereNode.setName(self.uniqueName('NPCToon'))
        self.detectAvatars()
        self.setParent(ToontownGlobals.SPRender)
        self.startLookAround()

    def initToonState(self):
        if self.attributes.get('shadowHidden', False):
            self.hideShadow()
        for fields in [('chatter', self.startTalkSequence), ('animState', self.setAnimState), ('relativePos', self.setPos)]:
            field, setter = fields
            if field in self.attributes:
                setter(*self.attributes[field])

        if self.attributes.get('reparentOnReload', False):
            self.accept('enterPlayground', self.initToonPos)
        self.initToonPos()
        self.postToonStateInit()

    def initToonPos(self):
        if 'pos' in self.attributes:
            pos = self.attributes['pos']
            self.setPos(*pos[0])
            self.setH(pos[1])
        else:
            npcOrigin = self.attributes['originId'] if 'originId' in self.attributes else self.getNpcOrigin()
            if '%s' in npcOrigin:
                npcOrigin %= self.posIndex
            npcOrigin = self.getNpcOriginParent().find(npcOrigin)
            if not npcOrigin.isEmpty():
                self.reparentTo(npcOrigin)

    def getNpcOriginParent(self):
        return render

    def getNpcOrigin(self):
        return '**/npc_origin_%s'

    def postToonStateInit(self):
        pass

    def wantsSmoothing(self):
        return 0

    def detectAvatars(self):
        self.accept('enter' + self.cSphereNode.getName(), self.handleCollisionSphereEnter)

    def ignoreAvatars(self):
        self.ignore('enter' + self.cSphereNode.getName())

    def getCollSphereRadius(self):
        return 3.25

    def __initCollisions(self, radius):
        self.cSphere = CollisionTube(0.0, 1.0, 0.0, 0.0, 1.0, 5.0, radius)
        self.cSphere.setTangible(0)
        self.cSphereNode = CollisionNode('cSphereNode')
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)

    def __deleteCollisions(self):
        del self.cSphere
        del self.cSphereNode
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath

    def handleCollisionSphereEnter(self, collEntry):
        pass

    def setupAvatars(self, av):
        self.ignoreAvatars()
        self.lookAtAvatar(av)

    def lookAtAvatar(self, av):
        av.headsUp(self, 0, 0, 0)
        self.headsUp(av, 0, 0, 0)
        av.stopLookAround()
        av.lerpLookAt(Point3(-0.5, 4, 0), time=0.5)
        self.stopLookAround()
        self.lerpLookAt(Point3(av.getPos(self)), time=0.5)

    def b_setPageNumber(self, paragraph, pageNumber):
        self.setPageNumber(paragraph, pageNumber)
        self.d_setPageNumber(paragraph, pageNumber)

    def d_setPageNumber(self, paragraph, pageNumber):
        timestamp = ClockDelta.globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('setPageNumber', [paragraph, pageNumber, timestamp])

    def freeAvatar(self):
        base.localAvatar.posCamera(0, 0)
        base.cr.playGame.getPlace().setState('walk')

    def setPositionIndex(self, posIndex):
        self.posIndex = posIndex

    def setNpcId(self, npcId):
        self.npcId = npcId
        self.attributes = NPCToons.SpecialNPCAttributes.get(npcId, {})