# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.racing.RaceHeadFrame
from panda3d.core import Vec4
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toon import ToonHead

class RaceHeadFrame(DirectButton):

    def __init__(self, av = None, color = Vec4(1, 1, 1, 1), *args, **kwargs):
        self.panelGeom = loader.loadModel('phase_4/models/karting/racing_panel')
        self.panelGeom.find('**/*fg').setColor(color)
        opts = {'relief': None,
         'geom': self.panelGeom,
         'geom_scale': (1, 1, 0.5),
         'pos': (0, 0, 0)}
        opts.update(kwargs)
        apply(DirectButton.__init__, (self,) + args, opts)
        self.initialiseoptions(RaceHeadFrame)
        if av:
            self.setAv(av)
        return

    def setAv(self, av):
        self.head = self.attachNewNode('head', 20)
        self.head.setPosHprScale(0, -0.5, -0.09, 180.0, 0.0, 0.0, 0.2, 0.2, 0.2)
        self.head.setBin('gui-popup', 0)
        self.headModel = ToonHead.ToonHead()
        self.headModel.setupHead(av, forGui=1)
        self.headModel.reparentTo(self.head)

    def destroy(self):
        self.headModel.delete()
        del self.headModel
        self.head.removeNode()
        del self.head
        DirectButton.destroy(self)