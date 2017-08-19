# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.uberdog.ARGManager
from direct.interval.IntervalGlobal import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.DirectObject import DirectObject
Hood2Details = {2747: ['intel', ['How do you know about this?!',
         'Either way, this is not the end of your journey.',
         'Our group has been hiding within these empty shops for years.',
         'One day you may be strong enough to understand.']],
 3717: ['intel', ['You just never really give up, do you ever?',
         'Maybe you could be of good use to us...',
         'But until then... We need you to be patient.',
         "Because we don't know how much longer going sad will be a thing...",
         'Need more? See the Karnie.']],
 2803: ['intel', ["I'll give ya something kid, ya know what you're doin'",
         'But I know the first rule of INTEL...',
         'Never talk about INTEL...',
         "If you're looking for answers, try the library..."]],
 9501: ['intel', ['Shh... This is a place of silence!',
         "Oh wait... You didn't hear that, did you?",
         '...',
         "You're going to blow our cover, lurking around here.",
         'Go talk in the screen room instead!']],
 9633: ['intel', ["We can't keep this up much longer.", "We were hoping you'd just give up.", "Would you look at the time, I can't because my clock is dirty..."]],
 9613: ['intel', ["Okay, fine, we'll tell you.",
         'We may be planning something soon...',
         'Those Techbots are getting too strong.',
         'There is nothing more we can tell you... for now.']]}

class ARGManager(DirectObject):
    notify = directNotify.newCategory('ARGManager')

    def __init__(self):
        self.track = None
        self.setupEvents()
        return

    def delete(self):
        self.cleanupTrack()
        self.cleanupEvents()

    def getZoneId(self):
        if hasattr(base.cr.playGame, 'place') and base.cr.playGame.place:
            return base.cr.playGame.place.getZoneId()

    def showMessages(self, messages):
        self.track = Sequence()
        for i, message in enumerate(messages):
            if i:
                self.track.append(Wait(3))
            self.track.append(Func(base.localAvatar.setSystemMessage, 0, message, 4))

        self.track.append(Func(self.cleanupTrack))
        self.track.start()

    def __chatSaid(self, message):
        if self.track:
            return
        zoneId = self.getZoneId()
        if not zoneId or zoneId not in Hood2Details:
            return
        requiredMessage, responses = Hood2Details[zoneId]
        if requiredMessage.lower() not in message.lower():
            return
        self.showMessages(responses)

    def setupEvents(self):
        self.accept('chatSaid', self.__chatSaid)

    def cleanupEvents(self):
        self.ignore('chatSaid')

    def cleanupTrack(self):
        if self.track:
            self.track.pause()
            self.track = None
        return