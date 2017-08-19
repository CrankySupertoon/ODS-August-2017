# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toonbase.ToonBase
from panda3d.core import Camera, Connection, CullBinManager, DSearchPath, Filename, Lens, MouseWatcher, PGButton, TrueClock, URLSpec, VirtualFile, VirtualFileSystem, WindowProperties, loadPrcFile, loadPrcFileData
import atexit
from direct.directnotify import DirectNotifyGlobal
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.showbase.PythonUtil import *
from direct.showbase.Transitions import Transitions
from direct.task import *
from direct.interval.IntervalGlobal import *
import math
import os
import random
import shutil
from sys import platform
import sys
import time
import ToontownGlobals
from otp.otpbase import OTPBase
from otp.otpbase import OTPGlobals
from otp.nametag.ChatBalloon import ChatBalloon
from otp.nametag import NametagGlobals
from otp.margins.MarginManager import MarginManager
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownBattleGlobals
from toontown.toontowngui import TTDialog
from ToontownTransitions import ToontownTransitions
from toontown.toontowngui.CameraViewfinder import CameraViewfinder
from toontown.uberdog.ARGManager import ARGManager
if sys.platform != 'android':
    import tempfile
    tempdir = tempfile.mkdtemp()
    vfs = VirtualFileSystem.getGlobalPtr()
    searchPath = DSearchPath()
    searchPath.appendDirectory(Filename('/phase_3/etc'))
    for filename in ['toonmono.cur', 'icon.ico']:
        p3filename = Filename(filename)
        found = vfs.resolveFilename(p3filename, searchPath)
        if not found:
            continue
        with open(os.path.join(tempdir, filename), 'wb') as f:
            f.write(vfs.readFile(p3filename, False))

    loadPrcFileData('Window: icon', 'icon-filename %s' % Filename.fromOsSpecific(os.path.join(tempdir, 'icon.ico')))
else:
    tempdir = ''

class ToonBase(OTPBase.OTPBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonBase')

    def __init__(self):
        OTPBase.OTPBase.__init__(self)
        self.disableShowbaseMouse()
        self.addCullBins()
        self.debugRunningMultiplier /= OTPGlobals.ToonSpeedFactor
        self.toonChatSounds = self.config.GetBool('toon-chat-sounds', 1)
        self.placeBeforeObjects = self.config.GetBool('place-before-objects', 1)
        self.endlessQuietZone = False
        self.wantDynamicShadows = 0
        self.exitErrorCode = 0
        camera.setPosHpr(0, 0, 0, 0, 0, 0)
        self.camLens.setMinFov(settings['fov'] / (4.0 / 3.0))
        self.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        self.musicManager.setVolume(0.65)
        if settings['greenScreen']:
            ToontownGlobals.DefaultBackgroundColor = (0, 1, 0, 1)
        self.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        self.transitions = ToontownTransitions()
        self.argManager = ARGManager()
        self.exitFunc = self.userExit
        globalClock.setMaxDt(0.2)
        self.enableParticles()
        self.__listenForScreenshots()
        self.initShadowTrav()
        self.accept('disableScreenShotCam', self.disableScreenShotCam)
        if platform == 'darwin':
            self.acceptOnce(ToontownGlobals.QuitGameHotKeyOSX, self.exitOSX)
            self.accept(ToontownGlobals.QuitGameHotKeyRepeatOSX, self.exitOSX)
            self.acceptOnce(ToontownGlobals.HideGameHotKeyOSX, self.hideGame)
            self.accept(ToontownGlobals.HideGameHotKeyRepeatOSX, self.hideGame)
            self.acceptOnce(ToontownGlobals.MinimizeGameHotKeyOSX, self.minimizeGame)
            self.accept(ToontownGlobals.MinimizeGameHotKeyRepeatOSX, self.minimizeGame)
        self.nametagsHidden = False
        self.accept('f2', self.toggleNametags)
        self.accept('f3', self.toggleGui)
        self.accept('f4', self.oobe)
        self.accept('panda3d-render-error', self.panda3dRenderError)
        self.accept('PandaPaused', self.disableAllAudio)
        self.accept('PandaRestarted', self.enableAllAudio)
        self.wantPets = self.config.GetBool('want-pets', 1)
        self.wantBingo = self.config.GetBool('want-fish-bingo', 1)
        self.wantKarts = self.config.GetBool('want-karts', 1)
        self.inactivityTimeout = self.config.GetFloat('inactivity-timeout', ToontownGlobals.KeyboardTimeout)
        if self.inactivityTimeout:
            self.notify.debug('Enabling Panda timeout: %s' % self.inactivityTimeout)
            self.mouseWatcherNode.setInactivityTimeout(self.inactivityTimeout)
        self.mouseWatcherNode.setEnterPattern('mouse-enter-%r')
        self.mouseWatcherNode.setLeavePattern('mouse-leave-%r')
        self.mouseWatcherNode.setButtonDownPattern('button-down-%r')
        self.mouseWatcherNode.setButtonUpPattern('button-up-%r')
        self.autoPlayAgain = self.config.GetBool('auto-play-again', 0)
        self.skipMinigameReward = self.config.GetBool('skip-minigame-reward', 0)
        self.wantMinigameDifficulty = self.config.GetBool('want-minigame-difficulty', 0)
        self.minigameDifficulty = self.config.GetFloat('minigame-difficulty', -1.0)
        if self.minigameDifficulty == -1.0:
            del self.minigameDifficulty
        self.minigameSafezoneId = self.config.GetInt('minigame-safezone-id', -1)
        if self.minigameSafezoneId == -1:
            del self.minigameSafezoneId
        cogdoGameSafezoneId = self.config.GetInt('cogdo-game-safezone-id', -1)
        cogdoGameDifficulty = self.config.GetFloat('cogdo-game-difficulty', -1)
        if cogdoGameDifficulty != -1:
            self.cogdoGameDifficulty = cogdoGameDifficulty
        if cogdoGameSafezoneId != -1:
            self.cogdoGameSafezoneId = cogdoGameSafezoneId
        ToontownBattleGlobals.SkipMovie = self.config.GetBool('skip-battle-movies', 0)
        self.housingEnabled = self.config.GetBool('want-housing', 1)
        self.cannonsEnabled = self.config.GetBool('estate-cannons', 0)
        self.fireworksEnabled = self.config.GetBool('estate-fireworks', 0)
        self.dayNightEnabled = self.config.GetBool('estate-day-night', 0)
        self.cloudPlatformsEnabled = self.config.GetBool('estate-clouds', 0)
        self.slowQuietZone = self.config.GetBool('slow-quiet-zone', 0)
        self.slowQuietZoneDelay = self.config.GetFloat('slow-quiet-zone-delay', 5)
        self.killInterestResponse = self.config.GetBool('kill-interest-response', 0)
        self.oldX = max(1, base.win.getXSize())
        self.oldY = max(1, base.win.getYSize())
        self.aspectRatio = float(self.oldX) / self.oldY
        self.snapshotSfx = loader.loadSfx('phase_4/audio/sfx/Photo_shutter.ogg')
        self.flashTrack = None
        self.viewfinder = None
        self.monsters = []
        return

    def getServerVersion(self):
        return config.GetString('server-version', '')

    def getMainTheme(self):
        if settings['musicEasterEgg'] and settings.get('preferredShard') == 'Toon Valley':
            return loader.loadMusic('phase_3/audio/bgm/tt_joke_theme.ogg')
        else:
            return loader.loadMusic('phase_3/audio/bgm/tt_theme.ogg')

    def openMainWindow(self, *args, **kw):
        result = OTPBase.OTPBase.openMainWindow(self, *args, **kw)
        self.setCursorAndIcon()
        return result

    def setCursorAndIcon(self):
        if not tempdir:
            return
        atexit.register(shutil.rmtree, tempdir)
        wp = WindowProperties()
        wp.setCursorFilename(Filename.fromOsSpecific(os.path.join(tempdir, 'toonmono.cur')))
        wp.setIconFilename(Filename.fromOsSpecific(os.path.join(tempdir, 'icon.ico')))
        self.win.requestProperties(wp)

    def addCullBins(self):
        cbm = CullBinManager.getGlobalPtr()
        cbm.addBin('ground', CullBinManager.BTUnsorted, 18)
        cbm.addBin('shadow', CullBinManager.BTBackToFront, 19)
        cbm.addBin('gui-popup', CullBinManager.BTUnsorted, 60)

    def disableShowbaseMouse(self):
        self.useDrive()
        self.disableMouse()
        if self.mouseInterface:
            self.mouseInterface.detachNode()
        if self.mouse2cam:
            self.mouse2cam.detachNode()

    def toggleNametags(self):
        from otp.nametag import Nametag
        if self.nametagsHidden:
            for nametag in Nametag.AllNametags:
                nametag.show()

        else:
            for nametag in Nametag.AllNametags:
                nametag.hide()

        self.nametagsHidden = not self.nametagsHidden

    def toggleGui(self):
        if aspect2d.isHidden():
            aspect2d.show()
        else:
            aspect2d.hide()

    def __listenForScreenshots(self, task = None):
        self.accept(ToontownGlobals.ScreenshotHotkey, self.takeScreenShot)
        self.accept(ToontownGlobals.ScreenshotCameraHotkey, self.enableScreenShotCam)

    def takeScreenShot(self):
        if self.flashTrack and self.flashTrack.isPlaying():
            return
        if not os.path.exists(TTLocalizer.ScreenshotPath):
            os.mkdir(TTLocalizer.ScreenshotPath)
            self.notify.info('Made new directory to save screenshots.')
        namePrefix = TTLocalizer.ScreenshotPath + 'screenshot'
        if self.viewfinder:
            render2d.hide()
        self.graphicsEngine.renderFrame()
        messenger.send('takeScreenShot')
        if self.viewfinder:
            render2d.show()
        self.screenshot(namePrefix=namePrefix)
        base.playSfx(self.snapshotSfx)
        self.transitions.setFadeColor(1, 1, 1)
        self.transitions.fadeOut(0.15)
        self.flashTrack = Sequence(Func(self.transitions.fadeIn, 0.8), Wait(1), Func(self.transitions.setFadeColor, 0, 0, 0), Func(self.__listenForScreenshots))
        self.flashTrack.start()

    def enableScreenShotCam(self):
        if not hasattr(self, 'localAvatar') or not self.localAvatar or not self.cr.playGame.place or not self.cr.playGame.place.fsm or self.cr.playGame.place.fsm.getCurrentState().getName() != 'walk':
            return
        if self.flashTrack and self.flashTrack.isPlaying():
            return
        if self.viewfinder:
            self.disableScreenShotCam()
            return
        self.localAvatar.fpsMode = True
        self.localAvatar.startUpdateSmartCamera()
        self.viewfinder = CameraViewfinder()

    def disableScreenShotCam(self):
        if not self.viewfinder:
            return
        else:
            self.viewfinder.removeNode()
            self.viewfinder = None
            self.localAvatar.stopUpdateSmartCamera()
            self.localAvatar.fpsMode = False
            self.__listenForScreenshots()
            if self.cr.playGame.place.fsm.getCurrentState().getName() == 'walk':
                self.localAvatar.startUpdateSmartCamera()
            return

    def initNametagGlobals(self):
        arrow = loader.loadModel('phase_3/models/props/arrow')
        card = loader.loadModel('phase_3/models/props/panel')
        speech3d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox'))
        thought3d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox_thought_cutout'))
        speech2d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox_noarrow'))
        chatButtonGui = loader.loadModel('phase_3/models/gui/chat_button_gui')
        NametagGlobals.setCamera(self.cam)
        NametagGlobals.setArrowModel(arrow)
        NametagGlobals.setNametagCard(card)
        if self.mouseWatcherNode:
            NametagGlobals.setMouseWatcher(self.mouseWatcherNode)
        NametagGlobals.setSpeechBalloon3d(speech3d)
        NametagGlobals.setThoughtBalloon3d(thought3d)
        NametagGlobals.setSpeechBalloon2d(speech2d)
        NametagGlobals.setThoughtBalloon2d(thought3d)
        NametagGlobals.setPageButton(PGButton.SReady, chatButtonGui.find('**/Horiz_Arrow_UP'))
        NametagGlobals.setPageButton(PGButton.SDepressed, chatButtonGui.find('**/Horiz_Arrow_DN'))
        NametagGlobals.setPageButton(PGButton.SRollover, chatButtonGui.find('**/Horiz_Arrow_Rllvr'))
        NametagGlobals.setQuitButton(PGButton.SReady, chatButtonGui.find('**/CloseBtn_UP'))
        NametagGlobals.setQuitButton(PGButton.SDepressed, chatButtonGui.find('**/CloseBtn_DN'))
        NametagGlobals.setQuitButton(PGButton.SRollover, chatButtonGui.find('**/CloseBtn_Rllvr'))
        rolloverSound = DirectGuiGlobals.getDefaultRolloverSound()
        if rolloverSound:
            NametagGlobals.setRolloverSound(rolloverSound)
        clickSound = DirectGuiGlobals.getDefaultClickSound()
        if clickSound:
            NametagGlobals.setClickSound(clickSound)
        NametagGlobals.setToon(self.cam)
        self.marginManager = MarginManager()
        self.margins = self.aspect2d.attachNewNode(self.marginManager, DirectGuiGlobals.MIDGROUND_SORT_INDEX + 1)
        mm = self.marginManager
        padding = 0.0225
        self.leftCells = [mm.addGridCell(0.2 + padding, -0.45, base.a2dTopLeft), mm.addGridCell(0.2 + padding, -0.9, base.a2dTopLeft), mm.addGridCell(0.2 + padding, -1.35, base.a2dTopLeft)]
        self.bottomCells = [mm.addGridCell(-0.87, 0.2 + padding, base.a2dBottomCenter),
         mm.addGridCell(-0.43, 0.2 + padding, base.a2dBottomCenter),
         mm.addGridCell(0.01, 0.2 + padding, base.a2dBottomCenter),
         mm.addGridCell(0.45, 0.2 + padding, base.a2dBottomCenter),
         mm.addGridCell(0.89, 0.2 + padding, base.a2dBottomCenter)]
        self.rightCells = [mm.addGridCell(-0.2 - padding, -1.35, base.a2dTopRight), mm.addGridCell(-0.2 - padding, -0.9, base.a2dTopRight), mm.addGridCell(-0.2 - padding, -0.45, base.a2dTopRight)]

    def hideFriendMargins(self):
        middleCell = self.rightCells[1]
        topCell = self.rightCells[2]
        self.setCellsAvailable([middleCell, topCell], False)

    def showFriendMargins(self):
        middleCell = self.rightCells[1]
        topCell = self.rightCells[2]
        self.setCellsAvailable([middleCell, topCell], True)

    def setCellsAvailable(self, cell_list, available):
        for cell in cell_list:
            self.marginManager.setCellAvailable(cell, available)

    def startShow(self, cr):
        self.cr = cr
        base.graphicsEngine.renderFrame()
        if base.pipe.getInterfaceName() == 'TinyPanda':
            cr.handleNoConnection(TTLocalizer.TinyPandaWarning, self.__sawTinyPanda, (0, 0.85, 0.4), False)
        elif self.hasIntegratedGraphics():
            if not settings.get('igWarning', False):
                cr.handleNoConnection(TTLocalizer.IntegratedGraphicsWarning, self.__sawIntegratedGraphics, (0.08, 0.85, 0.4))
            else:
                cr.startConnecting()
        else:
            cr.startConnecting()
            settings['igWarning'] = False
        self.lastSpeedHackCheck = time.time()
        self.lastTrueClockTime = TrueClock.getGlobalPtr().getLongTime()
        taskMgr.add(self.__speedHackCheckTick, 'speedHackCheck-tick')

    def createServerList(self):
        serverPort = config.GetInt('server-port', 7199)
        clientagents = config.GetInt('client-agents', 1) - 1
        serverPort += random.randint(0, clientagents) * 100
        self.serverList = []
        for name in self.cr.gameServer.split(';'):
            url = URLSpec(name, 1)
            if config.GetBool('server-force-ssl', False):
                url.setScheme('s')
            if not url.hasPort():
                url.setPort(serverPort)
            self.serverList.append(url)

    def __sawTinyPanda(self):
        sys.exit()

    def __sawIntegratedGraphics(self):
        settings['igWarning'] = True
        self.cr.cleanupNoConnection()
        self.cr.startConnecting()

    def hasIntegratedGraphics(self):
        vendor = base.win.getGsg().getDriverVendor()
        return 'Intel' in vendor or 'PowerVR' in vendor

    def __speedHackCheckTick(self, task):
        elapsed = time.time() - self.lastSpeedHackCheck
        tcElapsed = TrueClock.getGlobalPtr().getLongTime() - self.lastTrueClockTime
        if tcElapsed > elapsed + 0.05:
            self.cr.stopReaderPollTask()
            self.cr.lostConnection()
            return task.done
        self.lastSpeedHackCheck = time.time()
        self.lastTrueClockTime = TrueClock.getGlobalPtr().getLongTime()
        return task.cont

    def exitShow(self, errorCode = None):
        self.notify.info('Exiting Toontown: errorCode = %s' % errorCode)
        sys.exit()

    def setExitErrorCode(self, code):
        self.exitErrorCode = code

    def getExitErrorCode(self):
        return self.exitErrorCode

    def userExit(self):
        try:
            self.localAvatar.d_setAnimState('TeleportOut', 1)
        except:
            pass

        if self.cr.miscManager:
            self.cr.miscManager.setDisconnectReason(ToontownGlobals.DisconnectCloseWindow)
        base.cr._userLoggingOut = False
        try:
            localAvatar
        except:
            pass
        else:
            messenger.send('clientLogout')
            self.cr.dumpAllSubShardObjects()

        self.cr.loginFSM.request('shutdown')
        self.notify.warning('Could not request shutdown; exiting anyway.')
        self.ignore(ToontownGlobals.QuitGameHotKeyOSX)
        self.ignore(ToontownGlobals.QuitGameHotKeyRepeatOSX)
        self.ignore(ToontownGlobals.HideGameHotKeyOSX)
        self.ignore(ToontownGlobals.HideGameHotKeyRepeatOSX)
        self.ignore(ToontownGlobals.MinimizeGameHotKeyOSX)
        self.ignore(ToontownGlobals.MinimizeGameHotKeyRepeatOSX)
        self.exitShow()

    def panda3dRenderError(self):
        if self.cr.miscManager:
            self.cr.miscManager.setDisconnectReason(ToontownGlobals.DisconnectGraphicsError)
        self.cr.sendDisconnect()
        sys.exit()

    def playMusic(self, music, looping = 0, interrupt = 1, volume = None, time = 0.0):
        if music.status() == music.PLAYING and music.getLoop() == looping:
            if volume is not None and music.getVolume() != volume:
                music.setVolume(volume)
            return
        else:
            OTPBase.OTPBase.playMusic(self, music, looping, interrupt, volume, time)
            return

    def fadeMusic(self, music, duration):
        if music.status() != music.PLAYING:
            return
        Sequence(LerpFunc(music.setVolume, fromData=music.getVolume(), toData=0, duration=duration), Func(music.stop)).start()

    def exitOSX(self):
        self.confirm = TTDialog.TTGlobalDialog(doneEvent='confirmDone', message=TTLocalizer.OptionsPageExitConfirm, style=TTDialog.TwoChoice)
        self.confirm.show()
        self.accept('confirmDone', self.handleConfirm)

    def handleConfirm(self):
        status = self.confirm.doneStatus
        self.ignore('confirmDone')
        self.confirm.cleanup()
        del self.confirm
        if status == 'ok':
            self.userExit()

    def hideGame(self):
        hideCommand = 'osascript -e \'tell application "System Events"\n                                            set frontProcess to first process whose frontmost is true\n                                            set visible of frontProcess to false\n                                       end tell\''
        os.system(hideCommand)

    def minimizeGame(self):
        wp = WindowProperties()
        wp.setMinimized(True)
        base.win.requestProperties(wp)