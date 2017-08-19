# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.DistributedPaintShopInterior
from direct.distributed.DistributedObject import DistributedObject
from direct.actor.Actor import Actor
from RandomBuilding import RandomBuilding

class DistributedPaintShopInterior(DistributedObject, RandomBuilding):

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.setup()

    def setup(self):
        randomGen = self.getRandomGen()
        colors = self.getColors()
        self.interior = loader.loadModel('phase_4/models/modules/PaintShopInterior')
        self.interior.reparentTo(render)
        self.mixer = Actor('phase_4/models/props/pos_PS_Mixer_zero', {'mix': 'phase_4/models/props/pos_PS_Mixer_mix'})
        self.mixer.reparentTo(self.interior)
        self.mixer.setPlayRate(2.1, 'mix')
        self.mixer.loop('mix', fromFrame=20, toFrame=160)
        if settings['smoothAnimations']:
            self.mixer.setBlend(frameBlend=True)
        self.setupDoor(randomGen, colors, self.interior, -0.25)
        self.resetNPCs()

    def disable(self):
        self.mixer.removeNode()
        del self.mixer
        self.interior.removeNode()
        del self.interior
        DistributedObject.disable(self)