# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.DLTownLoader
from toontown.town import DLStreet, TownLoader

class DLTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = DLStreet.DLStreet
        self.musicFile = 'phase_8/audio/bgm/DL_SZ.ogg'
        self.activityMusicFile = 'phase_8/audio/bgm/DL_SZ_activity.ogg'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        dnaFile = 'phase_8/dna/donalds_dreamland_' + str(self.branchZone) + '.bdna'
        self.createHood(dnaFile)