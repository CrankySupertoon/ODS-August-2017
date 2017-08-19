# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.launcher.GuidelinesScreen
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from toontown.toontowngui.TTDialog import TTDialog
from toontown.toontowngui import GUIUtils
from toontown.toonbase import ToontownGlobals, TTLocalizer
GuidelineColors = [(0.486, 0.757, 0.876, 1),
 (0.399, 0.768, 0.439, 1),
 (0.268, 0.751, 0.334, 1),
 (0.914, 0.333, 0.193, 1)]
GuidelineCliparts = ['phase_3/maps/clipart/flippypie.png',
 'phase_3/maps/clipart/toondog.png',
 'phase_3/maps/clipart/toontownwave.png',
 'phase_3/maps/clipart/distoontown.png']

class GuidelinesScreen(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, relief=None, geom=DGG.getDefaultDialogGeom(), geom_scale=(2, 1, 0.9), pos=(0, 0, 0), text=TTLocalizer.LauncherGuidelineTitle, text_scale=0.09, text_pos=(0, 0.315), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_font=ToontownGlobals.getMinnieFont())
        self.initialiseoptions(GuidelinesScreen)
        self.title = DirectLabel(self, relief=None, text='', text_scale=0.07, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_font=ToontownGlobals.getMinnieFont(), pos=(-0.23, 0, 0.15), text_align=TextNode.ALeft)
        self.description = DirectLabel(self, relief=None, text='', text_scale=0.05, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_wordwrap=21, pos=(-0.23, 0, 0.025), text_align=TextNode.ALeft)
        self.leftButton = DirectButton(self, relief=None, state=DGG.NORMAL, image=Preloaded['yellowArrow'], pos=(-0.93, 0, 0), image_scale=0.75, command=self.__increaseIndex, extraArgs=[-1])
        self.rightButton = DirectButton(self, relief=None, state=DGG.NORMAL, image=Preloaded['yellowArrow'], pos=(0.93, 0, 0), image_scale=(-0.75, 0.75, 0.75), command=self.__increaseIndex, extraArgs=[1])
        self.art = GUIUtils.loadCardModel(transparency=True)
        self.art.setTexture(loader.loadTexture('phase_3/maps/clipart/flippypie.png'), 1)
        self.art.setScale(0.32)
        self.art.setPos(-0.6, 0, -0.05)
        self.art.reparentTo(self)
        self.confirmDialog = None
        self.loaded = True
        self.index = 0
        self.maxIndex = 3
        self.__increaseIndex(0)
        return

    def destroy(self):
        DirectFrame.destroy(self)
        if not self.loaded:
            return
        self.hide()
        self.title.destroy()
        self.description.destroy()
        self.leftButton.destroy()
        self.rightButton.destroy()
        self.art.removeNode()
        del self.title
        del self.description
        del self.leftButton
        del self.rightButton
        del self.art
        self.loaded = False

    def show(self):
        DirectFrame.show(self)
        base.transitions.fadeScreen(0.5)
        self.setBin('gui-popup', 0)

    def deleteConfirmDialog(self):
        if self.confirmDialog:
            self.confirmDialog.destroy()
        self.confirmDialog = None
        return

    def __increaseIndex(self, inc):
        self.index += inc
        if self.index < 0:
            self.destroy()
            return
        elif self.index > self.maxIndex:
            self.deleteConfirmDialog()
            self.leftButton['state'] = DGG.DISABLED
            self.rightButton['state'] = DGG.DISABLED
            self.confirmDialog = TTDialog(style=4, fadeScreen=None, text=TTLocalizer.LauncherGuidelineConfirm, text_wordwrap=23, command=self.__confirmGuidelines)
            self.confirmDialog.setBin('gui-popup', 0)
            self.confirmDialog.setPos(0, 0, 0.1)
            self.confirmDialog.show()
            self.index = self.maxIndex
            return
        else:
            self['geom_color'] = GuidelineColors[self.index]
            self.title['text'] = TTLocalizer.LauncherTitles[self.index]
            self.description['text'] = TTLocalizer.LauncherGuidelines[self.index]
            self.art.setTexture(loader.loadTexture(GuidelineCliparts[self.index]), 1)
            if self.index % 2 == 0:
                self.title.setPos(-0.23, 0, 0.15)
                self.description.setPos(-0.23, 0, 0.025)
                self.art.setPos(-0.6, 0, -0.05)
            else:
                self.title.setPos(-0.8, 0, 0.15)
                self.description.setPos(-0.8, 0, 0.025)
                self.art.setPos(0.55, 0, -0.05)
            return

    def __confirmGuidelines(self, response):
        self.deleteConfirmDialog()
        if response > 0:
            self.destroy()
            messenger.send('guidelinesAccepted')
        else:
            self.leftButton['state'] = DGG.NORMAL
            self.rightButton['state'] = DGG.NORMAL

    def hide(self):
        try:
            DirectFrame.hide(self)
        except:
            pass

        base.transitions.noTransitions()
        self.deleteConfirmDialog()