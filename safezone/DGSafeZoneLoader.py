# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.safezone.DGSafeZoneLoader
from toontown.safezone import DGPlayground
from toontown.safezone import SafeZoneLoader

class DGSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = DGPlayground.DGPlayground
        self.musicFile = 'phase_8/audio/bgm/DG_nbrhood.ogg'
        self.activityMusicFile = 'phase_8/audio/bgm/DG_SZ_activity.ogg'
        self.dnaFile = 'phase_8/dna/daisys_garden_sz.bdna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.birdSound = map(loader.loadSfx, ['phase_8/audio/sfx/SZ_DG_bird_01.ogg',
         'phase_8/audio/sfx/SZ_DG_bird_02.ogg',
         'phase_8/audio/sfx/SZ_DG_bird_03.ogg',
         'phase_8/audio/sfx/SZ_DG_bird_04.ogg'])

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)
        del self.birdSound