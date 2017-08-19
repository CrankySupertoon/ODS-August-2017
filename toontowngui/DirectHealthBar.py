# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toontowngui.DirectHealthBar
from direct.gui.DirectGui import *
from toontown.suit import SuitHealthBar

class DirectHealthBar(DirectWaitBar):

    def __init__(self, *args, **kwargs):
        DirectWaitBar.__init__(self, *args, **kwargs)
        self.initialiseoptions(DirectHealthBar)

    def updateColor(self):
        r, g, b, _ = SuitHealthBar.HEALTH_COLORS[SuitHealthBar.getHealthCondition(self.getPercentage(self['value'], self['range']))]
        self['barColor'] = (r,
         g,
         b,
         1)
        self['frameColor'] = (r * 0.7,
         g * 0.7,
         b * 0.7,
         1)

    def getPercentage(self, value, range):
        return float(value) / float(range)