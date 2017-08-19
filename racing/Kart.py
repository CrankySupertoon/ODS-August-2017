# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.racing.Kart
from panda3d.physics import ActorNode
from panda3d.core import GeomNode, NodePath, Point3, Texture
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from toontown.racing.KartDNA import *
from toontown.toonbase import TTLocalizer

class Kart(NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory('Kart')
    index = 0
    baseScale = 2.0
    RFWHEEL = 0
    LFWHEEL = 1
    RRWHEEL = 2
    LRWHEEL = 3
    wheelData = [{'node': 'wheel*Node2'},
     {'node': 'wheel*Node1'},
     {'node': 'wheel*Node3'},
     {'node': 'wheel*Node4'}]
    ShadowScale = 2.5
    SFX_BaseDir = 'phase_6/audio/sfx/'
    SFX_KartStart = SFX_BaseDir + 'KART_Engine_start_%d.ogg'
    SFX_KartLoop = SFX_BaseDir + 'KART_Engine_loop_%d.ogg'

    def __init__(self):
        NodePath.__init__(self)
        an = ActorNode('vehicle-test')
        anp = NodePath(an)
        NodePath.assign(self, anp)
        self.actorNode = an
        Kart.index += 1
        self.updateFields = []
        self.kartDNA = [-1] * getNumFields()
        self.kartAccessories = {KartDNA.ebType: None,
         KartDNA.spType: None,
         KartDNA.fwwType: (None, None),
         KartDNA.bwwType: (None, None)}
        self.texCount = 1
        return

    def delete(self):
        self.__stopWheelSpin()
        del self.kartDNA
        del self.updateFields
        self.kartLoopSfx.stop()
        NodePath.removeNode(self)

    def getKartBounds(self):
        return self.geom.getTightBounds()

    def getBaseScale(self):
        type = self.kartDNA[KartDNA.bodyType]
        if type == 3:
            return 0.5
        else:
            return 2.0

    def generateKart(self, forGui = 0):
        self.geom = None
        self.pitchNode = None
        self.toonNode = None
        self.rotateNode = self.attachNewNode('rotate')
        baseScale = self.getBaseScale()
        self.__createKart()
        self.setScale(2)
        self.flattenMedium()
        if self.kartDNA[KartDNA.bodyType] == 3:
            self.pitchNode.setScale(5)
            self.pitchNode.setPos(0, 0, 1.5)
            if self.__class__.__name__ == 'DistributedVehicle':
                self.toonNode.setPos(-0.35, 0.9, 0.15)
            else:
                self.toonNode.setPos(-0.35, 0.5, 0.35)
            for node in self.findAllMatches('**/shadow*'):
                node.removeNode()

        tempNode = NodePath('tempNode')
        self.accGeomScale = tempNode.getScale(self.pitchNode) * baseScale
        tempNode.removeNode()
        if not self.hasNoAccessories():
            self.__applyBodyColor()
            self.__applyEngineBlock()
            self.__applySpoiler()
            self.__applyFrontWheelWells()
            self.__applyBackWheelWells()
            self.__applyRims()
            self.__applyDecals()
            self.__applyAccessoryColor()
        self.wheelCenters = []
        self.wheelBases = []
        for wheel in self.wheelData:
            center = self.geom.find('**/' + wheel['node'])
            self.wheelCenters.append(center)
            wheelBase = center.getParent().attachNewNode('wheelBase')
            wheelBase.setPos(center.getPos())
            wheelBase.setZ(0)
            self.wheelBases.append(wheelBase)

        self.wheelBaseH = self.wheelCenters[0].getH()
        self.__startWheelSpin()
        self.setWheelSpinSpeed(0)
        if not forGui:
            self.shadowJoint = self.geom
            self.initializeDropShadow()
            self.dropShadow.setScale(self.ShadowScale)
        else:
            self.shadowJoint = self.rotateNode
            self.initializeDropShadow()
            self.dropShadow.setScale(1.3, 3, 1)
        kartType = self.kartDNA[KartDNA.bodyType]
        self.kartStartSfx = loader.loadSfx(self.SFX_KartStart % kartType)
        self.kartLoopSfx = loader.loadSfx(self.SFX_KartLoop % kartType)
        self.kartLoopSfx.setLoop()
        return

    def initializeDropShadow(self):
        self.dropShadow = loader.loadModel('phase_3/models/props/drop_shadow')
        self.dropShadow.setScale(0.4)
        self.dropShadow.flattenMedium()
        self.dropShadow.setBillboardAxis(2)
        self.dropShadow.setColor(0.0, 0.0, 0.0, 0.5, 1)
        self.dropShadow.reparentTo(self.geom)

    def __createKart(self):
        type = self.kartDNA[KartDNA.bodyType]
        kartBodyPath = getKartModelPath(type)
        self.geom = loader.loadModel(kartBodyPath)
        self.geom.reparentTo(self.rotateNode)
        self.geom.setH(180)
        self.geom.setPos(0.0, 0, 0.025)
        self.pitchNode = self.geom.find('**/suspensionNode')
        if type == 3:
            self.toonNode = self.attachNewNode('toonNode')
        else:
            self.toonNode = self.geom.find('**/toonNode')
        scale = 1.0 / self.pitchNode.getScale()[0]
        scale /= self.getBaseScale()
        self.toonNode.setScale(scale)
        h = (180 + self.pitchNode.getH()) % 360
        self.toonNode.setH(h)
        pos = Point3(0, -1.3, -7)
        self.toonNode.setPos(pos)

    def resetGeomPos(self):
        self.geom.setPos(0, 0, 0.025)

    def hasNoAccessories(self):
        return self.kartDNA[KartDNA.bodyType] in NoAccessories

    def __update(self):
        if self.hasNoAccessories():
            self.updateFields = []
            return
        else:
            for field in self.updateFields:
                if field == KartDNA.bodyType:
                    if hasattr(self, 'geom'):
                        if self.geom:
                            self.geom.removeNode()
                            self.geom = None
                        self.__createKart()
                        self.__applyBodyColor()
                        self.__applyEngineBlock()
                        self.__applySpoiler()
                        self.__applyFrontWheelWells()
                        self.__applyRims()
                        self.__applyDecals()
                        self.__applyAccessoryColor()
                    else:
                        raise StandardError, 'Kart::__update - Has this method been called before generateKart?'
                elif field == KartDNA.bodyColor:
                    self.__applyBodyColor()
                elif field == KartDNA.accColor:
                    self.__applyAccessoryColor()
                elif field == KartDNA.ebType:
                    if self.kartAccessories[KartDNA.ebType] != None:
                        name = self.kartAccessories[KartDNA.ebType].getName()
                        self.geom.find('**/%s' % name).removeNode()
                        self.kartAccessories[KartDNA.ebType].removeNode()
                        self.kartAccessories[KartDNA.ebType] = None
                    self.__applyEngineBlock()
                elif field == KartDNA.spType:
                    if self.kartAccessories[KartDNA.spType] != None:
                        name = self.kartAccessories[KartDNA.spType].getName()
                        self.geom.find('**/%s' % name).removeNode()
                        self.kartAccessories[KartDNA.spType].removeNode()
                        self.kartAccessories[KartDNA.spType] = None
                    self.__applySpoiler()
                elif field == KartDNA.fwwType:
                    if self.kartAccessories[KartDNA.fwwType] != (None, None):
                        left, right = self.kartAccessories[KartDNA.fwwType]
                        self.geom.find('**/%s' % left.getName()).removeNode()
                        self.geom.find('**/%s' % right.getName()).removeNode()
                        left.removeNode()
                        right.removeNode()
                        self.kartAccessories[KartDNA.fwwType] = (None, None)
                    self.__applyFrontWheelWells()
                elif field == KartDNA.bwwType:
                    if self.kartAccessories[KartDNA.bwwType] != (None, None):
                        left, right = self.kartAccessories[KartDNA.bwwType]
                        self.geom.find('**/%s' % left.getName()).removeNode()
                        self.geom.find('**/%s' % right.getName()).removeNode()
                        left.removeNode()
                        right.removeNode()
                        self.kartAccessories[KartDNA.bwwType] = (None, None)
                    self.__applyBackWheelWells()
                else:
                    if field == KartDNA.rimsType:
                        self.__applyRims()
                    elif field == KartDNA.decalType:
                        self.__applyDecals()
                    self.__applyAccessoryColor()

            self.updateFields = []
            return

    def updateDNAField(self, field, fieldValue):
        self.kartDNA[field] = fieldValue
        self.updateFields.append(field)
        self.__update()

    def __applyBodyColor(self):
        if self.kartDNA[KartDNA.bodyColor] == InvalidEntry:
            bodyColor = getDefaultColor()
        else:
            bodyColor = getAccessory(self.kartDNA[KartDNA.bodyColor])
        self.geom.find('**/chasse').setColorScale(bodyColor)

    def __applyAccessoryColor(self):
        if self.kartDNA[KartDNA.accColor] == InvalidEntry:
            accColor = getDefaultColor()
        else:
            accColor = getAccessory(self.kartDNA[KartDNA.accColor])
        for decal in ('hood', 'rightSide', 'leftSide'):
            self.geom.find('**/%sDecal' % decal).setColorScale(accColor)

        for type in [KartDNA.ebType, KartDNA.spType]:
            model = self.kartAccessories.get(type, None)
            if model != None and not model.find('**/vertex').isEmpty():
                if self.kartDNA[KartDNA.accColor] == InvalidEntry:
                    accColor = getDefaultColor()
                else:
                    accColor = getAccessory(self.kartDNA[KartDNA.accColor])
                model.find('**/vertex').setColorScale(accColor)

        for type in [KartDNA.fwwType, KartDNA.bwwType]:
            lModel, rModel = self.kartAccessories.get(type, (None, None))
            if lModel != None and not lModel.find('**/vertex').isEmpty():
                if self.kartDNA[KartDNA.accColor] == InvalidEntry:
                    accColor = getDefaultColor()
                else:
                    accColor = getAccessory(self.kartDNA[KartDNA.accColor])
                lModel.find('**/vertex').setColorScale(accColor)
                rModel.find('**/vertex').setColorScale(accColor)

        return

    def __applyEngineBlock(self):
        ebType = self.kartDNA[KartDNA.ebType]
        if ebType == InvalidEntry:
            return
        ebPath = getAccessory(ebType)
        attachNode = getAccessoryAttachNode(ebType)
        model = loader.loadModel(ebPath)
        self.kartAccessories[KartDNA.ebType] = model
        model.setScale(self.accGeomScale)
        if not model.find('**/vertex').isEmpty():
            if self.kartDNA[KartDNA.accColor] == InvalidEntry:
                accColor = getDefaultColor()
            else:
                accColor = getAccessory(self.kartDNA[KartDNA.accColor])
            model.find('**/vertex').setColorScale(accColor)
        engineBlockNode = self.geom.find('**/%s' % attachNode)
        model.setPos(engineBlockNode.getPos(self.pitchNode))
        model.setHpr(engineBlockNode.getHpr(self.pitchNode))
        model.reparentTo(self.pitchNode)

    def __applySpoiler(self):
        spType = self.kartDNA[KartDNA.spType]
        if spType == InvalidEntry:
            return
        spPath = getAccessory(spType)
        attachNode = getAccessoryAttachNode(spType)
        model = loader.loadModel(spPath)
        self.kartAccessories[KartDNA.spType] = model
        model.setScale(self.accGeomScale)
        spoilerNode = self.geom.find('**/%s' % attachNode)
        model.setPos(spoilerNode.getPos(self.pitchNode))
        model.setHpr(spoilerNode.getHpr(self.pitchNode))
        model.reparentTo(self.pitchNode)

    def __applyRims(self):
        if self.kartDNA[KartDNA.rimsType] == InvalidEntry:
            rimTexPath = getAccessory(getDefaultRim())
        else:
            rimTexPath = getAccessory(self.kartDNA[KartDNA.rimsType])
        rimTex = loader.loadTexture('%s.jpg' % rimTexPath, '%s_a.rgb' % rimTexPath)
        rimTex.setMinfilter(Texture.FTLinearMipmapLinear)
        for pos in ('leftFront', 'rightFront', 'leftRear', 'rightRear'):
            wheelRim = self.geom.find('**/%sWheelRim' % pos)
            wheelRim.setTexture(rimTex, self.texCount)

        self.texCount += 1

    def __applyFrontWheelWells(self):
        fwwType = self.kartDNA[KartDNA.fwwType]
        if fwwType == InvalidEntry:
            return
        fwwPath = getAccessory(fwwType)
        attachNode = getAccessoryAttachNode(fwwType)
        leftAttachNode = attachNode % 'left'
        rightAttachNode = attachNode % 'right'
        leftModel = loader.loadModel(fwwPath)
        rightModel = loader.loadModel(fwwPath)
        self.kartAccessories[KartDNA.fwwType] = (leftModel, rightModel)
        if not leftModel.find('**/vertex').isEmpty():
            if self.kartDNA[KartDNA.accColor] == InvalidEntry:
                accColor = getDefaultColor()
            else:
                accColor = getAccessory(self.kartDNA[KartDNA.accColor])
            leftModel.find('**/vertex').setColorScale(accColor)
            rightModel.find('**/vertex').setColorScale(accColor)
        leftNode = self.geom.find('**/%s' % leftAttachNode)
        rightNode = self.geom.find('**/%s' % rightAttachNode)
        leftModel.reparentTo(self.pitchNode)
        rightModel.reparentTo(self.pitchNode)
        leftModel.setPos(rightNode.getPos(self.pitchNode))
        leftModel.setHpr(rightNode.getHpr(self.pitchNode))
        leftModel.setScale(self.accGeomScale)
        leftModel.setSx(-1.0 * leftModel.getSx())
        leftModel.setTwoSided(True)
        rightModel.setPos(leftNode.getPos(self.pitchNode))
        rightModel.setHpr(leftNode.getHpr(self.pitchNode))
        rightModel.setScale(self.accGeomScale)

    def __applyBackWheelWells(self):
        bwwType = self.kartDNA[KartDNA.bwwType]
        if bwwType == InvalidEntry:
            return
        bwwPath = getAccessory(bwwType)
        attachNode = getAccessoryAttachNode(bwwType)
        leftAttachNode = attachNode % 'left'
        rightAttachNode = attachNode % 'right'
        leftModel = loader.loadModel(bwwPath)
        rightModel = loader.loadModel(bwwPath)
        self.kartAccessories[KartDNA.bwwType] = (leftModel, rightModel)
        if not leftModel.find('**/vertex').isEmpty():
            if self.kartDNA[KartDNA.accColor] == InvalidEntry:
                accColor = getDefaultColor()
            else:
                accColor = getAccessory(self.kartDNA[KartDNA.accColor])
            leftModel.find('**/vertex').setColorScale(accColor)
            rightModel.find('**/vertex').setColorScale(accColor)
        leftNode = self.geom.find('**/%s' % leftAttachNode)
        rightNode = self.geom.find('**/%s' % rightAttachNode)
        leftModel.reparentTo(self.pitchNode)
        rightModel.reparentTo(self.pitchNode)
        leftModel.setPos(rightNode.getPos(self.pitchNode))
        leftModel.setHpr(rightNode.getHpr(self.pitchNode))
        leftModel.setScale(self.accGeomScale)
        leftModel.setSx(-1.0 * leftModel.getSx())
        leftModel.setTwoSided(True)
        rightModel = rightModel.instanceTo(self.pitchNode)
        rightModel.setPos(leftNode.getPos(self.pitchNode))
        rightModel.setHpr(leftNode.getHpr(self.pitchNode))
        rightModel.setScale(self.accGeomScale)

    def __applyDecals(self):
        hoodDecal = self.geom.find('**/hoodDecal')
        rightSideDecal = self.geom.find('**/rightSideDecal')
        leftSideDecal = self.geom.find('**/leftSideDecal')
        if self.kartDNA[KartDNA.decalType] != InvalidEntry:
            decalId = getAccessory(self.kartDNA[KartDNA.decalType])
            kartDecal = getDecalId(self.kartDNA[KartDNA.bodyType])
            hoodDecalTex = loader.loadTexture('phase_6/maps/%s_HoodDecal_%s.jpg' % (kartDecal, decalId), 'phase_6/maps/%s_HoodDecal_%s_a.rgb' % (kartDecal, decalId))
            sideDecalTex = loader.loadTexture('phase_6/maps/%s_SideDecal_%s.jpg' % (kartDecal, decalId), 'phase_6/maps/%s_SideDecal_%s_a.rgb' % (kartDecal, decalId))
            hoodDecalTex.setMinfilter(Texture.FTLinearMipmapLinear)
            sideDecalTex.setMinfilter(Texture.FTLinearMipmapLinear)
            hoodDecal.setTexture(hoodDecalTex, self.texCount)
            rightSideDecal.setTexture(sideDecalTex, self.texCount)
            leftSideDecal.setTexture(sideDecalTex, self.texCount)
            hoodDecal.show()
            rightSideDecal.show()
            leftSideDecal.show()
        else:
            hoodDecal.hide()
            rightSideDecal.hide()
            leftSideDecal.hide()
        self.texCount += 1

    def rollSuspension(self, roll):
        if not self.hasNoAccessories():
            self.pitchNode.setR(roll)

    def pitchSuspension(self, pitch):
        if not self.hasNoAccessories():
            self.pitchNode.setP(pitch)

    def getDNA(self):
        return self.kartDNA

    def setDNA(self, dna):
        if self.kartDNA != [-1] * getNumFields():
            for field in xrange(len(self.kartDNA)):
                if dna[field] != self.kartDNA[field]:
                    self.updateDNAField(field, dna[field])

            return
        self.kartDNA = dna

    def getBodyType(self):
        return self.kartDNA[KartDNA.bodyType]

    def getBodyColor(self):
        return self.kartDNA[KartDNA.bodyColor]

    def getAccessoryColor(self):
        return self.kartDNA[KartDNA.accColor]

    def getEngineBlockType(self):
        return self.kartDNA[KartDNA.ebType]

    def getSpoilerType(self):
        return self.kartDNA[KartDNA.spType]

    def getFrontWheelWellType(self):
        return self.kartDNA[KartDNA.fwwType]

    def getBackWheelWellType(self):
        return self.kartDNA[KartDNA.bwwType]

    def getRimType(self):
        return self.kartDNA[KartDNA.rimsType]

    def getDecalType(self):
        return self.kartDNA[KartDNA.decalType]

    def getGeomNode(self):
        return self.geom

    def spinWheels(self, amount):
        newSpin = (self.oldSpinAmount + amount) % 360
        for wheelNode in self.wheelCenters:
            wheelNode.setP(newSpin)

        self.oldSpinAmount = newSpin

    def setWheelSpinSpeed(self, speed):
        pass

    def __startWheelSpin(self):
        self.oldSpinAmount = 0

    def __stopWheelSpin(self):
        pass

    def turnWheels(self, amount):
        amount += self.wheelBaseH
        node = self.wheelCenters[self.RFWHEEL]
        node.setH(amount)
        node = self.wheelCenters[self.LFWHEEL]
        node.setH(amount)

    def generateEngineStartTrack(self):
        return Parallel(SoundInterval(self.kartStartSfx), Func(self.kartLoopSfx.play), LerpFunctionInterval(self.kartLoopSfx.setVolume, fromData=0, toData=0.4, duration=self.kartStartSfx.length()))

    def generateEngineStopTrack(self, duration = 0):
        return Parallel(LerpFunctionInterval(self.kartLoopSfx.setVolume, fromData=0.4, toData=0, duration=duration))