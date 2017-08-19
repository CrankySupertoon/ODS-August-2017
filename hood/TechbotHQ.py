# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.hood.TechbotHQ
from panda3d.core import Lens
from toontown.coghq.TechbotHQLoader import TechbotHQLoader
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.hood.CogHood import CogHood
from toontown.hood import ZoneUtil

class TechbotHQ(CogHood):
    notify = directNotify.newCategory('TechbotHQ')
    ID = ToontownGlobals.TechbotHQ
    LOADER_CLASS = TechbotHQLoader

    def load(self):
        CogHood.load(self)
        self.sky.hide()

    def enter(self, requestStatus):
        CogHood.enter(self, requestStatus)
        base.localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.TechbotHQCameraNear, ToontownGlobals.TechbotHQCameraFar)

    def spawnTitleText(self, zoneId, floorNum = None):
        if ZoneUtil.isServerRoomInteriorZone(zoneId):
            text = '%s\n%s' % (ToontownGlobals.StreetNames[zoneId][-1], TTLocalizer.ServerRoomFloorTitle % (floorNum + 1))
            self.doSpawnTitleText(text)
            return
        CogHood.spawnTitleText(self, zoneId)