# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAStorage
from direct.directnotify import DirectNotifyGlobal
from DNASuitPoint import DNASuitPoint
from DNASuitPath import DNASuitPath
from DNASuitEdge import DNASuitEdge

class DNAStorage:
    notify = DirectNotifyGlobal.directNotify.newCategory('DNAStorage')

    def __init__(self):
        self.suitPoints = []
        self.suitPointMap = {}
        self.visGroups = []
        self.suitEdges = {}
        self.battleCells = []
        self.blockTitles = {}
        self.blockBuildingTypes = {}
        self.blockDoors = {}
        self.blockPosHpr = {}
        self.blockNumbers = []
        self.blockZones = {}

    def getSuitPath(self, startPoint, endPoint, minPathLen = 40, maxPathLen = 300):
        path = DNASuitPath()
        path.addPoint(startPoint)
        while path.getNumPoints() < maxPathLen:
            startPointIndex = startPoint.getIndex()
            if startPointIndex == endPoint.getIndex():
                if path.getNumPoints() >= minPathLen:
                    break
            if startPointIndex not in self.suitEdges:
                raise Exception('Could not find DNASuitPath.')
            edges = self.suitEdges[startPointIndex]
            for edge in edges:
                startPoint = edge.getEndPoint()
                startPointType = startPoint.getPointType()
                if startPointType != DNASuitPoint.FRONT_DOOR_POINT:
                    if startPointType != DNASuitPoint.SIDE_DOOR_POINT:
                        break
            else:
                raise Exception('Could not find DNASuitPath.')

            path.addPoint(startPoint)

        return path

    def getSuitEdgeTravelTime(self, startIndex, endIndex, suitWalkSpeed):
        startPoint = self.suitPointMap.get(startIndex)
        endPoint = self.suitPointMap.get(endIndex)
        if not startPoint or not endPoint:
            return 0.0
        distance = (endPoint.getPos() - startPoint.getPos()).length()
        return distance / suitWalkSpeed

    def getSuitEdgeZone(self, startIndex, endIndex):
        return self.getSuitEdge(startIndex, endIndex).getZoneId()

    def getAdjacentPoints(self, point):
        path = DNASuitPath()
        startIndex = point.getIndex()
        if startIndex not in self.suitEdges:
            return path
        for edge in self.suitEdges[startIndex]:
            path.addPoint(edge.getEndPoint())

        return path

    def storeSuitPoint(self, suitPoint):
        if not isinstance(suitPoint, DNASuitPoint):
            raise TypeError('suitPoint must be an instance of DNASuitPoint')
        self.suitPoints.append(suitPoint)
        self.suitPointMap[suitPoint.getIndex()] = suitPoint

    def getSuitPointAtIndex(self, index):
        return self.suitPoints[index]

    def getSuitPointWithIndex(self, index):
        return self.suitPointMap.get(index)

    def resetSuitPoints(self):
        for i in self.suitEdges.keys():
            for edge in self.suitEdges[i]:
                edge.destroy()

            del self.suitEdges[i][:]
            del self.suitEdges[i]

        del self.suitPoints[:]
        self.suitPointMap.clear()
        self.suitEdges.clear()

    def getNumDNAVisGroups(self):
        return len(self.visGroups)

    def getDNAVisGroups(self):
        return self.visGroups

    def getDNAVisGroupName(self, i):
        return self.visGroups[i].getName()

    def storeDNAVisGroup(self, group):
        self.visGroups.append(group)

    def storeSuitEdge(self, startIndex, endIndex, zoneId):
        startPoint = self.getSuitPointWithIndex(startIndex)
        endPoint = self.getSuitPointWithIndex(endIndex)
        edge = DNASuitEdge(startPoint, endPoint, zoneId)
        self.suitEdges.setdefault(startIndex, []).append(edge)
        return edge

    def getSuitEdge(self, startIndex, endIndex):
        edges = self.suitEdges[startIndex]
        for edge in edges:
            if edge.getEndPoint().getIndex() == endIndex:
                return edge

    def removeBattleCell(self, cell):
        self.battleCells.remove(cell)

    def storeBattleCell(self, cell):
        self.battleCells.append(cell)

    def resetBattleCells(self):
        del self.battleCells[:]

    def getBlock(self, name):
        block = name[name.find(':') - 2:name.find(':')]
        if not block[0].isdigit():
            block = block[1:]
        return block

    def getBlockBuildingType(self, blockNumber):
        if blockNumber in self.blockBuildingTypes:
            return self.blockBuildingTypes[blockNumber]

    def getTitleFromBlockNumber(self, blockNumber):
        if blockNumber in self.blockTitles:
            return self.blockTitles[blockNumber]
        return ''

    def getDoorPosHprFromBlockNumber(self, blockNumber):
        key = str(blockNumber)
        if key in self.blockDoors:
            return self.blockDoors[key]

    def getBlockPosHpr(self, blockNumber):
        key = str(blockNumber)
        if key in self.blockPosHpr:
            return self.blockPosHpr[key]
        else:
            return (None, None)
            return None

    def storeBlockDoor(self, blockNumber, door):
        self.blockDoors[str(blockNumber)] = door

    def storeBlockPosHpr(self, blockNumber, posHpr):
        self.blockPosHpr[str(blockNumber)] = posHpr

    def storeBlockTitle(self, blockNumber, title):
        self.blockTitles[blockNumber] = title

    def storeBlockBuildingType(self, blockNumber, buildingType):
        self.blockBuildingTypes[blockNumber] = buildingType

    def storeBlock(self, blockNumber, title, bldgType, zoneId):
        self.storeBlockNumber(blockNumber)
        self.storeBlockTitle(blockNumber, title)
        self.storeBlockBuildingType(blockNumber, bldgType)
        self.storeBlockZone(blockNumber, zoneId)

    def resetDNAVisGroups(self):
        for visGroup in self.visGroups:
            visGroup.destroy()

        del self.visGroups[:]

    def getNumDNAVisGroupsAI(self):
        return self.getNumDNAVisGroups()

    def getNumSuitPoints(self):
        return len(self.suitPoints)

    def getNumVisiblesInDNAVisGroup(self, i):
        return self.visGroups[i].getNumVisibles()

    def getVisibleName(self, i, j):
        return self.visGroups[i].getVisibleName(j)

    def getDNAVisGroupAI(self, i):
        return self.visGroups[i]

    def discoverContinuity(self):
        return 1

    def resetBlockNumbers(self):
        del self.blockNumbers[:]
        self.blockZones.clear()
        self.resetBlockDoors()
        self.resetBlockPosHpr()
        self.blockTitles.clear()
        self.blockBuildingTypes.clear()

    def getNumBlockNumbers(self):
        return len(self.blockNumbers)

    def storeBlockNumber(self, blockNumber):
        self.blockNumbers.append(blockNumber)

    def getBlockNumberAt(self, index):
        return self.blockNumbers[index]

    def getZoneFromBlockNumber(self, blockNumber):
        if blockNumber in self.blockZones:
            return self.blockZones[blockNumber]

    def getBlockNumberFromZone(self, zone):
        if zone in self.blockZones.values():
            return self.blockZones.keys()[self.blockZones.values().index(zone)]

    def storeBlockZone(self, blockNumber, zoneId):
        self.blockZones[blockNumber] = zoneId

    def resetBlockZones(self):
        self.blockZones.clear()

    def resetBlockDoors(self):
        self.blockDoors.clear()

    def resetBlockPosHpr(self):
        self.blockPosHpr.clear()

    def cleanup(self):
        self.resetBattleCells()
        self.resetBlockNumbers()
        self.resetDNAVisGroups()
        self.resetSuitPoints()