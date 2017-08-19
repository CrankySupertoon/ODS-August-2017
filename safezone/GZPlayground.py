# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.safezone.GZPlayground
from direct.fsm import State
from toontown.safezone import GolfKart
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toontowngui import TTDialog
import Playground
import sys

class GZPlayground(Playground.Playground):

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.parentFSM = parentFSM
        self.golfKartBlockDoneEvent = 'golfKartBlockDone'
        self.fsm.addState(State.State('golfKartBlock', self.enterGolfKartBlock, self.exitGolfKartBlock, ['walk']))
        state = self.fsm.getStateNamed('walk')
        state.addTransition('golfKartBlock')
        self.golfKartDoneEvent = 'golfKartDone'
        self.trolley = None
        self.warningDialog = None
        return

    def destroyWarningDialog(self):
        if self.warningDialog:
            self.warningDialog.destroy()
            self.warningDialog = None
        return

    def warningDone(self, *args):
        self.destroyWarningDialog()
        self.fsm.request('walk')

    def enterGolfKartBlock(self, golfKart):
        if sys.platform == 'android':
            base.localAvatar.b_setAnimState('neutral', 1)
            self.destroyWarningDialog()
            self.warningDialog = TTDialog.TTDialog(text=TTLocalizer.AndroidGolfMessage, command=self.warningDone, style=TTDialog.Acknowledge)
            self.warningDialog.show()
            return
        base.localAvatar.laffMeter.start()
        base.localAvatar.b_setAnimState('off', 1)
        self.accept(self.golfKartDoneEvent, self.handleGolfKartDone)
        self.trolley = GolfKart.GolfKart(self, self.fsm, self.golfKartDoneEvent, golfKart.getDoId())
        self.trolley.load()
        self.trolley.enter()

    def exitGolfKartBlock(self):
        base.localAvatar.laffMeter.stop()
        self.destroyWarningDialog()
        self.ignore(self.golfKartDoneEvent)
        if self.trolley:
            self.trolley.unload()
            self.trolley.exit()
            self.trolley = None
        return

    def detectedGolfKartCollision(self, golfKart):
        self.notify.debug('detectedGolfkartCollision()')
        self.fsm.request('golfKartBlock', [golfKart])

    def handleGolfKartDone(self, doneStatus):
        self.notify.debug('handling golf kart  done event')
        mode = doneStatus['mode']
        if mode == 'reject':
            self.fsm.request('walk')
        elif mode == 'exit':
            self.fsm.request('walk')
        elif mode == 'golfcourse':
            self.doneStatus = {'loader': 'golfcourse',
             'where': 'golfcourse',
             'hoodId': self.loader.hood.id,
             'zoneId': doneStatus['zoneId'],
             'shardId': None,
             'courseId': doneStatus['courseId']}
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + mode + ' in handleGolfKartDone')
        return