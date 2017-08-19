# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.shtiker.OptionsPage
from panda3d.core import AntialiasAttrib, FrameRateMeter, Lens, TextNode, Vec4
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from direct.showbase import PythonUtil
from direct.task import Task
import DisplaySettingsDialog
import ShtikerPage
import OptionChooser
import ControlConfigDialog
from otp.avatar import Avatar
from otp.speedchat import SCColorScheme
from otp.speedchat import SCStaticTextTerminal
from otp.speedchat import SpeedChat
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toon import Toon
from toontown.toontowngui import TTDialog
from BookElements import *
from toontown.fishing import FishGlobals
import sys
speedChatStyles = ((2000,
  (200 / 255.0, 60 / 255.0, 229 / 255.0),
  (200 / 255.0, 135 / 255.0, 255 / 255.0),
  (220 / 255.0, 195 / 255.0, 229 / 255.0)),
 (2012,
  (142 / 255.0, 151 / 255.0, 230 / 255.0),
  (173 / 255.0, 180 / 255.0, 237 / 255.0),
  (220 / 255.0, 195 / 255.0, 229 / 255.0)),
 (2001,
  (0 / 255.0, 0 / 255.0, 255 / 255.0),
  (140 / 255.0, 150 / 255.0, 235 / 255.0),
  (201 / 255.0, 215 / 255.0, 255 / 255.0)),
 (2010,
  (0 / 255.0, 119 / 255.0, 190 / 255.0),
  (53 / 255.0, 180 / 255.0, 255 / 255.0),
  (201 / 255.0, 215 / 255.0, 255 / 255.0)),
 (2014,
  (0 / 255.0, 64 / 255.0, 128 / 255.0),
  (0 / 255.0, 64 / 255.0, 128 / 255.0),
  (201 / 255.0, 215 / 255.0, 255 / 255.0)),
 (2002,
  (90 / 255.0, 175 / 255.0, 225 / 255.0),
  (120 / 255.0, 215 / 255.0, 255 / 255.0),
  (208 / 255.0, 230 / 255.0, 250 / 255.0)),
 (2003,
  (130 / 255.0, 235 / 255.0, 235 / 255.0),
  (120 / 255.0, 225 / 255.0, 225 / 255.0),
  (234 / 255.0, 255 / 255.0, 255 / 255.0)),
 (2004,
  (0 / 255.0, 200 / 255.0, 70 / 255.0),
  (0 / 255.0, 200 / 255.0, 80 / 255.0),
  (204 / 255.0, 255 / 255.0, 204 / 255.0)),
 (2015,
  (13 / 255.0, 255 / 255.0, 100 / 255.0),
  (64 / 255.0, 255 / 255.0, 131 / 255.0),
  (204 / 255.0, 255 / 255.0, 204 / 255.0)),
 (2005,
  (235 / 255.0, 230 / 255.0, 0 / 255.0),
  (255 / 255.0, 250 / 255.0, 100 / 255.0),
  (255 / 255.0, 250 / 255.0, 204 / 255.0)),
 (2006,
  (255 / 255.0, 153 / 255.0, 0 / 255.0),
  (229 / 255.0, 147 / 255.0, 0 / 255.0),
  (255 / 255.0, 234 / 255.0, 204 / 255.0)),
 (2011,
  (255 / 255.0, 177 / 255.0, 62 / 255.0),
  (255 / 255.0, 200 / 255.0, 117 / 255.0),
  (255 / 255.0, 234 / 255.0, 204 / 255.0)),
 (2007,
  (255 / 255.0, 0 / 255.0, 50 / 255.0),
  (229 / 255.0, 0 / 255.0, 50 / 255.0),
  (255 / 255.0, 204 / 255.0, 204 / 255.0)),
 (2013,
  (130 / 255.0, 0 / 255.0, 26 / 255.0),
  (179 / 255.0, 0 / 255.0, 50 / 255.0),
  (255 / 255.0, 204 / 255.0, 204 / 255.0)),
 (2016,
  (176 / 255.0, 35 / 255.0, 0 / 255.0),
  (240 / 255.0, 48 / 255.0, 0 / 255.0),
  (255 / 255.0, 204 / 255.0, 204 / 255.0)),
 (2008,
  (255 / 255.0, 153 / 255.0, 193 / 255.0),
  (240 / 255.0, 157 / 255.0, 192 / 255.0),
  (255 / 255.0, 215 / 255.0, 238 / 255.0)),
 (2009,
  (170 / 255.0, 120 / 255.0, 20 / 255.0),
  (165 / 255.0, 120 / 255.0, 50 / 255.0),
  (210 / 255.0, 200 / 255.0, 180 / 255.0)))
PageMode = PythonUtil.Enum('Options, OptionsTwo, OptionsThree, Codes')
titleHeight = 0.61
textStartHeight = 0.45
textRowHeight = 0.145
leftMargin = -0.72
buttonbase_xcoord = 0.35
buttonbase_ycoord = 0.45
button_image_scale = (0.7, 1, 1)
button_textpos = (0, -0.02)
options_text_scale = 0.052
disabled_arrow_color = Vec4(0.6, 0.6, 0.6, 1.0)
speed_chat_scale = 0.055

def toggleSettingsList(settingName):
    messenger.send('wakeup')
    setting = settings.get(settingName, [])
    avId = base.localAvatar.doId
    if avId in setting:
        setting.remove(avId)
    else:
        setting.append(avId)
    settings[settingName] = setting


class OptionsPage(ShtikerPage.ShtikerPage):
    notify = directNotify.newCategory('OptionsPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.mode = None
        self.optionsTabPage = None
        self.codesTabPage = None
        self.optionsTwoTabPage = None
        self.optionsThreeTabPage = None
        self.title = None
        self.optionsTab = None
        self.codesTab = None
        return

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.optionsTabPage = OptionsTabPage(self)
        self.optionsTabPage.hide()
        self.codesTabPage = CodesTabPage(self)
        self.codesTabPage.hide()
        self.optionsTwoTabPage = OptionsTwoTabPage(self)
        self.optionsTwoTabPage.hide()
        self.optionsThreeTabPage = OptionsThreeTabPage(self)
        self.optionsThreeTabPage.hide()
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.OptionsPageTitle, text_scale=0.12, pos=(0, 0, 0.61))
        gui = loader.loadModel('phase_3.5/models/gui/fishingBook')
        normalColor = (1, 1, 1, 1)
        clickColor = (0.8, 0.8, 0, 1)
        rolloverColor = (0.15, 0.82, 1.0, 1)
        diabledColor = (1.0, 0.98, 0.15, 1)
        self.leftArrow = Button(parent=self, pos=(-0.33, 0, 0.65), type='yellowArrow', image_scale=0.6, command=self.offsetPageIndex, extraArgs=[-1])
        self.rightArrow = Button(parent=self, pos=(0.33, 0, 0.65), type='yellowArrow', image_scale=-0.6, command=self.offsetPageIndex, extraArgs=[1])
        self.optionsTab = DirectButton(parent=self, relief=None, text=TTLocalizer.OptionsPageTitle, text_scale=TTLocalizer.OPoptionsTab, text_align=TextNode.ALeft, text_pos=(0.01, 0.0, 0.0), image=gui.find('**/tabs/polySurface1'), image_pos=(0.55, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Options], pos=(-0.36, 0, 0.77))
        self.codesTab = DirectButton(parent=self, relief=None, text=TTLocalizer.OptionsPageCodesTab, text_scale=TTLocalizer.OPoptionsTab, text_align=TextNode.ALeft, text_pos=(-0.035, 0.0, 0.0), image=gui.find('**/tabs/polySurface2'), image_pos=(0.12, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Codes], pos=(0.11, 0, 0.77))
        gui.removeNode()
        return

    def enter(self):
        self.setMode(PageMode.Options, updateAnyways=1)
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        self.optionsTabPage.exit()
        self.codesTabPage.exit()
        self.optionsTwoTabPage.exit()
        self.optionsThreeTabPage.exit()
        ShtikerPage.ShtikerPage.exit(self)

    def unload(self):
        if self.optionsTabPage:
            self.optionsTabPage.unload()
            self.optionsTabPage = None
        if self.optionsTwoTabPage:
            self.optionsTwoTabPage.unload()
            self.optionsTwoTabPage = None
        if self.optionsThreeTabPage:
            self.optionsThreeTabPage.unload()
            self.optionsThreeTabPage = None
        if self.codesTabPage:
            self.codesTabPage.unload()
            self.codesTabPage = None
        if self.title:
            self.title.destroy()
            self.title = None
        if self.optionsTab:
            self.optionsTab.destroy()
            self.optionsTab = None
        if self.codesTab:
            self.codesTab.destroy()
            self.codesTab = None
        if self.leftArrow:
            self.leftArrow.destroy()
            self.leftArrow = None
        if self.rightArrow:
            self.rightArrow.destroy()
            self.rightArrow = None
        ShtikerPage.ShtikerPage.unload(self)
        return

    def offsetPageIndex(self, index):
        self.setMode(self.mode + index)

    def setMode(self, mode, updateAnyways = 0):
        if self.mode == mode and not updateAnyways:
            return
        messenger.send('wakeup')
        self.mode = mode
        if mode == PageMode.Options:
            self.title['text'] = TTLocalizer.OptionsPageTitle
            self.optionsTab['state'] = DGG.DISABLED
            self.optionsTabPage.enter()
            self.codesTab['state'] = DGG.NORMAL
            self.codesTabPage.exit()
            self.optionsTwoTabPage.exit()
            self.leftArrow.hide()
            self.rightArrow.show()
        elif mode == PageMode.Codes:
            self.title['text'] = TTLocalizer.CdrPageTitle
            self.optionsTab['state'] = DGG.NORMAL
            self.optionsTabPage.exit()
            self.optionsTwoTabPage.exit()
            self.optionsThreeTabPage.exit()
            self.codesTab['state'] = DGG.DISABLED
            self.codesTabPage.enter()
            self.leftArrow.hide()
            self.rightArrow.hide()
        elif mode == PageMode.OptionsTwo:
            self.optionsTabPage.exit()
            self.optionsTwoTabPage.enter()
            self.optionsThreeTabPage.exit()
            self.leftArrow.show()
            self.rightArrow.show()
        elif mode == PageMode.OptionsThree:
            self.optionsTwoTabPage.exit()
            self.optionsThreeTabPage.enter()
            self.leftArrow.show()
            self.rightArrow.hide()


class OptionsTabPage(DirectFrame):
    notify = directNotify.newCategory('OptionsTabPage')
    DisplaySettingsTaskName = 'save-display-settings'
    DisplaySettingsDelay = 60
    ChangeDisplaySettings = config.GetBool('change-display-settings', 1)
    ChangeDisplayAPI = config.GetBool('change-display-api', 0)

    def __init__(self, parent = aspect2d):
        self.parent = parent
        self.currentSizeIndex = None
        DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()
        return

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)
        return

    def load(self):
        self.displaySettings = None
        self.displaySettingsChanged = 0
        self.displaySettingsSize = (None, None)
        self.displaySettingsFullscreen = None
        self.displaySettingsApi = None
        self.displaySettingsApiChanged = 0
        self.Music_Label = Label(parent=self, text=TTLocalizer.OptionsPageMusic, row=0)
        self.SoundFX_Label = Label(parent=self, text=TTLocalizer.OptionsPageSFX, row=1)
        self.Friends_Label = Label(parent=self, row=3)
        self.Whispers_Label = Label(parent=self, row=4)
        self.DisplaySettings_Label = Label(parent=self, row=5)
        self.SpeedChatStyle_Label = Label(parent=self, text=TTLocalizer.OptionsPageSpeedChatStyleLabel, row=6)
        self.ToonChatSounds_Label = Label(parent=self, row=2, zPadding=0.025, scale=0.9)
        self.Music_toggleSlider = Slider(parent=self, row=0, value=settings['musicVol'] * 100, range=(0, 100), command=self.__doMusicLevel)
        self.SoundFX_toggleSlider = Slider(parent=self, row=1, value=settings['sfxVol'] * 100, range=(0, 100), command=self.__doSfxLevel)
        self.Friends_toggleButton = Button(parent=self, row=3, command=self.__doToggleAcceptFriends)
        self.Whispers_toggleButton = Button(parent=self, row=4, command=self.__doToggleAcceptWhispers)
        self.DisplaySettingsButton = Button(parent=self, row=5, text=TTLocalizer.OptionsPageChange, command=self.__doDisplaySettings)
        self.speedChatStyleLeftArrow = Button(parent=self, row=6, scale=(-1, 1, 1), x=0.25, type='blueArrow', command=self.__doSpeedChatStyleLeft)
        self.speedChatStyleRightArrow = Button(parent=self, row=6, x=0.65, type='blueArrow', command=self.__doSpeedChatStyleRight)
        self.ToonChatSounds_toggleButton = Button(parent=self, row=2, zPadding=0.025, scale=0.8, command=self.__doToggleToonChatSounds)
        self.speedChatStyleText = SpeedChat.SpeedChat(name='OptionsPageStyleText', structure=[2000])
        self.speedChatStyleText.setScale(speed_chat_scale)
        self.speedChatStyleText.setPos(0.37, 0, buttonbase_ycoord - textRowHeight * 6 + 0.03)
        self.speedChatStyleText.reparentTo(self, DGG.FOREGROUND_SORT_INDEX)
        self.exitButton = Button(parent=self, image_scale=1.15, text=TTLocalizer.OptionsPageExitToontown, pos=(0.45, 0, -0.6), command=self.__handleExitShowWithConfirm)
        return

    def enter(self):
        self.show()
        taskMgr.remove(self.DisplaySettingsTaskName)
        self.__setAcceptFriendsButton()
        self.__setAcceptWhispersButton()
        self.__setDisplaySettings()
        self.__setToonChatSoundsButton()
        self.speedChatStyleText.enter()
        self.speedChatStyleIndex = base.localAvatar.getSpeedChatStyleIndex()
        self.updateSpeedChatStyle()
        if self.parent.book.safeMode:
            self.exitButton.hide()
        else:
            self.exitButton.show()

    def exit(self):
        self.ignore('confirmDone')
        self.hide()
        self.speedChatStyleText.exit()
        if self.displaySettingsChanged:
            taskMgr.doMethodLater(self.DisplaySettingsDelay, self.writeDisplaySettings, self.DisplaySettingsTaskName)

    def unload(self):
        self.writeDisplaySettings()
        taskMgr.remove(self.DisplaySettingsTaskName)
        if self.displaySettings != None:
            self.ignore(self.displaySettings.doneEvent)
            self.displaySettings.unload()
        self.displaySettings = None
        self.exitButton.destroy()
        self.Music_toggleSlider.destroy()
        self.SoundFX_toggleSlider.destroy()
        self.Friends_toggleButton.destroy()
        self.Whispers_toggleButton.destroy()
        self.DisplaySettingsButton.destroy()
        self.speedChatStyleLeftArrow.destroy()
        self.speedChatStyleRightArrow.destroy()
        del self.exitButton
        del self.SoundFX_Label
        del self.Music_Label
        del self.Friends_Label
        del self.Whispers_Label
        del self.SpeedChatStyle_Label
        del self.SoundFX_toggleSlider
        del self.Music_toggleSlider
        del self.Friends_toggleButton
        del self.Whispers_toggleButton
        del self.speedChatStyleLeftArrow
        del self.speedChatStyleRightArrow
        self.speedChatStyleText.exit()
        self.speedChatStyleText.destroy()
        del self.speedChatStyleText
        self.currentSizeIndex = None
        return

    def __doMusicLevel(self):
        vol = self.Music_toggleSlider['value']
        vol = float(vol) / 100
        settings['musicVol'] = vol
        base.musicManager.setVolume(vol)

    def __doSfxLevel(self):
        vol = self.SoundFX_toggleSlider['value']
        vol = float(vol) / 100
        settings['sfxVol'] = vol
        for sfm in base.sfxManagerList:
            sfm.setVolume(vol)

        self.__setToonChatSoundsButton()

    def __doToggleToonChatSounds(self):
        messenger.send('wakeup')
        settings['toonChatSounds'] = not settings['toonChatSounds']
        base.toonChatSounds = settings['toonChatSounds']
        self.__setToonChatSoundsButton()

    def __setToonChatSoundsButton(self):
        if base.toonChatSounds:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOnLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOffLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn
        if base.sfxActive:
            self.ToonChatSounds_Label.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.ToonChatSounds_toggleButton['state'] = DGG.NORMAL
        else:
            self.ToonChatSounds_Label.setColorScale(0.5, 0.5, 0.5, 0.5)
            self.ToonChatSounds_toggleButton['state'] = DGG.DISABLED

    def __doToggleAcceptFriends(self):
        toggleSettingsList('notAcceptingNewFriends')
        self.__setAcceptFriendsButton()

    def __doToggleAcceptWhispers(self):
        toggleSettingsList('notAcceptingNonFriendWhispers')
        self.__setAcceptWhispersButton()

    def __setAcceptFriendsButton(self):
        if base.localAvatar.isAcceptingNewFriends():
            self.Friends_Label['text'] = TTLocalizer.OptionsPageFriendsEnabledLabel
            self.Friends_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Friends_Label['text'] = TTLocalizer.OptionsPageFriendsDisabledLabel
            self.Friends_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

    def __setAcceptWhispersButton(self):
        if base.localAvatar.isAcceptingWhispers():
            self.Whispers_Label['text'] = TTLocalizer.OptionsPageWhisperEnabledLabel
            self.Whispers_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Whispers_Label['text'] = TTLocalizer.OptionsPageWhisperDisabledLabel
            self.Whispers_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

    def __doDisplaySettings(self):
        if self.displaySettings == None:
            self.displaySettings = DisplaySettingsDialog.DisplaySettingsDialog()
            self.displaySettings.load()
            self.accept(self.displaySettings.doneEvent, self.__doneDisplaySettings)
        self.displaySettings.enter(self.ChangeDisplaySettings, self.ChangeDisplayAPI)
        return

    def __doneDisplaySettings(self, anyChanged, apiChanged):
        if anyChanged:
            self.__setDisplaySettings()
            properties = base.win.getProperties()
            self.displaySettingsChanged = 1
            self.displaySettingsSize = (properties.getXSize(), properties.getYSize())
            self.displaySettingsFullscreen = properties.getFullscreen()
            self.displaySettingsApi = base.pipe.getInterfaceName()
            self.displaySettingsApiChanged = apiChanged

    def __setDisplaySettings(self):
        properties = base.win.getProperties()
        if properties.getFullscreen():
            screensize = '%s x %s' % (properties.getXSize(), properties.getYSize())
        else:
            screensize = TTLocalizer.OptionsPageDisplayWindowed
        api = base.pipe.getInterfaceName()
        settings = {'screensize': screensize,
         'api': api}
        if self.ChangeDisplayAPI:
            OptionsPage.notify.debug('change display settings...')
            text = TTLocalizer.OptionsPageDisplaySettings % settings
        else:
            OptionsPage.notify.debug('no change display settings...')
            text = TTLocalizer.OptionsPageDisplaySettingsNoApi % settings
        self.DisplaySettings_Label['text'] = text

    def __doSpeedChatStyleLeft(self):
        if self.speedChatStyleIndex > 0:
            self.speedChatStyleIndex = self.speedChatStyleIndex - 1
            self.updateSpeedChatStyle()

    def __doSpeedChatStyleRight(self):
        if self.speedChatStyleIndex < len(speedChatStyles) - 1:
            self.speedChatStyleIndex = self.speedChatStyleIndex + 1
            self.updateSpeedChatStyle()

    def updateSpeedChatStyle(self):
        nameKey, arrowColor, rolloverColor, frameColor = speedChatStyles[self.speedChatStyleIndex]
        newSCColorScheme = SCColorScheme.SCColorScheme(arrowColor=arrowColor, rolloverColor=rolloverColor, frameColor=frameColor)
        self.speedChatStyleText.setColorScheme(newSCColorScheme)
        self.speedChatStyleText.clearMenu()
        colorName = SCStaticTextTerminal.SCStaticTextTerminal(nameKey)
        self.speedChatStyleText.append(colorName)
        self.speedChatStyleText.finalize()
        self.speedChatStyleText.setPos(0.445 - self.speedChatStyleText.getWidth() * speed_chat_scale / 2, 0, self.speedChatStyleText.getPos()[2])
        if self.speedChatStyleIndex > 0:
            self.speedChatStyleLeftArrow['state'] = DGG.NORMAL
        else:
            self.speedChatStyleLeftArrow['state'] = DGG.DISABLED
        if self.speedChatStyleIndex < len(speedChatStyles) - 1:
            self.speedChatStyleRightArrow['state'] = DGG.NORMAL
        else:
            self.speedChatStyleRightArrow['state'] = DGG.DISABLED
        base.localAvatar.b_setSpeedChatStyleIndex(self.speedChatStyleIndex)

    def writeDisplaySettings(self, task = None):
        if not self.displaySettingsChanged:
            return
        taskMgr.remove(self.DisplaySettingsTaskName)
        settings['res'] = (self.displaySettingsSize[0], self.displaySettingsSize[1])
        settings['fullscreen'] = self.displaySettingsFullscreen
        return Task.done

    def __handleExitShowWithConfirm(self):
        self.confirm = TTDialog.TTGlobalDialog(doneEvent='confirmDone', message=TTLocalizer.OptionsPageExitConfirm, style=TTDialog.TwoChoice)
        self.confirm.show()
        self.parent.doneStatus = {'mode': 'exit',
         'exitTo': 'closeShard'}
        self.accept('confirmDone', self.__handleConfirm)

    def __handleConfirm(self):
        status = self.confirm.doneStatus
        self.ignore('confirmDone')
        self.confirm.cleanup()
        del self.confirm
        if status == 'ok':
            base.cr._userLoggingOut = True
            messenger.send(self.parent.doneEvent)


class CodesTabPage(DirectFrame):
    notify = directNotify.newCategory('CodesTabPage')

    def __init__(self, parent = aspect2d):
        self.parent = parent
        DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()
        return

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)
        return

    def load(self):
        self.notice = DirectLabel(parent=self, relief=None, text=TTLocalizer.CodeRedemptionWarning, text_scale=0.06, pos=(0.0, 0, 0.53), text_fg=(1.0, 0, 0, 1))
        cdrGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui')
        self.resultPanelSuccessGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_success')
        self.resultPanelFailureGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_failure')
        self.resultPanelErrorGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_error')
        self.successSfx = loader.loadSfx('phase_3.5/audio/sfx/tt_s_gui_sbk_cdrSuccess.ogg')
        self.failureSfx = loader.loadSfx('phase_3.5/audio/sfx/tt_s_gui_sbk_cdrFailure.ogg')
        self.instructionPanel = DirectFrame(parent=self, relief=None, image=cdrGui.find('**/tt_t_gui_sbk_cdrPresent'), image_scale=0.8, text=TTLocalizer.CdrInstructions, text_pos=TTLocalizer.OPCodesInstructionPanelTextPos, text_align=TextNode.ACenter, text_scale=TTLocalizer.OPCodesResultPanelTextScale, text_wordwrap=TTLocalizer.OPCodesInstructionPanelTextWordWrap, pos=(-0.429, 0, -0.05))
        self.codeBox = DirectFrame(parent=self, relief=None, image=cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox'), pos=(0.433, 0, 0.35))
        self.flippyFrame = DirectFrame(parent=self, relief=None, image=cdrGui.find('**/tt_t_gui_sbk_cdrFlippy'), pos=(0.44, 0, -0.353))
        self.codeInput = DirectEntry(parent=self.codeBox, relief=DGG.GROOVE, scale=0.08, pos=(-0.33, 0, -0.006), borderWidth=(0.05, 0.05), frameColor=((1, 1, 1, 1), (1, 1, 1, 1), (0.5, 0.5, 0.5, 0.5)), state=DGG.NORMAL, text_align=TextNode.ALeft, text_scale=TTLocalizer.OPCodesInputTextScale, width=10.5, numLines=1, focus=1, backgroundFocus=0, cursorKeys=1, text_fg=(0, 0, 0, 1), suppressMouse=1, autoCapitalize=0, command=self.__submitCode)
        self.submitButton = Button(parent=self, image_scale=1.15, text=TTLocalizer.NameShopSubmitButton, text_scale=TTLocalizer.OPCodesSubmitTextScale, text_pos=TTLocalizer.OPCodesSubmitTextPos, pos=(0.45, 0.0, 0.0896), command=self.__submitCode)
        self.resultPanel = DirectFrame(parent=self, relief=None, image=self.resultPanelSuccessGui, text='', text_pos=TTLocalizer.OPCodesResultPanelTextPos, text_align=TextNode.ACenter, text_scale=TTLocalizer.OPCodesResultPanelTextScale, text_wordwrap=TTLocalizer.OPCodesResultPanelTextWordWrap, pos=(-0.42, 0, -0.0567))
        self.resultPanel.hide()
        self.closeButton = Button(parent=self.resultPanel, pos=(0.296, 0, -0.466), type='closeButton', image_scale=1, command=self.__hideResultPanel)
        cdrGui.removeNode()
        return

    def enter(self):
        self.show()
        localAvatar.chatMgr.fsm.request('otherDialog')
        self.codeInput['focus'] = 1
        self.codeInput.enterText('')
        self.__enableCodeEntry()

    def exit(self):
        self.resultPanel.hide()
        self.hide()
        localAvatar.chatMgr.fsm.request('mainMenu')

    def unload(self):
        self.instructionPanel.destroy()
        self.instructionPanel = None
        self.codeBox.destroy()
        self.codeBox = None
        self.flippyFrame.destroy()
        self.flippyFrame = None
        self.codeInput.destroy()
        self.codeInput = None
        self.submitButton.destroy()
        self.submitButton = None
        self.resultPanel.destroy()
        self.resultPanel = None
        self.closeButton.destroy()
        self.closeButton = None
        del self.successSfx
        del self.failureSfx
        return

    def __submitCode(self, input = None):
        if input == None:
            input = self.codeInput.get()
        self.codeInput['focus'] = 1
        if input == '':
            return
        else:
            messenger.send('wakeup')
            if hasattr(base.cr, 'codeRedemptionMgr'):
                base.cr.codeRedemptionMgr.redeemCode(input, self.__getCodeResult)
            self.codeInput.enterText('')
            self.__disableCodeEntry()
            return

    def __getCodeResult(self, result):
        self.notify.debug('result = %s' % result)
        self.__enableCodeEntry()
        if result == 0:
            self.resultPanel['image'] = self.resultPanelSuccessGui
            self.resultPanel['text'] = TTLocalizer.CdrResultSuccess
        elif result == 1:
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultInvalidCode
        elif result == 2:
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultExpiredCode
        elif result == 3:
            self.resultPanel['image'] = self.resultPanelErrorGui
        elif result == 4:
            self.resultPanel['image'] = self.resultPanelErrorGui
            self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyRedeemed
        elif result == 5:
            self.resultPanel['image'] = self.resultPanelErrorGui
            self.resultPanel['text'] = TTLocalizer.CdrResultNotReady
        elif result == 6:
            self.resultPanel['image'] = self.resultPanelErrorGui
            self.resultPanel['text'] = TTLocalizer.CdrResultNotEligible
        if result == 0:
            self.successSfx.play()
        else:
            self.failureSfx.play()
        self.resultPanel.show()

    def __hideResultPanel(self):
        self.resultPanel.hide()

    def __disableCodeEntry(self):
        self.codeInput['state'] = DGG.DISABLED
        self.submitButton['state'] = DGG.DISABLED

    def __enableCodeEntry(self):
        self.codeInput['state'] = DGG.NORMAL
        self.codeInput['focus'] = 1
        self.submitButton['state'] = DGG.NORMAL


class OptionsTwoTabPage(DirectFrame):
    notify = directNotify.newCategory('OptionsTwoTabPage')

    def __init__(self, parent = aspect2d):
        self.parent = parent
        self.currentSizeIndex = None
        DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()
        return

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)
        return

    def load(self):
        self.controlDialog = None
        self.fov_label = Label(parent=self, text=TTLocalizer.FieldOfViewLabel, row=0)
        self.cogInterface_label = Label(parent=self, row=1)
        self.tpTransition_label = Label(parent=self, row=2)
        self.patTransition_label = Label(parent=self, row=3)
        self.fpsMeter_label = Label(parent=self, row=4)
        self.antiAlias_label = Label(parent=self, row=5)
        self.smoothAnimations_label = Label(parent=self, row=6)
        self.ttoAspectRatio_label = Label(parent=self, row=7)
        self.fov_slider = Slider(parent=self, row=0, value=settings['fov'], range=(ToontownGlobals.DefaultCameraFov, ToontownGlobals.MaxCameraFov), command=self.__doFov)
        self.cogInterface_toggleButton = Button(parent=self, row=1, command=self.__doToggleCogInterface)
        self.tpTransition_toggleButton = Button(parent=self, row=2, command=self.__doToggleTpTransition)
        self.patTransition_toggleButton = Button(parent=self, row=3, command=self.__doTogglePatTransition)
        self.fpsMeter_toggleButton = Button(parent=self, row=4, command=self.__doToggleFpsMeter)
        self.antiAlias_toggleButton = Button(parent=self, row=5, command=self.__doToggleAntiAlias)
        self.smoothAnimations_toggleButton = Button(parent=self, row=6, command=self.__doToggleSmoothAnimations)
        self.ttoAspectRatio_toggleButton = Button(parent=self, row=7, command=self.__doToggleTTOAspectRatio)
        return

    def enter(self):
        self.show()
        self.__setCogInterfaceButton()
        self.__setTpTransitionButton()
        self.__setPatTransitionButton()
        self.__setFpsMeterButton()
        self.__setAntiAliasButton()
        self.__setSmoothAnimationsButton()
        self.__setTTOAspectRatioButton()

    def exit(self):
        self.ignoreAll()
        self.hide()

    def unload(self):
        self.fov_label.destroy()
        del self.fov_label
        self.fov_slider.destroy()
        del self.fov_slider
        self.cogInterface_label.destroy()
        del self.cogInterface_label
        self.cogInterface_toggleButton.destroy()
        del self.cogInterface_label
        self.tpTransition_label.destroy()
        del self.tpTransition_label
        self.tpTransition_toggleButton.destroy()
        del self.tpTransition_toggleButton
        self.patTransition_label.destroy()
        del self.patTransition_label
        self.patTransition_toggleButton.destroy()
        del self.patTransition_toggleButton
        self.fpsMeter_label.destroy()
        del self.fpsMeter_label
        self.fpsMeter_toggleButton.destroy()
        del self.fpsMeter_toggleButton
        self.antiAlias_label.destroy()
        del self.antiAlias_label
        self.antiAlias_toggleButton.destroy()
        del self.antiAlias_toggleButton
        self.smoothAnimations_label.destroy()
        del self.smoothAnimations_label
        self.smoothAnimations_toggleButton.destroy()
        del self.smoothAnimations_toggleButton
        self.ttoAspectRatio_label.destroy()
        del self.ttoAspectRatio_label
        self.ttoAspectRatio_toggleButton.destroy()
        del self.ttoAspectRatio_toggleButton

    def __doFov(self):
        fov = self.fov_slider['value']
        settings['fov'] = fov
        base.camLens.setMinFov(fov / (4.0 / 3.0))

    def __doToggleCogInterface(self):
        messenger.send('wakeup')
        settings['cogInterface'] = not settings['cogInterface']
        self.__setCogInterfaceButton()

    def __setCogInterfaceButton(self):
        self.cogInterface_label['text'] = TTLocalizer.CogInterfaceLabelOn if settings['cogInterface'] else TTLocalizer.CogInterfaceLabelOff
        self.cogInterface_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if settings['cogInterface'] else TTLocalizer.OptionsPageToggleOn

    def __doToggleTpTransition(self):
        messenger.send('wakeup')
        settings['tpTransition'] = not settings['tpTransition']
        self.__setTpTransitionButton()

    def __setTpTransitionButton(self):
        self.tpTransition_label['text'] = TTLocalizer.TpTransitionLabelOn if settings['tpTransition'] else TTLocalizer.TpTransitionLabelOff
        self.tpTransition_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if settings['tpTransition'] else TTLocalizer.OptionsPageToggleOn

    def __doTogglePatTransition(self):
        messenger.send('wakeup')
        settings['patTransition'] = not settings['patTransition']
        self.__setPatTransitionButton()

    def __setPatTransitionButton(self):
        self.patTransition_label['text'] = TTLocalizer.PatTransitionLabelOn if settings['patTransition'] else TTLocalizer.PatTransitionLabelOff
        self.patTransition_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if settings['patTransition'] else TTLocalizer.OptionsPageToggleOn

    def __doToggleFpsMeter(self):
        messenger.send('wakeup')
        settings['fpsMeter'] = not settings['fpsMeter']
        base.setFrameRateMeter(settings['fpsMeter'])
        self.__setFpsMeterButton()

    def __setFpsMeterButton(self):
        self.fpsMeter_label['text'] = TTLocalizer.FpsMeterLabelOn if settings['fpsMeter'] else TTLocalizer.FpsMeterLabelOff
        self.fpsMeter_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if settings['fpsMeter'] else TTLocalizer.OptionsPageToggleOn

    def __doToggleAntiAlias(self):
        messenger.send('wakeup')
        settings['antiAliasing'] = not settings['antiAliasing']
        if settings['antiAliasing'] and sys.platform != 'android':
            render.setAntialias(AntialiasAttrib.MMultisample)
        else:
            render.clearAntialias()
        self.__setAntiAliasButton()

    def __setAntiAliasButton(self):
        self.antiAlias_label['text'] = TTLocalizer.AntiAliasingLabelOn if settings['antiAliasing'] else TTLocalizer.AntiAliasingLabelOff
        self.antiAlias_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if settings['antiAliasing'] else TTLocalizer.OptionsPageToggleOn

    def __doToggleSmoothAnimations(self):
        messenger.send('wakeup')
        settings['smoothAnimations'] = not settings['smoothAnimations']
        Avatar.reconsiderFrameBlend()
        self.__setSmoothAnimationsButton()

    def __setSmoothAnimationsButton(self):
        self.smoothAnimations_label['text'] = TTLocalizer.SmoothAnimationsLabelOn if settings['smoothAnimations'] else TTLocalizer.SmoothAnimationsLabelOff
        self.smoothAnimations_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if settings['smoothAnimations'] else TTLocalizer.OptionsPageToggleOn

    def __doToggleTTOAspectRatio(self):
        messenger.send('wakeup')
        settings['ttoAspectRatio'] = not settings['ttoAspectRatio']
        if settings['ttoAspectRatio']:
            base.applyForcedAspectRatio(1.33)
        else:
            base.unapplyForcedAspectRatio()
        self.__setTTOAspectRatioButton()

    def __setTTOAspectRatioButton(self):
        self.ttoAspectRatio_label['text'] = TTLocalizer.TTOAspectRatioLabelOn if settings['ttoAspectRatio'] else TTLocalizer.TTOAspectRatioLabelOff
        self.ttoAspectRatio_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if settings['ttoAspectRatio'] else TTLocalizer.OptionsPageToggleOn


class OptionsThreeTabPage(DirectFrame):
    notify = directNotify.newCategory('OptionsThreeTabPage')

    def __init__(self, parent = aspect2d):
        self.parent = parent
        self.currentSizeIndex = None
        self.controlDialog = None
        DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()
        return

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)
        return

    def load(self):
        self.teleport_label = Label(parent=self, row=0)
        self.teleport_toggleButton = Button(parent=self, row=0, command=self.__doToggleTeleport)
        self.minigame_label = Label(parent=self, row=1)
        self.minigame_toggleButton = Button(parent=self, row=1, command=self.__doToggleMinigame)
        self.greenScreen_label = Label(parent=self, row=2)
        self.greenScreen_toggleButton = Button(parent=self, row=2, command=self.__doToggleGreenScreen)
        self.musicEasterEgg_label = Label(parent=self, row=3)
        self.musicEasterEgg_toggleButton = Button(parent=self, row=3, command=self.__doToggleMusicEasterEgg)
        self.controls_label = Label(parent=self, row=4)
        self.controls_toggleButton = Button(parent=self, row=4, command=self.__doToggleControls)
        self.controls_openButton = Button(parent=self, row=4, xPadding=0.315, text=TTLocalizer.ControlConfigure, command=self.__doOpenControls)
        self.optionChoosers = {'pole': OptionChooser.OptionChooser(self, TTLocalizer.FishingPoleLabel, 5, self.__updateFishingPole, [False], self.__applyFishingPole),
         'lure': OptionChooser.OptionChooser(self, TTLocalizer.FishingLureLabel, 6, self.__updateFishingLure, [False], self.__applyFishingLure),
         'nametag_style': OptionChooser.OptionChooser(self, TTLocalizer.NametagStyleLabel, 7, self.__updateNametagStyle, [False], self.__applyNametagStyle)}

    def enter(self):
        self.show()
        self.__setTeleportButton()
        self.__setMinigameButton()
        self.__setGreenScreenButton()
        self.__setMusicEasterEggButton()
        self.__setControlsButton()
        self.__updateNametagStyle()
        self.__updateFishingPole()
        self.__updateFishingLure()
        self.accept('refreshNametagStyle', self.__updateNametagStyle)
        self.accept('refreshFishingRod', self.__updateFishingPole)
        self.accept('refreshFishingLure', self.__updateFishingLure)

    def exit(self):
        self.ignoreAll()
        self.destroyControlDialog()
        self.hide()
        for chooser in self.optionChoosers.values():
            chooser.exit(chooser.index)

    def unload(self):
        for chooser in self.optionChoosers.values():
            optionChooser.unload()

        del self.optionChoosers
        self.teleport_label.destroy()
        del self.teleport_label
        self.teleport_toggleButton.destroy()
        del self.teleport_toggleButton
        self.minigame_label.destroy()
        del self.minigame_label
        self.minigame_toggleButton.destroy()
        del self.minigame_toggleButton
        self.greenScreen_label.destroy()
        del self.greenScreen_label
        self.greenScreen_toggleButton.destroy()
        del self.greenScreen_toggleButton
        self.musicEasterEgg_label.destroy()
        del self.musicEasterEgg_label
        self.musicEasterEgg_toggleButton.destroy()
        del self.musicEasterEgg_toggleButton
        self.controls_label.destroy()
        del self.controls_label
        self.controls_toggleButton.destroy()
        del self.controls_toggleButton
        self.controls_openButton.destroy()
        del self.controls_openButton

    def destroyControlDialog(self):
        if self.controlDialog:
            self.controlDialog.destroy()
            self.controlDialog = None
        return

    def __doToggleTeleport(self):
        toggleSettingsList('notAcceptingTeleports')
        self.__setTeleportButton()

    def __setTeleportButton(self):
        self.teleport_label['text'] = TTLocalizer.TeleportLabelOn if base.localAvatar.isAcceptingTeleports() else TTLocalizer.TeleportLabelOff
        self.teleport_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if base.localAvatar.isAcceptingTeleports() else TTLocalizer.OptionsPageToggleOn

    def __updateNametagStyle(self, resetIndex = True):
        chooser = self.optionChoosers['nametag_style']
        if resetIndex:
            chooser.setIndex(base.localAvatar.nametagStyles.index(base.localAvatar.getNametagStyle()))
        nametagId = base.localAvatar.nametagStyles[chooser.index]
        chooser.setDisplayText('%s\n%s' % (base.localAvatar.getName(), TTLocalizer.NametagFontNames[nametagId]))
        chooser.setDisplayFont(ToontownGlobals.getNametagFont(nametagId))
        chooser.decideButtons(0, len(base.localAvatar.nametagStyles) - 1)

    def __applyNametagStyle(self, index):
        if index != -1 and index != base.localAvatar.nametagStyles.index(base.localAvatar.getNametagStyle()):
            base.localAvatar.requestNametagStyle(base.localAvatar.nametagStyles[index])

    def __updateFishingPole(self, resetIndex = True):
        chooser = self.optionChoosers['pole']
        if resetIndex:
            chooser.setIndex(base.localAvatar.getFishingRod())
        durability = base.localAvatar.getFishingRodDurability()[chooser.index]
        maxDurability = FishGlobals.Rod2Durability[chooser.index]
        chooser.setDisplayText('%s\n(%s/%s)' % (TTLocalizer.FishingRodNameDict[chooser.index], durability, maxDurability))
        chooser.decideButtons(0, base.localAvatar.maxFishingRod)

    def __applyFishingPole(self, index):
        if index != -1 and index != base.localAvatar.getFishingRod():
            base.localAvatar.requestFishingRod(index)

    def __updateFishingLure(self, resetIndex = True):
        chooser = self.optionChoosers['lure']
        if resetIndex:
            chooser.setIndex(base.localAvatar.getFishingLure())
        textColor = FishGlobals.Lure2TextColor[chooser.index]
        chooser.setDisplayText('\x01%s\x01%s\n(%sx)' % (textColor, TTLocalizer.FishingLureColors[chooser.index], FishGlobals.Lure2Speed[chooser.index]))
        chooser.setDisplayShadow((0, 0, 0, 1))
        chooser.decideButtons(0, base.localAvatar.maxFishingLure)

    def __applyFishingLure(self, index):
        if index != -1 and index != base.localAvatar.getFishingLure():
            base.localAvatar.requestFishingLure(index)

    def __doToggleMinigame(self):
        messenger.send('wakeup')
        settings['bulletHell'] = not settings['bulletHell']
        self.__setMinigameButton()

    def __doToggleGreenScreen(self):
        messenger.send('wakeup')
        settings['greenScreen'] = not settings['greenScreen']
        self.__setGreenScreenButton()

    def __doToggleMusicEasterEgg(self):
        messenger.send('wakeup')
        settings['musicEasterEgg'] = not settings['musicEasterEgg']
        self.__setMusicEasterEggButton()

    def __doToggleControls(self):
        messenger.send('wakeup')
        settings['customControls'] = not settings['customControls']
        self.__setControlsButton()

    def __setMinigameButton(self):
        enabled = settings['bulletHell']
        self.minigame_label['text'] = TTLocalizer.UndertaleMinigameOn if enabled else TTLocalizer.UndertaleMinigameOff
        self.minigame_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if enabled else TTLocalizer.OptionsPageToggleOn

    def __setGreenScreenButton(self):
        enabled = settings['greenScreen']
        self.greenScreen_label['text'] = TTLocalizer.GreenScreenOn if enabled else TTLocalizer.GreenScreenOff
        self.greenScreen_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if enabled else TTLocalizer.OptionsPageToggleOn
        ToontownGlobals.DefaultBackgroundColor = (0, 1, 0, 1) if enabled else (0.3, 0.3, 0.3, 1)
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)

    def __setMusicEasterEggButton(self):
        enabled = settings['musicEasterEgg']
        self.musicEasterEgg_label['text'] = TTLocalizer.MusicEasterEggOn if enabled else TTLocalizer.MusicEasterEggOff
        self.musicEasterEgg_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if enabled else TTLocalizer.OptionsPageToggleOn
        if base.cr.playGame.place and base.cr.playGame.place.loader and hasattr(base.cr.playGame.place.loader, 'resetBattleMusic'):
            base.cr.playGame.place.loader.resetBattleMusic()

    def __setControlsButton(self):
        enabled = settings['customControls']
        self.controls_label['text'] = TTLocalizer.ControlConfigOn if enabled else TTLocalizer.ControlConfigOff
        self.controls_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff if enabled else TTLocalizer.OptionsPageToggleOn
        if enabled:
            self.controls_openButton.show()
        else:
            self.controls_openButton.hide()

    def __doOpenControls(self):
        if not self.controlDialog:
            self.controlDialog = ControlConfigDialog.ControlConfigDialog()