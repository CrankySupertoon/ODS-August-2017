# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.battle.BattlePlace
from panda3d.core import CollisionEntry, NodePath
from toontown.hood import Place, ZoneUtil
from toontown.toonbase import ToontownGlobals

class BattlePlace(Place.Place):

    def setState(self, state, battleEvent = None):
        if battleEvent:
            self.fsm.request(state, [battleEvent])
        else:
            self.fsm.request(state)

    def enterWalk(self, flag = 0):
        Place.Place.enterWalk(self, flag)
        self.accept('enterBattle', self.handleBattleEntry)

    def exitWalk(self):
        Place.Place.exitWalk(self)
        self.ignore('enterBattle')

    def enterWaitForBattle(self):
        base.localAvatar.b_setAnimState('neutral', 1)

    def exitWaitForBattle(self):
        pass

    def enterBattle(self, event):
        self.loader.music.stop()
        base.playMusic(self.loader.battleMusic, looping=1, volume=0.9)
        self.enterTownBattle(event)
        base.localAvatar.b_setAnimState('off', 1)
        self.accept('teleportQuery', self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.cantLeaveGame = 1

    def enterTownBattle(self, event):
        self.loader.townBattle.enter(event, self.fsm.getStateNamed('battle'))

    def exitBattle(self):
        self.loader.townBattle.exit()
        self.loader.battleMusic.stop()
        base.playMusic(self.loader.music, looping=1, volume=0.8)
        base.localAvatar.cantLeaveGame = 0
        base.localAvatar.setTeleportAvailable(0)
        self.ignore('teleportQuery')

    def handleBattleEntry(self):
        self.fsm.request('battle')

    def enterFallDown(self, extraArgs = []):
        base.localAvatar.laffMeter.start()
        base.localAvatar.b_setAnimState('FallDown', callback=self.handleFallDownDone, extraArgs=extraArgs)

    def handleFallDownDone(self):
        base.cr.playGame.getPlace().setState('walk')

    def exitFallDown(self):
        base.localAvatar.laffMeter.stop()

    def enterSquished(self):
        base.localAvatar.laffMeter.start()
        base.localAvatar.b_setAnimState('Squish')
        taskMgr.doMethodLater(2.0, self.handleSquishDone, base.localAvatar.uniqueName('finishSquishTask'))

    def handleSquishDone(self, extraArgs = []):
        base.cr.playGame.getPlace().setState('walk')

    def exitSquished(self):
        taskMgr.remove(base.localAvatar.uniqueName('finishSquishTask'))
        base.localAvatar.laffMeter.stop()

    def enterZone(self, newZone):
        if isinstance(newZone, CollisionEntry):
            try:
                newZone = int(newZone.getIntoNodePath().getTag('DNAVisGroup'))
            except:
                return

        self.doEnterZone(newZone)

    def doEnterZone(self, newZoneId):
        if newZoneId == self.zoneId:
            return
        else:
            if newZoneId != None:
                if hasattr(self, 'zoneVisDict'):
                    visList = self.zoneVisDict[newZoneId]
                else:
                    visList = base.cr.playGame.getPlace().loader.zoneVisDict[newZoneId]
                base.cr.sendSetZoneMsg(newZoneId, visList)
                self.notify.debug('Entering Zone %d' % newZoneId)
            self.zoneId = newZoneId
            return

    def genDNAFileName(self, zoneId):
        hoodId = ZoneUtil.getHoodId(zoneId)
        hood = ToontownGlobals.dnaMap[hoodId]
        phase = ToontownGlobals.streetPhaseMap[hoodId]
        if hoodId == zoneId:
            zoneId = 'sz'
        return 'phase_%s/dna/%s_%s.bdna' % (phase, hood, zoneId)