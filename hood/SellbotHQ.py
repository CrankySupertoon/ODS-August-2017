# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.hood.SellbotHQ
from panda3d.core import Lens
from toontown.coghq.SellbotCogHQLoader import SellbotCogHQLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.CogHood import CogHood

class SellbotHQ(CogHood):
    notify = directNotify.newCategory('SellbotHQ')
    ID = ToontownGlobals.SellbotHQ
    LOADER_CLASS = SellbotCogHQLoader

    def load(self):
        CogHood.load(self)
        self.sky.setScale(3.0)

    def enter(self, requestStatus):
        CogHood.enter(self, requestStatus)
        base.localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.CogHQCameraNear, ToontownGlobals.CogHQCameraFar)