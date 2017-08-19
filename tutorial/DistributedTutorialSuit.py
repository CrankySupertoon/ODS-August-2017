# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.DistributedTutorialSuit
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from toontown.distributed.DelayDeletable import DelayDeletable
from toontown.suit.DistributedSuitBase import DistributedSuitBase

class DistributedTutorialSuit(DistributedSuitBase, DelayDeletable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTutorialSuit')

    def __init__(self, cr):
        DistributedSuitBase.__init__(self, cr)
        self.fsm = ClassicFSM.ClassicFSM('DistributedTutorialSuit', [State.State('Off', self.enterOff, self.exitOff, ['WaitForBattle', 'Battle']), State.State('Battle', self.enterBattle, self.exitBattle, []), State.State('WaitForBattle', self.enterWaitForBattle, self.exitWaitForBattle, ['Battle'])], 'Off', 'Off')
        self.fsm.enterInitialState()
        self.deleted = False

    def announceGenerate(self):
        DistributedSuitBase.announceGenerate(self)
        self.setState('WaitForBattle')
        holly = self.cr.playGame.place.tutorial.getHollywood()
        self.setPosHpr(holly.getPos(), holly.getHpr())
        holly.delete()

    def disable(self):
        self.setState('Off')
        DistributedSuitBase.disable(self)

    def delete(self):
        if self.deleted:
            return
        del self.fsm
        DistributedSuitBase.delete(self)
        self.deleted = True