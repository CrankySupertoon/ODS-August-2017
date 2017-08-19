# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.TutorialUtil
from panda3d.core import Quat, Vec3, headsUp
from toontown.suit.DistributedSuitBase import DistributedSuitBase
from toontown.suit.BossCog import BossCog
from toontown.suit.SuitDNA import SuitDNA
from toontown.suit.Suit import Suit
import random
DistributedSuit = 0
RegularSuit = 1
BossSuit = 2

def getHeadsUpHpr(fromPos, toPos):
    quat = Quat()
    headsUp(quat, toPos - fromPos, Vec3.up())
    return quat.getHpr()


def createSuit(self, suitName, posHpr, type = RegularSuit, hasNametag = True, active = False, level = None, parent = None, anim = 'neutral'):
    if not parent:
        parent = self.getGeom()
    if type == DistributedSuit:
        suit = DistributedSuitBase(base.cr)
        suit.doId = id(suit)
    elif type == RegularSuit:
        suit = Suit()
    elif type == BossSuit:
        suit = BossCog()
    dna = SuitDNA()
    if type == BossSuit:
        dna.newBossCog(suitName)
    elif not suitName:
        dna.newSuitRandom()
    elif not isinstance(suitName, str):
        dna.newSuit(random.choice(suitName))
    else:
        dna.newSuit(suitName)
    suit.setDNA(dna)
    suit.reparentTo(parent)
    suit.setPosHpr(*posHpr)
    suit.loop(anim)
    if not hasNametag:
        suit.nametag3d.removeNode()
        suit.nametag.destroy()
    else:
        suit.setDisplayLevel(level)
        if active:
            suit.addActive()
    return suit


def cleanupActor(actor):
    if actor:
        actor.delete()