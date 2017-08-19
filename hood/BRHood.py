# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.hood.BRHood
from toontown.safezone.BRSafeZoneLoader import BRSafeZoneLoader
from toontown.town.BRTownLoader import BRTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood

class BRHood(ToonHood):
    notify = directNotify.newCategory('BRHood')
    ID = ToontownGlobals.TheBrrrgh
    TOWNLOADER_CLASS = BRTownLoader
    SAFEZONELOADER_CLASS = BRSafeZoneLoader
    SKY_FILE = 'phase_3.5/models/props/BR_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (0.3, 0.6, 1.0, 1.0)