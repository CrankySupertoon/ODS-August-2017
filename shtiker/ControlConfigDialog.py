# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.shtiker.ControlConfigDialog
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from otp.otpbase import OTPGlobals
from toontown.toonbase import ToontownGlobals, TTLocalizer
from BookElements import *

class ControlConfigDialog(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, aspect2d, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(1.37, 1, 1.37), pos=(0, 0, 0), text=TTLocalizer.ControlConfigTitle, text_scale=0.09, text_pos=(0, 0.58))
        self.initialiseoptions(ControlConfigDialog)
        self.changes = {}
        self.controlLabels = {}
        self.popupDialog = None
        self.cancelButton = Button(parent=self, type='closeButton', pos=(-0.2, 0, -0.55), text=TTLocalizer.lCancel, text_scale=0.06, text_pos=(0, -0.1), image_scale=1, command=self.destroy)
        self.okButton = Button(parent=self, type='okButton', pos=(0.2, 0, -0.55), text=TTLocalizer.lOK, text_scale=0.06, text_pos=(0, -0.1), image_scale=1, command=self.applyChanges)
        for i, key in enumerate(OTPGlobals.CONTROL_KEYS):
            keyLabel = Label(parent=self, pos=(-0.39, 0, 0.41 + i * -0.1), text=TTLocalizer.ControlKeys[key], text_scale=0.055, text_align=TextNode.ACenter)
            configButton = Button(parent=self, pos=(0.08, 0, 0.425 + i * -0.1), image_scale=(0.9, 0, 0.9), text=TTLocalizer.ControlConfigure, text_scale=0.055, text_pos=(0, -0.01), command=self.configureKey, extraArgs=[key])
            self.controlLabels[key] = Label(parent=self, pos=(0.45, 0, 0.41 + i * -0.1), text=TTLocalizer.getFancyButtonName(base.getKey(key)), text_scale=0.055, text_align=TextNode.ACenter)

        return

    def destroy(self):
        self.destroyPopup()
        del self.changes
        del self.controlLabels
        DirectFrame.destroy(self)

    def destroyPopup(self):
        if self.popupDialog:
            base.transitions.noTransitions()
            self.popupDialog.cleanup()
            self.popupDialog = None
        return

    def applyChanges(self):
        if not self.changes:
            self.destroy()
            return
        controls = settings.get('controls', {})
        for name, value in self.changes.iteritems():
            controls[name] = value

        settings['controls'] = controls
        self.destroy()

    def configureKey(self, key):
        self.destroyPopup()
        base.transitions.fadeScreen(0.7)
        self.popupDialog = DirectDialog(relief=None, suppressMouse=True, suppressKeys=True, image=DGG.getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(2.2, 0, 0.4), pos=(-0.05, 0, 0), text=TTLocalizer.ControlConfigPopup, text_pos=(-1, -0.01), text_scale=0.08)
        event = 'registerButton-' + key
        base.buttonThrowers[0].node().setButtonDownEvent(event)
        self.popupDialog.accept(event, self.registerKey, [key])
        return

    def registerKey(self, key, value):
        self.destroyPopup()
        self.changes[key] = value
        self.controlLabels[key]['text'] = TTLocalizer.getFancyButtonName(value)