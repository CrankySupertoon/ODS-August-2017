# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.minigame.MinigameGlobals
from direct.showbase import PythonUtil
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil
from random import choice
latencyTolerance = 10.0
MaxLoadTime = 40.0
rulesDuration = 21
JellybeanTrolleyHolidayScoreMultiplier = 2
DifficultyOverrideMult = int(65536)

def QuantizeDifficultyOverride(diffOverride):
    return int(round(diffOverride * DifficultyOverrideMult)) / float(DifficultyOverrideMult)


NoDifficultyOverride = 2147483647
NoTrolleyZoneOverride = -1
SafeZones = [ToontownGlobals.ToontownCentral,
 ToontownGlobals.DonaldsDock,
 ToontownGlobals.DaisyGardens,
 ToontownGlobals.MinniesMelodyland,
 ToontownGlobals.TheBrrrgh,
 ToontownGlobals.DonaldsDreamland,
 ToontownGlobals.ForestsEnd]

def getDifficulty(trolleyZone):
    hoodZone = getSafezoneId(trolleyZone)
    return float(SafeZones.index(hoodZone)) / (len(SafeZones) - 1)


def getSafezoneId(trolleyZone):
    return ZoneUtil.getHoodId(trolleyZone)


def getScoreMult(trolleyZone):
    szId = getSafezoneId(trolleyZone)
    multiplier = PythonUtil.lerp(1.0, 1.5, float(SafeZones.index(szId)) / (len(SafeZones) - 1))
    return multiplier