# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.hood.FEHood
from otp.ai.MagicWordGlobal import *
from toontown.safezone.FESafeZoneLoader import FESafeZoneLoader
from toontown.town.FETownLoader import FETownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood

class FEHood(ToonHood):
    notify = directNotify.newCategory('FEHood')
    ID = ToontownGlobals.ForestsEnd
    TOWNLOADER_CLASS = FETownLoader
    SAFEZONELOADER_CLASS = FESafeZoneLoader
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (1.0, 0.5, 0.4, 1.0)