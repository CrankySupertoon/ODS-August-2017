# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.DDTownLoader
from toontown.town import DDStreet, TownLoader

class DDTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = DDStreet.DDStreet
        self.musicFile = 'phase_6/audio/bgm/DD_SZ.ogg'
        self.activityMusicFile = 'phase_6/audio/bgm/DD_SZ_activity.ogg'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        dnaFile = 'phase_6/dna/donalds_dock_' + str(self.branchZone) + '.bdna'
        self.createHood(dnaFile)