# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.friends.TTFriendsManager
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.otpbase import OTPLocalizer, OTPGlobals
from otp.speedchat import SCDecoders
from toontown.hood import ZoneUtil
from toontown.speedchat import TTSCDecoders
import time

class TTFriendsManager(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.nextTeleportFail = 0

    def d_removeFriend(self, friendId):
        self.sendUpdate('removeFriend', [friendId])

    def d_requestFriendsList(self):
        self.sendUpdate('requestFriendsList', [])

    def friendList(self, resp):
        base.cr.handleGetFriendsList(resp)

    def friendOnline(self, id):
        base.cr.handleFriendOnline(id)

    def friendOffline(self, id):
        base.cr.handleFriendOffline(id)

    def friendsOnline(self, ids):
        base.cr.handleFriendsOnline(ids)

    def d_getAvatarDetails(self, avId):
        self.sendUpdate('getAvatarDetails', [avId])

    def friendDetails(self, friendDetails):
        avId, inventory, trackAccess, hp, maxHp, defaultShard, lastHood, dnaString, experience, trackBonusLevel, npcFriends, lastSeen = friendDetails
        fields = [['setExperience', experience],
         ['setTrackAccess', trackAccess],
         ['setTrackBonusLevel', trackBonusLevel],
         ['setInventory', inventory],
         ['setHp', hp],
         ['setMaxHp', maxHp],
         ['setDefaultShard', defaultShard],
         ['setLastHood', lastHood],
         ['setDNAString', dnaString],
         ['setNPCFriendsDict', npcFriends],
         ['setLastSeen', lastSeen]]
        base.cr.n_handleGetAvatarDetailsResp(avId, fields=fields)

    def d_getPetDetails(self, avId):
        self.sendUpdate('getPetDetails', [avId])

    def petDetails(self, petDetails):
        avId, ownerId, petName, traitSeed, sz, traits, trickAptitudes, moods, dna, lastSeen = petDetails
        fields = list(zip(('setHead', 'setEars', 'setNose', 'setTail', 'setBodyTexture', 'setColor', 'setColorScale', 'setEyeColor', 'setGender'), dna))
        fields.extend(zip(('setBoredom', 'setRestlessness', 'setPlayfulness', 'setLoneliness', 'setSadness', 'setAffection', 'setHunger', 'setConfusion', 'setExcitement', 'setFatigue', 'setAnger', 'setSurprise'), moods))
        fields.extend(zip(('setForgetfulness', 'setBoredomThreshold', 'setRestlessnessThreshold', 'setPlayfulnessThreshold', 'setLonelinessThreshold', 'setSadnessThreshold', 'setFatigueThreshold', 'setHungerThreshold', 'setConfusionThreshold', 'setExcitementThreshold', 'setAngerThreshold', 'setSurpriseThreshold', 'setAffectionThreshold'), traits))
        fields.append(('setOwnerId', ownerId))
        fields.append(('setPetName', petName))
        fields.append(('setTraitSeed', traitSeed))
        fields.append(('setSafeZone', sz))
        fields.append(('setLastSeenTimestamp', lastSeen))
        fields.append(('setTrickAptitudes', trickAptitudes))
        base.cr.n_handleGetAvatarDetailsResp(avId, fields=fields)

    def d_teleportQuery(self, toId):
        self.sendUpdate('routeTeleportQuery', [toId])

    def teleportQuery(self, fromId):
        if not hasattr(base, 'localAvatar'):
            self.sendUpdate('teleportResponse', [fromId,
             0,
             0,
             0,
             0])
            return
        if not hasattr(base.localAvatar, 'getTeleportAvailable') or not hasattr(base.localAvatar, 'ghostMode'):
            self.sendUpdate('teleportResponse', [fromId,
             0,
             0,
             0,
             0])
            return
        if not base.localAvatar.isAcceptingTeleports():
            self.sendUpdate('teleportResponse', [fromId,
             3,
             0,
             0,
             0])
            return
        if base.localAvatar.isIgnored(fromId):
            self.sendUpdate('teleportResponse', [fromId,
             2,
             0,
             0,
             0])
            return
        friend = base.cr.identifyFriend(fromId)
        if not base.localAvatar.getTeleportAvailable() or base.localAvatar.ghostMode:
            if hasattr(friend, 'getName') and self.nextTeleportFail < time.time():
                self.nextTeleportFail = time.time() + OTPGlobals.TeleportFailCooldown
                base.localAvatar.setSystemMessage(fromId, OTPLocalizer.WhisperFailedVisit % friend.getName())
            self.sendUpdate('teleportResponse', [fromId,
             0,
             0,
             0,
             0])
            return
        hoodId = base.cr.playGame.getPlaceId()
        if hasattr(friend, 'getName'):
            base.localAvatar.setSystemMessage(fromId, OTPLocalizer.WhisperComingToVisit % friend.getName())
        self.sendUpdate('teleportResponse', [fromId,
         base.localAvatar.getTeleportAvailable(),
         base.localAvatar.defaultShard,
         hoodId,
         base.localAvatar.getZoneId()])

    def d_teleportResponse(self, toId, available, shardId, hoodId, zoneId):
        self.sendUpdate('teleportResponse', [toId,
         available,
         shardId,
         hoodId,
         zoneId])

    def setTeleportResponse(self, fromId, available, shardId, hoodId, zoneId):
        base.localAvatar.teleportResponse(fromId, available, shardId, hoodId, zoneId)

    def d_whisperSCTo(self, toId, msgIndex):
        base.talkAssistant.logWhisperTo(toId, SCDecoders.decodeSCStaticTextMsg(msgIndex))
        self.sendUpdate('whisperSCTo', [toId, msgIndex])

    def setWhisperSCFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCFrom'):
            return
        base.localAvatar.setWhisperSCFrom(fromId, msgIndex)

    def d_whisperSCCustomTo(self, toId, msgIndex):
        base.talkAssistant.logWhisperTo(toId, SCDecoders.decodeSCCustomMsg(msgIndex))
        self.sendUpdate('whisperSCCustomTo', [toId, msgIndex])

    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCCustomFrom'):
            return
        base.localAvatar.setWhisperSCCustomFrom(fromId, msgIndex)

    def d_whisperSCEmoteTo(self, toId, emoteId):
        self.sendUpdate('whisperSCEmoteTo', [toId, emoteId])

    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCEmoteFrom'):
            return
        base.localAvatar.setWhisperSCEmoteFrom(fromId, emoteId)

    def d_sendTalkWhisper(self, receiverAvId, message):
        base.talkAssistant.logWhisperTo(receiverAvId, message)
        self.sendUpdate('sendTalkWhisper', [receiverAvId, message])

    def receiveTalkWhisper(self, fromId, message):
        base.localAvatar.setTalkWhisper(fromId, message)

    def d_battleSOS(self, toId):
        self.sendUpdate('battleSOS', [toId])

    def setBattleSOS(self, fromId):
        base.localAvatar.battleSOS(fromId)

    def d_teleportGiveup(self, toId):
        self.sendUpdate('teleportGiveup', [toId])

    def setTeleportGiveup(self, fromId):
        base.localAvatar.teleportGiveup(fromId)

    def d_whisperSCToontaskTo(self, toId, taskId, toNpcId, toonProgress, msgIndex):
        base.talkAssistant.logWhisperTo(toId, TTSCDecoders.decodeTTSCToontaskMsg(taskId, toNpcId, toonProgress, msgIndex))
        self.sendUpdate('whisperSCToontaskTo', [toId,
         taskId,
         toNpcId,
         toonProgress,
         msgIndex])

    def setWhisperSCToontaskFrom(self, fromId, taskId, toNpcId, toonProgress, msgIndex):
        base.localAvatar.setWhisperSCToontaskFrom(fromId, taskId, toNpcId, toonProgress, msgIndex)

    def d_sleepAutoReply(self, toId):
        self.sendUpdate('sleepAutoReply', [toId])

    def setSleepAutoReply(self, fromId):
        base.localAvatar.setSleepAutoReply(fromId)