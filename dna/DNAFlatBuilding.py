# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAFlatBuilding
from panda3d.core import DecalEffect, NodePath
import DNANode
import DNAWall
import random

class DNAFlatBuilding(DNANode.DNANode):
    COMPONENT_CODE = 9
    currentWallHeight = 0

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
        self.width = 0
        self.hasDoor = False

    def setWidth(self, width):
        self.width = width

    def getWidth(self):
        return self.width

    def setCurrentWallHeight(self, currentWallHeight):
        DNAFlatBuilding.currentWallHeight = currentWallHeight

    def getCurrentWallHeight(self):
        return DNAFlatBuilding.currentWallHeight

    def setHasDoor(self, hasDoor):
        self.hasDoor = hasDoor

    def getHasDoor(self):
        return self.hasDoor

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.width = dgi.getInt16() / 100.0
        self.hasDoor = dgi.getBool()

    def setupGenericSuitFlatBuilding(self, nodePath, dnaStorage, name, wallName):
        if self.name[:2] != 'tb':
            return
        name = name + self.name[2:]
        node = nodePath.attachNewNode(name)
        node.setPosHpr(self.pos, self.hpr)
        numCodes = assetStorage.getNumCatalogCodes(wallName)
        if numCodes < 1:
            return
        code = assetStorage.getCatalogCode(wallName, random.randint(0, numCodes - 1))
        wallNode = assetStorage.findNode(code, self.getName())
        if not wallNode:
            return
        wallNode.reparentTo(node, 0)
        wallScale = wallNode.getScale()
        wallScale.setX(self.width)
        wallScale.setZ(DNAFlatBuilding.currentWallHeight)
        wallNode.setScale(wallScale)
        if self.hasDoor:
            wallNodePath = node.find('wall_*')
            doorNode = assetStorage.findNode('suit_door', self.getName())
            doorNode.reparentTo(wallNodePath, 0)
            doorNode.setScale(hidden, 1, 1, 1)
            doorNode.setPosHpr(0.5, 0, 0, 0, 0, 0)
            doorNode.setDepthOffset(5)
            wallNodePath.setEffect(DecalEffect.make())
        node.flattenMedium()
        node.stash()

    def setupSuitFlatBuilding(self, nodePath, dnaStorage):
        self.setupGenericSuitFlatBuilding(nodePath, dnaStorage, 'sb', 'suit_wall')

    def setupCogdoFlatBuilding(self, nodePath, dnaStorage):
        self.setupGenericSuitFlatBuilding(nodePath, dnaStorage, 'cb', 'cogdo_wall')

    def traverse(self, nodePath, dnaStorage):
        DNAFlatBuilding.currentWallHeight = 0
        node = nodePath.attachNewNode(self.name)
        internalNode = node.attachNewNode(self.name + '-internal')
        self.scale.setX(self.width)
        internalNode.setScale(self.scale)
        node.setPosHpr(self.pos, self.hpr)
        for child in self.children:
            if isinstance(child, DNAWall.DNAWall):
                child.traverse(internalNode, dnaStorage)
            else:
                child.traverse(node, dnaStorage)

        if DNAFlatBuilding.currentWallHeight > 0:
            cameraBarrier = assetStorage.findNode('wall_camera_barrier', self.getName())
            cameraBarrier.reparentTo(internalNode, 0)
            cameraBarrier.setScale((1, 1, DNAFlatBuilding.currentWallHeight))
            internalNode.flattenStrong()
            collisionNode = node.find('**/door_*/+CollisionNode')
            if not collisionNode.isEmpty():
                collisionNode.setName('KnockKnockDoorSphere_' + dnaStorage.getBlock(self.name))
            cameraBarrier.wrtReparentTo(nodePath, 0)
            wallCollection = internalNode.findAllMatches('wall*')
            wallHolder = node.attachNewNode('wall_holder')
            wallDecal = node.attachNewNode('wall_decal')
            windowCollection = internalNode.findAllMatches('**/window*')
            doorCollection = internalNode.findAllMatches('**/door*')
            corniceCollection = internalNode.findAllMatches('**/cornice*_d')
            wallCollection.reparentTo(wallHolder)
            windowCollection.reparentTo(wallDecal)
            doorCollection.reparentTo(wallDecal)
            corniceCollection.reparentTo(wallDecal)
            for i in xrange(wallHolder.getNumChildren()):
                iNode = wallHolder.getChild(i)
                iNode.clearTag('DNACode')

            wallHolder.flattenStrong()
            wallDecal.flattenStrong()
            holderChild0 = wallHolder.getChild(0)
            wallDecal.getChildren().reparentTo(holderChild0)
            holderChild0.reparentTo(internalNode)
            holderChild0.setEffect(DecalEffect.make())
            wallHolder.removeNode()
            wallDecal.removeNode()
            self.setupSuitFlatBuilding(nodePath, dnaStorage)
            self.setupCogdoFlatBuilding(nodePath, dnaStorage)
            node.flattenStrong()