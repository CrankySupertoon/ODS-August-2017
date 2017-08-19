# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.distributed.ToontownDistrict
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from otp.distributed import DistributedDistrict

class ToontownDistrict(DistributedDistrict.DistributedDistrict):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownDistrict')

    def __init__(self, cr):
        DistributedDistrict.DistributedDistrict.__init__(self, cr)
        self.avatarCount = 0
        self.invasionStatus = 0
        self.suitStatus = ''
        self.groupAvCount = []
        self.easterEgg = False

    def hasEasterEgg(self):
        return self.easterEgg