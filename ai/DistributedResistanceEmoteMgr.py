# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.ai.DistributedResistanceEmoteMgr
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from otp.speedchat import SpeedChatGlobals
from toontown.toon import TTEmote
from toontown.toonbase import TTLocalizer
RESIST_INDEX = TTEmote.Emotes.index('resistance-salute')

class DistributedResistanceEmoteMgr(DistributedObject):

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, self.phraseSaid)

    def delete(self):
        self.ignoreAll()
        DistributedObject.delete(self)

    def phraseSaid(self, phraseId):
        if phraseId == 513:
            self.addResistanceEmote()

    def addResistanceEmote(self):
        av = base.localAvatar
        if not av.emoteAccess[RESIST_INDEX]:
            self.sendUpdate('addResistanceEmote', [])
            Sequence(Wait(1), Func(av.setSystemMessage, 0, TTLocalizer.ResistanceEmote1), Wait(3), Func(av.setSystemMessage, 0, TTLocalizer.ResistanceEmote2), Wait(4), Func(av.setSystemMessage, 0, TTLocalizer.ResistanceEmote3)).start()