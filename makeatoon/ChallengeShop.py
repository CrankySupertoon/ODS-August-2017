# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.makeatoon.ChallengeShop
from panda3d.core import TextNode, Texture
from direct.fsm import StateData
from direct.task.Task import Task
from direct.gui.DirectGui import *
from toontown.toontowngui import GUIUtils, TTDialog
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toon.LaffMeter import LaffMeter

class ChallengeShop(StateData.StateData):

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.toon = None
        self.frame = None
        self.dialog = None
        return

    def enter(self, toon):
        self.toon = toon
        if self.toon.hpLimit == -1:
            self.toon.hpLimit = ToontownGlobals.MaxHpLimit
        self.load()
        self.frame.show()
        self.laffFrame.show()
        self.acceptOnce('last', lambda : self.__handleDoneStatus('last'))
        self.acceptOnce('next', lambda : self.__handleDoneStatus('next'))

    def exit(self):
        if self.toon.hpLimit == ToontownGlobals.MaxHpLimit:
            self.toon.hpLimit = -1
        self.ignoreAll()
        self.toon = None
        self.frame.hide()
        self.laffFrame.hide()
        return

    def load(self):
        if self.frame:
            return
        else:
            self.frame = DirectFrame(base.a2dRightCenter, relief=None, image=Preloaded['squareBox'], image_color=(0.16, 0.69, 1, 1), image_scale=(0.9, 1, 0.75), pos=(-0.5, 0, -0.2))
            self.frame.hide()
            self.hardcoreLabel = DirectLabel(self.frame, relief=None, text=TTLocalizer.HardcoreChallenge, text_scale=0.1, text_font=ToontownGlobals.getSuitFont(), pos=(0, 0, 0.225))
            self.hardcoreHelpButton = DirectButton(self.frame, relief=None, image=Preloaded['purpleHelpButton'], pos=(0.325, 0, -0.275), scale=0.75, command=self.__helpHardcore)
            self.hardcoreActivateButton = DirectButton(self.frame, relief=None, image=Preloaded['squareBox'], image_color=(1, 0, 0, 1), pos=(0, 0, 0.06), image_scale=(0.4, 1, 0.15), text=TTLocalizer.CapitalOff, text_scale=0.1, text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), text_pos=(0, -0.025), command=self.__toggleHardcore)
            self.hardcoreIcon1 = GUIUtils.loadTextureModel(loader.loadTexture('phase_3/maps/tommy_taunt.png'), transparency=True)
            self.hardcoreIcon1.reparentTo(self.frame)
            self.hardcoreIcon1.setScale(0.15)
            self.hardcoreIcon1.setR(20)
            self.hardcoreIcon1.setPos(-0.275, 0, 0.55)
            self.hardcoreIcon2 = GUIUtils.loadTextureModel(loader.loadTexture('phase_3/maps/star_taunt.png'), transparency=True)
            self.hardcoreIcon2.reparentTo(self.frame)
            self.hardcoreIcon2.setScale(0.135)
            self.hardcoreIcon2.setR(-20)
            self.hardcoreIcon2.setPos(0.275, 0, 0.55)
            self.hardcoreIcon3 = GUIUtils.loadTextureModel(loader.loadTexture('phase_3/maps/empty_laff.png'), transparency=True)
            self.hardcoreIcon3.reparentTo(self.frame)
            self.hardcoreIcon3.setScale(0.135)
            self.hardcoreIcon3.setPos(0, 0, -0.195)
            self.laffFrame = base.a2dLeftCenter.attachNewNode('laffFrame')
            self.laffFrame.hide()
            self.laffCircle = DirectFrame(self.laffFrame, relief=None, image='phase_3/maps/gui-circle.png', image_color=(0.16, 0.69, 1, 1), pos=(0.5, 0, -0.3), scale=0.4)
            self.laffCircle.setTransparency(True)
            self.laffMeter = LaffMeter(self.toon.style, ToontownGlobals.MaxHpLimit, ToontownGlobals.MaxHpLimit)
            self.laffMeter.reparentTo(self.laffFrame)
            self.laffMeter.setScale(0.15)
            self.laffMeter.setPos(0.5, 0, -0.3)
            self.laffMeter.start()
            self.laffArrowL = DirectButton(self.laffFrame, relief=None, image=Preloaded['yellowArrow'], pos=(0.075, 0, -0.25), state=DGG.NORMAL)
            self.laffArrowR = DirectButton(self.laffArrowL, relief=None, image=Preloaded['yellowArrow'], pos=(0.85, 0, 0), image_scale=(-1, 1, 1), state=DGG.DISABLED)
            self.laffLabel = DirectLabel(self.laffFrame, relief=None, text=TTLocalizer.LaffChallenge, text_scale=0.1, pos=(0.45, 0, 0.2), image=Preloaded['squareBox'], image_scale=(0.95, 0, 0.15), image_pos=(0.06, 0, 0.03), image_color=(0.16, 0.69, 1, 1))
            self.laffHelpButton = DirectButton(self.laffLabel, relief=None, image=Preloaded['purpleHelpButton'], pos=(0.41, 0, 0.03), scale=0.75, command=self.__helpLaff)
            self.laffArrowL.bind(DGG.B1PRESS, self.__taskUpdate, extraArgs=[-1])
            self.laffArrowL.bind(DGG.B1RELEASE, self.__taskDone)
            self.laffArrowR.bind(DGG.B1PRESS, self.__taskUpdate, extraArgs=[1])
            self.laffArrowR.bind(DGG.B1RELEASE, self.__taskDone)
            return

    def unload(self):
        if not self.frame:
            return
        else:
            for element in (self.hardcoreLabel,
             self.hardcoreHelpButton,
             self.hardcoreActivateButton,
             self.frame,
             self.laffCircle,
             self.laffMeter,
             self.laffArrowL,
             self.laffArrowR,
             self.laffLabel,
             self.laffHelpButton):
                element.destroy()

            for element in (self.hardcoreIcon1,
             self.hardcoreIcon2,
             self.hardcoreIcon3,
             self.laffFrame):
                element.removeNode()

            self.destroyDialog()
            self.hardcoreLabel = None
            self.hardcoreHelpButton = None
            self.hardcoreActivateButton = None
            self.hardcoreIcon1 = None
            self.hardcoreIcon2 = None
            self.hardcoreIcon3 = None
            self.frame = None
            self.laffFrame = None
            self.laffCircle = None
            self.laffMeter = None
            self.laffArrowL = None
            self.laffArrowR = None
            self.laffLabel = None
            self.laffHelpButton = None
            return

    def destroyDialog(self, *args):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        return

    def openDialog(self, message, command = None):
        if not command:
            command = self.destroyDialog
        self.destroyDialog()
        self.dialog = TTDialog.TTDialog(style=TTDialog.Acknowledge, text=message, text_wordwrap=25, text_align=TextNode.ACenter, command=command)

    def continueToNameShop(self, *args):
        self.destroyDialog()
        messenger.send('next')

    def checkChallenges(self):
        if self.toon.hpLimit == ToontownGlobals.MaxHpLimit and not self.toon.hardcoreMode:
            self.destroyDialog()
            return True
        challenges = []
        if self.toon.hpLimit != ToontownGlobals.MaxHpLimit:
            challenges.append(TTLocalizer.LaffChallengeConfirmMessage % self.toon.hpLimit)
        if self.toon.hardcoreMode:
            challenges.append(TTLocalizer.HardcoreChallengeConfirmMessage)
        self.openDialog(TTLocalizer.ChallengeConfirmMessage % '\n'.join(challenges), self.continueToNameShop)
        return False

    def __handleDoneStatus(self, doneStatus):
        self.doneStatus = doneStatus
        messenger.send(self.doneEvent)

    def __helpHardcore(self):
        self.openDialog(TTLocalizer.HardcoreHelpMessage)

    def __helpLaff(self):
        self.openDialog(TTLocalizer.LaffLimitHelpMessage)

    def __toggleHardcore(self):
        self.toon.hardcoreMode = not self.toon.hardcoreMode
        if self.toon.hardcoreMode:
            self.hardcoreActivateButton['text'] = TTLocalizer.CapitalOn
            self.hardcoreActivateButton['image_color'] = (0, 1, 0, 1)
        else:
            self.hardcoreActivateButton['text'] = TTLocalizer.CapitalOff
            self.hardcoreActivateButton['image_color'] = (1, 0, 0, 1)

    def __updateLaffMeter(self, amount):
        self.toon.hpLimit += amount
        hitLimit = False
        if ToontownGlobals.MinHpLimit >= self.toon.hpLimit:
            self.laffArrowL['state'] = DGG.DISABLED
            hitLimit = True
        else:
            self.laffArrowL['state'] = DGG.NORMAL
        if self.toon.hpLimit >= ToontownGlobals.MaxHpLimit:
            self.laffArrowR['state'] = DGG.DISABLED
            hitLimit = True
        else:
            self.laffArrowR['state'] = DGG.NORMAL
        self.laffMeter.adjustFace(self.toon.hpLimit, ToontownGlobals.MaxHpLimit, 1)
        return hitLimit

    def __runTask(self, task):
        if task.time - task.prevTime < task.delayTime:
            return Task.cont
        task.delayTime = max(0.05, task.delayTime * 0.75)
        task.prevTime = task.time
        hitLimit = self.__updateLaffMeter(task.delta)
        if hitLimit:
            return Task.done
        else:
            return Task.cont

    def __taskDone(self, event):
        taskMgr.remove('runLaffCounter')

    def __taskUpdate(self, delta, event):
        task = Task(self.__runTask)
        task.delayTime = 0.4
        task.prevTime = 0.0
        task.delta = delta
        hitLimit = self.__updateLaffMeter(delta)
        if not hitLimit:
            taskMgr.add(task, 'runLaffCounter')