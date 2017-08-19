# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.safezone.DDSafeZoneLoader
from toontown.safezone import SafeZoneLoader, DDPlayground

class DDSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = DDPlayground.DDPlayground
        self.musicFile = 'phase_6/audio/bgm/DD_nbrhood.ogg'
        self.activityMusicFile = 'phase_6/audio/bgm/DD_SZ_activity.ogg'
        self.dnaFile = 'phase_6/dna/donalds_dock_sz.bdna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.seagullSound = loader.loadSfx('phase_6/audio/sfx/SZ_DD_Seagull.ogg')
        self.underwaterSound = loader.loadSfx('phase_4/audio/sfx/AV_ambient_water.ogg')
        self.swimSound = loader.loadSfx('phase_4/audio/sfx/AV_swim_single_stroke.ogg')
        self.submergeSound = loader.loadSfx('phase_5.5/audio/sfx/AV_jump_in_water.ogg')
        self.boat = self.geom.find('**/donalds_boat')
        self.dockSound = loader.loadSfx('phase_6/audio/sfx/SZ_DD_dockcreak.ogg')
        self.foghornSound = loader.loadSfx('phase_5/audio/sfx/SZ_DD_foghorn.ogg')
        self.bellSound = loader.loadSfx('phase_6/audio/sfx/SZ_DD_shipbell.ogg')
        self.waterSound = loader.loadSfx('phase_6/audio/sfx/SZ_DD_waterlap.ogg')
        wheel = self.boat.find('**/wheel')
        if not wheel.isEmpty():
            wheel.hide()
        water = self.geom.find('**/water')
        water.setColorScale(1, 1, 1, 0.7)
        water.setTransparency(1)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)
        del self.seagullSound
        del self.underwaterSound
        del self.swimSound
        del self.dockSound
        del self.foghornSound
        del self.bellSound
        del self.waterSound
        del self.submergeSound
        del self.boat