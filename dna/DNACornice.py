# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNACornice
from panda3d.core import DecalEffect, LVector3, LVector3f, LVector4, LVector4f
import DNAGroup
import DNAUtil

class DNACornice(DNAGroup.DNAGroup):
    COMPONENT_CODE = 12

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def makeFromDGI(self, dgi):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.color = DNAUtil.dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        pParentXScale = nodePath.getParent().getScale().getX()
        parentZScale = nodePath.getScale().getZ()
        node = assetStorage.findNode(self.code, self.getName())
        nodePathA = nodePath.attachNewNode('cornice-internal', 0)
        np = node.find('**/*_d').copyTo(nodePathA, 0)
        np.setPosHprScale(LVector3f(0, 0, 0), LVector3f(0, 0, 0), LVector3f(1, pParentXScale / parentZScale, pParentXScale / parentZScale))
        np.setEffect(DecalEffect.make())
        np.flattenStrong()
        np = node.find('**/*_nd').copyTo(nodePathA, 1)
        np.setPosHprScale(LVector3f(0, 0, 0), LVector3f(0, 0, 0), LVector3f(1, pParentXScale / parentZScale, pParentXScale / parentZScale))
        np.flattenStrong()
        nodePathA.setPosHprScale(LVector3f(0, 0, node.getScale().getZ()), LVector3f(0, 0, 0), LVector3f(1, 1, 1))
        nodePathA.setColor(self.color)
        nodePathA.flattenStrong()
        node.removeNode()