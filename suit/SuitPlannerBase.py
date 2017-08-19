# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.suit.SuitPlannerBase
from direct.directnotify.DirectNotifyGlobal import *
from toontown.hood import ZoneUtil, HoodUtil
from toontown.toonbase import ToontownGlobals, ToontownBattleGlobals
from toontown.building import SuitBuildingGlobals
from toontown.dna.DNAInteractiveProp import DNAInteractiveProp
from toontown.dna.DNASuitPoint import DNASuitPoint
from toontown.dna.DNAStorage import DNAStorage
from toontown.dna.DNAParser import loadDNAFileAI

class SuitPlannerBase:
    notify = directNotify.newCategory('SuitPlannerBase')
    SuitHoodInfo = [[2100,
      5,
      15,
      0,
      5,
      20,
      3,
      (1, 5, 10, 40, 60, 80),
      (20, 20, 20, 20, 20),
      (1, 2, 3),
      []],
     [2200,
      3,
      10,
      0,
      5,
      15,
      3,
      (1, 5, 10, 40, 60, 80),
      (10, 60, 10, 10, 10),
      (1, 2, 3),
      []],
     [2300,
      3,
      10,
      0,
      5,
      15,
      3,
      (1, 5, 10, 40, 60, 80),
      (10, 10, 35, 35, 10),
      (1, 2, 3),
      []],
     [1100,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (90, 10, 0, 0, 0),
      (2, 3, 4),
      []],
     [1200,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (0, 0, 90, 10, 0),
      (3, 4, 5, 6),
      []],
     [1300,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (35, 35, 10, 10, 10),
      (3, 4, 5, 6),
      []],
     [3100,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (90, 10, 0, 0, 0),
      (5, 6, 7),
      []],
     [3200,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (10, 15, 20, 25, 30),
      (5, 6, 7),
      []],
     [3300,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (5, 80, 5, 5, 5),
      (7, 8, 9),
      []],
     [4100,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (0, 0, 50, 50, 0),
      (2, 3, 4),
      []],
     [4200,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (0, 0, 80, 10, 10),
      (3, 4, 5, 6),
      []],
     [4300,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (50, 50, 0, 0, 0),
      (3, 4, 5, 6),
      []],
     [5100,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (0, 20, 10, 60, 10),
      (2, 3, 4),
      []],
     [5200,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (10, 60, 0, 20, 10),
      (3, 4, 5, 6),
      []],
     [5300,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (5, 5, 5, 80, 5),
      (3, 4, 5, 6),
      []],
     [9100,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (20, 20, 20, 20, 20),
      (6, 7, 8, 9),
      []],
     [9200,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (5, 5, 80, 5, 5),
      (6, 7, 8, 9),
      []],
     [9300,
      1,
      5,
      0,
      99,
      100,
      4,
      (1, 5, 10, 40, 60, 80),
      (5, 5, 5, 5, 80),
      (6, 7, 8, 9),
      []],
     [10000,
      3,
      15,
      0,
      5,
      15,
      3,
      (1, 5, 10, 40, 60, 80),
      (100, 0, 0, 0, 0),
      (7, 8, 9, 10),
      []],
     [11000,
      3,
      15,
      0,
      0,
      0,
      4,
      (1, 5, 10, 40, 60, 80),
      (0, 0, 0, 100, 0),
      (4, 5, 6),
      []],
     [11200,
      10,
      20,
      0,
      0,
      0,
      4,
      (1, 5, 10, 40, 60, 80),
      (0, 0, 0, 100, 0),
      (4, 5, 6),
      []],
     [12000,
      10,
      20,
      0,
      0,
      0,
      4,
      (1, 5, 10, 40, 60, 80),
      (0, 0, 100, 0, 0),
      (7, 8, 9),
      []],
     [13000,
      10,
      20,
      0,
      0,
      0,
      4,
      (1, 5, 10, 40, 60, 80),
      (0, 100, 0, 0, 0),
      (8, 9, 10),
      []],
     [14000,
      10,
      20,
      0,
      0,
      0,
      4,
      (1, 5, 10, 40, 60, 80),
      (0, 0, 0, 0, 100),
      (8, 9, 10),
      []]]
    SUIT_HOOD_INFO_ZONE = 0
    SUIT_HOOD_INFO_MIN = 1
    SUIT_HOOD_INFO_MAX = 2
    SUIT_HOOD_INFO_BMIN = 3
    SUIT_HOOD_INFO_BMAX = 4
    SUIT_HOOD_INFO_BWEIGHT = 5
    SUIT_HOOD_INFO_SMAX = 6
    SUIT_HOOD_INFO_JCHANCE = 7
    SUIT_HOOD_INFO_TRACK = 8
    SUIT_HOOD_INFO_LVL = 9
    SUIT_HOOD_INFO_HEIGHTS = 10
    TOTAL_BWEIGHT = 0
    TOTAL_BWEIGHT_PER_TRACK = [0,
     0,
     0,
     0,
     0]
    TOTAL_BWEIGHT_PER_HEIGHT = [0,
     0,
     0,
     0,
     0]
    for currHoodInfo in SuitHoodInfo:
        weight = currHoodInfo[SUIT_HOOD_INFO_BWEIGHT]
        tracks = currHoodInfo[SUIT_HOOD_INFO_TRACK]
        levels = currHoodInfo[SUIT_HOOD_INFO_LVL]
        heights = [0,
         0,
         0,
         0,
         0]
        for level in levels:
            minFloors, maxFloors = SuitBuildingGlobals.SuitBuildingInfo[level - 1][0]
            for i in xrange(minFloors - 1, maxFloors):
                heights[i] += 1

        currHoodInfo[SUIT_HOOD_INFO_HEIGHTS] = heights
        TOTAL_BWEIGHT += weight
        TOTAL_BWEIGHT_PER_TRACK[0] += weight * tracks[0]
        TOTAL_BWEIGHT_PER_TRACK[1] += weight * tracks[1]
        TOTAL_BWEIGHT_PER_TRACK[2] += weight * tracks[2]
        TOTAL_BWEIGHT_PER_TRACK[3] += weight * tracks[3]
        TOTAL_BWEIGHT_PER_TRACK[4] += weight * tracks[4]
        TOTAL_BWEIGHT_PER_HEIGHT[0] += weight * heights[0]
        TOTAL_BWEIGHT_PER_HEIGHT[1] += weight * heights[1]
        TOTAL_BWEIGHT_PER_HEIGHT[2] += weight * heights[2]
        TOTAL_BWEIGHT_PER_HEIGHT[3] += weight * heights[3]
        TOTAL_BWEIGHT_PER_HEIGHT[4] += weight * heights[4]

    def __init__(self):
        self.suitWalkSpeed = ToontownGlobals.SuitWalkSpeed
        self.dnaStore = None
        self.pointIndexes = {}
        return

    def delete(self):
        del self.dnaStore

    def setupDNA(self):
        if self.dnaStore:
            return None
        else:
            self.dnaStore = DNAStorage()
            dnaFileName = self.genDNAFileName()
            loadDNAFileAI(self.dnaStore, dnaFileName)
            self.initDNAInfo()
            return None

    def genDNAFileName(self):
        zoneId = self.getZoneId()
        hoodId = ZoneUtil.getHoodId(zoneId)
        hood = ToontownGlobals.dnaMap[hoodId]
        phase = ToontownGlobals.streetPhaseMap[hoodId]
        if hoodId == zoneId:
            zoneId = 'sz'
        return 'phase_%s/dna/%s_%s.bdna' % (phase, hood, zoneId)

    def getZoneId(self):
        return self.zoneId

    def setZoneId(self, zoneId):
        self.notify.debug('setting zone id for suit planner')
        self.zoneId = zoneId
        self.setupDNA()

    def extractGroupName(self, groupFullName):
        return groupFullName.split(':', 1)[0]

    def initDNAInfo(self):
        numGraphs = self.dnaStore.discoverContinuity()
        if numGraphs != 1:
            self.notify.info('zone %s has %s disconnected suit paths.' % (self.zoneId, numGraphs))
        self.battlePosDict = {}
        self.cellToGagBonusDict = {}
        for i in xrange(self.dnaStore.getNumDNAVisGroupsAI()):
            vg = self.dnaStore.getDNAVisGroupAI(i)
            zoneId = int(self.extractGroupName(vg.getName()))
            if vg.getNumBattleCells() == 1:
                battleCell = vg.getBattleCell(0)
                self.battlePosDict[zoneId] = vg.getBattleCell(0).getPos()
            elif vg.getNumBattleCells() > 1:
                self.notify.warning('multiple battle cells for zone: %d' % zoneId)
                self.battlePosDict[zoneId] = vg.getBattleCell(0).getPos()
            for i in xrange(vg.getNumChildren()):
                childDnaGroup = vg.at(i)
                if isinstance(childDnaGroup, DNAInteractiveProp):
                    self.notify.debug('got interactive prop %s' % childDnaGroup)
                    battleCellId = childDnaGroup.getCellId()
                    if battleCellId == -1:
                        self.notify.warning('interactive prop %s  at %s not associated with a a battle' % (childDnaGroup, zoneId))
                    elif battleCellId == 0:
                        if zoneId in self.cellToGagBonusDict:
                            self.notify.error('FIXME battle cell at zone %s has two props %s %s linked to it' % (zoneId, self.cellToGagBonusDict[zoneId], childDnaGroup))
                        else:
                            name = childDnaGroup.getName()
                            propType = HoodUtil.calcPropType(name)
                            if propType in ToontownBattleGlobals.PropTypeToTrackBonus:
                                trackBonus = ToontownBattleGlobals.PropTypeToTrackBonus[propType]
                                self.cellToGagBonusDict[zoneId] = trackBonus

        self.dnaStore.resetDNAVisGroups()
        self.streetPointList = []
        self.frontdoorPointList = []
        self.sidedoorPointList = []
        self.cogHQDoorPointList = []
        numPoints = self.dnaStore.getNumSuitPoints()
        for i in xrange(numPoints):
            point = self.dnaStore.getSuitPointAtIndex(i)
            if point.getPointType() == DNASuitPoint.FRONT_DOOR_POINT:
                self.frontdoorPointList.append(point)
            elif point.getPointType() == DNASuitPoint.SIDE_DOOR_POINT:
                self.sidedoorPointList.append(point)
            elif point.getPointType() == DNASuitPoint.COGHQ_IN_POINT or point.getPointType() == DNASuitPoint.COGHQ_OUT_POINT:
                self.cogHQDoorPointList.append(point)
            else:
                self.streetPointList.append(point)
            self.pointIndexes[point.getIndex()] = point

    def genPath(self, startPoint, endPoint, minPathLen, maxPathLen):
        return self.dnaStore.getSuitPath(startPoint, endPoint, minPathLen, maxPathLen)

    def getDnaStore(self):
        return self.dnaStore