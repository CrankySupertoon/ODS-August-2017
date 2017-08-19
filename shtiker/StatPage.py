# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.shtiker.StatPage
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui import TTDialog
from BookElements import *
import ShtikerPage, math

class StatPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.dialog = None
        self.chunkCount = 11
        self.index = 0
        self.maxIndex = len(base.localAvatar.stats) / self.chunkCount
        return

    def load(self):
        self.row = DirectLabel(parent=self, relief=None, text_align=TextNode.ALeft, text='', text_scale=0.045, text_wordwrap=16, text_font=ToontownGlobals.getChalkFont(), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), image='phase_3/maps/stat_board.png', image_scale=(0.42, 0, 0.6), image_pos=(0.35, 0, -0.45), pos=(-0.35, 0, 0.4))
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.StatPageTitle, text_scale=0.12, pos=(-0.18, 0, 0.62))
        self.resetButton = Button(parent=self, image_scale=(0.76, 0, 1), text=TTLocalizer.StatPageClear, text_scale=0.055, pos=(0.25, 0, 0.65), command=self.__showDialog)
        self.leftArrow = DirectButton(parent=self, relief=None, image=Preloaded['slimBlueArrow'], state=DGG.NORMAL, pos=(-0.55, 0, 0), scale=0.6, command=self.addPageIndex, extraArgs=[-1])
        self.leftArrow.hide()
        self.rightArrow = DirectButton(parent=self, relief=None, image=Preloaded['slimBlueArrow'], state=DGG.NORMAL, pos=(0.55, 0, 0), scale=(-0.6, 0.6, 0.6), command=self.addPageIndex, extraArgs=[1])
        self.sequence = None
        return

    def disableButtons(self):
        self.leftArrow.hide()
        self.rightArrow.hide()

    def enableButtons(self):
        if self.index <= 0:
            self.leftArrow.hide()
        else:
            self.leftArrow.show()
        if self.index >= self.maxIndex:
            self.rightArrow.hide()
        else:
            self.rightArrow.show()

    def enter(self):
        self.show()
        self.updateStats()
        self.accept('refreshStats', self.updateStats)

    def exit(self):
        self.ignoreAll()
        self.unloadDialog()
        self.hide()

    def unload(self):
        self.unloadDialog()
        self.row.destroy()
        del self.row
        self.title.destroy()
        del self.title
        self.resetButton.destroy()
        del self.resetButton
        self.leftArrow.destroy()
        del self.leftArrow
        self.rightArrow.destroy()
        del self.rightArrow
        if self.sequence:
            self.sequence.pause()
        del self.sequence
        ShtikerPage.ShtikerPage.unload(self)

    def unloadDialog(self, arg = None):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        return

    def updateStats(self):
        start = self.chunkCount * self.index
        stats = base.localAvatar.stats[start:start + self.chunkCount]
        allStats = []
        for i in xrange(len(stats)):
            if start + i < len(TTLocalizer.Stats):
                allStats.append((TTLocalizer.Stats[start + i] + ': %s') % '{:,}'.format(stats[i]))
            else:
                break

        self.row['text'] = '\n\n'.join(allStats)
        self.sequence = None
        return

    def __showDialog(self):
        self.dialog = TTDialog.TTDialog(style=TTDialog.TwoChoice, text=TTLocalizer.StatPageClearAsk, text_wordwrap=15, command=self.__handleDialogResponse)
        self.dialog.show()

    def __handleDialogResponse(self, response):
        self.unloadDialog()
        if response <= 0:
            return
        base.localAvatar.wipeStats()
        self.dialog = TTDialog.TTDialog(style=TTDialog.Acknowledge, text=TTLocalizer.StatPageClearDone, text_wordwrap=15, command=self.unloadDialog)
        self.dialog.show()

    def addPageIndex(self, index):
        if self.sequence:
            return
        self.index += index
        self.disableButtons()
        self.sequence = Sequence(self.row.hprInterval(1, (90.5, 0, 0), (0, 0, 0), blendType='easeInOut'), Func(self.updateStats), self.row.hprInterval(1, (0, 0, 0), (90.5, 0, 0), blendType='easeInOut'), Func(self.enableButtons))
        self.sequence.start()