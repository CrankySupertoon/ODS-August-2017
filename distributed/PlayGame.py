# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.distributed.PlayGame
from toontown.toonbase.ToonBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task.Task import Task
from ToontownMsgTypes import *
from toontown.toonbase import ToontownGlobals
from toontown.hood import TTHood
from toontown.hood import DDHood
from toontown.hood import MMHood
from toontown.hood import BRHood
from toontown.hood import DGHood
from toontown.hood import DLHood
from toontown.hood import GSHood
from toontown.hood import OZHood
from toontown.hood import GZHood
from toontown.hood import FEHood
from toontown.hood import SellbotHQ, CashbotHQ, LawbotHQ, BossbotHQ, TechbotHQ
from toontown.cogtown import CTCHood
from direct.task import TaskManagerGlobal
from toontown.hood import QuietZoneState
from toontown.hood import ZoneUtil
from toontown.hood import EstateHood
from toontown.hood import PartyHood
from toontown.toonbase import TTLocalizer
from toontown.parties.PartyGlobals import GoToPartyStatus
from toontown.dna.DNAParser import *

class PlayGame(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayGame')
    Hood2ClassDict = {ToontownGlobals.ToontownCentral: TTHood.TTHood,
     ToontownGlobals.DonaldsDock: DDHood.DDHood,
     ToontownGlobals.TheBrrrgh: BRHood.BRHood,
     ToontownGlobals.MinniesMelodyland: MMHood.MMHood,
     ToontownGlobals.DaisyGardens: DGHood.DGHood,
     ToontownGlobals.DonaldsDreamland: DLHood.DLHood,
     ToontownGlobals.GoofySpeedway: GSHood.GSHood,
     ToontownGlobals.OutdoorZone: OZHood.OZHood,
     ToontownGlobals.CogtownCentral: CTCHood.CTCHood,
     ToontownGlobals.MyEstate: EstateHood.EstateHood,
     ToontownGlobals.BossbotHQ: BossbotHQ.BossbotHQ,
     ToontownGlobals.SellbotHQ: SellbotHQ.SellbotHQ,
     ToontownGlobals.CashbotHQ: CashbotHQ.CashbotHQ,
     ToontownGlobals.LawbotHQ: LawbotHQ.LawbotHQ,
     ToontownGlobals.TechbotHQ: TechbotHQ.TechbotHQ,
     ToontownGlobals.GolfZone: GZHood.GZHood,
     ToontownGlobals.PartyHood: PartyHood.PartyHood,
     ToontownGlobals.ForestsEnd: FEHood.FEHood}
    Hood2StateDict = {ToontownGlobals.ToontownCentral: 'TTHood',
     ToontownGlobals.DonaldsDock: 'DDHood',
     ToontownGlobals.TheBrrrgh: 'BRHood',
     ToontownGlobals.MinniesMelodyland: 'MMHood',
     ToontownGlobals.DaisyGardens: 'DGHood',
     ToontownGlobals.DonaldsDreamland: 'DLHood',
     ToontownGlobals.GoofySpeedway: 'GSHood',
     ToontownGlobals.OutdoorZone: 'OZHood',
     ToontownGlobals.CogtownCentral: 'CTCHood',
     ToontownGlobals.MyEstate: 'EstateHood',
     ToontownGlobals.BossbotHQ: 'BossbotHQ',
     ToontownGlobals.SellbotHQ: 'SellbotHQ',
     ToontownGlobals.CashbotHQ: 'CashbotHQ',
     ToontownGlobals.LawbotHQ: 'LawbotHQ',
     ToontownGlobals.TechbotHQ: 'TechbotHQ',
     ToontownGlobals.GolfZone: 'GZHood',
     ToontownGlobals.PartyHood: 'PartyHood',
     ToontownGlobals.ForestsEnd: 'FEHood'}

    def __init__(self, parentFSM, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.place = None
        self.fsm = ClassicFSM.ClassicFSM('PlayGame', [State.State('start', self.enterStart, self.exitStart, ['quietZone']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['TTHood',
          'DDHood',
          'BRHood',
          'MMHood',
          'DGHood',
          'DLHood',
          'GSHood',
          'OZHood',
          'GZHood',
          'FEHood',
          'SellbotHQ',
          'CashbotHQ',
          'LawbotHQ',
          'BossbotHQ',
          'TechbotHQ',
          'CTCHood',
          'EstateHood',
          'PartyHood']),
         State.State('TTHood', self.enterTTHood, self.exitTTHood, ['quietZone']),
         State.State('DDHood', self.enterDDHood, self.exitDDHood, ['quietZone']),
         State.State('BRHood', self.enterBRHood, self.exitBRHood, ['quietZone']),
         State.State('MMHood', self.enterMMHood, self.exitMMHood, ['quietZone']),
         State.State('DGHood', self.enterDGHood, self.exitDGHood, ['quietZone']),
         State.State('DLHood', self.enterDLHood, self.exitDLHood, ['quietZone']),
         State.State('GSHood', self.enterGSHood, self.exitGSHood, ['quietZone']),
         State.State('OZHood', self.enterOZHood, self.exitOZHood, ['quietZone']),
         State.State('GZHood', self.enterGZHood, self.exitGZHood, ['quietZone']),
         State.State('FEHood', self.enterFEHood, self.exitFEHood, ['quietZone']),
         State.State('BossbotHQ', self.enterBossbotHQ, self.exitBossbotHQ, ['quietZone']),
         State.State('SellbotHQ', self.enterSellbotHQ, self.exitSellbotHQ, ['quietZone']),
         State.State('CashbotHQ', self.enterCashbotHQ, self.exitCashbotHQ, ['quietZone']),
         State.State('LawbotHQ', self.enterLawbotHQ, self.exitLawbotHQ, ['quietZone']),
         State.State('TechbotHQ', self.enterTechbotHQ, self.exitTechbotHQ, ['quietZone']),
         State.State('CTCHood', self.enterCTCHood, self.exitCTCHood, ['quietZone']),
         State.State('EstateHood', self.enterEstateHood, self.exitEstateHood, ['quietZone']),
         State.State('PartyHood', self.enterPartyHood, self.exitPartyHood, ['quietZone'])], 'start', 'start')
        self.fsm.enterInitialState()
        self.parentFSM = parentFSM
        self.parentFSM.getStateNamed('playGame').addChild(self.fsm)
        self.hoodDoneEvent = 'hoodDone'
        self.hood = None
        self.quietZoneDoneEvent = uniqueName('quietZoneDone')
        self.quietZoneStateData = None
        self.signs = {}
        return

    def enter(self, hoodId, zoneId, avId):
        if hoodId == ToontownGlobals.PartyHood:
            self.getPartyZoneAndGoToParty(avId, zoneId)
            return
        else:
            loaderName = ZoneUtil.getLoaderName(zoneId)
            whereName = ZoneUtil.getToonWhereName(zoneId)
            self.fsm.request('quietZone', [{'loader': loaderName,
              'where': whereName,
              'how': 'teleportIn',
              'hoodId': hoodId,
              'zoneId': zoneId,
              'shardId': None,
              'avId': avId}])
            return

    def exit(self):
        if base.placeBeforeObjects and self.quietZoneStateData:
            self.quietZoneStateData.exit()
            self.quietZoneStateData.unload()
            self.quietZoneStateData = None
        self.ignore(self.quietZoneDoneEvent)
        return

    def load(self):
        pass

    def loadDnaStore(self):
        self.unloadDnaStore()
        if not hasattr(self, 'dnaStore'):
            self.dnaStore = DNAStorage()

    def unloadDnaStore(self):
        if hasattr(self, 'dnaStore'):
            self.dnaStore.cleanup()
            del self.dnaStore

    def unload(self):
        self.unloadDnaStore()
        if self.hood:
            self.hood.exit()
            self.hood.unload()
            self.hood = None
        base.cr.cache.flush()
        return

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def handleHoodDone(self):
        doneStatus = self.hood.getDoneStatus()
        shardId = doneStatus['shardId']
        if shardId != None:
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
            base.transitions.fadeOut(0)
            return
        elif doneStatus['where'] == 'party':
            self.getPartyZoneAndGoToParty(doneStatus['avId'], doneStatus['zoneId'])
            return
        else:
            how = doneStatus['how']
            if how in ('tunnelIn', 'teleportIn', 'doorIn', 'elevatorIn'):
                self.fsm.request('quietZone', [doneStatus])
            else:
                self.notify.error('Exited hood with unexpected mode %s' % how)
            return

    def _destroyHood(self):
        self.unload()

    def enterQuietZone(self, requestStatus):
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.quietZoneStateData = QuietZoneState.QuietZoneState(self.quietZoneDoneEvent)
        self._quietZoneLeftEvent = self.quietZoneStateData.getQuietZoneLeftEvent()
        if base.placeBeforeObjects:
            self.acceptOnce(self._quietZoneLeftEvent, self.handleLeftQuietZone)
        self._enterWaitForSetZoneResponseMsg = self.quietZoneStateData.getEnterWaitForSetZoneResponseMsg()
        self.acceptOnce(self._enterWaitForSetZoneResponseMsg, self.handleWaitForSetZoneResponse)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)

    def exitQuietZone(self):
        self.ignore(self._quietZoneLeftEvent)
        self.ignore(self._enterWaitForSetZoneResponseMsg)
        if not base.placeBeforeObjects:
            self.ignore(self.quietZoneDoneEvent)
            self.quietZoneStateData.exit()
            self.quietZoneStateData.unload()
            self.quietZoneStateData = None
        return

    def handleWaitForSetZoneResponse(self, requestStatus):
        hoodId = requestStatus['hoodId']
        toHoodPhrase = ToontownGlobals.hoodNameMap[hoodId][0]
        hoodName = ToontownGlobals.hoodNameMap[hoodId][-1]
        zoneId = requestStatus['zoneId']
        branchZone = ZoneUtil.getBranchZone(zoneId)
        loaderName = requestStatus['loader']
        avId = requestStatus.get('avId', -1)
        ownerId = requestStatus.get('ownerId', avId)
        if not loader.inBulkBlock:
            if hoodId == ToontownGlobals.MyEstate:
                if 'ownerName' in requestStatus:
                    loader.beginBulkLoad('hood', TTLocalizer.HeadingToEstate % requestStatus['ownerName'], True, TTLocalizer.TIP_ESTATE, ToontownGlobals.MyEstate)
                elif avId == -1:
                    loader.beginBulkLoad('hood', TTLocalizer.HeadingToYourEstate, True, TTLocalizer.TIP_ESTATE, ToontownGlobals.MyEstate)
                else:
                    owner = base.cr.identifyAvatar(ownerId)
                    if owner == None:
                        friend = base.cr.identifyAvatar(avId)
                        if friend != None:
                            avName = friend.getName()
                            loader.beginBulkLoad('hood', TTLocalizer.HeadingToFriend % avName, True, TTLocalizer.TIP_ESTATE, ToontownGlobals.MyEstate)
                        else:
                            self.notify.warning("we can't perform this teleport")
                            return
                    else:
                        avName = owner.getName()
                        loader.beginBulkLoad('hood', TTLocalizer.HeadingToEstate % avName, True, TTLocalizer.TIP_ESTATE, ToontownGlobals.MyEstate)
            elif ZoneUtil.isCogHQZone(zoneId):
                loader.beginBulkLoad('hood', TTLocalizer.HeadingToHood % {'to': toHoodPhrase,
                 'hood': hoodName}, True, TTLocalizer.TIP_COGHQ, branchZone)
            elif ZoneUtil.isGoofySpeedwayZone(zoneId):
                loader.beginBulkLoad('hood', TTLocalizer.HeadingToHood % {'to': toHoodPhrase,
                 'hood': hoodName}, True, TTLocalizer.TIP_KARTING, zoneId)
            else:
                if ZoneUtil.isInTutorial():
                    toHoodPhrase, inHoodPhrase, hoodName = TTLocalizer.Tutorial
                    branchZone = ToontownGlobals.CogtownCentral
                loader.beginBulkLoad('hood', TTLocalizer.HeadingToHood % {'to': toHoodPhrase,
                 'hood': hoodName}, True, TTLocalizer.TIP_GENERAL, branchZone)
        self.loadDnaStore()
        hoodClass = self.getHoodClassByNumber(hoodId)
        self.hood = hoodClass(self.fsm, self.hoodDoneEvent, self.dnaStore, hoodId)
        self.hood.load()
        self.hood.loadLoader(requestStatus)
        if not base.placeBeforeObjects:
            loader.endBulkLoad('hood')
        return

    def handleLeftQuietZone(self):
        status = self.quietZoneStateData.getRequestStatus()
        hoodState = self.getHoodStateByNumber(status['hoodId'])
        self.fsm.request(hoodState, [status])

    def handleQuietZoneDone(self):
        if base.placeBeforeObjects:
            self.quietZoneStateData.exit()
            self.quietZoneStateData.unload()
            self.quietZoneStateData = None
            loader.endBulkLoad('hood')
        else:
            self.handleLeftQuietZone()
        return

    def enterTTHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitTTHood(self):
        self._destroyHood()

    def enterDDHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitDDHood(self):
        self._destroyHood()

    def enterMMHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitMMHood(self):
        self._destroyHood()

    def enterBRHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitBRHood(self):
        self._destroyHood()

    def enterDGHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitDGHood(self):
        self._destroyHood()

    def enterDLHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitDLHood(self):
        self._destroyHood()

    def enterGSHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitGSHood(self):
        self._destroyHood()

    def enterOZHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitOZHood(self):
        self._destroyHood()

    def enterGZHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitGZHood(self):
        self._destroyHood()

    def enterFEHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitFEHood(self):
        self._destroyHood()

    def enterSellbotHQ(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitSellbotHQ(self):
        self._destroyHood()

    def enterCashbotHQ(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitCashbotHQ(self):
        self._destroyHood()

    def enterLawbotHQ(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitLawbotHQ(self):
        self._destroyHood()

    def enterBossbotHQ(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitBossbotHQ(self):
        self._destroyHood()

    def enterTechbotHQ(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitTechbotHQ(self):
        self._destroyHood()

    def enterCTCHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        if ZoneUtil.isInTutorial():
            messenger.send('toonArrivedTutorial')
            base.localAvatar.book.obscureButton(1)
            base.localAvatar.book.setSafeMode(1)
            base.localAvatar.laffMeter.obscure(1)
            base.localAvatar.chatMgr.obscure(1, 1, 1)
            base.localAvatar.obscureFriendsListButton(1)
            requestStatus['how'] = 'tutorial'
        self.hood.enter(requestStatus)

    def exitCTCHood(self):
        self.unloadDnaStore()
        self._destroyHood()
        if base.localAvatar.book.isObscured():
            base.localAvatar.book.obscureButton(0)
            base.localAvatar.book.setSafeMode(0)
            base.localAvatar.laffMeter.obscure(0)
            base.localAvatar.chatMgr.obscure(0, 0, 0)
            base.localAvatar.obscureFriendsListButton(-1)

    def enterEstateHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitEstateHood(self):
        self._destroyHood()

    def enterPartyHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        requestStatus['where'] = 'party'
        self.hood.enter(requestStatus)

    def exitPartyHood(self):
        self._destroyHood()

    def getPartyZoneAndGoToParty(self, avId, zoneId):
        self.doneStatus = {'avId': avId,
         'zoneId': zoneId,
         'hoodId': ToontownGlobals.PartyHood,
         'loader': 'safeZoneLoader',
         'how': 'teleportIn',
         'shardId': None}
        if avId < 0:
            avId = base.localAvatar.getDoId()
        base.cr.partyManager.requestPartyZone(avId, zoneId, callback=self.goToParty)
        return

    def goToParty(self, ownerId, partyId, zoneId):
        if ownerId == 0 or partyId == 0 or zoneId == 0:
            self.doneStatus['where'] = 'playground'
        else:
            self.doneStatus['where'] = 'party'
        self.doneStatus['ownerId'] = ownerId
        self.doneStatus['partyId'] = partyId
        self.doneStatus['zoneId'] = zoneId
        self.fsm.request('quietZone', [self.doneStatus])

    def goToPartyFailed(self, reason):
        self.notify.debug('goToPartyFailed')
        failedToVisitAvId = self.doneStatus.get('avId')
        message = base.cr.partyManager.getGoToPartyFailedMessage(reason)
        self.notify.debug('goToPartyFailed, why =: %s' % message)
        self.ignore('gotLocalPartyZone')
        zoneId = base.localAvatar.lastHood
        loaderName = ZoneUtil.getLoaderName(zoneId)
        whereName = ZoneUtil.getToonWhereName(zoneId)
        base.localAvatar.setSystemMessage(0, message)
        self.fsm.request('quietZone', [{'loader': loaderName,
          'where': whereName,
          'how': 'teleportIn',
          'hoodId': zoneId,
          'zoneId': zoneId,
          'shardId': None}])
        return Task.done

    def getHoodClassByNumber(self, hoodNumber):
        return self.Hood2ClassDict[hoodNumber]

    def getHoodStateByNumber(self, hoodNumber):
        return self.Hood2StateDict[hoodNumber]

    def setPlace(self, place):
        self.place = place
        if self.place:
            messenger.send('playGameSetPlace')

    def getPlace(self):
        return self.place

    def getPlaceId(self):
        if self.hood:
            return self.hood.hoodId
        else:
            return None