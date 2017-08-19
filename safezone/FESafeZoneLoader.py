# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.safezone.FESafeZoneLoader
from toontown.safezone import SafeZoneLoader, FEPlayground

class FESafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = FEPlayground.FEPlayground
        self.musicFile = 'phase_8/audio/bgm/FE_SZ.ogg'
        self.activityMusicFile = 'phase_6/audio/bgm/DD_SZ_activity.ogg'
        self.dnaFile = 'phase_8/dna/forests_end_sz.bdna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)