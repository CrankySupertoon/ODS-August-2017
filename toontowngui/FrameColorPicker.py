# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toontowngui.FrameColorPicker
from direct.gui.DirectGui import *
from otp.otpgui.ColorPicker import ColorPicker
from toontown.toonbase import TTLocalizer, ToontownGlobals

class FrameColorPicker(ColorPicker):

    def __init__(self, minSat, maxSat, minVal, maxVal, frameCallback, text = TTLocalizer.ChooseAColor):
        self.frameCallback = frameCallback
        self.pickedColor = None
        gui = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okImage = [ gui.find('**/ChtBx_OKBtn_' + name) for name in ('UP', 'DN', 'Rllvr') ]
        self.frame = DirectFrame(relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=1.075, text=text, text_scale=0.09, text_pos=(0, 0.4))
        self.okButton = DirectButton(self.frame, relief=None, image=okImage, pos=(0, 0, -0.375), text=TTLocalizer.lOK, text_scale=0.06, text_pos=(0, -0.1), command=self.__colorChosen)
        ColorPicker.__init__(self, self.frame, minSat, maxSat, minVal, maxVal, self.__changeColor, (0.15, 0, 0.035))
        gui.removeNode()
        return

    def destroy(self):
        ColorPicker.destroy(self)
        self.frame.destroy()
        self.okButton.destroy()
        del self.frame
        del self.okButton

    def __changeColor(self, color):
        self.frame['geom_color'] = color
        self.pickedColor = color

    def __colorChosen(self):
        self.frameCallback(self.pickedColor)
        self.destroy()