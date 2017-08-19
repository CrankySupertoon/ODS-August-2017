# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNADoor
from panda3d.core import DecalEffect, GeomNode, LVector4, LVector4f, Light, NodePath
import DNANode
import DNAUtil

class DNADoor(DNANode.DNANode):
    COMPONENT_CODE = 16

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
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

    @staticmethod
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color, pos = (0, 0, 0), hpr = (0, 0, 0), scale = (1, 1, 1)):
        doorNodePath.setPosHprScale(doorOrigin, pos, hpr, scale)
        doorNodePath.setColor(color, 0)
        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.setName('doorFrameHoleLeft')
        leftHole.hide()
        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.setName('doorFrameHoleRight')
        rightHole.hide()
        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.setName('leftDoor')
        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.setName('rightDoor')
        doorFlat = doorNodePath.find('door_*_flat')
        if doorFlat:
            doorFlat.setEffect(DecalEffect.make())
            doorFlat.setDepthOffset(5)
        for door in (leftDoor, rightDoor):
            door.wrtReparentTo(parentNode, 0)
            door.setColor(color, 0)
            door.setDepthOffset(5)

        for hole in (leftHole, rightHole):
            hole.wrtReparentTo(doorFlat, 0)
            hole.setColor((0, 0, 0, 1), 0)

        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2)
        doorTrigger.wrtReparentTo(parentNode, 0)
        doorTrigger.setName('door_trigger_' + str(block))
        if not dnaStore.getDoorPosHprFromBlockNumber(block):
            dnaStore.storeBlockDoor(block, doorOrigin)
        doorNodePath.flattenLight()

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.color = DNAUtil.dgiExtractColor(dgi)

    def setParent(self, parent, dnaStore):
        DNANode.DNANode.setParent(self, parent, dnaStore)
        parentName = parent.getName()
        if ':' in parentName:
            block = int(parentName.split(':')[0][2:])
            dnaStore.storeBlockPosHpr(block, [parent.getPos(), parent.getHpr()])

    def traverse(self, nodePath, dnaStorage):
        frontNode = nodePath.find('**/*_front')
        if not frontNode.getNode(0).isGeomNode():
            frontNode = frontNode.find('**/+GeomNode')
        frontNode.setEffect(DecalEffect.make())
        doorNode = assetStorage.findNode(self.code, self.getName())
        doorNode.reparentTo(frontNode, 0)
        doorNode.flattenMedium()
        block = dnaStorage.getBlock(nodePath.getName())
        DNADoor.setupDoor(doorNode, nodePath, nodePath.find('**/*door_origin'), dnaStorage, block, self.color, self.pos, self.hpr, self.scale)