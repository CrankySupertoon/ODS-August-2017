# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.battle.MovieSOS
from panda3d.core import Camera
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
import MovieCamera
from otp.nametag.NametagConstants import *
from otp.nametag import NametagGlobals
from toontown.toonbase import TTLocalizer
notify = DirectNotifyGlobal.directNotify.newCategory('MovieSOS')

def doSOSs(calls):
    if len(calls) == 0:
        return (None, None)
    else:

        def callerFunc(toon, handle):
            toon.setChatAbsolute(TTLocalizer.MovieSOSCallHelp % handle.getName(), CFSpeech | CFTimeout)
            handle.d_battleSOS(handle.doId)

        def calleeFunc(toon, handle):
            toon.setChatAbsolute(TTLocalizer.MovieSOSCallHelp % handle.getName(), CFSpeech | CFTimeout)

        def observerFunc(toon):
            toon.setChatAbsolute(TTLocalizer.MovieSOSObserverHelp, CFSpeech | CFTimeout)

        mtrack = Sequence()
        for c in calls:
            toon = c['toon']
            targetType = c['targetType']
            handle = c['target']
            mtrack.append(Wait(0.5))
            if targetType == 'observer':
                ival = Func(observerFunc, toon)
            elif targetType == 'caller':
                ival = Func(callerFunc, toon, handle)
            elif targetType == 'callee':
                ival = Func(calleeFunc, toon, handle)
            else:
                notify.error('invalid target type: %s' % targetType)
            mtrack.append(ival)
            mtrack.append(Wait(2.0))
            notify.debug('toon: %s calls for help' % toon.getName())

        camDuration = mtrack.getDuration()
        camTrack = MovieCamera.chooseSOSShot(toon, camDuration)
        return (mtrack, camTrack)