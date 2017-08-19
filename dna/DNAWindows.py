# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAWindows
from panda3d.core import DecalEffect, LVector4, LVector4f, NodePath
import DNAGroup
import DNAUtil
import random

class DNAWindows(DNAGroup.DNAGroup):
    COMPONENT_CODE = 11

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)
        self.windowCount = 0

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def setWindowCount(self, windowCount):
        self.windowCount = windowCount

    def getWindowCount(self):
        return self.windowCount

    @staticmethod
    def setupWindows(parentNode, dnaStorage, code, windowCount, color, hpr, scale):
        stripped = code[:-1]
        nodeR = assetStorage.findNode(stripped + 'r')
        nodeL = assetStorage.findNode(stripped + 'l')
        if nodeR is None or nodeL is None:
            raise Exception('DNAWindows code %s not found inDNAStorage' % code)

        def makeWindow(x, y, z, parentNode, color, scale, hpr, flip = False):
            node = nodeR if not flip else nodeL
            window = node.copyTo(parentNode, 0)
            window.setColor(color)
            window.setScale(NodePath(), scale)
            window.setHpr(hpr)
            window.setPos(x, y, z)
            window.setEffect(DecalEffect.make())
            window.flattenStrong()
            window.setDepthOffset(5)

        offset = lambda : random.random() % 0.0375
        if windowCount == 1:
            makeWindow(offset() + 0.5, 0, offset() + 0.5, parentNode, color, scale, hpr)
        elif windowCount == 2:
            makeWindow(offset() + 0.33, 0, offset() + 0.5, parentNode, color, scale, hpr)
            makeWindow(offset() + 0.66, 0, offset() + 0.5, parentNode, color, scale, hpr, True)
        elif windowCount == 3:
            makeWindow(offset() + 0.33, 0, offset() + 0.66, parentNode, color, scale, hpr)
            makeWindow(offset() + 0.66, 0, offset() + 0.66, parentNode, color, scale, hpr, True)
            makeWindow(offset() + 0.5, 0, offset() + 0.33, parentNode, color, scale, hpr)
        elif windowCount == 4:
            makeWindow(offset() + 0.33, 0, offset() + 0.25, parentNode, color, scale, hpr)
            makeWindow(offset() + 0.66, 0, offset() + 0.25, parentNode, color, scale, hpr, True)
            makeWindow(offset() + 0.33, 0, offset() + 0.66, parentNode, color, scale, hpr)
            makeWindow(offset() + 0.66, 0, offset() + 0.66, parentNode, color, scale, hpr, True)
        else:
            raise NotImplementedError('Invalid window count ' + str(windowCount))
        nodeR.removeNode()
        nodeL.removeNode()
        return

    def makeFromDGI(self, dgi):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.color = DNAUtil.dgiExtractColor(dgi)
        self.windowCount = dgi.getUint8()

    def traverse(self, nodePath, dnaStorage):
        if self.getWindowCount() == 0:
            return
        parentX = nodePath.getParent().getScale().getX()
        scale = random.random() % 0.0375
        if parentX <= 5.0:
            scale += 1.0
        elif parentX <= 10.0:
            scale += 1.15
        else:
            scale += 1.3
        hpr = (0, 0, 0)
        DNAWindows.setupWindows(nodePath, dnaStorage, self.getCode(), self.getWindowCount(), self.getColor(), hpr, scale)