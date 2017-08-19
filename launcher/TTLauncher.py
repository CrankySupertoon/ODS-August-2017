# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.launcher.TTLauncher
from panda3d.core import Filename, HTTPClient, MultiplexStream, Notify, StreamWriter
from direct.directnotify import DirectNotifyGlobal, Notifier
import os
import sys
import time

class LogAndOutput:

    def __init__(self, orig, log):
        self.orig = orig
        self.log = log

    def write(self, str):
        self.log.write(str)
        self.log.flush()
        self.orig.write(str)
        self.orig.flush()

    def flush(self):
        self.log.flush()
        self.orig.flush()


class TTLauncher:
    notify = DirectNotifyGlobal.directNotify.newCategory('TTLauncher')

    def __init__(self):
        self.http = HTTPClient()
        if sys.platform == 'android':
            return
        ltime = 1 and time.localtime()
        logSuffix = '%02d%02d%02d_%02d%02d%02d' % (ltime[0] - 2000,
         ltime[1],
         ltime[2],
         ltime[3],
         ltime[4],
         ltime[5])
        if not os.path.exists('user/logs/'):
            os.mkdir('user/logs/')
            self.notify.info('Made new directory to save logs.')
        logfile = os.path.join('user/logs', logSuffix + '.log')
        log = open(logfile, 'a')
        logOut = LogAndOutput(sys.stdout, log)
        logErr = LogAndOutput(sys.stderr, log)
        sys.stdout = logOut
        sys.stderr = logErr
        self.nout = MultiplexStream()
        Notify.ptr().setOstreamPtr(self.nout, 0)
        Notifier.Notifier.streamWriter = StreamWriter(self.nout, False)
        self.nout.addFile(Filename(logfile))
        self.nout.addStandardOutput()

    def setPandaErrorCode(self):
        pass

    def setDisconnectDetails(self, disconnectCode, disconnectMsg):
        self.disconnectCode = disconnectCode
        self.disconnectMsg = disconnectMsg

    def setDisconnectDetailsNormal(self):
        self.setDisconnectDetails(0, 'normal')