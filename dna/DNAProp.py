# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAProp
from panda3d.core import LVector4, LVector4f, ModelNode
import DNANode
import DNAUtil

class DNAProp(DNANode.DNANode):
    COMPONENT_CODE = 4

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.color = DNAUtil.dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        if self.code == 'DCS':
            node = ModelNode(self.name)
            node.setPreserveTransform(ModelNode.PTNet)
            node = nodePath.attachNewNode(node)
        else:
            node = assetStorage.findNode(self.code, self.getName())
            if node is None:
                node = nodePath.attachNewNode(self.name, 0)
            else:
                node.reparentTo(nodePath, 0)
                node.setName(self.name)
        node.setPosHprScale(self.pos, self.hpr, self.scale)
        node.setColorScale(self.color, 0)
        for child in self.children:
            child.traverse(node, dnaStorage)

        return