# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.hood.DDHood
from panda3d.core import Fog
from toontown.safezone.DDSafeZoneLoader import DDSafeZoneLoader
from toontown.town.DDTownLoader import DDTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood

class DDHood(ToonHood):
    notify = directNotify.newCategory('DDHood')
    ID = ToontownGlobals.DonaldsDock
    TOWNLOADER_CLASS = DDTownLoader
    SAFEZONELOADER_CLASS = DDSafeZoneLoader
    SKY_FILE = 'phase_3.5/models/props/BR_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (0.8, 0.6, 0.5, 1.0)

    def load(self):
        ToonHood.load(self)
        self.fog = Fog('DDFog')