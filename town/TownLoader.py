# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.TownLoader
from toontown.battle.BattleProps import *
from toontown.battle.BattleSounds import *
from toontown.distributed.ToontownMsgTypes import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import cleanupDialog
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import TownBattle
from toontown.toon import Toon
from toontown.battle import BattleParticles
from direct.fsm import StateData
from toontown.building import ToonInterior
from toontown.hood import QuietZoneState, ZoneUtil, HydrantInteractiveProp, MailboxInteractiveProp, TrashcanInteractiveProp
from direct.interval.IntervalGlobal import *
from toontown.dna.DNAParser import loadDNAFileAI

class TownLoader(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownLoader')

    def __init__(self, hood, parentFSMState, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.hood = hood
        self.parentFSMState = parentFSMState
        self.fsm = ClassicFSM.ClassicFSM('TownLoader', [State.State('start', self.enterStart, self.exitStart, ['quietZone', 'street', 'toonInterior']),
         State.State('street', self.enterStreet, self.exitStreet, ['quietZone']),
         State.State('toonInterior', self.enterToonInterior, self.exitToonInterior, ['quietZone']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['street', 'toonInterior']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')
        self.branchZone = None
        self.placeDoneEvent = 'placeDone'
        self.townBattleDoneEvent = 'town-battle-done'
        return

    def load(self, zoneId):
        self.zoneId = zoneId
        self.parentFSMState.addChild(self.fsm)
        self.branchZone = ZoneUtil.getBranchZone(zoneId)
        self.music = loader.loadMusic(self.musicFile)
        self.activityMusic = loader.loadMusic(self.activityMusicFile)
        self.resetBattleMusic()
        self.townBattle = TownBattle.TownBattle(self.townBattleDoneEvent)
        self.townBattle.load()

    def unload(self):
        globalPropPool.unloadProps()
        globalBattleSoundCache.clear()
        BattleParticles.unloadParticles()
        self.parentFSMState.removeChild(self.fsm)
        self.landmarkBlocks.removeNode()
        del self.landmarkBlocks
        del self.parentFSMState
        del self.fsm
        del self.streetClass
        self.hood.dnaStore.cleanup()
        del self.hood.dnaStore
        base.cr.playGame.loadDnaStore()
        self.hood.dnaStore = base.cr.playGame.dnaStore
        del self.hood
        del self.zoneDnaDict
        del self.zoneVisDict
        self.geom.removeNode()
        del self.geom
        del self.prop
        self.townBattle.unload()
        self.townBattle.cleanup()
        del self.townBattle
        del self.battleMusic
        del self.music
        del self.activityMusic
        self.deleteAnimatedProps()
        cleanupDialog('globalDialog')
        for zone in self.zoneDict.values():
            zone.removeNode()

        del self.zoneDict

    def enter(self, requestStatus):
        self.fsm.enterInitialState()
        self.setState(requestStatus['where'], requestStatus)

    def exit(self):
        self.ignoreAll()

    def resetBattleMusic(self):
        if settings['musicEasterEgg'] and base.cr.getShard().hasEasterEgg():
            self.battleMusic = loader.loadMusic('phase_3.5/audio/bgm/cogtastrophe.ogg')
        else:
            self.battleMusic = loader.loadMusic('phase_3.5/audio/bgm/encntr_general_bg.ogg')

    def setState(self, stateName, requestStatus):
        self.fsm.request(stateName, [requestStatus])

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def enterStreet(self, requestStatus):
        self.acceptOnce(self.placeDoneEvent, self.streetDone)
        self.place = self.streetClass(self, self.fsm, self.placeDoneEvent)
        self.place.load()
        base.cr.playGame.setPlace(self.place)
        self.place.enter(requestStatus)

    def exitStreet(self):
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)
        return

    def streetDone(self):
        self.requestStatus = self.place.doneStatus
        status = self.place.doneStatus
        if status['loader'] == 'townLoader' and ZoneUtil.getBranchZone(status['zoneId']) == self.branchZone and status['shardId'] == None:
            self.fsm.request('quietZone', [status])
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)
        return

    def enterToonInterior(self, requestStatus):
        self.acceptOnce(self.placeDoneEvent, self.handleToonInteriorDone)
        self.place = ToonInterior.ToonInterior(self, self.fsm.getStateNamed('toonInterior'), self.placeDoneEvent)
        base.cr.playGame.setPlace(self.place)
        self.place.load()
        self.place.enter(requestStatus)

    def exitToonInterior(self):
        self.ignore(self.placeDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)
        return

    def handleToonInteriorDone(self):
        status = self.place.doneStatus
        if ZoneUtil.getBranchZone(status['zoneId']) == self.branchZone and status['shardId'] == None:
            self.fsm.request('quietZone', [status])
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)
        return

    def enterQuietZone(self, requestStatus):
        self.quietZoneDoneEvent = uniqueName('quietZoneDone')
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.quietZoneStateData = QuietZoneState.QuietZoneState(self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)

    def exitQuietZone(self):
        self.ignore(self.quietZoneDoneEvent)
        del self.quietZoneDoneEvent
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        self.quietZoneStateData = None
        return

    def handleQuietZoneDone(self):
        status = self.quietZoneStateData.getRequestStatus()
        self.fsm.request(status['where'], [status])

    def enterFinal(self):
        pass

    def exitFinal(self):
        pass

    def createHood(self, dnaFile):
        self.landmarkBlocks = hidden.attachNewNode('landmarkBlocks')
        self.animPropDict = {}
        self.zoneIdToInteractivePropDict = {}
        self.zoneDict = {}
        self.zoneVisDict = {}
        self.zoneDnaDict = {}
        self.prop, self.geom = loader.loadDNAFile(self.hood.dnaStore, dnaFile, False)
        self.geom.reparentTo(hidden)
        self.geom.flattenMedium()
        self.makeDictionaries(self.hood.dnaStore)

    def makeDictionaries(self, dnaStore):
        for visGroup in dnaStore.getDNAVisGroups():
            groupName = base.cr.hoodMgr.extractGroupName(visGroup.getName())
            zoneId = int(groupName)
            visibles = [ZoneUtil.getBranchZone(zoneId)] + visGroup.getVisibles()
            self.zoneVisDict[zoneId] = [ int(vis) for vis in visibles ]
            self.zoneDnaDict[zoneId] = visGroup

    def showVisGroup(self, zoneId):
        if zoneId not in self.zoneDnaDict:
            return
        visGroup = self.zoneDnaDict[zoneId]
        if zoneId not in self.zoneDict:
            visGroup.loadVis = True
            node = visGroup.traverse(self.geom, self.hood.dnaStore)
            node.flattenMedium()
            self.reparentLandmarkBlockNodes(node)
            self.createAnimatedProps(node)
            self.tagFloorPolys(node)
            self.enterAnimatedProps(node)
            base.cr.hoodMgr.addLinkTunnelHooks(self.place, [node])
            self.zoneDict[zoneId] = node
        else:
            node = self.zoneDict[zoneId]
        node.unstash()

    def hideVisGroup(self, zoneId):
        if zoneId not in self.zoneDict:
            return
        node = self.zoneDict[zoneId]
        self.exitAnimatedProps(node)
        node.stash()

    def reparentLandmarkBlockNodes(self, node):
        for node in node.findAllMatches('**/sb*:*_landmark_*_DNARoot'):
            node.wrtReparentTo(self.landmarkBlocks)

    def tagFloorPolys(self, node):
        visGroupName = node.node().getName()
        for collision in node.findAllMatches('**/+CollisionNode'):
            collision.setTag('DNAVisGroup', visGroupName)

    def createAnimatedProps(self, node):
        animPropList = []
        for animatedProp in node.findAllMatches('**/animated_prop_*'):
            if animatedProp.getName().startswith('animated_prop_generic'):
                className = 'GenericAnimatedProp'
            elif animatedProp.getName().startswith('animated_prop_'):
                name = animatedProp.getName()[len('animated_prop_'):]
                className = name.split('_')[0]
            else:
                className = animatedProp.getName()[14:-8]
            symbols = {}
            base.cr.importModule(symbols, 'toontown.hood', [className])
            classObj = getattr(symbols[className], className)
            animPropObj = classObj(animatedProp)
            animPropList.append(animPropObj)

        for interactiveProp in node.findAllMatches('**/interactive_prop_*'):
            propName = interactiveProp.getName()
            if 'hydrant' in propName:
                prop = HydrantInteractiveProp.HydrantInteractiveProp(interactiveProp)
            elif 'trashcan' in propName:
                prop = TrashcanInteractiveProp.TrashcanInteractiveProp(interactiveProp)
            elif 'mailbox' in propName:
                prop = MailboxInteractiveProp.MailboxInteractiveProp(interactiveProp)
            else:
                continue
            animPropList.append(prop)
            self.zoneIdToInteractivePropDict[int(node.getName())] = prop

        self.animPropDict[node] = animPropList

    def deleteAnimatedProps(self):
        for zoneNode, animPropList in self.animPropDict.items():
            for animProp in animPropList:
                animProp.delete()

        del self.animPropDict

    def enterAnimatedProps(self, zoneNode):
        for animProp in self.animPropDict.get(zoneNode, ()):
            animProp.enter()

    def exitAnimatedProps(self, zoneNode):
        for animProp in self.animPropDict.get(zoneNode, ()):
            animProp.exit()

    def getInteractiveProp(self, zoneId):
        if zoneId in self.zoneIdToInteractivePropDict:
            return self.zoneIdToInteractivePropDict[zoneId]
        else:
            return None