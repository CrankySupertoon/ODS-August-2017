# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.DistributedBuildingQueryMgr
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed import DistributedObject

class DistributedBuildingQueryMgr(DistributedObject.DistributedObject):
    notify = directNotify.newCategory('DistributedBuildingQueryMgr')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.__callbacks = {}
        self.__context = 0
        self.cr = cr

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        DistributedObject.DistributedObject.announceGenerate(self)
        self.cr.buildingQueryMgr = self

    def delete(self):
        self.notify.debug('delete')
        DistributedObject.DistributedObject.delete(self)
        self.cr.buildingQueryMgr = None
        return

    def d_isSuit(self, zoneIds, callback):
        self.__context = (self.__context + 1) % 255
        self.__callbacks[self.__context] = callback
        self.sendUpdate('isSuit', [self.__context, zoneIds])

    def response(self, context, response):
        self.__callbacks.pop(context, lambda x: 0)(response)