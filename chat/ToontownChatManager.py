# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.chat.ToontownChatManager
from panda3d.core import TextNode, Vec3, Vec4
from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.chat import ChatManager
from TTChatInputSpeedChat import TTChatInputSpeedChat
from TTChatInputWhiteList import TTChatInputWhiteList
from ChatLog import ChatLog
import time

class ToontownChatManager(ChatManager.ChatManager):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownChatManager')

    def __init__(self, cr, localAvatar):
        gui = loader.loadModel('phase_3.5/models/gui/chat_input_gui')
        self.normalButton = DirectButton(image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(0.0683, 0, -0.072), parent=base.a2dTopLeft, scale=1.179, relief=None, image_color=Vec4(1, 1, 1, 1), text=('', OTPLocalizer.ChatManagerChat, OTPLocalizer.ChatManagerChat), text_align=TextNode.ALeft, text_scale=TTLocalizer.TCMnormalButton, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(-0.0525, -0.09), sortOrder=DGG.FOREGROUND_SORT_INDEX, command=self.__normalButtonPressed)
        self.normalButton.hide()
        self.openScSfx = loader.loadSfx('phase_3.5/audio/sfx/GUI_quicktalker.ogg')
        self.openScSfx.setVolume(0.6)
        self.scButton = DirectButton(image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=TTLocalizer.TCMscButtonPos, parent=base.a2dTopLeft, scale=1.179, relief=None, image_color=Vec4(0.75, 1, 0.6, 1), text=('', OTPLocalizer.GlobalSpeedChatName, OTPLocalizer.GlobalSpeedChatName), text_scale=TTLocalizer.TCMscButton, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(0, -0.09), sortOrder=DGG.FOREGROUND_SORT_INDEX, command=self.__scButtonPressed, clickSound=self.openScSfx)
        self.scButton.hide()
        self.logButton = DirectButton(image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(0.334, 0, -0.072), parent=base.a2dTopLeft, scale=1.179, relief=None, image_color=Vec4(1, 0.75, 0, 1), text=('', OTPLocalizer.ChatManagerLog, OTPLocalizer.ChatManagerLog), text_scale=TTLocalizer.TCMlogButton, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(0, -0.09), sortOrder=DGG.FOREGROUND_SORT_INDEX, command=self.__logButtonPressed)
        self.logButton.hide()
        self.whisperFrame = DirectFrame(parent=base.a2dTopLeft, relief=None, image=DGG.getDefaultDialogGeom(), image_scale=(0.77, 0.7, 0.2), image_color=OTPGlobals.GlobalDialogColor, pos=(0.4, 0, -0.105), text=OTPLocalizer.ChatManagerWhisperTo, text_wordwrap=6.5, text_scale=TTLocalizer.TCMwhisperFrame, text_fg=Vec4(0, 0, 0, 1), text_pos=(0.18, 0.04), sortOrder=DGG.FOREGROUND_SORT_INDEX)
        self.whisperFrame.hide()
        self.whisperButton = DirectButton(parent=self.whisperFrame, image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(-0.33, 0, 0.033), scale=1.179, relief=None, image_color=Vec4(1, 1, 1, 1), text=('',
         OTPLocalizer.ChatManagerChat,
         OTPLocalizer.ChatManagerChat,
         ''), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), text_scale=TTLocalizer.TCMwhisperButton, text_fg=(0, 0, 0, 1), text_pos=(0, -0.09), command=self.__whisperButtonPressed)
        self.whisperScButton = DirectButton(parent=self.whisperFrame, image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(-0.195, 0, 0.033), scale=1.179, relief=None, image_color=Vec4(0.75, 1, 0.6, 1), text=('',
         OTPLocalizer.GlobalSpeedChatName,
         OTPLocalizer.GlobalSpeedChatName,
         ''), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), text_scale=TTLocalizer.TCMwhisperScButton, text_fg=(0, 0, 0, 1), text_pos=(0, -0.09), command=self.__whisperScButtonPressed)
        self.whisperCancelButton = DirectButton(parent=self.whisperFrame, image=(gui.find('**/CloseBtn_UP'), gui.find('**/CloseBtn_DN'), gui.find('**/CloseBtn_Rllvr')), pos=(-0.06, 0, 0.033), scale=1.179, relief=None, text=('', OTPLocalizer.ChatManagerCancel, OTPLocalizer.ChatManagerCancel), text_scale=0.05, text_fg=(0, 0, 0, 1), text_pos=(0, -0.09), command=self.__whisperCancelPressed)
        gui.removeNode()
        ChatManager.ChatManager.__init__(self, cr, localAvatar)
        self.chatInputSpeedChat = TTChatInputSpeedChat(self)
        self.normalPos = Vec3(0.25, 0, -0.196)
        self.whisperPos = Vec3(0.25, 0, -0.28)
        self.speedChatPlusPos = Vec3(-0.35, 0, 0.71)
        self.chatInputNormal = TTChatInputWhiteList()
        self.chatInputNormal.setPos(self.speedChatPlusPos)
        self.chatInputNormal.reparentTo(base.a2dTopLeft)
        self.chatLog = ChatLog()
        self.chatLog.hide()
        self.speedchatTimeout = 0.0
        self.accept('openChatLog', self.__logButtonPressed)
        return

    def delete(self):
        ChatManager.ChatManager.delete(self)
        self.normalButton.destroy()
        del self.normalButton
        self.scButton.destroy()
        del self.scButton
        self.logButton.destroy()
        del self.logButton
        del self.openScSfx
        self.whisperFrame.destroy()
        del self.whisperFrame
        self.whisperButton.destroy()
        del self.whisperButton
        self.whisperScButton.destroy()
        del self.whisperScButton
        self.whisperCancelButton.destroy()
        del self.whisperCancelButton
        self.chatLog.destroy()
        del self.chatLog
        self.ignoreAll()

    def sendSCResistanceChatMessage(self, textId):
        messenger.send('chatUpdateSCResistance', [textId])
        self.announceSCChat()

    def sendSCToontaskChatMessage(self, taskId, toNpcId, toonProgress, msgIndex):
        messenger.send('chatUpdateSCToontask', [taskId,
         toNpcId,
         toonProgress,
         msgIndex])
        self.announceSCChat()

    def sendSCToontaskWhisperMessage(self, taskId, toNpcId, toonProgress, msgIndex, whisperAvatarId):
        messenger.send('whisperUpdateSCToontask', [taskId,
         toNpcId,
         toonProgress,
         msgIndex,
         whisperAvatarId])

    def enterMainMenu(self):
        self.chatInputNormal.setPos(self.normalPos)
        self.chatInputNormal.reparentTo(base.a2dTopLeft)
        if self.chatInputNormal.isActive():
            self.notify.debug('enterMainMenu calling checkObscured')
            ChatManager.ChatManager.checkObscurred(self)
        else:
            ChatManager.ChatManager.enterMainMenu(self)

    def enterNoTrueFriends(self):
        if self.noTrueFriends == None:
            buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            self.noTrueFriends = DirectFrame(parent=aspect2dp, pos=(0.0, 0.1, 0.2), relief=None, image=DGG.getDefaultDialogGeom(), image_color=OTPGlobals.GlobalDialogColor, image_scale=(1.4, 1.0, 1.1), text=OTPLocalizer.NoTrueFriends, text_wordwrap=20, text_scale=0.06, text_pos=(0, 0.3))
            DirectLabel(parent=self.noTrueFriends, relief=None, pos=(0, 0, 0.4), text=OTPLocalizer.NoTrueFriendsTitle, text_scale=0.08)
            DirectButton(self.noTrueFriends, image=okButtonImage, relief=None, text=OTPLocalizer.NoTrueFriendsOK, text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.0, 0.0, -0.4), command=self.__handleNoTrueFriendsOK)
            buttons.removeNode()
        self.noTrueFriends.show()
        return

    def exitNoTrueFriends(self):
        self.noTrueFriends.hide()

    def __normalButtonPressed(self):
        messenger.send('wakeup')
        if not base.cr.wantTypedChat():
            self.fsm.request('noSpeedchatPlus')
            return
        self.fsm.request('normalChat')

    def __scButtonPressed(self):
        if self.speedchatTimeout > time.time():
            return
        messenger.send('wakeup')
        if self.fsm.getCurrentState().getName() == 'speedChat':
            self.fsm.request('mainMenu')
        else:
            self.speedchatTimeout = time.time() + 0.5
            self.fsm.request('speedChat')

    def __logButtonPressed(self):
        messenger.send('wakeup')
        if self.fsm.getCurrentState().getName() == 'chatLog':
            self.fsm.request('mainMenu')
        else:
            self.fsm.request('chatLog')

    def __whisperButtonPressed(self, avatarName, avatarId):
        messenger.send('wakeup')
        if not base.cr.wantTypedChat():
            self.fsm.request('noSpeedchatPlus')
            return
        if avatarId:
            self.enterWhisperChat(avatarName, avatarId)
        self.whisperFrame.hide()

    def enterNormalChat(self):
        if not base.cr.wantTypedChat() or not base.localAvatar.getTutorialAck() or not ChatManager.ChatManager.enterNormalChat(self):
            self.fsm.request('mainMenu')

    def enterWhisperChat(self, avatarName, avatarId):
        if not base.cr.wantTypedChat():
            self.fsm.request('mainMenu')
            return
        else:
            result = ChatManager.ChatManager.enterWhisperChat(self, avatarName, avatarId)
            self.chatInputNormal.setPos(self.whisperPos)
            if result == None:
                self.notify.warning('something went wrong in enterWhisperChat, falling back to main menu')
                self.fsm.request('mainMenu')
            return

    def enterNoSpeedchatPlus(self):
        if self.noSpeedchatPlus == None:
            buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            self.noSpeedchatPlus = DirectFrame(parent=aspect2dp, pos=(0.0, 0.1, 0.05), relief=None, image=DGG.getDefaultDialogGeom(), image_color=OTPGlobals.GlobalDialogColor, image_scale=(1.4, 1.0, 1.58), text=OTPLocalizer.NoSpeedchatPlus, text_wordwrap=20, text_scale=0.06, text_pos=(0, 0.55))
            DirectLabel(parent=self.noSpeedchatPlus, relief=None, pos=(0, 0, 0.67), text=OTPLocalizer.NoSpeedchatPlusTitle, text_scale=0.08)
            DirectButton(self.noSpeedchatPlus, image=okButtonImage, relief=None, text=OTPLocalizer.NoTrueFriendsOK, text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.0, 0.0, -0.64), command=self.__handleNoTrueFriendsOK)
            buttons.removeNode()
        self.noSpeedchatPlus.show()
        return

    def exitNoSpeedchatPlus(self):
        self.noSpeedchatPlus.hide()

    def __whisperScButtonPressed(self, avatarName, avatarId):
        messenger.send('wakeup')
        if avatarId:
            if self.fsm.getCurrentState().getName() == 'whisperSpeedChat':
                self.fsm.request('whisper', [avatarName, avatarId])
            else:
                self.fsm.request('whisperSpeedChat', [avatarId])

    def __whisperCancelPressed(self):
        self.fsm.request('mainMenu')

    def __handleNoTrueFriendsOK(self):
        self.fsm.request('mainMenu')

    def messageSent(self):
        pass