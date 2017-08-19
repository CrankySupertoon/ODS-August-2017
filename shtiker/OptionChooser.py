# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.shtiker.OptionChooser
from panda3d.core import TextNode
from BookElements import *

class OptionChooser:

    def __init__(self, book, labelText, row, indexCommand, extraArgs, exitCommand):
        self.indexCommand = indexCommand
        self.extraArgs = extraArgs
        self.exit = exitCommand
        self.label = Label(parent=book, text=labelText, row=row)
        self.display = Label(parent=book, relief=None, text_scale=0.06, text_wordwrap=10, text_align=TextNode.ACenter, row=row, align='right')
        self.leftButton = Button(parent=book, image_scale=0.45, xPadding=-0.3, row=row, type='yellowArrow', command=self.offsetIndex, extraArgs=[-1])
        self.rightButton = Button(parent=book, image_scale=(-0.45, 0, 0.45), xPadding=0.3, row=row, type='yellowArrow', command=self.offsetIndex, extraArgs=[1])
        self.index = -1
        return

    def unload(self):
        self.label.destroy()
        del self.label
        self.display.destroy()
        del self.display
        self.leftButton.destroy()
        del self.leftButton
        self.rightButton.destroy()
        del self.rightButton

    def offsetIndex(self, offset):
        self.index += offset
        self.indexCommand(*self.extraArgs)

    def setIndex(self, index):
        self.index = index

    def setDisplayText(self, text):
        self.display['text'] = text

    def setDisplayShadow(self, shadow):
        self.display['text_shadow'] = shadow

    def setDisplayFont(self, font):
        self.display['text_font'] = font

    def decideButtons(self, minCount, maxCount):
        if self.index <= minCount:
            self.leftButton.hide()
        else:
            self.leftButton.show()
        if self.index >= maxCount:
            self.rightButton.hide()
        else:
            self.rightButton.show()