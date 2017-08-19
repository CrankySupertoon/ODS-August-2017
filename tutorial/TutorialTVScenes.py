# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.TutorialTVScenes
from panda3d.core import Camera
from direct.task.Task import Task
from otp.avatar import Emote
from toontown.television.TVScenes import *
from toontown.television.TVEffects import *
from toontown.suit.Suit import Suit
from toontown.suit.BossCog import BossCog
from toontown.suit.SuitDNA import SuitDNA
from toontown.toon import NPCToons, TTEmote
import random

class CEOScene(ThreeDScene):
    CameraPos = [(0, 203.5, 23.5, 0, 350, 0)]

    def __init__(self, effects = []):
        ThreeDScene.__init__(self, 'CEOScene', effects)
        self.geom = loader.loadModel('phase_12/models/bossbotHQ/BanquetInterior_1')
        self.geom.reparentTo(self)
        self.ceo = BossCog()
        dna = SuitDNA()
        dna.newBossCog('c')
        self.ceo.setDNA(dna)
        self.ceo.reparentTo(self)
        self.ceo.setPosHpr(0, 236.5, 0, 180, 0, 0)
        self.ceo.loop('Bb_neutral')

    def delete(self):
        if self.geom:
            self.geom.removeNode()
            self.geom = None
        if self.ceo:
            self.ceo.delete()
            self.ceo = None
        ThreeDScene.delete(self)
        return


class HeadHunterScene(ThreeDScene):
    CameraPos = [(-22, -12.5, 7, 92, -6, 0)]

    def __init__(self, effects = []):
        ThreeDScene.__init__(self, 'HeadHunterScene', effects)
        self.geom = loader.loadModel('phase_12/models/bossbotHQ/BossbotEntranceRoom')
        self.geom.reparentTo(self)
        self.cog = Suit()
        dna = SuitDNA()
        dna.newSuit('hh')
        self.cog.setDNA(dna)
        self.cog.reparentTo(self)
        self.cog.setPosHpr(-32.5, -12.5, 0.02, 270, 0, 0)
        self.cog.nametag3d.removeNode()
        self.cog.nametag.destroy()
        self.cog.loop('neutral')

    def delete(self):
        if self.geom:
            self.geom.removeNode()
            self.geom = None
        if self.cog:
            self.cog.delete()
            self.cog = None
        ThreeDScene.delete(self)
        return


class ScientistScene(ThreeDScene):
    CameraPos = [(-47.5, 0.5, 3.415, 90, 0, 0)]
    ToonPos = {2018: (-59, -1.5, 0.02, 270, 0, 0),
     2019: (-59, 0.5, 0.02, 270, 0, 0),
     2020: (-59, 2.5, 0.02, 270, 0, 0)}
    RandomEmotes = ['wave',
     'angry',
     'applause',
     'cringe',
     'confused',
     'slip-forward',
     'slip-backward',
     'resistance-salute',
     'surprise',
     'cry',
     'furious',
     'laugh',
     'idea',
     'taunt',
     'rage']

    def __init__(self, effects = []):
        ThreeDScene.__init__(self, 'ScientistScene', effects)
        self.geom = loader.loadModel('phase_3.5/models/modules/tt_m_ara_int_toonhall')
        self.geom.reparentTo(self)
        self.taskStarted = False
        self.npcs = []
        for id, posHpr in self.ToonPos.iteritems():
            npc = NPCToons.createLocalNPC(id)
            npc.reparentTo(self.geom)
            npc.setPosHpr(*posHpr)
            npc.nametag3d.removeNode()
            npc.nametag.destroy()
            self.npcs.append(npc)

    def delete(self):
        if self.geom:
            self.geom.removeNode()
            self.geom = None
        for npc in self.npcs:
            taskMgr.remove(npc.uniqueName('randomEmote'))
            npc.delete()

        self.npcs = []
        self.taskStarted = False
        ThreeDScene.delete(self)
        return

    def startTask(self):
        if self.taskStarted:
            return
        for i, npc in enumerate(self.npcs):
            taskMgr.doMethodLater(0.25 * i, lambda task, npc = npc: self.doRandomEmote(npc, task), npc.uniqueName('randomEmote'))

        self.taskStarted = True

    def stopTask(self):
        if not self.taskStarted:
            return
        for npc in self.npcs:
            taskMgr.remove(npc.uniqueName('randomEmote'))

        self.taskStarted = False

    def doRandomEmote(self, npc, task):
        Emote.globalEmote.doEmote(npc, TTEmote.Emotes.index(random.choice(self.RandomEmotes)), 0)
        task.delayTime = npc.emoteTrack.getDuration() + 1.0
        return task.again