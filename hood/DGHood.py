# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.hood.DGHood
from toontown.safezone.DGSafeZoneLoader import DGSafeZoneLoader
from toontown.town.DGTownLoader import DGTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood

class DGHood(ToonHood):
    notify = directNotify.newCategory('DGHood')
    ID = ToontownGlobals.DaisyGardens
    TOWNLOADER_CLASS = DGTownLoader
    SAFEZONELOADER_CLASS = DGSafeZoneLoader
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (0.8, 0.6, 1.0, 1.0)