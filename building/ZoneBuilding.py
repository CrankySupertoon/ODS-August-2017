# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.ZoneBuilding
from toontown.hood import ZoneUtil
import ToonInteriorColors
import random

class ZoneBuilding:

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def getBlock(self):
        return self.block

    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]

    def getRandomGen(self):
        randomGen = random.Random()
        randomGen.seed(self.zoneId)
        return randomGen

    def getColors(self):
        hoodId = ZoneUtil.getHoodId(self.zoneId)
        return ToonInteriorColors.colors[hoodId]