# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toonbase.ToontownTransitions
from panda3d.core import Vec3
from direct.showbase.Transitions import Transitions

class ToontownTransitions(Transitions):
    IrisModelName = 'phase_3/models/misc/iris'
    FadeModelName = 'phase_3/models/misc/fade'

    def __init__(self, model = None, pos = Vec3(0, 0, 0)):
        Transitions.__init__(self, None, model=model, pos=pos)
        return

    def loadFade(self):
        Transitions.loadFade(self)
        self.fade.setScale(30)