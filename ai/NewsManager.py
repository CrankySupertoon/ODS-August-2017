# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.ai.NewsManager
from panda3d.core import Notify
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from toontown.battle import SuitBattleGlobals
from toontown.estate import Estate
from toontown.toonbase import ToontownGlobals, ToontownBattleGlobals, TTLocalizer
from toontown.suit import SuitDNA
import HolidayGlobals

class NewsManager(DistributedObject):
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.invading = False
        self.activeHolidays = []
        cr.newsManager = self

    def delete(self):
        self.cr.newsManager = None
        DistributedObject.delete(self)
        return

    def isHolidayRunning(self, id):
        return id in self.activeHolidays

    def setActiveHolidays(self, ids):
        self.activeHolidays = ids

    def holidayNotify(self):
        for id in self.activeHolidays:
            self.broadcastHoliday(id, 'ongoingMessage')
            self.startSpecialHoliday(id)

    def broadcastHoliday(self, id, type):
        holiday = HolidayGlobals.getHoliday(id)
        if type in holiday:
            base.localAvatar.setSystemMessage(0, holiday[type])

    def startHoliday(self, id):
        if id in self.activeHolidays or id not in HolidayGlobals.Holidays:
            return
        self.activeHolidays.append(id)
        self.broadcastHoliday(id, 'startMessage')
        self.startSpecialHoliday(id)

    def endHoliday(self, id):
        if id not in self.activeHolidays or id not in HolidayGlobals.Holidays:
            return
        self.activeHolidays.remove(id)
        self.broadcastHoliday(id, 'endMessage')
        self.endSpecialHoliday(id)

    def startSpecialHoliday(self, id):
        if id == ToontownGlobals.APRIL_TOONS_WEEK:
            if isinstance(base.cr.playGame.getPlace(), Estate.Estate):
                base.localAvatar.startAprilToonsControls()
            base.localAvatar.chatMgr.chatInputSpeedChat.addAprilToonsMenu()
        elif id == ToontownGlobals.IDES_OF_MARCH:
            base.localAvatar.chatMgr.chatInputSpeedChat.addIdesOfMarchMenu()
        elif id == ToontownGlobals.HALLOWEEN:
            base.localAvatar.chatMgr.chatInputSpeedChat.addHalloweenMenu()
        elif id == ToontownGlobals.CHRISTMAS:
            base.localAvatar.chatMgr.chatInputSpeedChat.addWinterMenu()

    def endSpecialHoliday(self, id):
        if id == ToontownGlobals.APRIL_TOONS_WEEK:
            if isinstance(base.cr.playGame.getPlace(), Estate.Estate):
                base.localAvatar.stopAprilToonsControls()
            base.localAvatar.chatMgr.chatInputSpeedChat.removeAprilToonsMenu()
        elif id == ToontownGlobals.IDES_OF_MARCH:
            base.localAvatar.chatMgr.chatInputSpeedChat.removeIdesOfMarchMenu()
        elif id == ToontownGlobals.HALLOWEEN:
            base.localAvatar.chatMgr.chatInputSpeedChat.removeHalloweenMenu()
        elif id == ToontownGlobals.CHRISTMAS:
            base.localAvatar.chatMgr.chatInputSpeedChat.removeWinterMenu()

    def setInvasionStatus(self, msgType, suitType, remaining, flags):
        if len(TTLocalizer.SuitInvasions) <= msgType:
            return
        if suitType in SuitDNA.suitHeadTypes:
            attributes = SuitBattleGlobals.SuitAttributes[suitType]
            suitNames = {'singular': attributes['name'],
             'plural': attributes['pluralname']}
        elif suitType in SuitDNA.suitDepts:
            suitNames = {'singular': SuitDNA.getDeptFullname(suitType),
             'plural': SuitDNA.getDeptFullnameP(suitType)}
        else:
            return
        track = Sequence()
        for i, message in enumerate(TTLocalizer.SuitInvasions[msgType]):
            track.append(Wait(5 if i else 1))
            track.append(Func(base.localAvatar.setSystemMessage, 0, (TTLocalizer.SuitInvasionPrefix + message) % suitNames))

        track.start()