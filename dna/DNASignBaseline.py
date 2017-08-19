# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNASignBaseline
from panda3d.core import BamFile, NodePath, StringStream, compressString, decompressString
import DNANode

class DNASignBaseline(DNANode.DNANode):
    COMPONENT_CODE = 6

    def __init__(self):
        DNANode.DNANode.__init__(self, '')
        self.data = ''

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.data = dgi.getString()
        if len(self.data):
            self.data = decompressString(self.data)

    def traverse(self, nodePath, dnaStorage):
        node = nodePath.attachNewNode('baseline', 0)
        node.setPosHpr(self.pos, self.hpr)
        node.setDepthOffset(10)
        node.setPos(node, 0, -0.1, 0)
        if self.data:
            bf = BamFile()
            ss = StringStream()
            ss.setData(self.data)
            bf.openRead(ss)
            signText = NodePath(bf.readNode())
            signText.reparentTo(node)
        node.flattenStrong()
        for child in self.children:
            child.traverse(nodePath, dnaStorage)