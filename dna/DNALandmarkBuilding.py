# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNALandmarkBuilding
from panda3d.core import LVector4, LVector4f
import DNANode
import DNAUtil

class DNALandmarkBuilding(DNANode.DNANode):
    COMPONENT_CODE = 13

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
        self.code = ''
        self.wallColor = LVector4f(1, 1, 1, 1)
        self.title = ''
        self.buildingType = ''
        self.door = None
        return

    def setBuildingType(self, buildingType):
        self.buildingType = buildingType

    def getBuildingType(self):
        return self.buildingType

    def setTitle(self, title):
        self.title = title

    def getTitle(self):
        return self.title

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def setWallColor(self, color):
        self.wallColor = color

    def getWallColor(self):
        return self.wallColor

    def setupSuitBuildingOrigin(self, nodePathA, nodePathB):
        if self.getName()[:2] == 'tb' and self.getName()[3].isdigit() and self.getName().find(':') != -1:
            name = self.getName()
            name = 's' + name[1:]
            node = nodePathB.find('**/*suit_building_origin')
            if node.isEmpty():
                node = nodePathA.attachNewNode(name)
                node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
            else:
                node.wrtReparentTo(nodePathA, 0)
                node.setName(name)

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.wallColor = DNAUtil.dgiExtractColor(dgi)
        self.title = DNAUtil.dgiExtractString8(dgi)
        self.buildingType = DNAUtil.dgiExtractString8(dgi)

    def traverse(self, nodePath, dnaStorage):
        node = assetStorage.findNode(self.code, self.getName())
        node.reparentTo(nodePath, 0)
        node.setName(self.name)
        node.setPosHprScale(self.pos, self.hpr, self.scale)
        self.setupSuitBuildingOrigin(nodePath, node)
        for child in self.children:
            child.traverse(node, dnaStorage)

        node.flattenStrong()