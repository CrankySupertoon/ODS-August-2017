# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.coghq.CogDisguiseGlobals
from toontown.suit import SuitDNA
import types
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
from otp.otpbase import OTPGlobals
PartsPerSuit = (17, 14, 12, 10, 19)
PartsPerSuitBitmasks = (131071, 130175, 56447, 56411, 524287)
AllParts = 17
AllBits = 524287
MinPartLoss = 2
MaxPartLoss = 4
MeritsPerLevel = ((100, 130, 160, 190, 800),
 (160, 210, 260, 310, 1300),
 (260, 340, 420, 500, 2100),
 (420, 550, 680, 810, 3400),
 (680, 890, 1100, 1310, 5500),
 (1100, 1440, 1780, 2120, 8900),
 (1780, 2330, 2880, 3430, 14400),
 (2880, 3770, 4660, 5500, 23300, 2880, 23300, 2880, 3770, 4660, 5500, 23300, 2880, 3770, 4660, 5500, 6440, 7330, 8220, 9110, 10000, 23300, 2880, 3770, 4660, 5500, 6440, 7330, 8220, 9110, 10000, 23300, 2880, 3770, 4660, 5500, 6440, 7330, 8220, 9110, 10000, 23300, 0),
 (60, 80, 100, 120, 500),
 (100, 130, 160, 190, 800),
 (160, 210, 260, 310, 1300),
 (260, 340, 420, 500, 2100),
 (420, 550, 680, 810, 3400),
 (680, 890, 1100, 1310, 5500),
 (1100, 1440, 1780, 2120, 8900),
 (1780, 2330, 2880, 3430, 14400, 1780, 14400, 1780, 2330, 2880, 3430, 14400, 1780, 2330, 2880, 3430, 3980, 4530, 5080, 5630, 6180, 14400, 1780, 2330, 2880, 3430, 3980, 4530, 5080, 5630, 6180, 14400, 1780, 2330, 2880, 3430, 3980, 4530, 5080, 5630, 6180, 14400, 0),
 (40, 50, 60, 70, 300),
 (60, 80, 100, 120, 500),
 (100, 130, 160, 190, 800),
 (160, 210, 260, 310, 1300),
 (260, 340, 420, 500, 2100),
 (420, 550, 680, 810, 3400),
 (680, 890, 1100, 1310, 5500),
 (1100, 1440, 1780, 2120, 8900, 1100, 8900, 1100, 1440, 1780, 2120, 8900, 1100, 1440, 1780, 2120, 2460, 2800, 3140, 3480, 3820, 8900, 1100, 1440, 1780, 2120, 2460, 2800, 3140, 3480, 3820, 8900, 1100, 1440, 1780, 2120, 2460, 2800, 3140, 3480, 3820, 8900, 0),
 (20, 30, 40, 50, 200),
 (40, 50, 60, 70, 300),
 (60, 80, 100, 120, 500),
 (100, 130, 160, 190, 800),
 (160, 210, 260, 310, 1300),
 (260, 340, 420, 500, 2100),
 (420, 550, 680, 810, 3400),
 (680, 890, 1100, 1310, 5500, 680, 5500, 680, 890, 1100, 1310, 5500, 680, 890, 1100, 1310, 1520, 1730, 1940, 2150, 2360, 5500, 680, 890, 1100, 1310, 1520, 1730, 1940, 2150, 2360, 5500, 680, 890, 1100, 1310, 1520, 1730, 1940, 2150, 2360, 5500, 0),
 (20, 30, 40, 50, 200),
 (40, 50, 60, 70, 300),
 (60, 80, 100, 120, 500),
 (100, 130, 160, 190, 800),
 (160, 210, 260, 310, 1300),
 (260, 340, 420, 500, 2100),
 (420, 550, 680, 810, 3400),
 (680, 890, 1100, 1310, 5500, 680, 5500, 680, 890, 1100, 1310, 5500, 680, 890, 1100, 1310, 1520, 1730, 1940, 2150, 2360, 5500, 680, 890, 1100, 1310, 1520, 1730, 1940, 2150, 2360, 5500, 680, 890, 1100, 1310, 1520, 1730, 1940, 2150, 2360, 5500, 0))
leftLegUpper = 1
leftLegLower = 2
leftLegFoot = 4
rightLegUpper = 8
rightLegLower = 16
rightLegFoot = 32
torsoLeftShoulder = 64
torsoRightShoulder = 128
torsoChest = 256
torsoHealthMeter = 512
torsoPelvis = 1024
leftArmUpper = 2048
leftArmLower = 4096
leftArmHand = 8192
rightArmUpper = 16384
rightArmLower = 32768
rightArmHand = 65536
headSkull = 131072
headBrain = 262144
upperTorso = torsoLeftShoulder
leftLegIndex = 0
rightLegIndex = 1
torsoIndex = 2
leftArmIndex = 3
rightArmIndex = 4
headIndex = 5
PartsQueryMasks = (leftLegFoot + leftLegLower + leftLegUpper,
 rightLegFoot + rightLegLower + rightLegUpper,
 torsoPelvis + torsoHealthMeter + torsoChest + torsoRightShoulder + torsoLeftShoulder,
 leftArmHand + leftArmLower + leftArmUpper,
 rightArmHand + rightArmLower + rightArmUpper,
 headSkull + headBrain)
PartsQueryNames = {}
for i in xrange(AllParts):
    PartsQueryNames[2 ** i] = TTLocalizer.CogPartNames[i]

suitTypes = PythonUtil.Enum(('NoSuit', 'NoMerits', 'FullSuit'))

def getNextPart(parts, partIndex, dept):
    dept = dept2deptIndex(dept)
    needMask = PartsPerSuitBitmasks[dept] & PartsQueryMasks[partIndex]
    haveMask = parts[dept] & PartsQueryMasks[partIndex]
    nextPart = ~needMask | haveMask
    nextPart = nextPart ^ nextPart + 1
    nextPart = nextPart + 1 >> 1
    return nextPart


def getPartName(partArray):
    for part in partArray:
        if part:
            return PartsQueryNames[part]


def isPartComplete(parts, partIndex, dept):
    return not getNextPart(parts, partIndex, dept)


def isSuitComplete(parts, dept):
    dept = dept2deptIndex(dept)
    return parts[dept] == PartsPerSuitBitmasks[dept]


def getTotalMerits(toon, index):
    from toontown.battle import SuitBattleGlobals
    cogIndex = toon.cogTypes[index] + SuitDNA.suitsPerDept * index
    cogTypeStr = SuitDNA.suitHeadTypes[cogIndex]
    cogBaseLevel = SuitBattleGlobals.SuitAttributes[cogTypeStr]['level']
    cogLevel = toon.cogLevels[index] - cogBaseLevel
    cogLevel = max(min(cogLevel, len(MeritsPerLevel[cogIndex]) - 1), 0)
    return MeritsPerLevel[cogIndex][cogLevel]


def getTotalParts(bitString, shiftWidth = 32):
    sum = 0
    for shift in xrange(0, shiftWidth):
        sum += bitString >> shift & 1

    return sum


def dept2deptIndex(dept):
    if type(dept) == types.StringType:
        dept = SuitDNA.suitDepts.index(dept)
    return dept