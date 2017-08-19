# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.ToonTeleportPanel
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
import ToonAvatarDetailPanel
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
globalTeleport = None

def showTeleportPanel(avId, avName, avDisableName):
    global globalTeleport
    if globalTeleport != None:
        globalTeleport.cleanup()
        globalTeleport = None
    globalTeleport = ToonTeleportPanel(avId, avName, avDisableName)
    return


def hideTeleportPanel():
    global globalTeleport
    if globalTeleport != None:
        globalTeleport.cleanup()
        globalTeleport = None
    return


def unloadTeleportPanel():
    global globalTeleport
    if globalTeleport != None:
        globalTeleport.cleanup()
        globalTeleport = None
    return


class ToonTeleportPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonTeleportPanel')

    def __init__(self, avId, avName, avDisableName):
        DirectFrame.__init__(self, pos=(-1.01, 0.1, -0.35), parent=base.a2dTopRight, image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.0, 1.0, 0.6), text='', text_wordwrap=13.5, text_scale=0.06, text_pos=(0.0, 0.18))
        messenger.send('releaseDirector')
        self['image'] = DGG.getDefaultDialogGeom()
        self.avId = avId
        self.avName = avName
        self.avDisableName = avDisableName
        self.fsm = ClassicFSM.ClassicFSM('ToonTeleportPanel', [State.State('off', self.enterOff, self.exitOff),
         State.State('begin', self.enterBegin, self.exitBegin),
         State.State('checkAvailability', self.enterCheckAvailability, self.exitCheckAvailability),
         State.State('notAvailable', self.enterNotAvailable, self.exitNotAvailable),
         State.State('ignored', self.enterIgnored, self.exitIgnored),
         State.State('noTeleport', self.enterNoTeleport, self.exitNoTeleport),
         State.State('notOnline', self.enterNotOnline, self.exitNotOnline),
         State.State('wentAway', self.enterWentAway, self.exitWentAway),
         State.State('self', self.enterSelf, self.exitSelf),
         State.State('unknownHood', self.enterUnknownHood, self.exitUnknownHood),
         State.State('otherShard', self.enterOtherShard, self.exitOtherShard),
         State.State('teleport', self.enterTeleport, self.exitTeleport)], 'off', 'off')
        from toontown.friends import FriendInviter
        FriendInviter.hideFriendInviter()
        ToonAvatarDetailPanel.hideAvatarDetail()
        self.bOk = DirectButton(self, image=Preloaded['okButton'], relief=None, text=TTLocalizer.TeleportPanelOK, text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.0, 0.0, -0.1), command=self.__handleOk)
        self.bOk.hide()
        self.bCancel = DirectButton(self, image=Preloaded['closeButton'], relief=None, text=TTLocalizer.TeleportPanelCancel, text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.0, 0.0, -0.1), command=self.__handleCancel)
        self.bCancel.hide()
        self.bYes = DirectButton(self, image=Preloaded['okButton'], relief=None, text=TTLocalizer.TeleportPanelYes, text_scale=0.05, text_pos=(0.0, -0.1), pos=(-0.15, 0.0, -0.15), command=self.__handleYes)
        self.bYes.hide()
        self.bNo = DirectButton(self, image=Preloaded['closeButton'], relief=None, text=TTLocalizer.TeleportPanelNo, text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.15, 0.0, -0.15), command=self.__handleNo)
        self.bNo.hide()
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        self.show()
        self.fsm.enterInitialState()
        self.fsm.request('begin')
        return

    def cleanup(self):
        self.fsm.request('off')
        del self.fsm
        self.ignore(self.avDisableName)
        self.destroy()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterBegin(self):
        myId = base.localAvatar.doId
        if self.avId == myId:
            self.fsm.request('self')
        elif self.avId in base.cr.doId2do:
            self.fsm.request('checkAvailability')
        elif base.cr.isFriend(self.avId):
            if base.cr.isFriendOnline(self.avId):
                self.fsm.request('checkAvailability')
            else:
                self.fsm.request('notOnline')
        else:
            self.fsm.request('wentAway')

    def exitBegin(self):
        pass

    def enterCheckAvailability(self):
        myId = base.localAvatar.getDoId()
        base.cr.ttFriendsManager.d_teleportQuery(self.avId)
        self['text'] = TTLocalizer.TeleportPanelCheckAvailability % self.avName
        self.accept('teleportResponse', self.__teleportResponse)
        self.bCancel.show()

    def exitCheckAvailability(self):
        self.ignore('teleportResponse')
        self.bCancel.hide()

    def enterNotAvailable(self):
        self['text'] = TTLocalizer.TeleportPanelNotAvailable % self.avName
        self.bOk.show()

    def exitNotAvailable(self):
        self.bOk.hide()

    def enterIgnored(self):
        self['text'] = TTLocalizer.TeleportPanelIgnored % self.avName
        self.bOk.show()

    def exitIgnored(self):
        self.bOk.hide()

    def enterNoTeleport(self):
        self['text'] = TTLocalizer.TeleportPanelNoTeleport % self.avName
        self.bOk.show()

    def exitNoTeleport(self):
        self.bOk.hide()

    def enterNotOnline(self):
        self['text'] = TTLocalizer.TeleportPanelNotOnline % self.avName
        self.bOk.show()

    def exitNotOnline(self):
        self.bOk.hide()

    def enterWentAway(self):
        self['text'] = TTLocalizer.TeleportPanelWentAway % self.avName
        self.bOk.show()

    def exitWentAway(self):
        self.bOk.hide()

    def enterUnknownHood(self, hoodId):
        self['text'] = TTLocalizer.TeleportPanelUnknownHood % base.cr.hoodMgr.getFullnameFromId(hoodId)
        self.bOk.show()

    def exitUnknownHood(self):
        self.bOk.hide()

    def enterSelf(self):
        self['text'] = TTLocalizer.TeleportPanelDenySelf
        self.bOk.show()

    def exitSelf(self):
        self.bOk.hide()

    def enterOtherShard(self, shardId, hoodId, zoneId):
        shardName = base.cr.getShardName(shardId)
        if shardName is None:
            self.fsm.request('notAvailable')
            return
        else:
            myShardName = base.cr.getShardName(base.localAvatar.defaultShard)
            pop = None
            for shard in base.cr.listActiveShards():
                if shard[0] == shardId:
                    pop = shard[2]

            self.bYes.show()
            self.bNo.show()
            if pop and pop > localAvatar.shardPage.midPop:
                self.notify.warning('Entering full shard: issuing performance warning')
                self['text'] = TTLocalizer.TeleportPanelBusyShard % {'avName': self.avName}
                self.bYes.hide()
                self.bNo.hide()
                self.bOk.show()
            else:
                self['text'] = TTLocalizer.TeleportPanelOtherShard % {'avName': self.avName,
                 'shardName': shardName,
                 'myShardName': myShardName}
            self.shardId = shardId
            self.hoodId = hoodId
            self.zoneId = zoneId
            return

    def exitOtherShard(self):
        self.bYes.hide()
        self.bNo.hide()

    def enterTeleport(self, shardId, hoodId, zoneId):
        shardName = base.cr.getShardName(shardId)
        if shardName is None:
            shardName = 'unknown'
        hoodsVisited = base.localAvatar.hoodsVisited
        if hoodId == ToontownGlobals.MyEstate:
            if shardId == base.localAvatar.defaultShard:
                shardId = None
            place = base.cr.playGame.getPlace()
            place.requestTeleport(hoodId, zoneId, shardId, self.avId)
            unloadTeleportPanel()
        elif hoodId not in hoodsVisited + ToontownGlobals.HoodsAlwaysVisited:
            self.fsm.request('unknownHood', [hoodId])
        else:
            if shardId == base.localAvatar.defaultShard:
                shardId = None
            place = base.cr.playGame.getPlace()
            place.requestTeleport(hoodId, zoneId, shardId, self.avId)
            unloadTeleportPanel()
        return

    def exitTeleport(self):
        pass

    def __handleOk(self):
        unloadTeleportPanel()

    def __handleCancel(self):
        unloadTeleportPanel()

    def __handleYes(self):
        self.fsm.request('teleport', [self.shardId, self.hoodId, self.zoneId])

    def __handleNo(self):
        unloadTeleportPanel()

    def __teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        if avId != self.avId:
            return
        if available == 0:
            self.fsm.request('notAvailable')
        elif available == 2:
            self.fsm.request('ignored')
        elif available == 3:
            self.fsm.request('noTeleport')
        elif shardId != base.localAvatar.defaultShard:
            self.fsm.request('otherShard', [shardId, hoodId, zoneId])
        else:
            self.fsm.request('teleport', [shardId, hoodId, zoneId])

    def __handleDisableAvatar(self):
        self.fsm.request('wentAway')