# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.hood.DLHood
from panda3d.core import Lens
from toontown.safezone.DLSafeZoneLoader import DLSafeZoneLoader
from toontown.town.DLTownLoader import DLTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood

class DLHood(ToonHood):
    notify = directNotify.newCategory('DLHood')
    ID = ToontownGlobals.DonaldsDreamland
    TOWNLOADER_CLASS = DLTownLoader
    SAFEZONELOADER_CLASS = DLSafeZoneLoader
    SKY_FILE = 'phase_8/models/props/DL_sky'
    TITLE_COLOR = (1.0, 0.9, 0.5, 1.0)

    def enter(self, requestStatus):
        ToonHood.enter(self, requestStatus)
        base.camLens.setNearFar(ToontownGlobals.DDLCameraNear, ToontownGlobals.DDLCameraFar)

    def exit(self):
        ToonHood.exit(self)
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)