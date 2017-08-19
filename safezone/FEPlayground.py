# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.safezone.FEPlayground
from direct.task import Task
from toontown.safezone import Playground
import random

class FEPlayground(Playground.Playground):

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        taskMgr.doMethodLater(1, self.__birds, 'DG-birds')

    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('DG-birds')

    def __birds(self, task):
        return task.done
        base.playSfx(random.choice(self.loader.birdSound))
        time = random.random() * 20.0 + 1
        taskMgr.doMethodLater(time, self.__birds, 'DG-birds')
        return Task.done