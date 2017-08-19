# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.determination.BreaktimeInterface
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals, TTLocalizer
from DrawnSquare import DrawnSquare

class BreaktimeInterface(DrawnSquare):

    def __init__(self):
        DrawnSquare.__init__(self, aspect2d, scale=(1, 1, 0.5), pos=(-0.5, 0, -0.35))
        self.card.setScale(self.scale)
        self.label = DirectLabel(self.card, relief=None, pos=(0.5, 0, 0.5), text_fg=(1, 1, 1, 1), text_scale=(0.07, 0.14), text_font=ToontownGlobals.getMinnieFont(), text='')
        return

    def destroy(self):
        if not DrawnSquare.destroy(self):
            return
        self.label.destroy()
        del self.label
        self.stopTimer()

    def startTimer(self, time):
        self.time = time + 1
        self.__decreaseTime()
        taskMgr.doMethodLater(1, self.__decreaseTime, self.uniqueName('breakTimer'))

    def stopTimer(self):
        taskMgr.remove(self.uniqueName('breakTimer'))

    def __decreaseTime(self, task = None):
        if self.time == 0:
            return
        self.time -= 1
        self.label['text'] = TTLocalizer.MinigameBreaktime % self.time
        if task:
            return task.again