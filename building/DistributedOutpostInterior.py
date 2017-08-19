# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.DistributedOutpostInterior
from direct.distributed.DistributedObject import DistributedObject
from RandomBuilding import RandomBuilding

class DistributedOutpostInterior(DistributedObject, RandomBuilding):

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.setup()

    def setup(self):
        randomGen = self.getRandomGen()
        colors = self.getColors()
        self.interior = loader.loadModel('phase_4/models/modules/toon_outpost_interior')
        self.interior.reparentTo(render)
        self.setupDoor(randomGen, colors, self.interior)
        self.replaceRandomInModel(randomGen, colors, self.interior)
        self.interior.flattenMedium()
        self.resetNPCs()

    def disable(self):
        self.interior.removeNode()
        del self.interior
        DistributedObject.disable(self)