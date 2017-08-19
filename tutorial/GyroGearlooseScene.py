# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.GyroGearlooseScene
from panda3d.core import CardMaker, NodePath, Texture
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from toontown.catalog import CatalogFurnitureItem
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals, TTLocalizer

class GyroGearlooseScene(NodePath):
    GyroId = 7024
    ChairId = 120

    def __init__(self):
        NodePath.__init__(self, 'GyroGearlooseScene')
        floorTex = loader.loadTexture('phase_3.5/maps/cobblestone_purple.jpg')
        wallTex = loader.loadTexture('phase_4/maps/platformTop.jpg')
        evidenceModel = loader.loadModel('phase_11/models/lawbotHQ/LB_evidence')
        evidenceModel3 = evidenceModel.find('**/evidence3')
        evidenceModel.removeNode()
        self.talkSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_stomper_med.ogg')
        self.blackoutText = DirectLabel(relief=None, pos=(0, 0, 0.8), text_scale=0.11, text_font=ToontownGlobals.getChalkFont(), text_fg=(1, 1, 1, 1), sortOrder=2000, text='')
        self.blackoutText.hide()
        self.geom = loader.loadModel('phase_10/models/cashbotHQ/ZONE04a')
        self.geom.reparentTo(self)
        self.geom.setScale(0.7)
        self.geom.find('**/floor').setTexture(floorTex, 1)
        self.geom.find('**/walls').setTexture(wallTex, 1)
        self.connector = loader.loadModel('phase_10/models/cashbotHQ/connector_7cubeR2')
        self.connector.reparentTo(self.geom)
        self.connector.setPos(15.0525, 112.5, 5)
        self.connector.setColorScale(0.8, 0.8, 0.8, 1)
        self.connector.find('**/wall').setTexture(wallTex, 1)
        self.connector.find('**/floor').setTexture(floorTex, 1)
        self.connector.find('**/stair').setTexture(floorTex, 1)
        self.desk = loader.loadModel('phase_3.5/models/modules/desk_only_wo_phone')
        self.desk.reparentTo(self)
        self.desk.setPos(-30, -26, 0.02)
        self.desk.setHpr(315, 0, 0)
        self.chair = loader.loadModel(CatalogFurnitureItem.FurnitureTypes[self.ChairId][0])
        self.chair.reparentTo(self)
        self.chair.setPos(-27.5, -21.1, 0.02)
        self.chair.setHpr(315, 0, 0)
        self.board = NodePath(CardMaker('gyro-board-1').generate())
        self.board.reparentTo(self.geom)
        self.board.setPos(-37.9, -44, 3)
        self.board.setHpr(135, 0, 0)
        self.board.setScale(7)
        self.board.setTexture(loader.loadTexture('phase_5/maps/gyro_board_1.png'), 1)
        self.blueBoard = NodePath(CardMaker('gyro-board-2').generate())
        self.blueBoard.reparentTo(self.geom)
        self.blueBoard.setPos(-49.4, -33, 3)
        self.blueBoard.setHpr(135, 0, 0)
        self.blueBoard.setScale(7)
        self.blueBoard.setTexture(loader.loadTexture('phase_3.5/maps/elephantDiagram.jpg'), 1)
        self.evidence = []
        for posHpr in [(-25.1, -20, 0.02, 327, 0, 0), (-27.1, -15.5, 0.02, 165, 0, 0), (-28.5, -17.4, 0.02, 100, 0, 0)]:
            evidence = evidenceModel3.copyTo(self)
            evidence.setScale(25)
            evidence.setPosHpr(*posHpr)
            evidence.hide()
            self.evidence.append(evidence)

        self.gyro = NPCToons.createLocalNPC(self.GyroId)
        self.gyro.addActive()
        return

    def delete(self):
        self.removeNode()

    def removeNode(self):
        if self.blackoutText:
            self.blackoutText.destroy()
        if self.gyro:
            self.gyro.delete()
        self.talkSfx = None
        self.blackoutText = None
        self.geom = None
        self.connector = None
        self.desk = None
        self.chair = None
        self.board = None
        self.blueBoard = None
        self.evidence = None
        self.gyro = None
        NodePath.removeNode(self)
        return

    def gyroSit(self):
        chairPos, chairHpr, _, _ = CatalogFurnitureItem.ChairToPosHpr[self.ChairId]
        self.gyro.reparentTo(self.chair)
        self.gyro.setPos(*chairPos)
        self.gyro.setHpr(*chairHpr)
        self.gyro.loop('sit')

    def makeSequence(self):
        sequence = Sequence(Func(self.gyroSit), Func(self.blackoutText.hide), Func(camera.reparentTo, self), Func(camera.setPosHpr, -1, -7.645, 6.215, 115, 0, 0))
        for evidence in self.evidence:
            evidence.hide()
            sequence.append(Sequence(Wait(1.5), Func(base.transitions.fadeOut, 0), Wait(0.3), Func(evidence.show), Func(base.playSfx, self.talkSfx, volume=0.4), Func(base.transitions.fadeIn, 0)))

        sequence.append(Sequence(Wait(1.5), Func(base.transitions.fadeOut, 0), Func(self.blackoutText.show)))
        for message in TTLocalizer.TutorialScroogeMessages:
            sequence.append(self.__makeBlackoutSequence(2, message))

        sequence.append(Sequence(Wait(2), Func(self.blackoutText.hide), Func(base.transitions.fadeIn, 0), Func(camera.reparentTo, hidden)))
        return sequence

    def __makeBlackoutSequence(self, wait, text, volume = 0.4):
        return Sequence(Wait(wait), Func(self.__setBlackoutText, self.talkSfx, text, volume))

    def __setBlackoutText(self, sfx, text, volume):
        base.playSfx(sfx, volume=volume)
        self.blackoutText['text'] = self.blackoutText['text'] + text + '\n\n'