# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.makeatoon.BodyShop
from direct.fsm import StateData
from toontown.toontowngui.IntuitiveBodyPicker import IntuitiveBodyPicker

class BodyShop(StateData.StateData):

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.toon = None
        self.frame = None
        return

    def enter(self, toon):
        self.toon = toon
        self.bodyPicker.setToon(self.toon)
        self.frame.show()
        self.acceptOnce('last', lambda : self.__handleDoneStatus('last'))
        self.acceptOnce('next', lambda : self.__handleDoneStatus('next'))

    def exit(self):
        self.ignoreAll()
        self.toon = None
        self.frame.hide()
        return

    def load(self):
        if self.frame:
            return
        self.frame = base.a2dBottomRight.attachNewNode('bodyShop')
        self.frame.hide()
        self.bodyPicker = IntuitiveBodyPicker(self.frame, (-0.93, 0, 1.6))

    def unload(self):
        if not self.frame:
            return
        else:
            self.frame.removeNode()
            self.bodyPicker.removeNode()
            self.frame = None
            self.bodyPicker = None
            return

    def __handleDoneStatus(self, doneStatus):
        self.doneStatus = doneStatus
        messenger.send(self.doneEvent)