# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toptoons.PeriodPicker
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals, TTLocalizer
from CategoryPicker import CategoryPicker

class PeriodPicker(DirectFrame):

    def __init__(self, successCallback, failCallback, *args, **kwargs):
        self.successCallback = successCallback
        self.failCallback = failCallback
        baseArgs = {'relief': None,
         'geom': DGG.getDefaultDialogGeom(),
         'geom_color': ToontownGlobals.GlobalDialogColor,
         'geom_scale': (1.5, 1, 1),
         'pos': (0, 0, -2.5),
         'text': TTLocalizer.TopToonsPeriodTitle,
         'text_scale': 0.1,
         'text_pos': (0, 0.325)}
        kwargs.update(baseArgs)
        DirectFrame.__init__(self, *args, **kwargs)
        self.initialiseoptions(PeriodPicker)
        jarGui = loader.loadModel('phase_3.5/models/gui/jar_gui')
        jar = jarGui.find('**/Jar')
        self.jars = []
        for i, x in enumerate([-0.45, 0, 0.45]):
            self.jars.append(DirectButton(self, relief=None, state=DGG.DISABLED, image=jar, image_scale=0.25 + i * 0.2, text_scale=0.075, text2_scale=0.085, text_pos=(0, -0.25), text=TTLocalizer.TopToonPeriods[i] + '\n' + TTLocalizer.TopToons, pos=(x, 0, 0), command=self.__choose, extraArgs=[2 - i]))

        self.stopButton = DirectButton(self, relief=None, state=DGG.DISABLED, image=Preloaded['circleButton'], image_color=(1, 0.55, 0, 1), image_scale=0.5, pos=(0.65, 0, 0.4), text='X', text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.05, text_pos=(-0.005, -0.01), command=self.__close)
        self.auxiliaryGui = None
        self.appearSequence = Sequence(self.posInterval(1.5, (0, 0, 0), (0, 0, -2.5), blendType='easeInOut'), Func(self.enableButtons))
        self.appearSequence.start()
        return

    def destroy(self):
        DirectFrame.destroy(self)
        if self.auxiliaryGui:
            self.auxiliaryGui.destroy()
        self.auxiliaryGui = None
        if not hasattr(self, 'jars'):
            return
        else:
            for jar in self.jars:
                jar.destroy()

            del self.jars
            self.stopButton.destroy()
            del self.stopButton
            return

    def enableButtons(self):
        for button in self.jars + [self.stopButton]:
            button['state'] = DGG.NORMAL

    def __choose(self, period):
        self.destroy()
        self.auxiliaryGui = CategoryPicker(self.successCallback, self.failCallback, period)

    def __close(self):
        self.failCallback()
        self.destroy()