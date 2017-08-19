# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.Street
from toontown.battle.BattleProps import *
from toontown.battle.BattleSounds import *
from toontown.distributed.ToontownMsgTypes import *
from direct.gui.DirectGui import cleanupDialog
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from toontown.battle import BattlePlace
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.task import Task
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs
from toontown.battle import BattleParticles
from toontown.building import Elevator
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.estate import HouseGlobals
from toontown.toonbase import TTLocalizer
from direct.interval.IntervalGlobal import *
from otp.nametag import NametagGlobals

class Street(BattlePlace.BattlePlace):
    notify = DirectNotifyGlobal.directNotify.newCategory('Street')

    def __init__(self, loader, parentFSM, doneEvent):
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.fsm = ClassicFSM.ClassicFSM('Street', [State.State('start', self.enterStart, self.exitStart, ['walk',
          'tunnelIn',
          'doorIn',
          'teleportIn',
          'elevatorIn']),
         State.State('walk', self.enterWalk, self.exitWalk, ['push',
          'sit',
          'stickerBook',
          'WaitForBattle',
          'battle',
          'doorOut',
          'elevator',
          'tunnelIn',
          'tunnelOut',
          'teleportOut',
          'quest',
          'stopped',
          'fishing',
          'died']),
         State.State('sit', self.enterSit, self.exitSit, ['walk']),
         State.State('push', self.enterPush, self.exitPush, ['walk']),
         State.State('stickerBook', self.enterStickerBook, self.exitStickerBook, ['walk',
          'push',
          'sit',
          'battle',
          'doorOut',
          'elevator',
          'tunnelIn',
          'tunnelOut',
          'WaitForBattle',
          'teleportOut',
          'quest',
          'stopped',
          'fishing']),
         State.State('WaitForBattle', self.enterWaitForBattle, self.exitWaitForBattle, ['battle', 'walk']),
         State.State('battle', self.enterBattle, self.exitBattle, ['walk', 'teleportOut', 'died']),
         State.State('doorIn', self.enterDoorIn, self.exitDoorIn, ['walk', 'stopped']),
         State.State('doorOut', self.enterDoorOut, self.exitDoorOut, ['walk', 'stopped']),
         State.State('elevatorIn', self.enterElevatorIn, self.exitElevatorIn, ['walk']),
         State.State('elevator', self.enterElevator, self.exitElevator, ['walk']),
         State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, ['walk',
          'teleportOut',
          'quietZone',
          'WaitForBattle',
          'battle']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, ['teleportIn', 'quietZone', 'WaitForBattle']),
         State.State('died', self.enterDied, self.exitDied, ['quietZone']),
         State.State('tunnelIn', self.enterTunnelIn, self.exitTunnelIn, ['walk']),
         State.State('tunnelOut', self.enterTunnelOut, self.exitTunnelOut, ['final']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['teleportIn']),
         State.State('quest', self.enterQuest, self.exitQuest, ['walk', 'stopped']),
         State.State('stopped', self.enterStopped, self.exitStopped, ['walk', 'teleportOut']),
         State.State('fishing', self.enterFishing, self.exitFishing, ['walk']),
         State.State('final', self.enterFinal, self.exitFinal, ['start', 'doorOut', 'teleportOut'])], 'start', 'final')
        self.parentFSM = parentFSM
        self.elevatorDoneEvent = 'elevatorDone'

    def enter(self, requestStatus):
        self._ttfToken = None
        self.fsm.enterInitialState()
        base.playMusic(self.loader.music, looping=1, volume=0.8)
        self.loader.geom.reparentTo(render)
        self.loader.geom.unstash()
        self.accept('on-floor', self.enterZone)
        base.localAvatar.setGeom(self.loader.geom)
        base.localAvatar.setOnLevelGround(1)
        self._telemLimiter = TLGatherAllAvs('Street', RotationLimitToH)
        NametagGlobals.setMasterArrowsOn(1)
        if base.cr.newsManager.isHolidayRunning(ToontownGlobals.HALLOWEEN) and self.loader.hood.spookySkyFile:
            self.loader.geom.setColorScale(0.55, 0.55, 0.65, 1)
            self.loader.hood.startSpookySky()
        else:
            self.loader.geom.setColorScale(1, 1, 1, 1)
            self.loader.hood.startSky()
        self.accept('doorDoneEvent', self.handleDoorDoneEvent)
        self.accept('DistributedDoor_doorTrigger', self.handleDoorTrigger)
        self.enterZone(requestStatus['zoneId'])
        self.fsm.request(requestStatus['how'], [requestStatus])
        return

    def exit(self):
        self.ignore('on-floor')
        self.loader.geom.stash()
        self._telemLimiter.destroy()
        del self._telemLimiter
        NametagGlobals.setMasterArrowsOn(0)
        self.loader.hood.stopSky()
        self.loader.music.stop()
        base.localAvatar.setGeom(render)
        base.localAvatar.setOnLevelGround(0)

    def load(self):
        BattlePlace.BattlePlace.load(self)
        self.parentFSM.getStateNamed('street').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('street').removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.enterZone(None)
        cleanupDialog('globalDialog')
        self.ignoreAll()
        BattlePlace.BattlePlace.unload(self)
        return

    def enterElevatorIn(self, requestStatus):
        self._eiwbTask = taskMgr.add(Functor(self._elevInWaitBldgTask, requestStatus['bldgDoId']), uniqueName('elevInWaitBldg'))

    def _elevInWaitBldgTask(self, bldgDoId, task):
        bldg = base.cr.doId2do.get(bldgDoId)
        if bldg:
            if bldg.elevatorNodePath is not None:
                if self._enterElevatorGotElevator():
                    return Task.done
        return Task.cont

    def _enterElevatorGotElevator(self):
        if not messenger.whoAccepts('insideVictorElevator'):
            return False
        messenger.send('insideVictorElevator')
        return True

    def exitElevatorIn(self):
        taskMgr.remove(self._eiwbTask)

    def enterElevator(self, distElevator):
        base.localAvatar.cantLeaveGame = 1
        self.accept(self.elevatorDoneEvent, self.handleElevatorDone)
        self.elevator = Elevator.Elevator(self.fsm.getStateNamed('elevator'), self.elevatorDoneEvent, distElevator)
        self.elevator.load()
        self.elevator.enter()

    def exitElevator(self):
        base.localAvatar.cantLeaveGame = 0
        self.ignore(self.elevatorDoneEvent)
        self.elevator.unload()
        self.elevator.exit()
        del self.elevator

    def detectedElevatorCollision(self, distElevator):
        self.fsm.request('elevator', [distElevator])
        return None

    def handleElevatorDone(self, doneStatus):
        self.notify.debug('handling elevator done event')
        where = doneStatus['where']
        if where == 'reject':
            if hasattr(base.localAvatar, 'elevatorNotifier') and base.localAvatar.elevatorNotifier.isNotifierOpen():
                pass
            else:
                self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where in ('suitInterior', 'cogdoInterior'):
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + where + ' in handleElevatorDone')

    def enterTunnelIn(self, requestStatus):
        self.enterZone(requestStatus['zoneId'])
        BattlePlace.BattlePlace.enterTunnelIn(self, requestStatus)

    def enterTeleportIn(self, requestStatus):
        zoneId = requestStatus['zoneId']
        self._ttfToken = self.addSetZoneCompleteCallback(Functor(self._teleportToFriend, requestStatus))
        self.enterZone(zoneId)
        BattlePlace.BattlePlace.enterTeleportIn(self, requestStatus)

    def enterDoorIn(self, requestStatus):
        self.enterZone(requestStatus['zoneId'])
        BattlePlace.BattlePlace.enterDoorIn(self, requestStatus)

    def _teleportToFriend(self, requestStatus):
        avId = requestStatus['avId']
        hoodId = requestStatus['hoodId']
        zoneId = requestStatus['zoneId']
        if avId != -1:
            if avId not in base.cr.doId2do:
                friend = base.cr.identifyAvatar(avId)
                if friend == None:
                    handle = base.cr.identifyFriend(avId)
                    requestStatus = {'how': 'teleportIn',
                     'hoodId': hoodId,
                     'zoneId': hoodId,
                     'shardId': None,
                     'loader': 'safeZoneLoader',
                     'where': 'playground',
                     'avId': avId}
                    self.fsm.request('final')
                    self.__teleportOutDone(requestStatus)
        return

    def exitTeleportIn(self):
        self.removeSetZoneCompleteCallback(self._ttfToken)
        self._ttfToken = None
        BattlePlace.BattlePlace.exitTeleportIn(self)
        return

    def enterTeleportOut(self, requestStatus):
        BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        hoodId = requestStatus['hoodId']
        zoneId = requestStatus['zoneId']
        shardId = requestStatus['shardId']
        if hoodId == self.loader.hood.id and shardId == None:
            if zoneId == self.zoneId:
                self.fsm.request('teleportIn', [requestStatus])
            elif requestStatus['where'] == 'street' and ZoneUtil.getBranchZone(zoneId) == self.loader.branchZone:
                self.fsm.request('quietZone', [requestStatus])
            else:
                self.doneStatus = requestStatus
                messenger.send(self.doneEvent)
        elif hoodId == ToontownGlobals.MyEstate:
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)
        return

    def exitTeleportOut(self):
        BattlePlace.BattlePlace.exitTeleportOut(self)

    def goHomeFailed(self, task):
        self.notifyUserGoHomeFailed()
        self.ignore('setLocalEstateZone')
        self.doneStatus['avId'] = -1
        self.doneStatus['zoneId'] = self.getZoneId()
        self.fsm.request('teleportIn', [self.doneStatus])
        return Task.done

    def doEnterZone(self, newZoneId):
        if newZoneId == self.zoneId:
            return
        else:
            if newZoneId is None:
                visList = []
            elif newZoneId in self.loader.zoneVisDict:
                visList = self.loader.zoneVisDict[newZoneId]
            else:
                visList = self.loader.zoneVisDict.values()[0]
            for zoneId, node in self.loader.zoneDict.iteritems():
                if zoneId not in visList:
                    self.loader.hideVisGroup(zoneId)

            for zoneId in visList:
                self.loader.showVisGroup(zoneId)

            if newZoneId is not None:
                base.cr.sendSetZoneMsg(newZoneId, visList)
            self.zoneId = newZoneId
            return