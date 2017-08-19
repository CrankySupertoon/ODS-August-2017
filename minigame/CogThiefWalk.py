# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.minigame.CogThiefWalk
from toontown.safezone import Walk

class CogThiefWalk(Walk.Walk):
    notify = directNotify.newCategory('CogThiefWalk')

    def __init__(self, doneEvent):
        Walk.Walk.__init__(self, doneEvent)

    def enter(self, slowWalk = 0):
        base.localAvatar.startPosHprBroadcast()
        base.localAvatar.startBlink()
        base.localAvatar.showName()
        base.localAvatar.collisionsOn()
        base.localAvatar.enableAvatarControls()

    def exit(self):
        self.fsm.request('off')
        self.ignore(base.getKey('pickup'))
        base.localAvatar.disableAvatarControls()
        base.localAvatar.stopPosHprBroadcast()
        base.localAvatar.stopBlink()
        base.localAvatar.collisionsOff()
        base.localAvatar.controlManager.placeOnFloor()