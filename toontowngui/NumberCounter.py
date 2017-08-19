# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toontowngui.NumberCounter
from direct.gui.DirectGui import *
from direct.task.Task import Task

class NumberCounter(DirectFrame):

    def __init__(self, minimum, maximum, event, increment, *args, **kwargs):
        DirectFrame.__init__(self)
        self.initialiseoptions(NumberCounter)
        self.minimum = minimum
        self.maximum = maximum
        self.current = self.minimum
        self.event = event
        self.downArrow = DirectButton(self, relief=None, image=Preloaded['blueArrow'], image_scale=(-1, 1, 1), pos=(-0.13, 0, 0), state=DGG.NORMAL)
        self.upArrow = DirectButton(self, relief=None, image=Preloaded['blueArrow'], image_scale=1, pos=(0.13, 0, 0), state=DGG.NORMAL)
        self.label = DirectLabel(self, relief=None, text='', text_scale=0.06, text_pos=(0, -0.015))
        self.downArrow.bind(DGG.B1PRESS, self.__taskUpdate, extraArgs=[-1])
        self.downArrow.bind(DGG.B1RELEASE, self.__taskDone)
        self.upArrow.bind(DGG.B1PRESS, self.__taskUpdate, extraArgs=[1])
        self.upArrow.bind(DGG.B1RELEASE, self.__taskDone)
        self.increment = increment
        self.delay = 0.001
        self.updateCounter(0)
        return

    def destroy(self):
        DirectFrame.destroy(self)
        if hasattr(self, 'downArrow'):
            self.downArrow.destroy()
            self.upArrow.destroy()
            self.label.destroy()
            del self.downArrow
            del self.upArrow
            del self.label

    def updateCounter(self, amount):
        self.current += amount * self.increment
        hitLimit = 0
        if self.current <= self.minimum:
            self.downArrow['state'] = DGG.DISABLED
            self.current = self.minimum
            hitLimit = 1
        else:
            self.downArrow['state'] = DGG.NORMAL
        if self.current >= self.maximum:
            self.upArrow['state'] = DGG.DISABLED
            self.current = self.maximum
            hitLimit = 1
        else:
            self.upArrow['state'] = DGG.NORMAL
        self.label['text'] = str(self.current)
        if amount != 0:
            messenger.send(self.event, [self.current])
        return hitLimit

    def __runTask(self, task):
        if task.time - task.prevTime < task.delayTime:
            return Task.cont
        task.delayTime = self.delay
        task.prevTime = task.time
        hitLimit = self.updateCounter(task.delta)
        if hitLimit:
            return Task.done
        else:
            return Task.cont

    def __taskDone(self, event):
        messenger.send('wakeup')
        taskMgr.remove(self.taskName('runCounter'))

    def __taskUpdate(self, delta, event):
        messenger.send('wakeup')
        task = Task(self.__runTask)
        task.delayTime = 0.1
        task.prevTime = 0.0
        task.delta = delta
        hitLimit = self.updateCounter(delta)
        if not hitLimit:
            taskMgr.add(task, self.taskName('runCounter'))