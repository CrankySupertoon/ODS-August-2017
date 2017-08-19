# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.friends.FriendHandle
from otp.ai.MagicWordGlobal import *
from otp.chat.ChatGarbler import ChatGarbler
from toontown.toonbase import ToontownGlobals, TTLocalizer

class FriendHandle(ChatGarbler):

    def __init__(self, doId, name, style, petId, isAPet = False):
        self.doId = doId
        self.style = style
        self.petId = petId
        self.isAPet = isAPet
        self.name = name

    def isAdmin(self):
        return False

    def getDoId(self):
        return self.doId

    def getPetId(self):
        return self.petId

    def hasPet(self):
        return self.getPetId() != 0

    def isPet(self):
        return self.isAPet

    def getName(self):
        return self.name

    def getFont(self):
        return ToontownGlobals.getToonFont()

    def getStyle(self):
        return self.style

    def uniqueName(self, idString):
        return idString + '-' + str(self.getDoId())

    def d_battleSOS(self, sendToId):
        base.cr.ttFriendsManager.d_battleSOS(self.doId)

    def d_teleportQuery(self, requesterId):
        base.cr.ttFriendsManager.d_teleportQuery(self.doId)

    def d_teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        base.cr.ttFriendsManager.d_teleportResponse(self.doId, available, shardId, hoodId, zoneId)

    def d_teleportGiveup(self, requesterId):
        base.cr.ttFriendsManager.d_teleportGiveup(self.doId)

    def isUnderstandable(self):
        if base.cr.wantTypedChat():
            return 1
        if base.localAvatar.isTrueFriends(self.doId):
            return 1
        return 0

    def getMessages(self):
        if self.style:
            return TTLocalizer.ChatGarblers[self.style.head[0]]
        else:
            return DistributedPlayer.DistributedPlayer.getMessages(self)