# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.DistributedKartShopInterior
from direct.distributed.DistributedObject import DistributedObject
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase
from ZoneBuilding import ZoneBuilding

class DistributedKartShopInterior(DistributedObject, ZoneBuilding):

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.setup()

    def disable(self):
        self.interior.removeNode()
        del self.interior
        DistributedObject.disable(self)

    def setup(self):
        self.interior = loader.loadModel('phase_6/models/karting/KartShop_Interior')
        self.interior.reparentTo(render)
        self.interior.flattenMedium()
        for npcToon in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npcToon.initToonState()