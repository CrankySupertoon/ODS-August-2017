# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.DistributedPetshopInterior
from direct.distributed.DistributedObject import DistributedObject
from direct.actor.Actor import Actor
from RandomBuilding import RandomBuilding

class DistributedPetshopInterior(DistributedObject, RandomBuilding):

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.setup()

    def setup(self):
        randomGen = self.getRandomGen()
        colors = self.getColors()
        self.interior = loader.loadModel('phase_4/models/modules/PetShopInterior')
        self.interior.reparentTo(render)
        self.fish = Actor('phase_4/models/props/interiorfish-zero', {'swim': 'phase_4/models/props/interiorfish-swim'})
        self.fish.reparentTo(self.interior)
        self.fish.setColorScale(0.8, 0.9, 1, 0.8)
        self.fish.setScale(0.8)
        self.fish.setPos(0, 6, -4)
        self.fish.setPlayRate(0.7, 'swim')
        self.fish.loop('swim')
        if settings['smoothAnimations']:
            self.fish.setBlend(frameBlend=True)
        self.setupDoor(randomGen, colors, self.interior, -0.25)
        self.resetNPCs()

    def disable(self):
        self.fish.cleanup()
        del self.fish
        self.interior.removeNode()
        del self.interior
        DistributedObject.disable(self)