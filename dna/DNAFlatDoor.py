# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAFlatDoor
from panda3d.core import DecalEffect
import DNADoor

class DNAFlatDoor(DNADoor.DNADoor):
    COMPONENT_CODE = 17

    def traverse(self, nodePath, dnaStorage):
        node = assetStorage.findNode(self.code, self.getName())
        node.reparentTo(nodePath, 0)
        node.setScale(hidden, 1, 1, 1)
        node.setPosHpr((0.5, 0, 0), (0, 0, 0))
        node.setColor(self.color)
        node.getNode(0).setEffect(DecalEffect.make())
        node.flattenStrong()