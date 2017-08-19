# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toontowngui.IntuitiveColorPicker
from panda3d.core import Texture
from direct.gui.DirectGui import *
from otp.otpgui.ColorPicker import ColorPicker
from toontown.toonbase import TTLocalizer, ToontownGlobals
import math, colorsys

class IntuitiveColorPicker(DirectFrame):

    def __init__(self, parent, minSat, maxSat, minVal, maxVal, callback, colors, pos = (0, 0, 0)):
        self.colors = colors[:]
        self.colors.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb[:-1]))
        self.autoPress = False
        self.callback = callback
        self.part = 0
        self.row = 0
        DirectFrame.__init__(self, parent, relief=None, image=Preloaded['squareBox'], image_color=(0.16, 0.69, 1, 1), image_scale=(0.9, 1, 0.8), pos=pos)
        self.initialiseoptions(IntuitiveColorPicker)
        self.colorPicker = ColorPicker(self, minSat, maxSat, minVal, maxVal, callback, (0.135, 0, 0))
        self.switchButton = DirectButton(self, relief=None, image=Preloaded['squareBox'], image_color=(0, 1, 0, 1), image_scale=(0.9, 0, 0.1), pos=(0, 0, -0.41), text=TTLocalizer.ColorPicker, text_scale=0.055, text_pos=(0, -0.0185), command=self.__switch, pressEffect=False)
        self.regularFrame = self.attachNewNode('regularFrame')
        self.regularButtons = []
        for row in xrange(5):
            self.regularButtons.append([ self.getRegularButton(row, column) for column in xrange(6) ])

        self.regularIncButton = DirectButton(self.regularFrame, relief=None, image=Preloaded['scrollBlueArrow'], pos=(0, 0, 0.32), command=self.__incrementRow, extraArgs=[-1])
        self.regularDecButton = DirectButton(self.regularFrame, relief=None, image=Preloaded['scrollBlueArrow'], pos=(0, 0, -0.32), hpr=(0, 0, 180), command=self.__incrementRow, extraArgs=[1])
        self.partButtons = []
        self.colorPicker.hide()
        self.__updateRows()
        return

    def setAutoPress(self, autoPress, button = None):
        self.autoPress = autoPress
        if button is not None:
            self.__chooseRegular(button.color)
        return

    def removeNode(self):
        self.destroy()

    def destroy(self):
        if not self.switchButton:
            return
        else:
            DirectFrame.destroy(self)
            for button in self.partButtons:
                button.destroy()

            for buttons in self.regularButtons:
                for button in buttons:
                    button.destroy()

            self.switchButton.destroy()
            self.colorPicker.removeNode()
            self.regularFrame.removeNode()
            self.regularIncButton.destroy()
            self.regularDecButton.destroy()
            self.switchButton = None
            self.colorPicker = None
            self.regularFrame = None
            self.partButtons = []
            self.regularButtons = []
            self.regularIncButton = None
            self.regularDecButton = None
            self.callback = None
            return

    def setPartButtons(self, partButtons, xStart, xIncrement):
        self.partButtons = [ self.getPartButton(xStart, xIncrement, *button) for button in partButtons ]
        self.__choosePart(0)

    def getPartButton(self, xStart, xIncrement, part, text):
        return DirectButton(self, relief=None, image=Preloaded['squareBox'], image_scale=(0.2, 1, 0.1), pos=(xStart + part * xIncrement, 0, 0.435), text=text, text_scale=0.055, text_pos=(0, -0.0185), command=self.__choosePart, extraArgs=[part])

    def getRegularButton(self, row, column):
        button = DirectButton(self.regularFrame, relief=None, image=ToontownGlobals.getWhiteTexture(), image_scale=0.06, pos=(-0.305 + column * 0.12, 0, 0.24 - row * 0.12), pressEffect=False)
        button.bind(DGG.B1PRESS, lambda event: self.setAutoPress(True, button))
        button.bind(DGG.B1RELEASE, lambda event: self.setAutoPress(False))
        button.bind(DGG.WITHIN, lambda event: self.__checkAutoPress(button))
        return button

    def getMaxRow(self):
        return int(math.ceil((len(self.colors) - 30) / 5.0)) - 1

    def isPartChosen(self, part):
        return self.part in (0, part)

    def __checkAutoPress(self, button):
        if self.autoPress:
            self.__chooseRegular(button.color)

    def __choosePart(self, part):
        for i, button in enumerate(self.partButtons):
            button['image_color'] = (1, 0.5, 0, 1) if i == part else (1, 1, 0, 1)

        self.part = part

    def __chooseRegular(self, regular):
        if regular != -1:
            self.callback(self.colors[regular])

    def __switch(self):
        if self.colorPicker.isHidden():
            self.colorPicker.show()
            self.regularFrame.hide()
            self.switchButton['text'] = TTLocalizer.ColorRegular
        else:
            self.colorPicker.hide()
            self.regularFrame.show()
            self.switchButton['text'] = TTLocalizer.ColorPicker

    def __updateRows(self):
        self.regularIncButton.hide() if self.row == 0 else self.regularIncButton.show()
        self.regularDecButton.hide() if self.row == self.getMaxRow() else self.regularDecButton.show()
        start = self.row * 6
        for buttons in self.regularButtons:
            for button in buttons:
                button.color = -1
                button['image_color'] = (0, 0.2, 0.4, 1)

        for i, color in enumerate(self.colors[start:start + 30]):
            button = self.regularButtons[i / 6][i % 6]
            button.color = start + i
            button['image_color'] = color

    def __incrementRow(self, increment):
        self.row += increment
        self.__updateRows()