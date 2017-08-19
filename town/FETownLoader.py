# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.FETownLoader
from toontown.town import FEStreet, TownLoader

class FETownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = FEStreet.FEStreet
        self.musicFile = 'phase_6/audio/bgm/DD_SZ.ogg'
        self.activityMusicFile = 'phase_6/audio/bgm/DD_SZ_activity.ogg'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        dnaFile = 'phase_8/dna/forests_end_' + str(self.branchZone) + '.bdna'
        self.createHood(dnaFile)