# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.suit.DistributedServerRoomSuit
from toontown.suit import DistributedFactorySuit
from direct.directnotify import DirectNotifyGlobal

class DistributedServerRoomSuit(DistributedFactorySuit.DistributedFactorySuit):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedServerRoomSuit')