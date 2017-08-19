# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.DistributedHQInterior
from panda3d.core import ModelNode, NodePath, TextNode
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from otp.speedchat import SpeedChatGlobals
from toontown.dna.DNAParser import setupDoor
from toontown.toonbase import TTLocalizer, ToontownGlobals
from ZoneBuilding import ZoneBuilding

class DistributedHQInterior(DistributedObject, ZoneBuilding):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.leaderNames = []
        self.leaderScores = []
        self.numLeaders = 10
        self.sequence = None
        return

    def generate(self):
        DistributedObject.generate(self)
        self.interior = loader.loadModel('phase_3.5/models/modules/HQ_interior')
        self.interior.reparentTo(render)
        self.interior.flattenMedium()
        self.buildLeaderBoard()

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.setupDoors()
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, self.__phraseSaid)
        if self.windowOpen:
            for element in ('dan_window', 'jp_col', 'jp_col2'):
                self.interior.find('**/' + element).setZ(-16.4)

    def setWindowOpen(self, windowOpen):
        self.windowOpen = windowOpen
        if not self.isGenerated():
            return
        z = -16.4 if windowOpen else 0.0
        self.sequence = Parallel(self.interior.find('**/dan_window').posInterval(3, (0, 0, z)), self.interior.find('**/jp_col').posInterval(3, (0, 0, z)), self.interior.find('**/jp_col2').posInterval(3, (0, 0, z)))
        self.sequence.start()

    def buildLeaderBoard(self):
        self.leaderBoard = hidden.attachNewNode('leaderBoard')
        self.leaderBoard.setPosHprScale(0.1, 0, 4.5, 90, 0, 0, 0.9, 0.9, 0.9)
        self.leaderBoard.reparentTo(self.interior.find('**/empty_board').getChild(0))
        row = self.buildTitleRow()
        row.reparentTo(self.leaderBoard)
        self.nameTextNodes = []
        self.scoreTextNodes = []
        self.trophyStars = []
        for i in xrange(self.numLeaders):
            row, nameText, scoreText, trophyStar = self.buildLeaderRow()
            self.nameTextNodes.append(nameText)
            self.scoreTextNodes.append(scoreText)
            self.trophyStars.append(trophyStar)
            row.reparentTo(self.leaderBoard)
            row.setPos(0, 0, -(i + 1))

    def updateLeaderBoard(self):
        taskMgr.remove(self.uniqueName('starSpinHQ'))
        for i in xrange(len(self.leaderNames)):
            name = self.leaderNames[i]
            score = self.leaderScores[i]
            self.nameTextNodes[i].setText(name)
            self.scoreTextNodes[i].setText(str(score))
            self.updateTrophyStar(self.trophyStars[i], score)

        for i in xrange(len(self.leaderNames), self.numLeaders):
            self.nameTextNodes[i].setText('-')
            self.scoreTextNodes[i].setText('-')
            self.trophyStars[i].hide()

    def buildTitleRow(self):
        row = hidden.attachNewNode('leaderRow')
        nameText = TextNode('titleRow')
        nameText.setFont(ToontownGlobals.getSignFont())
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0.5, 0.75, 0.7, 1)
        nameText.setText(TTLocalizer.LeaderboardTitle)
        namePath = row.attachNewNode(nameText)
        namePath.setPos(0, 0, 0)
        return row

    def buildLeaderRow(self):
        row = hidden.attachNewNode('leaderRow')
        nameText = TextNode('nameText')
        nameText.setFont(ToontownGlobals.getToonFont())
        nameText.setAlign(TextNode.ALeft)
        nameText.setTextColor(1, 1, 1, 0.7)
        nameText.setText('-')
        namePath = row.attachNewNode(nameText)
        namePath.setPos(*TTLocalizer.DHQInamePathPos)
        namePath.setScale(TTLocalizer.DHQInamePath)
        scoreText = TextNode('scoreText')
        scoreText.setFont(ToontownGlobals.getToonFont())
        scoreText.setAlign(TextNode.ARight)
        scoreText.setTextColor(1, 1, 0.1, 0.7)
        scoreText.setText('-')
        scorePath = row.attachNewNode(scoreText)
        scorePath.setPos(*TTLocalizer.DHQIscorePathPos)
        trophyStar = self.buildTrophyStar()
        trophyStar.reparentTo(row)
        return (row,
         nameText,
         scoreText,
         trophyStar)

    def setLeaderBoard(self, leaderNames, leaderScores):
        self.leaderNames = leaderNames
        self.leaderScores = leaderScores
        self.updateLeaderBoard()

    def setupDoors(self):
        randomGen = self.getRandomGen()
        colors = self.getColors()
        door = assetStorage.findNode('door_double_round_ur')
        doorOrigins = render.findAllMatches('**/door_origin*')
        numDoorOrigins = doorOrigins.getNumPaths()
        for npIndex in xrange(numDoorOrigins):
            doorOrigin = doorOrigins[npIndex]
            doorOriginNPName = doorOrigin.getName()
            doorOriginIndexStr = doorOriginNPName[len('door_origin_'):]
            newNode = ModelNode('door_' + doorOriginIndexStr)
            newNodePath = NodePath(newNode)
            newNodePath.reparentTo(self.interior)
            doorNP = door.copyTo(newNodePath)
            doorOrigin.setScale(0.8, 0.8, 0.8)
            doorOrigin.setPos(doorOrigin, 0, -0.025, 0)
            doorColor = randomGen.choice(colors['TI_door'])
            triggerId = str(self.block) + '_' + doorOriginIndexStr
            setupDoor(doorNP, newNodePath, doorOrigin, base.cr.playGame.dnaStore, triggerId, doorColor)
            doorFrame = doorNP.find('door_*_flat')
            doorFrame.setColor(doorColor)

    def disable(self):
        if self.sequence:
            self.sequence.finish()
        self.leaderBoard.removeNode()
        del self.leaderBoard
        self.interior.removeNode()
        del self.interior
        del self.nameTextNodes
        del self.scoreTextNodes
        del self.trophyStars
        del self.sequence
        taskMgr.remove(self.uniqueName('starSpinHQ'))
        self.ignoreAll()
        DistributedObject.disable(self)

    def buildTrophyStar(self):
        trophyStar = loader.loadModel('phase_3.5/models/gui/name_star')
        trophyStar.hide()
        trophyStar.setPos(*TTLocalizer.DHQItrophyStarPos)
        return trophyStar

    def updateTrophyStar(self, trophyStar, score):
        scale = 0.8
        if score >= ToontownGlobals.TrophyStarLevels[4]:
            trophyStar.show()
            trophyStar.setScale(scale)
            trophyStar.setColor(ToontownGlobals.TrophyStarColors[4])
            if score >= ToontownGlobals.TrophyStarLevels[5]:
                task = taskMgr.add(self.__starSpin, self.uniqueName('starSpinHQ'))
                task.trophyStarSpeed = 15
                task.trophyStar = trophyStar
        elif score >= ToontownGlobals.TrophyStarLevels[2]:
            trophyStar.show()
            trophyStar.setScale(0.75 * scale)
            trophyStar.setColor(ToontownGlobals.TrophyStarColors[2])
            if score >= ToontownGlobals.TrophyStarLevels[3]:
                task = taskMgr.add(self.__starSpin, self.uniqueName('starSpinHQ'))
                task.trophyStarSpeed = 10
                task.trophyStar = trophyStar
        elif score >= ToontownGlobals.TrophyStarLevels[0]:
            trophyStar.show()
            trophyStar.setScale(0.75 * scale)
            trophyStar.setColor(ToontownGlobals.TrophyStarColors[0])
            if score >= ToontownGlobals.TrophyStarLevels[1]:
                task = taskMgr.add(self.__starSpin, self.uniqueName('starSpinHQ'))
                task.trophyStarSpeed = 8
                task.trophyStar = trophyStar
        else:
            trophyStar.hide()

    def __starSpin(self, task):
        now = globalClock.getFrameTime()
        r = now * task.trophyStarSpeed % 360.0
        task.trophyStar.setR(r)
        return task.cont

    def __phraseSaid(self, phraseId):
        if self.windowOpen or phraseId != 1099:
            return
        base.localAvatar.setSystemMessage(0, TTLocalizer.LoonyLabsEasterEgg, 4)
        self.sendUpdate('openWindow')