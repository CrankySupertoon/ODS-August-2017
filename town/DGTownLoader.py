# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.DGTownLoader
from toontown.town import DGStreet, TownLoader

class DGTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = DGStreet.DGStreet
        self.musicFile = 'phase_8/audio/bgm/DG_SZ.ogg'
        self.activityMusicFile = 'phase_8/audio/bgm/DG_SZ_activity.ogg'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        dnaFile = 'phase_8/dna/daisys_garden_' + str(self.branchZone) + '.bdna'
        self.createHood(dnaFile)