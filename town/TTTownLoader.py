# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.TTTownLoader
from toontown.town import TTStreet, TownLoader

class TTTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = TTStreet.TTStreet
        self.musicFile = 'phase_3.5/audio/bgm/TC_SZ.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        dnaFile = 'phase_5/dna/toontown_central_' + str(self.branchZone) + '.bdna'
        self.createHood(dnaFile)