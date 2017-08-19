# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toonbase.ToontownGlobals
from panda3d.core import BitMask32, Light, Vec4, invert
import TTLocalizer
from otp.otpbase.OTPGlobals import *
from direct.showbase.PythonUtil import Enum, invertDict
MapHotkey = 'alt'
CogHQCameraFov = 60.0
BossBattleCameraFov = 72.0
MakeAToonCameraFov = 48.0
CogdoFov = 56.9
VPElevatorFov = 53.0
CFOElevatorFov = 43.0
CJElevatorFov = 59.0
CEOElevatorFov = 59.0
CBElevatorFov = 42.0
CeilingBitmask = BitMask32(256)
FloorEventBitmask = BitMask32(16)
PieBitmask = BitMask32(256)
PetBitmask = BitMask32(8)
CatchGameBitmask = BitMask32(16)
CashbotBossObjectBitmask = BitMask32(16)
FurnitureSideBitmask = BitMask32(32)
FurnitureTopBitmask = BitMask32(64)
FurnitureDragBitmask = BitMask32(128)
PetLookatPetBitmask = BitMask32(256)
PetLookatNonPetBitmask = BitMask32(512)
BanquetTableBitmask = BitMask32(1024)
FullPies = 65535
CogHQCameraFar = 2000.0
CogHQCameraNear = 1.0
CashbotHQCameraFar = 2000.0
CashbotHQCameraNear = 1.0
LawbotHQCameraFar = 3000.0
LawbotHQCameraNear = 1.0
BossbotHQCameraFar = 3000.0
BossbotHQCameraNear = 1.0
TechbotHQCameraFar = 3000.0
TechbotHQCameraNear = 1.0
SpeedwayCameraFar = 8000.0
SpeedwayCameraNear = 1.0
DDLCameraFar = 2000.0
DDLCameraNear = 1.0
MaxMailboxContents = 60
MaxHouseItems = 250
MaxAccessories = 100
ExtraDeletedItems = 5
DeletedItemLifetime = 10080
CatalogNumWeeksPerSeries = 13
CatalogNumWeeks = 78
CatalogNPCId = 7028
PetFloorCollPriority = 5
PetPanelProximityPriority = 6
P_TooFast = -24
P_AlreadyOwnBiggerCloset = -23
P_ItemAlreadyRented = -22
P_ItemInPetTricks = -21
P_ItemInMyPhrases = -20
P_ItemAlreadyWorn = -19
P_ItemInCloset = -18
P_ItemOnGiftOrder = -17
P_ItemOnOrder = -16
P_ItemInMailbox = -15
P_PartyNotFound = 14
P_WillNotFit = -13
P_NotAGift = -12
P_OnOrderListFull = -11
P_MailboxFull = -10
P_NoPurchaseMethod = -9
P_ReachedPurchaseLimit = -8
P_NoRoomForItem = -7
P_NotShopping = -6
P_NotAtMailbox = -5
P_NotInCatalog = -4
P_NotEnoughMoney = -3
P_InvalidIndex = -2
P_UserCancelled = -1
P_ItemAvailable = 1
P_ItemOnOrder = 2
P_ItemUnneeded = 3
GIFT_user = 0
GIFT_admin = 1
GIFT_RAT = 2
GIFT_mobile = 3
GIFT_cogs = 4
GIFT_partyrefund = 5
FM_InvalidItem = -7
FM_NondeletableItem = -6
FM_InvalidIndex = -5
FM_NotOwner = -4
FM_NotDirector = -3
FM_RoomFull = -2
FM_HouseFull = -1
FM_MovedItem = 1
FM_SwappedItem = 2
FM_DeletedItem = 3
FM_RecoveredItem = 4
SPDonaldsBoat = 3
SPMinniesPiano = 4
MinHpLimit = 15
MaxHpLimit = 146
MinCarryLimit = 20
MaxCarryLimit = 80
MaxQuestCarryLimit = 4
GravityValue = 32.174
MaxCogSuitLevel = 49
CogSuitHPLevels = (14,
 19,
 29,
 39,
 49)

def getToonFont():
    return getInterfaceFontBy('toon')


def getBuildingNametagFont():
    return getInterfaceFontBy('building')


def getMinnieFont():
    return getInterfaceFontBy('minnie')


def getSuitFont():
    return getInterfaceFontBy('suit')


def getJiggeryPokeryFont():
    return getInterfaceFontBy('jiggeryPokery')


setInterfaceFonts(TTLocalizer.InterfaceFonts)
DonaldsDock = 1000
ToontownCentral = 2000
TheBrrrgh = 3000
MinniesMelodyland = 4000
DaisyGardens = 5000
OutdoorZone = 6000
ForestsEnd = 7000
GoofySpeedway = 8000
DonaldsDreamland = 9000
BarnacleBoulevard = 1100
SeaweedStreet = 1200
LighthouseLane = 1300
SillyStreet = 2100
LoopyLane = 2200
PunchlinePlace = 2300
WalrusWay = 3100
SleetStreet = 3200
PolarPlace = 3300
AltoAvenue = 4100
BaritoneBoulevard = 4200
TenorTerrace = 4300
ElmStreet = 5100
MapleStreet = 5200
OakStreet = 5300
LullabyLane = 9100
PajamaPlace = 9200
BedtimeBoulevard = 9300
ToonHall = 2513
HoodHierarchy = {ToontownCentral: (SillyStreet, LoopyLane, PunchlinePlace),
 DonaldsDock: (BarnacleBoulevard, SeaweedStreet, LighthouseLane),
 TheBrrrgh: (WalrusWay, SleetStreet, PolarPlace),
 MinniesMelodyland: (AltoAvenue, BaritoneBoulevard, TenorTerrace),
 DaisyGardens: (ElmStreet, MapleStreet, OakStreet),
 DonaldsDreamland: (LullabyLane, PajamaPlace, BedtimeBoulevard),
 GoofySpeedway: ()}
BossbotHQ = 10000
BossbotLobby = 10100
BossbotCountryClubIntA = 10500
BossbotCountryClubIntB = 10600
BossbotCountryClubIntC = 10700
SellbotHQ = 11000
SellbotLobby = 11100
SellbotFactoryExt = 11200
SellbotFactoryInt = 11500
SellbotFatalInt = 11600
CashbotHQ = 12000
CashbotLobby = 12100
CashbotMintIntA = 12500
CashbotMintIntB = 12600
CashbotMintIntC = 12700
CashbotMintIntD = 12800
LawbotHQ = 13000
LawbotLobby = 13100
LawbotOfficeExt = 13200
LawbotOfficeInt = 13300
LawbotStageIntA = 13300
LawbotStageIntB = 13400
LawbotStageIntC = 13500
LawbotStageIntD = 13600
TechbotHQ = 14000
TechbotHQLobby = 14100
TechbotServerRoomIntA = 14500
TechbotServerRoomIntB = 14600
TechbotServerRoomIntC = 14700
CogtownCentral = 21000
TutorialTerrace = 21100
MyEstate = 16000
GolfZone = 17000
PartyHood = 18000
HoodsAlwaysVisited = [17000, 18000]
UberZonesEnd = 1000
DynamicZonesBegin = 22000
DynamicZonesEnd = 1048576
cogDept2index = {'c': 0,
 'l': 1,
 'm': 2,
 's': 3,
 't': 4}
cogIndex2dept = invertDict(cogDept2index)
HQToSafezone = {SellbotHQ: DaisyGardens,
 CashbotHQ: DonaldsDreamland,
 LawbotHQ: TheBrrrgh,
 BossbotHQ: DonaldsDock,
 TechbotHQ: DonaldsDreamland}
CogDeptNames = [TTLocalizer.Bossbot,
 TTLocalizer.Lawbot,
 TTLocalizer.Cashbot,
 TTLocalizer.Sellbot,
 TTLocalizer.Techbot]

def cogHQZoneId2deptIndex(zone):
    if zone >= 14000 and zone <= 14999:
        return 4
    elif zone >= 13000:
        return 1
    elif zone >= 12000:
        return 2
    elif zone >= 11000:
        return 3
    else:
        return 0


def cogHQZoneId2dept(zone):
    return cogIndex2dept[cogHQZoneId2deptIndex(zone)]


def dept2cogHQ(dept):
    dept2hq = {'c': BossbotHQ,
     'l': LawbotHQ,
     'm': CashbotHQ,
     's': SellbotHQ,
     't': TechbotHQ}
    return dept2hq[dept]


MintNumFloors = {CashbotMintIntA: 20,
 CashbotMintIntB: 20,
 CashbotMintIntC: 20,
 CashbotMintIntD: 20}
CashbotMintCogLevel = 10
CashbotMintSkelecogLevel = 11
CashbotMintBossLevel = 12
MintNumBattles = {CashbotMintIntA: 4,
 CashbotMintIntB: 6,
 CashbotMintIntC: 8,
 CashbotMintIntD: 10}
MintCogBuckRewards = {CashbotMintIntA: 8,
 CashbotMintIntB: 14,
 CashbotMintIntC: 20,
 CashbotMintIntD: 26}
MintNumRooms = {CashbotMintIntA: 2 * (6,) + 5 * (7,) + 5 * (8,) + 5 * (9,) + 3 * (10,),
 CashbotMintIntB: 3 * (8,) + 6 * (9,) + 6 * (10,) + 5 * (11,),
 CashbotMintIntC: 4 * (10,) + 10 * (11,) + 6 * (12,),
 CashbotMintIntD: 10 * (12,) + 4 * (13,) + 6 * (14,)}
ServerRoomNumFloors = {TechbotServerRoomIntA: 20,
 TechbotServerRoomIntB: 20,
 TechbotServerRoomIntC: 20}
TechbotServerRoomCogLevel = 10
TechbotServerRoomSkelecogLevel = 11
TechbotServerRoomBossLevel = 12
ServerRoomNumBattles = {TechbotServerRoomIntA: 4,
 TechbotServerRoomIntB: 6,
 TechbotServerRoomIntC: 8}
ServerRoomCogBuckRewards = {TechbotServerRoomIntA: 8,
 TechbotServerRoomIntB: 14,
 TechbotServerRoomIntC: 20}
ServerRoomNumRooms = {TechbotServerRoomIntA: 2 * (6,) + 5 * (7,) + 5 * (8,) + 5 * (9,) + 3 * (10,),
 TechbotServerRoomIntB: 3 * (8,) + 6 * (9,) + 6 * (10,) + 5 * (11,),
 TechbotServerRoomIntC: 4 * (10,) + 10 * (11,) + 6 * (12,)}
BossbotCountryClubCogLevel = 11
BossbotCountryClubSkelecogLevel = 12
BossbotCountryClubBossLevel = 12
CountryClubNumRooms = {BossbotCountryClubIntA: (4,),
 BossbotCountryClubIntB: 3 * (8,) + 6 * (9,) + 6 * (10,) + 5 * (11,),
 BossbotCountryClubIntC: 4 * (10,) + 10 * (11,) + 6 * (12,)}
CountryClubNumBattles = {BossbotCountryClubIntA: 3,
 BossbotCountryClubIntB: 2,
 BossbotCountryClubIntC: 3}
CountryClubCogBuckRewards = {BossbotCountryClubIntA: 8,
 BossbotCountryClubIntB: 14,
 BossbotCountryClubIntC: 20}
LawbotStageCogLevel = 10
LawbotStageSkelecogLevel = 11
LawbotStageBossLevel = 12
StageNumBattles = {LawbotStageIntA: 0,
 LawbotStageIntB: 0,
 LawbotStageIntC: 0,
 LawbotStageIntD: 0}
StageNoticeRewards = {LawbotStageIntA: 75,
 LawbotStageIntB: 150,
 LawbotStageIntC: 225,
 LawbotStageIntD: 300}
StageNumRooms = {LawbotStageIntA: 2 * (6,) + 5 * (7,) + 5 * (8,) + 5 * (9,) + 3 * (10,),
 LawbotStageIntB: 3 * (8,) + 6 * (9,) + 6 * (10,) + 5 * (11,),
 LawbotStageIntC: 4 * (10,) + 10 * (11,) + 6 * (12,),
 LawbotStageIntD: 4 * (10,) + 10 * (11,) + 6 * (12,)}
FT_FullSuit = 'fullSuit'
FT_Leg = 'leg'
FT_Arm = 'arm'
FT_Torso = 'torso'
FT_Head = 'head'
factoryId2factoryType = {SellbotFactoryInt: FT_FullSuit,
 SellbotFatalInt: FT_FullSuit,
 LawbotOfficeInt: FT_FullSuit}
StreetNames = TTLocalizer.GlobalStreetNames
StreetBranchZones = StreetNames.keys()
Hoods = (DonaldsDock,
 ToontownCentral,
 TheBrrrgh,
 MinniesMelodyland,
 DaisyGardens,
 OutdoorZone,
 ForestsEnd,
 GoofySpeedway,
 DonaldsDreamland,
 BossbotHQ,
 SellbotHQ,
 CashbotHQ,
 LawbotHQ,
 TechbotHQ,
 GolfZone)
HoodsForTeleportAll = (DonaldsDock,
 ToontownCentral,
 TheBrrrgh,
 MinniesMelodyland,
 DaisyGardens,
 OutdoorZone,
 GoofySpeedway,
 DonaldsDreamland,
 BossbotHQ,
 SellbotHQ,
 CashbotHQ,
 LawbotHQ,
 TechbotHQ,
 GolfZone)
BingoCardNames = {'normal': 0,
 'corners': 1,
 'diagonal': 2,
 'threeway': 3,
 'blockout': 4}
NoPreviousGameId = 0
RaceGameId = 1
CannonGameId = 2
TagGameId = 3
PatternGameId = 4
RingGameId = 5
MazeGameId = 6
TugOfWarGameId = 7
CatchGameId = 8
DivingGameId = 9
TargetGameId = 10
VineGameId = 11
IceGameId = 12
CogThiefGameId = 13
TwoDGameId = 14
MinigameNames = {'race': RaceGameId,
 'cannon': CannonGameId,
 'tag': TagGameId,
 'pattern': PatternGameId,
 'jaymo': PatternGameId,
 'match': PatternGameId,
 'matching': PatternGameId,
 'ring': RingGameId,
 'maze': MazeGameId,
 'tug': TugOfWarGameId,
 'catch': CatchGameId,
 'diving': DivingGameId,
 'target': TargetGameId,
 'vine': VineGameId,
 'ice': IceGameId,
 'thief': CogThiefGameId,
 '2d': TwoDGameId}
MinigameTemplateId = -1
MinigameIDs = (RaceGameId,
 CannonGameId,
 TagGameId,
 PatternGameId,
 RingGameId,
 MazeGameId,
 TugOfWarGameId,
 CatchGameId,
 DivingGameId,
 TargetGameId,
 VineGameId,
 IceGameId,
 CogThiefGameId,
 TwoDGameId)
MinigamePlayerMatrix = {1: (CannonGameId,
     MazeGameId,
     TugOfWarGameId,
     RingGameId,
     VineGameId,
     CogThiefGameId,
     TwoDGameId,
     DivingGameId,
     CatchGameId,
     TargetGameId),
 2: (CannonGameId,
     MazeGameId,
     TugOfWarGameId,
     PatternGameId,
     TagGameId,
     RingGameId,
     VineGameId,
     IceGameId,
     CogThiefGameId,
     TwoDGameId,
     DivingGameId,
     CatchGameId,
     TargetGameId),
 3: (CannonGameId,
     MazeGameId,
     TugOfWarGameId,
     PatternGameId,
     RaceGameId,
     TagGameId,
     VineGameId,
     RingGameId,
     IceGameId,
     CogThiefGameId,
     TwoDGameId,
     DivingGameId,
     CatchGameId,
     TargetGameId),
 4: (CannonGameId,
     MazeGameId,
     TugOfWarGameId,
     PatternGameId,
     RaceGameId,
     TagGameId,
     VineGameId,
     RingGameId,
     IceGameId,
     CogThiefGameId,
     TwoDGameId,
     DivingGameId,
     CatchGameId,
     TargetGameId)}
KeyboardTimeout = 300
phaseMap = {ToontownCentral: 4,
 MyEstate: 5.5,
 DonaldsDock: 6,
 MinniesMelodyland: 6,
 GoofySpeedway: 6,
 TheBrrrgh: 8,
 DaisyGardens: 8,
 ForestsEnd: 8,
 DonaldsDreamland: 8,
 OutdoorZone: 6,
 BossbotHQ: 12,
 SellbotHQ: 9,
 CashbotHQ: 10,
 LawbotHQ: 11,
 TechbotHQ: 11,
 GolfZone: 6,
 PartyHood: 13,
 CogtownCentral: 4}
streetPhaseMap = {ToontownCentral: 5,
 DonaldsDock: 6,
 MinniesMelodyland: 6,
 GoofySpeedway: 6,
 TheBrrrgh: 8,
 DaisyGardens: 8,
 ForestsEnd: 8,
 DonaldsDreamland: 8,
 OutdoorZone: 8,
 BossbotHQ: 12,
 SellbotHQ: 9,
 CashbotHQ: 10,
 LawbotHQ: 11,
 TechbotHQ: 11,
 PartyHood: 13,
 CogtownCentral: 4}
dnaMap = {ToontownCentral: 'toontown_central',
 DonaldsDock: 'donalds_dock',
 MinniesMelodyland: 'minnies_melody_land',
 GoofySpeedway: 'goofy_speedway',
 TheBrrrgh: 'the_burrrgh',
 DaisyGardens: 'daisys_garden',
 ForestsEnd: 'forests_end',
 DonaldsDreamland: 'donalds_dreamland',
 OutdoorZone: 'outdoor_zone',
 BossbotHQ: 'cog_hq_bossbot',
 SellbotHQ: 'cog_hq_sellbot',
 CashbotHQ: 'cog_hq_cashbot',
 LawbotHQ: 'cog_hq_lawbot',
 TechbotHQ: 'cog_hq_techbot',
 GolfZone: 'golf_zone',
 CogtownCentral: 'cogtown_central'}
hoodNameMap = {DonaldsDock: TTLocalizer.DonaldsDock,
 ToontownCentral: TTLocalizer.ToontownCentral,
 TheBrrrgh: TTLocalizer.TheBrrrgh,
 MinniesMelodyland: TTLocalizer.MinniesMelodyland,
 DaisyGardens: TTLocalizer.DaisyGardens,
 OutdoorZone: TTLocalizer.OutdoorZone,
 ForestsEnd: TTLocalizer.ForestsEnd,
 GoofySpeedway: TTLocalizer.GoofySpeedway,
 DonaldsDreamland: TTLocalizer.DonaldsDreamland,
 BossbotHQ: TTLocalizer.BossbotHQ,
 SellbotHQ: TTLocalizer.SellbotHQ,
 CashbotHQ: TTLocalizer.CashbotHQ,
 LawbotHQ: TTLocalizer.LawbotHQ,
 TechbotHQ: TTLocalizer.TechbotHQ,
 MyEstate: TTLocalizer.MyEstate,
 GolfZone: TTLocalizer.GolfZone,
 PartyHood: TTLocalizer.PartyHood,
 CogtownCentral: TTLocalizer.CogtownCentral}
TrophyStarLevels = (10, 20, 30, 50, 75, 100)
TrophyStarColors = (Vec4(0.9, 0.6, 0.2, 1),
 Vec4(0.9, 0.6, 0.2, 1),
 Vec4(0.8, 0.8, 0.8, 1),
 Vec4(0.8, 0.8, 0.8, 1),
 Vec4(1, 1, 0, 1),
 Vec4(1, 1, 0, 1))
SuitWalkSpeed = 4.8
PieThrowArc = 0
PieThrowLinear = 1
PieCodeBossCog = 1
PieCodeNotBossCog = 2
PieCodeToon = 3
PieCodeBossInsides = 4
PieCodeDefensePan = 5
PieCodeProsecutionPan = 6
PieCodeLawyer = 7
PieCodeInvasionSuit = 8
PieCodeColors = {PieCodeBossCog: None,
 PieCodeNotBossCog: (0.8, 0.8, 0.8, 1),
 PieCodeToon: None}
BossCogRollSpeed = 7.5
BossCogTurnSpeed = 20
BossCogTreadSpeed = 3.5
BossCogDizzy = 0
BossCogElectricFence = 1
BossCogSwatLeft = 2
BossCogSwatRight = 3
BossCogAreaAttack = 4
BossCogFrontAttack = 5
BossCogRecoverDizzyAttack = 6
BossCogDirectedAttack = 7
BossCogStrafeAttack = 8
BossCogNoAttack = 9
BossCogGoonZap = 10
BossCogSlowDirectedAttack = 11
BossCogDizzyNow = 12
BossCogGavelStomp = 13
BossCogGavelHandle = 14
BossCogLawyerAttack = 15
BossCogMoveAttack = 16
BossCogGolfAttack = 17
BossCogGolfAreaAttack = 18
BossCogGearDirectedAttack = 19
BossCogOvertimeAttack = 20
BossCogAttackTimes = {BossCogElectricFence: 0,
 BossCogSwatLeft: 5.5,
 BossCogSwatRight: 5.5,
 BossCogAreaAttack: 4.5,
 BossCogFrontAttack: 2.65,
 BossCogRecoverDizzyAttack: 5.1,
 BossCogDirectedAttack: 4.84,
 BossCogNoAttack: 6,
 BossCogSlowDirectedAttack: 7.84,
 BossCogMoveAttack: 3,
 BossCogGolfAttack: 6,
 BossCogGolfAreaAttack: 7,
 BossCogGearDirectedAttack: 4.84,
 BossCogOvertimeAttack: 5}
BossCogDamageLevels = {BossCogElectricFence: 1,
 BossCogSwatLeft: 5,
 BossCogSwatRight: 5,
 BossCogAreaAttack: 10,
 BossCogFrontAttack: 3,
 BossCogRecoverDizzyAttack: 3,
 BossCogDirectedAttack: 3,
 BossCogStrafeAttack: 2,
 BossCogGoonZap: 5,
 BossCogSlowDirectedAttack: 10,
 BossCogGavelStomp: 20,
 BossCogGavelHandle: 2,
 BossCogLawyerAttack: 5,
 BossCogMoveAttack: 20,
 BossCogGolfAttack: 15,
 BossCogGolfAreaAttack: 15,
 BossCogGearDirectedAttack: 15,
 BossCogOvertimeAttack: 10}
BossCogBattleAPosHpr = (0, -25, 0, 0, 0, 0)
BossCogBattleBPosHpr = (0, 25, 0, 180, 0, 0)
SellbotBossMaxDamage = 100
SellbotBossMaxDamageNerfed = 100
SellbotBossBattleOnePosHpr = (0, -35, 0, -90, 0, 0)
SellbotBossBattleTwoPosHpr = (0, 60, 18, -90, 0, 0)
SellbotBossBattleThreeHpr = (180, 0, 0)
SellbotBossBottomPos = (0, -110, -6.5)
SellbotBossDeathPos = (0, -175, -6.5)
SellbotBossDooberTurnPosA = (-20, -50, 0)
SellbotBossDooberTurnPosB = (20, -50, 0)
SellbotBossDooberTurnPosDown = (0, -50, 0)
SellbotBossDooberTurnPosDown2 = (0, -60, 0)
SellbotBossDooberTurnPosDown3 = (0, -97, -6.5)
SellbotBossDooberFlyPos = (0, -135, -6.5)
SellbotBossTopRampPosA = (-80, -35, 18)
SellbotBossTopRampTurnPosA = (-80, 10, 18)
SellbotBossP3PosA = (-50, 40, 18)
SellbotBossTopRampPosB = (80, -35, 18)
SellbotBossTopRampTurnPosB = (80, 10, 18)
SellbotBossP3PosB = (50, 60, 18)
CashbotBossMaxDamage = 500
CashbotBossOffstagePosHpr = (120, -195, 0, 0, 0, 0)
CashbotBossBattleOnePosHpr = (120, -230, 0, 90, 0, 0)
CashbotRTBattleOneStartPosHpr = (94, -220, 0, 110, 0, 0)
CashbotBossBattleThreePosHpr = (120, -315, 0, 180, 0, 0)
CashbotToonsBattleThreeStartPosHpr = [(105, -285, 0, 208, 0, 0),
 (136, -342, 0, 398, 0, 0),
 (105, -342, 0, 333, 0, 0),
 (135, -292, 0, 146, 0, 0),
 (93, -303, 0, 242, 0, 0),
 (144, -327, 0, 64, 0, 0),
 (145, -302, 0, 117, 0, 0),
 (93, -327, 0, -65, 0, 0)]
CashbotBossSafePosHprs = [(120, -315, 30, 0, 0, 0),
 (77.2, -329.3, 0, -90, 0, 0),
 (77.1, -302.7, 0, -90, 0, 0),
 (165.7, -326.4, 0, 90, 0, 0),
 (165.5, -302.4, 0, 90, 0, 0),
 (107.8, -359.1, 0, 0, 0, 0),
 (133.9, -359.1, 0, 0, 0, 0),
 (107.0, -274.7, 0, 180, 0, 0),
 (134.2, -274.7, 0, 180, 0, 0)]
CashbotBossCranePosHprs = [(97.4, -337.6, 0, -45, 0, 0),
 (97.4, -292.4, 0, -135, 0, 0),
 (142.6, -292.4, 0, 135, 0, 0),
 (142.6, -337.6, 0, 45, 0, 0)]
CashbotBossToMagnetTime = 0.2
CashbotBossFromMagnetTime = 1
CashbotBossSafeKnockImpact = 0.5
CashbotBossSafeNewImpact = 0.0
CashbotBossGoonImpact = 0.1
CashbotBossKnockoutDamage = 15
TTWakeWaterHeight = -4.79
DDWakeWaterHeight = 1.669
EstateWakeWaterHeight = -0.3
OZWakeWaterHeight = -0.5
WakeRunDelta = 0.1
WakeWalkDelta = 0.2
NoItems = 0
NewItems = 1
OldItems = 2
SuitInvasionBegin = 0
SuitInvasionEnd = 1
SuitInvasionUpdate = 2
SuitInvasionBulletin = 3
SkelecogInvasionBegin = 4
SkelecogInvasionEnd = 5
SkelecogInvasionBulletin = 6
WaiterInvasionBegin = 7
WaiterInvasionEnd = 8
WaiterInvasionBulletin = 9
V2InvasionBegin = 10
V2InvasionEnd = 11
V2InvasionBulletin = 12
EndingInvasions = [SuitInvasionEnd,
 SkelecogInvasionEnd,
 WaiterInvasionEnd,
 V2InvasionEnd]
SUMMER_FIREWORKS = 1
NEW_YEAR_FIREWORKS = 2
HALLOWEEN = 3
CHRISTMAS = 4
SKELECOG_INVASION = 5
MR_HOLLYWOOD_INVASION = 6
BLACK_CAT_DAY = 9
RESISTANCE_EVENT = 10
KART_RECORD_DAILY_RESET = 11
KART_RECORD_WEEKLY_RESET = 12
CIRCUIT_RACING = 14
POLAR_PLACE_EVENT = 15
GRAND_PRIX = 16
FISH_BINGO = 17
SILLY_SATURDAY = 18
BOSSCOG_INVASION = 23
MARCH_INVASION = 24
MORE_XP_HOLIDAY = 25
BOSS_HOLIDAY = 26
DECEMBER_INVASION = 28
APRIL_TOONS_WEEK = 29
OCTOBER31_FIREWORKS = 31
NOVEMBER19_FIREWORKS = 32
SELLBOT_SURPRISE_1 = 33
SELLBOT_SURPRISE_2 = 34
SELLBOT_SURPRISE_3 = 35
SELLBOT_SURPRISE_4 = 36
CASHBOT_CONUNDRUM_1 = 37
CASHBOT_CONUNDRUM_2 = 38
CASHBOT_CONUNDRUM_3 = 39
CASHBOT_CONUNDRUM_4 = 40
LAWBOT_GAMBIT_1 = 41
LAWBOT_GAMBIT_2 = 42
LAWBOT_GAMBIT_3 = 43
LAWBOT_GAMBIT_4 = 44
TROUBLE_BOSSBOTS_1 = 45
TROUBLE_BOSSBOTS_2 = 46
TROUBLE_BOSSBOTS_3 = 47
TROUBLE_BOSSBOTS_4 = 48
JELLYBEAN_DAY = 49
FEBRUARY14_FIREWORKS = 51
JULY14_FIREWORKS = 52
JUNE22_FIREWORKS = 53
BIGWIG_INVASION = 54
COLD_CALLER_INVASION = 53
BEAN_COUNTER_INVASION = 54
DOUBLE_TALKER_INVASION = 55
DOWNSIZER_INVASION = 56
HYDRANT_ZERO_HOLIDAY = 58
VALENTOONS_DAY = 59
SILLYMETER_HOLIDAY = 60
MAILBOX_ZERO_HOLIDAY = 61
TRASHCAN_ZERO_HOLIDAY = 62
SILLY_SURGE_HOLIDAY = 63
SILLY_CHATTER_ONE = 67
SILLY_CHATTER_TWO = 68
SILLY_CHATTER_THREE = 69
SILLY_CHATTER_FOUR = 70
SILLY_TEST = 71
YES_MAN_INVASION = 72
TIGHTWAD_INVASION = 73
TELEMARKETER_INVASION = 74
HEADHUNTER_INVASION = 75
SPINDOCTOR_INVASION = 76
MONEYBAGS_INVASION = 77
TWOFACES_INVASION = 78
MINGLER_INVASION = 79
LOANSHARK_INVASION = 80
CORPORATE_RAIDER_INVASION = 81
ROBBER_BARON_INVASION = 82
LEGAL_EAGLE_INVASION = 83
BIG_WIG_INVASION = 84
BIG_CHEESE_INVASION = 85
DOWN_SIZER_INVASION = 86
MOVER_AND_SHAKER_INVASION = 87
DOUBLETALKER_INVASION = 88
PENNY_PINCHER_INVASION = 89
NAME_DROPPER_INVASION = 90
AMBULANCE_CHASER_INVASION = 91
MICROMANAGER_INVASION = 92
NUMBER_CRUNCHER_INVASION = 93
SILLY_CHATTER_FIVE = 94
VICTORY_PARTY_HOLIDAY = 95
SELLBOT_NERF_HOLIDAY = 96
JELLYBEAN_TROLLEY_HOLIDAY = 97
JELLYBEAN_FISHING_HOLIDAY = 98
JELLYBEAN_PARTIES_HOLIDAY = 99
TOP_TOONS_MARATHON = 101
SELLBOT_INVASION = 102
SELLBOT_FIELD_OFFICE = 103
SELLBOT_INVASION_MOVER_AND_SHAKER = 104
IDES_OF_MARCH = 105
EXPANDED_CLOSETS = 106
TAX_DAY_INVASION = 107
KARTING_TICKETS_HOLIDAY = 109
PRE_JULY_4_DOWNSIZER_INVASION = 110
PRE_JULY_4_BIGWIG_INVASION = 111
COMBO_FIREWORKS = 112
JELLYBEAN_TROLLEY_HOLIDAY_MONTH = 113
JELLYBEAN_FISHING_HOLIDAY_MONTH = 114
JELLYBEAN_PARTIES_HOLIDAY_MONTH = 115
SILLYMETER_EXT_HOLIDAY = 116
TOT_REWARD_JELLYBEAN_AMOUNT = 100
TOT_REWARD_END_OFFSET_AMOUNT = 0
LawbotBossMaxDamage = 2700
LawbotBossWinningTilt = 40
LawbotBossInitialDamage = 1350
LawbotBossBattleOnePosHpr = (-2.798, -60, 0, 0, 0, 0)
LawbotBossBattleTwoPosHpr = (-2.798, 89, 19.145, 0, 0, 0)
LawbotBossBattleThreePosHpr = LawbotBossBattleTwoPosHpr
LawbotBossBottomPos = (50, 39, 0)
LawbotBossDeathPos = (50, 40, 0)
LawbotBossGavelPosHprs = [(35, 78.328, 0, -135, 0, 0),
 (68.5, 78.328, 0, 135, 0, 0),
 (47, -33, 0, 45, 0, 0),
 (-50, -39, 0, -45, 0, 0),
 (-9, -37, 0, 0, 0, 0),
 (-9, 49, 0, -180, 0, 0),
 (32, 0, 0, 45, 0, 0),
 (33, 56, 0, 135, 0, 0)]
LawbotBossGavelTimes = [(0.2, 0.9, 0.6),
 (0.25, 1, 0.5),
 (1.0, 6, 0.5),
 (0.3, 3, 1),
 (0.26, 0.9, 0.45),
 (0.24, 1.1, 0.65),
 (0.27, 1.2, 0.45),
 (0.25, 0.95, 0.5)]
LawbotBossGavelHeadings = [(0,
  -15,
  4,
  -115,
  5,
  45),
 (0, -45, -4, -35, -45, -16, 32),
 (0, -8, 19, -7, 5, 23),
 (0, -4, 8, -16, 32, -45, 7, 7, -30, 19, -13, 25),
 (0, -45, -90, 45, 90),
 (0, -45, -90, 45, 90),
 (0, -45, 45),
 (0, -45, 45)]
LawbotBossCogRelBattleAPosHpr = (-25, -10, 0, 0, 0, 0)
LawbotBossCogRelBattleBPosHpr = (-25, 10, 0, 0, 0, 0)
LawbotBossCogAbsBattleAPosHpr = (-5, -2, 0, 0, 0, 0)
LawbotBossCogAbsBattleBPosHpr = (-5, 0, 0, 0, 0, 0)
LawbotBossInjusticePosHpr = (-3, 12, 0, 90, 0, 0)
LawbotBossInjusticeScale = (1.75, 1.75, 1.5)
LawbotBossDefensePanDamage = 1
LawbotBossLawyerPosHprs = [(-57, -24, 0, -90, 0, 0),
 (-57, -12, 0, -90, 0, 0),
 (-57, 0, 0, -90, 0, 0),
 (-57, 12, 0, -90, 0, 0),
 (-57, 24, 0, -90, 0, 0),
 (-57, 36, 0, -90, 0, 0),
 (-57, 48, 0, -90, 0, 0),
 (-57, 60, 0, -90, 0, 0),
 (-3, -37.3, 0, 0, 0, 0),
 (-3, 53, 0, -180, 0, 0)]
LawbotBossLawyerCycleTime = 6
LawbotBossLawyerToPanTime = 2.5
LawbotBossLawyerChanceToAttack = 50
LawbotBossLawyerHeal = 2
LawbotBossLawyerStunTime = 5
LawbotBossDifficultySettings = [(38, 4, 8, 1, 0, 0),
 (36, 5, 8, 1, 0, 0),
 (34, 5, 8, 1, 0, 0),
 (32, 6, 8, 2, 0, 0),
 (30, 6, 8, 2, 0, 0),
 (28, 7, 8, 3, 0, 0),
 (26, 7, 9, 3, 1, 1),
 (24, 8, 9, 4, 1, 1),
 (22, 8, 10, 4, 1, 0)]
LawbotBossCannonPosHprs = [(-40, -12, 0, -90, 0, 0),
 (-40, 0, 0, -90, 0, 0),
 (-40, 12, 0, -90, 0, 0),
 (-40, 24, 0, -90, 0, 0),
 (-40, 36, 0, -90, 0, 0),
 (-40, 48, 0, -90, 0, 0),
 (-40, 60, 0, -90, 0, 0),
 (-40, 72, 0, -90, 0, 0)]
LawbotBossCannonPosA = (-80, -51.48, 0)
LawbotBossCannonPosB = (-80, 70.73, 0)
LawbotBossChairPosHprs = [(60, 72, 0, -90, 0, 0),
 (60, 62, 0, -90, 0, 0),
 (60, 52, 0, -90, 0, 0),
 (60, 42, 0, -90, 0, 0),
 (60, 32, 0, -90, 0, 0),
 (60, 22, 0, -90, 0, 0),
 (70, 72, 5, -90, 0, 0),
 (70, 62, 5, -90, 0, 0),
 (70, 52, 5, -90, 0, 0),
 (70, 42, 5, -90, 0, 0),
 (70, 32, 5, -90, 0, 0),
 (70, 22, 5, -90, 0, 0)]
LawbotBossChairRow1PosB = (59.3, 48, 14.05)
LawbotBossChairRow1PosA = (59.3, -18.2, 14.05)
LawbotBossChairRow2PosB = (75.1, 48, 28.2)
LawbotBossChairRow2PosA = (75.1, -18.2, 28.2)
LawbotBossCannonBallMax = 12
LawbotBossJuryBoxStartPos = (94, -8, 5)
LawbotBossJuryBoxRelativeEndPos = (30, 0, 12.645)
LawbotBossJuryBoxMoveTime = 70
LawbotBossJurorsForBalancedScale = 8
LawbotBossDamagePerJuror = 68
LawbotBossCogJurorFlightTime = 10
LawbotBossCogJurorDistance = 75
LawbotBossBaseJurorNpcId = 2001
LawbotBossWitnessEpiloguePosHpr = (-3, 0, 0, 180, 0, 0)
LawbotBossChanceForTaunt = 25
LawbotBossBonusWaitTime = 60
LawbotBossBonusDuration = 20
LawbotBossBonusToonup = 10
LawbotBossBonusWeightMultiplier = 2
LawbotBossChanceToDoAreaAttack = 11
LOW_POP_JP = 0
MID_POP_JP = 100
HIGH_POP_JP = 200
LOW_POP_INTL = 399
MID_POP_INTL = 499
HIGH_POP_INTL = -1
LOW_POP = 100
MID_POP = 200
HIGH_POP = -1
PinballCannonBumper = 0
PinballCloudBumperLow = 1
PinballCloudBumperMed = 2
PinballCloudBumperHigh = 3
PinballTarget = 4
PinballRoof = 5
PinballHouse = 6
PinballFence = 7
PinballBridge = 8
PinballStatuary = 9
PinballScoring = [(100, 1),
 (150, 1),
 (200, 1),
 (250, 1),
 (350, 1),
 (100, 1),
 (50, 1),
 (25, 1),
 (100, 1),
 (10, 1)]
PinballCannonBumperInitialPos = (0, -20, 40)
RentalCop = 0
RentalCannon = 1
RentalGameTable = 2
ColorPlayer = (0.3, 0.7, 0.3, 1)
ColorAvatar = (0.3, 0.3, 0.7, 1)
ColorPet = (0.6, 0.4, 0.2, 1)
ColorFreeChat = (0.3, 0.3, 0.8, 1)
ColorSpeedChat = (0.2, 0.6, 0.4, 1)
ColorNoChat = (0.8, 0.5, 0.1, 1)
PICNIC_COUNTDOWN_TIME = 60
BossbotRTIntroStartPosHpr = (0, -64, 0, 180, 0, 0)
BossbotRTPreTwoPosHpr = (0, -20, 0, 180, 0, 0)
BossbotRTEpiloguePosHpr = (0, 90, 0, 180, 0, 0)
BossbotBossBattleOnePosHpr = (0, 355, 0, 0, 0, 0)
BossbotBossPreTwoPosHpr = (0, 20, 0, 0, 0, 0)
BossbotElevCamPosHpr = (0, -100.544, 7.18258, 0, 0, 0)
BossbotFoodModelScale = 0.75
BossbotNumFoodToExplode = 3
BossbotBossServingDuration = 300
BossbotPrepareBattleThreeDuration = 20
WaiterBattleAPosHpr = (20, -400, 0, 0, 0, 0)
WaiterBattleBPosHpr = (-20, -400, 0, 0, 0, 0)
BossbotBossBattleThreePosHpr = (0, 355, 0, 0, 0, 0)
DinerBattleAPosHpr = (20, -240, 0, 0, 0, 0)
DinerBattleBPosHpr = (-20, -240, 0, 0, 0, 0)
BossbotBossMaxDamage = 500
BossbotMaxSpeedDamage = 90
BossbotSpeedRecoverRate = 20
BossbotBossDifficultySettings = [(8, 4, 11, 3, 30, 25),
 (9, 5, 12, 6, 28, 26),
 (10, 6, 11, 7, 26, 27),
 (8, 8, 12, 8, 24, 28),
 (13, 5, 12, 9, 22, 29)]
BossbotRollSpeedMax = 22
BossbotRollSpeedMin = 7.5
BossbotTurnSpeedMax = 60
BossbotTurnSpeedMin = 20
BossbotTreadSpeedMax = 10.5
BossbotTreadSpeedMin = 3.5
CalendarFilterShowAll = 0
CalendarFilterShowOnlyHolidays = 1
CalendarFilterShowOnlyParties = 2
TTC = 1
DD = 2
MM = 3
GS = 4
DG = 5
BR = 6
OZ = 7
DL = 8
AnimPropTypes = Enum(('Unknown', 'Hydrant', 'Mailbox', 'Trashcan'), start=-1)
EmblemTypes = Enum(('Silver', 'Gold'))
NumEmblemTypes = 2
MaxBankMoney = 30000
DefaultBankItemId = 1300
ToonAnimStates = set(['off',
 'neutral',
 'victory',
 'Happy',
 'Sad',
 'Catching',
 'CatchEating',
 'Sleep',
 'walk',
 'jumpSquat',
 'jump',
 'jumpAirborne',
 'jumpLand',
 'run',
 'swim',
 'swimhold',
 'dive',
 'cringe',
 'OpenBook',
 'ReadBook',
 'CloseBook',
 'TeleportOut',
 'Died',
 'TeleportedOut',
 'TeleportIn',
 'Emote',
 'SitStart',
 'Sit',
 'Push',
 'Squish',
 'FallDown',
 'GolfPuttLoop',
 'GolfRotateLeft',
 'GolfRotateRight',
 'GolfPuttSwing',
 'GolfGoodPutt',
 'GolfBadPutt',
 'Flattened',
 'CogThiefRunning',
 'ScientistJealous',
 'ScientistEmcee',
 'ScientistWork',
 'ScientistLessWork',
 'ScientistPlay'])
AV_FLAG_REASON_TOUCH = 1
AV_FLAG_HISTORY_LEN = 500
AV_TOUCH_CHECK_DELAY_AI = 3.0
AV_TOUCH_CHECK_DELAY_CL = 1.0
AV_TOUCH_CHECK_DIST = 2.0
AV_TOUCH_CHECK_DIST_Z = 5.0
AV_TOUCH_CHECK_TIMELIMIT_CL = 0.002
AV_TOUCH_COUNT_LIMIT = 5
AV_TOUCH_COUNT_TIME = 300
PaintCost = 2000
BMovementSpeed = 0
BMovementSpeedMultiplier = 1.3
NPCCollisionDelay = 2.5
CostPerLaffRestock = 3
FISHSALE_COMPLETE = 0
FISHSALE_TROPHY = 1
FISHSALE_DUMPED = 2
CLERK_GOODBYE = 0
CLERK_GREETING = 1
CLERK_TOOKTOOLONG = 2
KnockKnockHeal = 12
KnockKnockCooldown = 600
CRATE_NOT_OWNER = 0
CRATE_NO_KEYS = 1
CRATE_BEANS = 2
CRATE_BUFFS = 3
CRATE_NAMETAGS = 4
CRATE_EMOTES = 5
CRATE_CLOTHING = 6
CRATE_ACCESSORIES = 7
STAT_COGS = 0
STAT_V2 = 1
STAT_SKELE = 2
STAT_UNIQUE = 3
STAT_BEANS_SPENT = 4
STAT_BEANS_EARNT = 5
STAT_TASKS = 6
STAT_VP = 7
STAT_CFO = 8
STAT_CJ = 9
STAT_CEO = 10
STAT_SOLO = 11
STAT_SOLO_VP = 12
STAT_SOLO_CFO = 13
STAT_SOLO_CJ = 14
STAT_SOLO_CEO = 15
STAT_SAD = 16
STAT_BLDG = 17
STAT_COGDO = 18
STAT_ITEMS = 19
STAT_GIFTS = 20
STAT_FISH = 21
STAT_FLOWERS = 22
STAT_RACING = 23
STAT_RACES_WON = 24
STAT_GOLF = 25
STAT_HOLES_IN_ONE = 26
STAT_COURSES_UNDER_PAR = 27
STAT_SOS = 28
STAT_UNITES_EARNT = 29
STAT_UNITES_USED = 30
STAT_SLIPS = 31
STAT_GAGS = 32
STAT_TROLLEY = 33
STAT_FRIENDS = 34
STAT_TV = 35
STAT_RING = 36
LAST_STAT = 36
IGNORED_STATS = [STAT_BEANS_SPENT,
 STAT_SOLO,
 STAT_SAD,
 STAT_UNITES_EARNT,
 STAT_RACING,
 STAT_TV]
MAX_TF_TRIES = 5
TF_COOLDOWN_SECS = 86400
TF_EXPIRE_SECS = 259200
TF_COOLDOWN = 0
TF_UNKNOWN_SECRET = 1
TF_SELF_SECRET = 2
TF_FRIENDS_LIST_FULL_YOU = 3
TF_FRIENDS_LIST_FULL_HIM = 4
TF_ALREADY_FRIENDS = 5
TF_ALREADY_FRIENDS_NAME = 6
TF_SUCCESS = 7
GROUP_ZONES = [11000,
 11100,
 11200,
 12000,
 12100,
 13000,
 13100,
 13200,
 10000,
 10100]
TOONUP_PULSE_ZONES = [ToontownCentral,
 DonaldsDock,
 DaisyGardens,
 MinniesMelodyland,
 TheBrrrgh,
 DonaldsDreamland]
TOONUP_FREQUENCY = 30
TV_NOT_OWNER = 0
TV_INVALID_VIDEO = 1
TV_OK = 2
COLOR_SATURATION_MIN = 0.5
COLOR_SATURATION_MAX = 0.8
COLOR_VALUE_MIN = 0.5
COLOR_VALUE_MAX = 0.8
TELEPORT_BUTTON_DEFAULT_COST = 50
TELEPORT_BUTTON_COSTS = {ToontownCentral: 5,
 DonaldsDock: 15,
 DaisyGardens: 30,
 MinniesMelodyland: 45,
 TheBrrrgh: 60,
 DonaldsDreamland: 75}

def getTeleportButtonCost(hoodId):
    return TELEPORT_BUTTON_COSTS.get(hoodId, TELEPORT_BUTTON_DEFAULT_COST)


BADGES = {0: ['cog', 1],
 1: ['friend', 1],
 2: ['friend', 25],
 3: ['friend', 50],
 4: ['friend', 100],
 5: ['quest', 25],
 6: ['quest', 50],
 7: ['quest', 150],
 8: ['quest', 300],
 9: ['story', 1],
 10: ['cog', 100],
 11: ['cog', 500],
 12: ['cog', 1000],
 13: ['cog', 5000],
 14: ['cog', 10000],
 15: ['cog', 15000],
 16: ['cog', 20000],
 17: ['bldg', 15],
 18: ['bldg', 30],
 19: ['bldg', 45],
 20: ['cogdo', 15],
 21: ['cogdo', 30],
 22: ['cogdo', 45],
 23: ['race', 1],
 24: ['race', 15],
 25: ['race', 30],
 26: ['unite', 10],
 27: ['solo', 1],
 28: ['soloVP', 1],
 29: ['soloCFO', 1],
 30: ['soloCJ', 1],
 31: ['soloCEO', 1],
 32: ['skele', 100],
 33: ['skele', 500],
 34: ['gift', 50],
 35: ['gift', 150],
 36: ['tv', 1],
 37: ['chairman', 1],
 38: ['bldg', 150],
 39: ['ring', 25]}
MAX_BADGE_HISTORY = {}
for badge in BADGES.values():
    badgeType, maxHistory = badge
    if badgeType not in MAX_BADGE_HISTORY or MAX_BADGE_HISTORY[badgeType] < max:
        MAX_BADGE_HISTORY[badgeType] = maxHistory

BADGE_TYPES = ['cog',
 'friend',
 'quest',
 'story',
 'bldg',
 'cogdo',
 'race',
 'unite',
 'solo',
 'soloVP',
 'soloCFO',
 'soloCJ',
 'soloCEO',
 'tv',
 'chairman',
 'skele',
 'gift',
 'ring']
STATISTICS_TO_BADGES = {STAT_COGS: 'cog',
 STAT_TASKS: 'quest',
 STAT_BLDG: 'bldg',
 STAT_COGDO: 'cogdo',
 STAT_RACES_WON: 'race',
 STAT_UNITES_USED: 'unite',
 STAT_SOLO: 'solo',
 STAT_SOLO_VP: 'soloVP',
 STAT_SOLO_CFO: 'soloCFO',
 STAT_SOLO_CJ: 'soloCJ',
 STAT_SOLO_CEO: 'soloCEO',
 STAT_TV: 'tv',
 STAT_SKELE: 'skele',
 STAT_GIFTS: 'gift',
 STAT_RING: 'ring'}
BADGE_COUNT = len(BADGES.keys())
BADGE_COLORS = {'cog': (0.8, 0.8, 0.8, 1),
 'friend': (0.6, 1, 0.5, 1),
 'quest': (1, 0.9, 0.6, 1),
 'story': (1, 0.9, 0.4, 1),
 'bldg': (0.6, 0.6, 0.6, 1),
 'cogdo': (0.76, 0.62, 0.86, 1),
 'race': (0.8, 0.8, 0, 1),
 'unite': (0.37, 0.56, 0.84, 1),
 'solo': (0.5, 0.5, 0.5, 1),
 'soloVP': (0.86, 0.62, 0.86, 1),
 'soloCFO': (0.4, 0.5, 0.3, 1),
 'soloCJ': (0.27, 0.56, 0.84, 1),
 'soloCEO': (0.98, 0.72, 0.52, 1),
 'tv': (0.7, 1, 0.3, 1),
 'chairman': (0.8, 0.8, 0.8, 1),
 'skele': (0.8, 0.8, 0.8, 1),
 'gift': (0.96, 0.51, 0.5, 1),
 'ring': (0.18, 0.55, 1, 1)}
BADGE_PROGRESS_COLORS = [(1, 0, 0, 0.5), (0, 1, 0, 0.5)]
BADGE_POSITIONS = [(-0.66, 0, 0.35),
 (-0.22, 0, 0.35),
 (-0.66, 0, -0.15),
 (-0.22, 0, -0.15)]
BADGE_MAX = 0
for requirement in BADGES.values():
    BADGE_MAX += requirement[1]

SZ_SKY = {ToontownCentral: 'phase_3.5/models/props/TT_sky',
 DonaldsDock: 'phase_3.5/models/props/BR_sky',
 DaisyGardens: 'phase_3.5/models/props/TT_sky',
 MinniesMelodyland: 'phase_6/models/props/MM_sky',
 TheBrrrgh: 'phase_3.5/models/props/BR_sky',
 DonaldsDreamland: 'phase_8/models/props/DL_sky',
 ForestsEnd: 'phase_3.5/models/props/TT_sky',
 CogtownCentral: 'phase_9/models/cogHQ/cog_sky'}
LOGIN_SCREEN_SZ = {ToontownCentral: ((30, 0, 26, -90, -20, 0, 14, 0, 33),
                   ((65.5, 17.5, 4.025, 180, 0, 0),
                    (80, 17.5, 4.025, 180, 0, 0),
                    (98.5, 15, 4.025, 90, 0, 0),
                    (98.5, -15, 4.025, 90, 0, 0),
                    (80, -17.5, 4.025, 0, 0, 0),
                    (65.5, -17.5, 4.025, 0, 0, 0)),
                   1.4,
                   []),
 DonaldsDock: ((-37, -37, 17, -180, -6, 0, -37, -21, 24),
               ((-20, -74, 5.69, 90, 0, 0),
                (-20, -82, 5.69, 90, 0, 0),
                (-28, -86, 5.69, 0, 0, 0),
                (-50, -86, 5.69, 0, 0, 0),
                (-55, -82, 5.69, -90, 0, 0),
                (-55, -74, 5.69, -90, 0, 0)),
               1.47,
               []),
 MinniesMelodyland: ((81, -19, 22, -90, -20, 0, 65, -19, 29),
                     ((138.6, 8.5, 4.63, 90, 0, 0),
                      (138.6, -20.5, 7.45, 90, 0, 0),
                      (138.6, -47.5, 4.63, 90, 0, 0),
                      (118.5, 0, 3.3, 90, 0, 0),
                      (115.5, -19, 0.82, 90, 0, 0),
                      (119, -38.5, 3.3, 90, 0, 0)),
                     1.54,
                     ['**/*hqMM*']),
 TheBrrrgh: ((-28, 23, 23, -70, -10, 0, -44, 23, 30),
             ((0.08, 54, 8.692, 90, 0, 0),
              (4.6, 46.8, 8.692, 90, 0, 0),
              (8.9, 39.3, 8.692, 90, 0, 0),
              (13, 32, 8.692, 90, 0, 0),
              (17.4, 24.4, 8.692, 90, 0, 0),
              (21.5, 17.1, 8.692, 90, 0, 0)),
             1.57,
             []),
 DonaldsDreamland: ((-63, 0, 15, 90, -10, 0, -47, 0, 22),
                    ((-109, -16, 1.62, 270, 0, 0),
                     (-109, -13, 1.62, 270, 0, 0),
                     (-109, -10, 1.89, 270, 0, 0),
                     (-109, 10, 2.12, 270, 0, 0),
                     (-109, 13, 2.1, 270, 0, 0),
                     (-109, 16, 2.07, 270, 0, 0)),
                    1.05,
                    []),
 ForestsEnd: ((-7.5, -35, 15, 0, -10, 0, -7.5, -51, 22),
              ((-23.38, 4.582, 2.468, 270, 0, 0),
               (-23.75, 17.15, 2.517, 270, 0, 0),
               (-17.66, 23.96, 2.594, 180, 0, 0),
               (0.63, 26.25, 2.529, 180, 0, 0),
               (7.62, 18.63, 2.499, 90, 0, 0),
               (6.7, 2.74, 2.496, 90, 0, 0)),
              1.25,
              [])}

def getSafezoneDNA(playground):
    if playground in phaseMap:
        return 'phase_%s/dna/%s_sz.bdna' % (phaseMap[playground], dnaMap[playground])


NPC_EXIT = 0
NPC_TIMER = 1
NPC_DONE = 2
NPC_NO_MONEY = 3
PAINT_INVALID_COLOR = 4
REPAINT_UNAVAILABLE = 0
REPAINT_NOT_OWNER = 1
REPAINT_INVALID_COLOR = 2
REPAINT_SUCCESS = 3
RepaintDialogAspectRatio = 1.7
PaintShopAspectRatio = 1.7
TutorialLaff = 120
SoundImmunityRound = 2
SOSCardRound = 4
HandicapRounds = 5
CogSOSRounds = 1
MaxSuitsBeforeToons = 2
CogupPercentage = 0.5
ToonPowerDownPercentage = 0.8
CogPowerUpPercentage = 1.2
ToonPowerUpPercentage = 1.2
CogPowerDownPercentage = 0.8
MoreXpTime = 604800
MonsterSuit = 0
MonsterGoon = 1
MonsterToon = 2
MonsterTaskTimes = {MonsterSuit: 10,
 MonsterGoon: 10,
 MonsterToon: 25}
TopToonMonthly = 0
TopToonWeekly = 1
TopToonDaily = 2
FlowerMultiplier = 5
SkippableTiers = {4: {'gagTracks': 3,
     'points': 3000,
     'zone': DonaldsDock,
     'money': 1000},
 7: {'gagTracks': 4,
     'points': 5000,
     'zone': DaisyGardens,
     'money': 2000}}