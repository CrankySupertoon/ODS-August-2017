# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAInteractiveProp
from panda3d.core import ModelNode
import DNAAnimProp

class DNAInteractiveProp(DNAAnimProp.DNAAnimProp):
    COMPONENT_CODE = 15

    def __init__(self, name):
        DNAAnimProp.DNAAnimProp.__init__(self, name)
        self.cellId = -1

    def setCellId(self, id):
        self.cellId = id

    def getCellId(self):
        return self.cellId

    def makeFromDGI(self, dgi):
        DNAAnimProp.DNAAnimProp.makeFromDGI(self, dgi)
        self.cellId = dgi.getInt16()

    def traverse(self, nodePath, dnaStorage):
        if self.code == 'DCS':
            node = ModelNode(self.name)
            node.setPreserveTransform(ModelNode.PTNet)
            node = nodePath.attachNewNode(node, 0)
        else:
            node = assetStorage.findNode(self.code, self.getName())
            node.reparentTo(nodePath, 0)
            node.setName(self.name)
        node.setTag('DNAAnim', self.animName)
        node.setTag('DNACellIndex', str(self.cellId))
        node.setPosHprScale(self.pos, self.hpr, self.scale)
        node.setColorScale(self.color, 0)
        node.flattenStrong()
        for child in self.children:
            child.traverse(node, dnaStorage)