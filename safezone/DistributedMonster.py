# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.safezone.DistributedMonster
from direct.distributed.DistributedObject import DistributedObject
from otp.avatar import Emote
from otp.nametag.NametagConstants import CFSpeech, CFTimeout
from otp.nametag import NametagGroup, NametagGlobals
from otp.otpbase import OTPLocalizer
from toontown.safezone import TreasureGlobals
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.suit import SuitDNA, Suit, Goon
from toontown.toon import ToonDNA, Toon, TTEmote
from toontown.toon.NPCToons import NameGen
import random

class DistributedMonster(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.index = 0
        self.seed = 0
        self.reward = 0
        self.taskIteration = 0
        self.actor = None
        self.randGen = None
        return

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.createActor()
        base.monsters.append(self)

    def delete(self):
        DistributedObject.delete(self)
        if self.actor:
            self.actor.delete()
            del self.actor
        del self.index
        del self.seed
        del self.randGen
        base.monsters.remove(self)

    def getNextType(self):
        return self.randGen.randrange(ToontownGlobals.MonsterSuit, ToontownGlobals.MonsterToon + 1)

    def createActor(self):
        self.type = self.getNextType()
        self.taskNum = 0
        if self.type == ToontownGlobals.MonsterSuit:
            self.createSuit()
        elif self.type == ToontownGlobals.MonsterGoon:
            self.createGoon()
        else:
            self.createToon()
        self.actor.setPickable(False)
        self.actor.initializeBodyCollisions('DistributedMonster-%d' % id(self.actor))
        self.actor.hide()
        self.updatePos()
        self.setTaskIteration(self.taskIteration)

    def createSuit(self):
        self.suitName = self.randGen.choice(SuitDNA.suitHeadTypes)
        self.dna = SuitDNA.SuitDNA()
        self.dna.newSuit(self.suitName)
        self.actor = Suit.Suit()
        self.actor.setDNA(self.dna)
        self.actor.setDisplayLevel()
        self.actor.loop('neutral')

    def createGoon(self):
        self.goonName = self.randGen.choice(SuitDNA.goonTypes)
        self.actor = Goon.Goon(self.goonName, False)
        self.actor.setName(TTLocalizer.MonsterGoonNames[self.goonName])
        self.actor.setPlayRate(0.5, 'walk')
        self.actor.loop('walk')

    def createToon(self):
        self.dna = ToonDNA.ToonDNA()
        self.dna.newToonRandom(self.seed)
        male = self.dna.getGender() == 'm'
        self.actor = Toon.Toon()
        self.actor.setDNA(self.dna)
        self.actor.setName(NameGen.randomNameMoreinfo(male, not male, self.randGen)[-1])
        self.actor.setPlayerType(NametagGroup.CCNonPlayer)
        self.actor.animFSM.request('neutral')
        self.messages = TTLocalizer.ChatGarblers[self.actor.style.head[0]]

    def getPos(self):
        if self.zoneId not in TreasureGlobals.MonsterSpawns:
            return ((0, 0, 0), 0)
        positions = TreasureGlobals.MonsterSpawns[self.zoneId]
        return positions[0 if len(positions) <= self.index else self.index]

    def updatePos(self):
        if not self.actor:
            return
        pos, h = self.getPos()
        self.actor.reparentTo(render)
        self.actor.setPos(*pos)
        self.actor.setHpr(h, 0, 0)

    def getIndex(self):
        return self.index

    def getSeed(self):
        return self.seed

    def getReward(self):
        return self.reward

    def getType(self):
        return self.type

    def getTaskIteration(self):
        return self.taskIteration

    def setIndex(self, index):
        self.index = index
        self.updatePos()

    def setSeed(self, seed):
        self.seed = seed
        self.randGen = random.Random()
        self.randGen.seed(seed)

    def setReward(self, reward):
        self.reward = reward

    def setTaskIteration(self, taskIteration):
        self.taskIteration = taskIteration
        if not self.actor:
            return
        if self.type == ToontownGlobals.MonsterSuit:
            self.__suitTask()
        elif self.type == ToontownGlobals.MonsterGoon:
            self.__goonTask()
        elif self.type == ToontownGlobals.MonsterToon:
            self.__toonTask()

    def setTalk(self, talk):
        if self.taskIteration in TTLocalizer.MonsterTalk[self.type]:
            self.actor.setChatAbsolute(TTLocalizer.MonsterTalk[self.type][self.taskIteration][talk], CFSpeech | CFTimeout, quiet=True)

    def d_catchMonster(self):
        self.sendUpdate('catchMonster', [])

    def monsterCatched(self, code):
        print 'Monster catched: %s' % self.code

    def __goonTask(self):
        if self.taskIteration == 0:
            self.actor.loop('walk')
        elif self.taskIteration in (3, 8):
            self.actor.play('collapse')
        elif self.taskIteration in (7, 10):
            self.actor.play('recovery')

    def __toonTask(self):
        length = len(TTEmote.Emotes)
        Emote.globalEmote.doEmote(self.actor, min(length - 1, length - self.taskIteration % length), volume=0)
        chatString = []
        for i in xrange(random.randint(4, 10)):
            chatString.append(random.choice(self.messages))

        self.actor.setChatAbsolute('\x01italic\x01%s\x02' % ' '.join(chatString), CFSpeech | CFTimeout, quiet=True)

    def __suitTask(self):
        taunts = OTPLocalizer.SuitFaceoffTaunts[self.suitName]
        length = len(taunts)
        self.actor.setChatAbsolute(taunts[max(0, min(length - 1, length - self.taskIteration % length))], CFSpeech | CFTimeout, quiet=True)

    def __mouseEnter(self, region, extra):
        print 'entered'

    def __mouseLeave(self, region, extra):
        print 'leavd'