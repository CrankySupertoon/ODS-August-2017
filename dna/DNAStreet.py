# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAStreet
from panda3d.core import LVector4, LVector4f, Texture
import DNANode
import DNAUtil

class DNAStreet(DNANode.DNANode):
    COMPONENT_CODE = 18

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
        self.code = ''
        self.streetTexture = ''
        self.sideWalkTexture = ''
        self.curbTexture = ''
        self.streetColor = LVector4f(1, 1, 1, 1)
        self.sidewalkColor = LVector4f(1, 1, 1, 1)
        self.curbColor = LVector4f(1, 1, 1, 1)
        self.setTexCnt = 0
        self.setColCnt = 0

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setStreetTexture(self, texture):
        self.streetTexture = texture

    def getStreetTexture(self):
        return self.streetTexture

    def setSidewalkTexture(self, texture):
        self.sidewalkTexture = texture

    def getSidewalkTexture(self):
        return self.sidewalkTexture

    def setCurbTexture(self, texture):
        self.curbTexture = texture

    def getCurbTexture(self):
        return self.curbTexture

    def setStreetColor(self, color):
        self.streetColor = color

    def getStreetColor(self):
        return self.streetColor

    def setSidewalkColor(self, color):
        self.SidewalkColor = color

    def getSidewalkColor(self):
        return self.sidewalkColor

    def getCurbColor(self):
        return self.curbColor

    def setTextureColor(self, color):
        self.Color = color

    def setTexture(self, texture):
        if self.setTexCnt == 0:
            self.streetTexture = texture
        if self.setTexCnt == 1:
            self.sidewalkTexture = texture
        if self.setTexCnt == 2:
            self.curbTexture = texture
        self.setTexCnt += 1

    def setColor(self, color):
        if self.setColCnt == 0:
            self.streetColor = color
        if self.setColCnt == 1:
            self.sidewalkColor = color
        if self.setColCnt == 2:
            self.curbColor = color
        self.setColCnt += 1

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.streetTexture = DNAUtil.dgiExtractString8(dgi)
        self.sidewalkTexture = DNAUtil.dgiExtractString8(dgi)
        self.curbTexture = DNAUtil.dgiExtractString8(dgi)
        self.streetColor = DNAUtil.dgiExtractColor(dgi)
        self.sideWalkColor = DNAUtil.dgiExtractColor(dgi)
        self.curbColor = DNAUtil.dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        node = assetStorage.findNode(self.code, self.getName())
        node.reparentTo(nodePath, 0)
        streetTexture = assetStorage.findTexture(self.streetTexture)
        sidewalkTexture = assetStorage.findTexture(self.sidewalkTexture)
        curbTexture = assetStorage.findTexture(self.curbTexture)
        if self.sidewalkTexture == 'street_sidewalk_BR_tex':
            for np in node.findAllMatches('+CollisionNode'):
                if 'sidewalk' in np.getName():
                    np.setTag('footstepCode', 'snow')

        if streetTexture is None:
            raise Exception('street texture not found in DNAStorage : ' + self.streetTexture)
        if sidewalkTexture is None:
            raise Exception('sidewalk texture not found in DNAStorage : ' + self.sidewalkTexture)
        if curbTexture is None:
            raise Exception('curb texture not found in DNAStorage : ' + self.curbTexture)
        streetNode = node.find('**/*_street')
        sidewalkNode = node.find('**/*_sidewalk')
        curbNode = node.find('**/*_curb')
        if not streetNode.isEmpty():
            streetNode.setTexture(streetTexture, 1)
            streetNode.setColorScale(self.streetColor, 0)
        if not sidewalkNode.isEmpty():
            sidewalkNode.setTexture(sidewalkTexture, 1)
            sidewalkNode.setColorScale(self.sidewalkColor, 0)
        if not curbNode.isEmpty():
            curbNode.setTexture(curbTexture, 1)
            curbNode.setColorScale(self.curbColor, 0)
        node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
        node.flattenStrong()
        return