# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.TTEmote
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from otp.avatar import Emote
from otp.otpbase import OTPLocalizer
from otp.nametag.NametagConstants import *
from toontown.toonbase import TTLocalizer
import random
EmoteSleepIndex = 5
EmoteClear = -1

def doDance(toon, volume = 1):
    sfx = loader.loadSfx('phase_3.5/audio/sfx/ENC_Win.ogg')
    duration = toon.getDuration('victory')
    track = Sequence(Func(toon.play, 'victory'), SoundInterval(sfx, loop=1, duration=duration - 1, node=toon, volume=volume), duration=0)
    return (track, duration, None)


def doAngry(toon, volume = 1):
    sfx = loader.loadSfx('phase_3.5/audio/%s' % ('dial/AV_bear_exclaim.ogg' if toon.style.getAnimal() == 'bear' else 'sfx/avatar_emotion_angry.ogg'))
    duration = toon.getDuration('angry')
    track = Sequence(Func(toon.angryEyes), Func(toon.blinkEyes), Func(toon.play, 'angry'), Func(base.playSfx, sfx, volume=volume, node=toon))
    exitTrack = Sequence(Func(toon.normalEyes), Func(toon.blinkEyes))
    return (track, duration, exitTrack)


def doBitter(toon, volume = 1):
    track = Sequence(Func(toon.angryEyes), Func(toon.blinkEyes))
    exitTrack = Sequence(Func(toon.normalEyes), Func(toon.blinkEyes))
    return (track, 3, exitTrack)


def doHappy(toon, volume = 1):
    track = Sequence(Func(toon.play, 'jump'), Func(toon.normalEyes), Func(toon.blinkEyes))
    duration = toon.getDuration('jump')
    return (track, duration, None)


def doSad(toon, volume = 1):
    track = Sequence(Func(toon.sadEyes), Func(toon.blinkEyes))
    exitTrack = Sequence(Func(toon.normalEyes), Func(toon.blinkEyes))
    return (track, 3, exitTrack)


def doSleep(toon, volume = 1):
    track = Sequence(Func(toon.stopLookAround), Func(toon.stopBlink), Func(toon.closeEyes), Func(toon.lerpLookAt, (0, 1, -4)), Func(toon.loop, 'neutral'), Func(toon.setPlayRate, 0.4, 'neutral'), Func(toon.setChatAbsolute, TTLocalizer.ToonSleepString, CFThought))

    def wakeUpFromSleepEmote():
        toon.startLookAround()
        toon.openEyes()
        toon.startBlink()
        toon.setPlayRate(1, 'neutral')
        toon.lerpLookAt((0, 1, 0), time=0.75)
        if toon.nametag.getChat() == TTLocalizer.ToonSleepString:
            toon.clearChat()

    exitTrack = Func(wakeUpFromSleepEmote)
    return (track, 4, exitTrack)


def doShrug(toon, volume = 1):
    sfx = loader.loadSfx('phase_3.5/audio/sfx/avatar_emotion_shrug.ogg')
    track = Sequence(Func(toon.play, 'shrug'), Func(base.playSfx, sfx, volume=volume, node=toon))
    duration = toon.getDuration('shrug')
    return (track, duration, None)


def doWave(toon, volume = 1):
    track = Func(toon.play, 'wave')
    duration = toon.getDuration('wave')
    return (track, duration, None)


def doApplause(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/avatar_emotion_applause.ogg')
    track = Sequence(Func(toon.play, 'applause'), Func(base.playSfx, sfx, volume=volume, node=toon))
    duration = toon.getDuration('applause')
    return (track, duration, None)


def doConfused(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/avatar_emotion_confused.ogg')
    track = Sequence(Func(toon.play, 'confused'), Func(base.playSfx, sfx, volume=volume, node=toon))
    duration = toon.getDuration('confused')
    return (track, duration, None)


def doSlipForward(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/MG_cannon_hit_dirt.ogg')
    track = Sequence(Func(toon.play, 'slip-forward'), Wait(0.7), Func(base.playSfx, sfx, volume=volume, node=toon))
    duration = toon.getDuration('slip-forward') - 0.7
    return (track, duration, None)


def doBored(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/avatar_emotion_bored.ogg')
    track = Sequence(Func(toon.play, 'bored'), Wait(2.2), Func(base.playSfx, sfx, volume=volume, node=toon))
    duration = toon.getDuration('bored') - 2.2
    return (track, duration, None)


def doBow(toon, volume = 1):
    animation = 'curtsy' if toon.style.torso[1] == 'd' else 'bow'
    track = Func(toon.play, animation)
    duration = toon.getDuration(animation)
    return (track, duration, None)


def doSlipBackward(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/MG_cannon_hit_dirt.ogg')
    track = Sequence(Func(toon.play, 'slip-backward'), Wait(0.7), Func(base.playSfx, sfx, volume=volume, node=toon))
    duration = toon.getDuration('slip-backward') - 0.7
    return (track, duration, None)


def doThink(toon, volume = 1):
    track = Sequence(ActorInterval(toon, 'think', startFrame=0, endFrame=46), ActorInterval(toon, 'think', startFrame=46, endFrame=0), duration=0)
    duration = toon.getDuration('think', toFrame=46) * 2
    return (track, duration, None)


def doIdea(toon, volume = 1):
    track = Func(toon.play, 'think')
    duration = toon.getDuration('think')
    return (track, duration, None)


def doCringe(toon, volume = 1):
    track = Func(toon.play, 'cringe')
    duration = toon.getDuration('cringe')
    return (track, duration, None)


def doResistanceSalute(toon, volume = 1):
    track = Sequence(Func(toon.setChatAbsolute, OTPLocalizer.CustomSCStrings[4020], CFSpeech | CFTimeout), Func(toon.setPlayRate, 0.75, 'victory'), Func(toon.pingpong, 'victory', fromFrame=0, toFrame=9), Func(toon.setPlayRate, 1, 'victory'))
    duration = 20 / toon.getFrameRate('victory')
    return (track, duration, None)


def doSurprise(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/avatar_emotion_surprise.ogg')
    anim = Sequence(ActorInterval(toon, 'conked', startFrame=9, endFrame=50), ActorInterval(toon, 'conked', startFrame=70, endFrame=101))
    track = Sequence(Func(toon.stopBlink), Func(toon.surpriseEyes), Func(toon.showMuzzle, 'surprise'), Parallel(Func(anim.start), Func(base.playSfx, sfx, volume=volume, node=toon)))
    exitTrack = Sequence(Func(toon.showMuzzle, 'neutral'), Func(toon.openEyes), Func(toon.startBlink), Func(anim.finish), Func(toon.stop), Func(sfx.stop))
    return (track, 3, exitTrack)


def doCry(toon, volume = 1):
    sfx = loader.loadSfx(random.choice(('phase_4/audio/sfx/avatar_emotion_very_sad_1.ogg', 'phase_4/audio/sfx/avatar_emotion_very_sad.ogg')))
    anim = Sequence(ActorInterval(toon, 'bad-putt', startFrame=29, endFrame=59, playRate=-0.75), ActorInterval(toon, 'bad-putt', startFrame=29, endFrame=59, playRate=0.75))
    track = Sequence(Func(toon.sadEyes), Func(toon.blinkEyes), Func(toon.showMuzzle, 'sad'), Parallel(Func(anim.start), Func(base.playSfx, sfx, volume=volume, node=toon)))
    exitTrack = Sequence(Func(toon.showMuzzle, 'neutral'), Func(toon.normalEyes), Func(anim.finish), Func(toon.stop), Func(sfx.stop))
    return (track, 4, exitTrack)


def doDelighted(toon, direction, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/delighted_06.ogg')
    anim = Sequence(ActorInterval(toon, direction), Wait(1), ActorInterval(toon, direction, playRate=-1))
    track = Sequence(Func(toon.blinkEyes), Func(toon.showMuzzle, 'smile'), Parallel(Func(anim.start), Func(base.playSfx, sfx, volume=volume, node=toon)))
    exitTrack = Sequence(Func(toon.showMuzzle, 'neutral'), Func(toon.blinkEyes), Func(anim.finish), Func(toon.stop), Func(sfx.stop))
    return (track, 2.5, exitTrack)


def doDelightedLeft(toon, volume = 1):
    return doDelighted(toon, 'left', volume)


def doDelightedRight(toon, volume = 1):
    return doDelighted(toon, 'right', volume)


def doFurious(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/furious_03.ogg')
    track = Sequence(Func(toon.angryEyes), Func(toon.blinkEyes), Func(toon.showMuzzle, 'angry'), Func(toon.play, 'angry'), Func(base.playSfx, sfx, volume=volume, node=toon))
    exitTrack = Sequence(Func(toon.normalEyes), Func(toon.blinkEyes), Func(toon.showMuzzle, 'neutral'))
    duration = toon.getDuration('angry')
    return (track, duration, exitTrack)


def doLaugh(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/avatar_emotion_laugh.ogg')
    track = Sequence(Func(toon.blinkEyes), Func(toon.showMuzzle, 'laugh'), Func(toon.setPlayRate, 10, 'neutral'), Func(toon.loop, 'neutral'), Func(base.playSfx, sfx, volume=volume, node=toon))
    exitTrack = Sequence(Func(toon.showMuzzle, 'neutral'), Func(toon.blinkEyes), Func(toon.setPlayRate, 1, 'neutral'))
    return (track, 2, exitTrack)


def doTaunt(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/avatar_emotion_taunt.ogg')
    track = Sequence(Func(toon.blinkEyes), Func(toon.play, 'taunt'), Func(base.playSfx, sfx, volume=volume, node=toon))
    duration = toon.getDuration('taunt')
    return (track, duration, None)


def doRage(toon, volume = 1):
    sfx = loader.loadSfx('phase_4/audio/sfx/furious_03.ogg')
    track = Sequence(Func(toon.blinkEyes), Func(toon.play, 'good-putt', fromFrame=12), Func(base.playSfx, sfx, volume=volume, node=toon))
    duration = toon.getDuration('good-putt', fromFrame=12)
    return (track, duration, None)


def returnToLastAnim(toon):
    if hasattr(toon, 'playingAnim') and toon.playingAnim:
        toon.loop(toon.playingAnim)
    elif not hasattr(toon, 'hp') or toon.hp > 0:
        toon.loop('neutral')
    else:
        toon.loop('sad-neutral')


EmoteFunc = [doWave,
 doHappy,
 doSad,
 doBitter,
 doAngry,
 doSleep,
 doShrug,
 doDance,
 doThink,
 doBored,
 doApplause,
 doCringe,
 doConfused,
 doSlipForward,
 doSlipBackward,
 doBow,
 doResistanceSalute,
 doSurprise,
 doCry,
 doDelightedLeft,
 doDelightedRight,
 doFurious,
 doLaugh,
 doIdea,
 doTaunt,
 doRage]
Emotes = ['wave',
 'happy',
 'sad',
 'bitter',
 'angry',
 'sleep',
 'shrug',
 'dance',
 'think',
 'bored',
 'applause',
 'cringe',
 'confused',
 'slip-forward',
 'slip-backward',
 'bow',
 'resistance-salute',
 'surprise',
 'cry',
 'delighted-left',
 'delighted-right',
 'furious',
 'laugh',
 'idea',
 'taunt',
 'rage']
EmoteNum = len(Emotes)
EmoteIds = range(EmoteNum)
HeadEmotes = [2, 3]
BodyEmotes = [ x for x in EmoteIds if x not in HeadEmotes ]

class TTEmote:
    notify = DirectNotifyGlobal.directNotify.newCategory('TTEmote')
    EmoteEnableStateChanged = 'EmoteEnableStateChanged'

    def __init__(self):
        if len(Emotes) != len(OTPLocalizer.EmoteList):
            self.notify.error('TTEmote.Emotes and OTPLocalizer.EmoteList are different lengths.')
        self.emoteState = [0] * EmoteNum

    def isValidEmote(self, emote):
        return emote >= 0 and emote < EmoteNum

    def isEnabled(self, emote):
        return self.isValidEmote(emote) and not self.emoteState[emote]

    def isLocal(self, toon):
        return hasattr(base, 'localAvatar') and toon == base.localAvatar

    def clearEmoteTrack(self, toon):
        if not self.isLocal(toon):
            return
        else:
            toon.emoteTrack = None
            toon.d_setEmoteState(EmoteClear, 1.0)
            return

    def offsetStatus(self, emotes, toon, offset):
        if not self.isLocal(toon):
            return
        for emote in emotes:
            self.emoteState[emote] += offset
            if self.emoteState[emote] < 0:
                self.emoteState[emote] = 0

        messenger.send(self.EmoteEnableStateChanged)

    def disableAll(self, toon, msg = None):
        self.offsetStatus(EmoteIds, toon, 1)

    def disableBody(self, toon, msg = None):
        self.offsetStatus(BodyEmotes, toon, 1)

    def disableHead(self, toon, msg = None):
        self.offsetStatus(HeadEmotes, toon, 1)

    def releaseAll(self, toon, msg = None):
        self.offsetStatus(EmoteIds, toon, -1)

    def releaseBody(self, toon, msg = None):
        self.offsetStatus(BodyEmotes, toon, -1)

    def releaseHead(self, toon, msg = None):
        self.offsetStatus(HeadEmotes, toon, -1)

    def doEmote(self, toon, emoteIndex, ts = 0, volume = 1, start = True):
        if not self.isValidEmote(emoteIndex):
            return (None, None)
        else:
            track, duration, exitTrack = EmoteFunc[emoteIndex](toon, volume)
            if not track or not duration:
                return (None, None)
            if not exitTrack:
                exitTrack = Sequence()
            track = Sequence(Func(self.disableAll, toon), track, Wait(duration), exitTrack, Func(returnToLastAnim, toon), Func(self.releaseAll, toon), Func(self.clearEmoteTrack, toon), autoFinish=1)
            if start:
                if toon.emoteTrack:
                    toon.emoteTrack.finish()
                toon.emoteTrack = track
                track.start(ts)
            return (track, duration)


Emote.globalEmote = TTEmote()