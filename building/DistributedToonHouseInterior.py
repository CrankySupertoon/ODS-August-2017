# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.DistributedToonHouseInterior
from direct.distributed.DistributedObject import DistributedObject
from toontown.building.HouseInterior import HouseInterior
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase
from ZoneBuilding import ZoneBuilding

class DistributedToonHouseInterior(DistributedObject, HouseInterior, ZoneBuilding):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        HouseInterior.__init__(self)
        self.ownerId = -1
        self.director = None
        self.posIndices = []
        return

    def getBlock(self):
        return self.block

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.setup()
        self.setPosIndices(self.posIndices)

    def disable(self):
        HouseInterior.disable(self)
        DistributedObject.disable(self)

    def getInteriorObject(self):
        return self

    def setPosIndices(self, posIndices):
        self.posIndices = posIndices
        if not self.interior:
            return
        for i, posHpr in enumerate(self.posIndices):
            origin = self.interior.find('**/npc_origin_%s' % i)
            if origin.isEmpty():
                origin = self.interior.attachNewNode('npc_origin_%s' % i)
            origin.setPosHpr(*posHpr)

        for npcToon in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npcToon.initToonState()