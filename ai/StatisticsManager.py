# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.ai.StatisticsManager
from direct.distributed.DistributedObject import DistributedObject

class StatisticsManager(DistributedObject):
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        cr.statisticsManager = self

    def delete(self):
        self.cr.statisticsManager = None
        DistributedObject.delete(self)
        return

    def d_requestToons(self, period, category):
        self.sendUpdate('requestToons', [period, category])

    def gotToons(self, topToons):
        messenger.send('gotTopToons', [topToons])