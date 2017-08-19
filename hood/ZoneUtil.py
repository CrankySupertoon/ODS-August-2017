# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.hood.ZoneUtil
from toontown.toonbase.ToontownGlobals import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.suit import SuitDNA
zoneUtilNotify = directNotify.newCategory('ZoneUtil')
tutorialDict = None

def isGoofySpeedwayZone(zoneId):
    return zoneId == 8000


def isCogHQZone(zoneId):
    return zoneId >= 10000 and zoneId < 15000


def isMintInteriorZone(zoneId):
    return zoneId in (CashbotMintIntA,
     CashbotMintIntB,
     CashbotMintIntC,
     CashbotMintIntD)


def isServerRoomInteriorZone(zoneId):
    return zoneId in (TechbotServerRoomIntA, TechbotServerRoomIntB, TechbotServerRoomIntC)


def isDynamicZone(zoneId):
    return zoneId >= DynamicZonesBegin and zoneId < DynamicZonesEnd


def isUberZone(zoneId):
    return zoneId < UberZonesEnd


def getStreetName(branchId):
    global tutorialDict
    if tutorialDict:
        branchId = TutorialTerrace
    return StreetNames[branchId][-1]


def getLoaderName(zoneId):
    if tutorialDict:
        if zoneId in tutorialDict['interiors']:
            return 'safeZoneLoader'
        else:
            return 'townLoader'
    suffix = zoneId % 1000
    if suffix >= 500:
        suffix -= 500
    if isCogHQZone(zoneId):
        return 'cogHQLoader'
    if suffix < 100:
        return 'safeZoneLoader'
    return 'townLoader'


def getBranchLoaderName(zoneId):
    return getLoaderName(getBranchZone(zoneId))


def getSuitWhereName(zoneId):
    return getWhereName(zoneId, 0)


def getToonWhereName(zoneId):
    return getWhereName(zoneId, 1)


def isPlayground(zoneId):
    return getWhereName(zoneId, False) == 'cogHQExterior' or zoneId % 1000 == 0 and zoneId < DynamicZonesBegin


def isHQ(zoneId):
    return zoneId in (2520, 1507, 3508, 4504, 5502, 7503, 9505)


def isPetshop(zoneId):
    return zoneId in (2522, 1510, 3511, 4508, 5505, 7504, 9508)


def isHouse(zoneId):
    return zoneId in (2516, 7501, 7502, 7503, 7504, 7505, 7506)


def getWhereName(zoneId, isToon):
    if tutorialDict:
        if zoneId in tutorialDict['interiors']:
            return 'toonInterior'
        elif zoneId == tutorialDict['exteriors'][0]:
            return 'playground'
        elif zoneId == tutorialDict['exteriors'][1]:
            return 'street'
        else:
            return 'toonInterior'
    suffix = zoneId % 1000
    suffix = suffix - suffix % 100
    if isCogHQZone(zoneId):
        if suffix == 0:
            return 'cogHQExterior'
        if suffix == 100:
            return 'cogHQLobby'
        if suffix == 200:
            return 'factoryExterior'
        if getHoodId(zoneId) == LawbotHQ and suffix in (300, 400, 500, 600):
            return 'stageInterior'
        if getHoodId(zoneId) == BossbotHQ and suffix in (500, 600, 700):
            return 'countryClubInterior'
        if suffix >= 500:
            if getHoodId(zoneId) == SellbotHQ:
                if suffix == 600:
                    return 'fatalInterior'
                else:
                    return 'factoryInterior'
            else:
                if getHoodId(zoneId) == CashbotHQ:
                    return 'mintInterior'
                if getHoodId(zoneId) == TechbotHQ:
                    return 'serverRoomInterior'
                zoneUtilNotify.error('unknown cogHQ interior for hood: ' + str(getHoodId(zoneId)))
        else:
            zoneUtilNotify.error('unknown cogHQ where: ' + str(zoneId))
    else:
        if suffix == 0:
            return 'playground'
        if suffix >= 500:
            if isToon:
                return 'toonInterior'
            else:
                return 'suitInterior'
    return 'street'


def getBranchZone(zoneId):
    if tutorialDict:
        if zoneId == tutorialDict['exteriors'][0]:
            return CogtownCentral
        if zoneId == tutorialDict['exteriors'][1]:
            return TutorialTerrace
    branchId = zoneId - zoneId % 100
    if not isCogHQZone(zoneId):
        if zoneId % 1000 >= 500:
            branchId -= 500
    return branchId


def getHoodId(zoneId):
    if tutorialDict:
        return CogtownCentral
    return zoneId - zoneId % 1000


def getSafeZoneId(zoneId):
    hoodId = getHoodId(zoneId)
    if hoodId in HQToSafezone:
        hoodId = HQToSafezone[hoodId]
    return hoodId


def isInterior(zoneId):
    if tutorialDict:
        return zoneId in tutorialDict['interiors']
    return zoneId % 1000 >= 500


def overrideOn(exteriorList, interiorList):
    global tutorialDict
    if tutorialDict:
        zoneUtilNotify.warning('setTutorialDict: tutorialDict is already set!')
    tutorialDict = {'exteriors': exteriorList,
     'interiors': interiorList}


def overrideOff():
    global tutorialDict
    tutorialDict = None
    return


def isInTutorial():
    return tutorialDict != None


def getWakeInfo(hoodId = None, zoneId = None):
    wakeWaterHeight = 0
    showWake = 0
    try:
        if hoodId is None:
            hoodId = base.cr.playGame.getPlaceId()
        if zoneId is None:
            zoneId = base.cr.playGame.getPlace().getZoneId()
        if zoneId == DonaldsDock:
            wakeWaterHeight = DDWakeWaterHeight
            showWake = 1
        elif zoneId == ToontownCentral:
            wakeWaterHeight = TTWakeWaterHeight
            showWake = 1
        elif zoneId == OutdoorZone:
            wakeWaterHeight = OZWakeWaterHeight
            showWake = 1
        elif hoodId == MyEstate:
            wakeWaterHeight = EstateWakeWaterHeight
            showWake = 1
    except:
        pass

    return (showWake, wakeWaterHeight)


def canWearSuit(zoneId, suitIndex):
    if suitIndex == -1 or zoneId >= DynamicZonesBegin:
        return True
    hoodId = getHoodId(zoneId)
    if suitIndex < 0 or suitIndex >= len(SuitDNA.suitDeptZones) or hoodId not in SuitDNA.suitDeptZones:
        return False
    requiredIndex = SuitDNA.suitDeptZones.index(hoodId)
    return suitIndex == requiredIndex