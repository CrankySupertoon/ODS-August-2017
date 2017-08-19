# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.launcher.RegisterScreen
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from otp.otpbase import OTPLocalizer
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.uberdog.ClientServicesManagerUtils import RegisterSuccess

class RegisterScreen(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=(0.5, 0.5, 0.5, 1), geom_scale=(1.3, 1, 0.8), pos=(0, 0, 0), text=TTLocalizer.LauncherRegisterTitle, text_scale=0.09, text_pos=(0, 0.25), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_font=ToontownGlobals.getMinnieFont())
        self.initialiseoptions(RegisterScreen)
        self.group = DirectFrame(self, pos=(0.05, 0, -0.26))
        self.userLabel = DirectLabel(self.group, relief=None, text=TTLocalizer.LauncherUsername, text_scale=0.05, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), pos=(-0.35, 0, 0.375), text_align=TextNode.ACenter)
        self.userBox = DirectEntry(self.userLabel, relief=DGG.SUNKEN, state=DGG.NORMAL, focus=1, pos=(0.24, 0, 0.005), scale=0.037, width=13)
        self.userBox.bind(DGG.ACCEPT, self.__register)
        self.mailLabel = DirectLabel(self.group, relief=None, text=TTLocalizer.LauncherEmail, text_scale=0.05, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), pos=(-0.35, 0, 0.275), text_align=TextNode.ACenter)
        self.mailBox = DirectEntry(self.mailLabel, relief=DGG.SUNKEN, state=DGG.NORMAL, pos=(0.24, 0, 0.005), scale=0.037, width=13)
        self.mailBox.bind(DGG.ACCEPT, self.__register)
        self.passLabel = DirectLabel(self.group, relief=None, text=TTLocalizer.LauncherPassword, text_scale=0.05, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), pos=(-0.35, 0, 0.175), text_align=TextNode.ACenter)
        self.passBox = DirectEntry(self.passLabel, relief=DGG.SUNKEN, state=DGG.NORMAL, pos=(0.24, 0, 0.005), scale=0.037, width=13, obscured=True)
        self.passBox.bind(DGG.ACCEPT, self.__register)
        self.repeatLabel = DirectLabel(self.group, relief=None, text=TTLocalizer.LauncherConfirmPassword, text_scale=0.05, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), pos=(-0.35, 0, 0.075), text_align=TextNode.ACenter)
        self.repeatBox = DirectEntry(self.repeatLabel, relief=DGG.SUNKEN, state=DGG.NORMAL, pos=(0.24, 0, 0.005), scale=0.037, width=13, obscured=True)
        self.repeatBox.bind(DGG.ACCEPT, self.__register)
        self.registerButton = DirectButton(self.group, relief=None, image=Preloaded['yellowButton'], text=TTLocalizer.LauncherRegister, text_fg=(0, 0, 0, 1), text_shadow=(1, 1, 1, 1), text_scale=0.06, text_pos=(0, -0.014), pos=(0.22, 0, -0.05), scale=0.8, command=self.__register, state=DGG.NORMAL)
        self.backButton = DirectButton(self.group, relief=None, image=Preloaded['yellowButton'], text=TTLocalizer.MakeAToonLast, text_fg=(0, 0, 0, 1), text_shadow=(1, 1, 1, 1), text_scale=0.06, text_pos=(0, -0.014), pos=(-0.4, 0, -0.05), scale=0.8, command=self.destroy, state=DGG.NORMAL)
        self.warningDialog = None
        self.loaded = True
        return

    def destroy(self, *args):
        DirectFrame.destroy(self)
        if not self.loaded:
            return
        self.hide()
        self.group.destroy()
        self.userLabel.destroy()
        self.userBox.destroy()
        self.mailLabel.destroy()
        self.mailBox.destroy()
        self.passLabel.destroy()
        self.passBox.destroy()
        self.repeatLabel.destroy()
        self.repeatBox.destroy()
        self.registerButton.destroy()
        self.backButton.destroy()
        del self.group
        del self.userLabel
        del self.userBox
        del self.mailLabel
        del self.mailBox
        del self.passLabel
        del self.passBox
        del self.repeatLabel
        del self.repeatBox
        del self.registerButton
        del self.backButton
        self.loaded = False

    def show(self):
        DirectFrame.show(self)
        base.transitions.fadeScreen(0.5)
        self.setBin('gui-popup', 0)
        self.accept('tab', self.__doTab)
        self.accept('arrow_up', self.__doTab)
        self.accept('arrow_down', self.__doTab)

    def hide(self):
        try:
            DirectFrame.hide(self)
        except:
            pass

        base.transitions.noTransitions()
        self.ignoreAll()
        self.deleteWarningDialog()

    def deleteWarningDialog(self, *args):
        if self.warningDialog:
            self.warningDialog.destroy()
        self.warningDialog = None
        return

    def __doTab(self):
        if self.userBox['focus']:
            target = self.mailBox
        elif self.mailBox['focus']:
            target = self.passBox
        elif self.passBox['focus']:
            target = self.repeatBox
        else:
            target = self.userBox
        for button in (self.userBox,
         self.mailBox,
         self.passBox,
         self.repeatBox):
            button['focus'] = button == target

    def getErrorText(self, error, seconds):
        return OTPLocalizer.RegisterErrors.get(error, OTPLocalizer.DefaultAuthError) % {'time': seconds}

    def enableButtons(self, enabled):
        state = DGG.NORMAL if enabled else DGG.DISABLED
        for button in (self.userBox,
         self.mailBox,
         self.passBox,
         self.repeatBox,
         self.backButton,
         self.registerButton):
            button['state'] = state

    def __register(self, *args):
        self.enableButtons(False)
        self.acceptOnce('registrationDone', self.__registrationDone)
        password = self.passBox.get()
        if password != self.repeatBox.get():
            base.cr.csm.registrationDone(RegisterSuccess.PasswordMismatch, 0)
            return
        base.cr.csm.d_register(self.userBox.get(), password, self.mailBox.get())

    def __registrationDone(self, response):
        if response.get('success', False):
            username = self.userBox.get()
            password = self.passBox.get()
            self.destroy()
            base.cr.launcher.loginWith(username, password)
        else:
            self.deleteWarningDialog()
            self.warningDialog = TTDialog.TTDialog(style=TTDialog.Acknowledge, fadeScreen=0, text=self.getErrorText(response['error'], response['seconds']), command=self.__warningShown)
            self.warningDialog.setBin('gui-popup', 0)
            self.warningDialog.show()

    def __warningShown(self, *args):
        self.deleteWarningDialog()
        self.enableButtons(True)