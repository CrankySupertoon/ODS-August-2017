# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.MMTownLoader
from toontown.town import MMStreet, TownLoader

class MMTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = MMStreet.MMStreet
        self.musicFile = 'phase_6/audio/bgm/MM_SZ.ogg'
        self.activityMusicFile = 'phase_6/audio/bgm/MM_SZ_activity.ogg'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        dnaFile = 'phase_6/dna/minnies_melody_land_' + str(self.branchZone) + '.bdna'
        self.createHood(dnaFile)

    def unload(self):
        TownLoader.TownLoader.unload(self)