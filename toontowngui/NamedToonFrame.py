# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toontowngui.NamedToonFrame
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from toontown.racing.RaceHeadFrame import RaceHeadFrame

class NamedToonFrame(RaceHeadFrame):

    def __init__(self, dna, name, command, extraArgs, color = (1, 1, 1, 1), scale = 0.35, textPos = (0.3, 0, 0.03), textScale = 0.13):
        RaceHeadFrame.__init__(self, dna, color, geom_scale=(0.5, 1, 0.5), geom1_color=(0.5, 0.9, 1, 1), geom2_color=(1, 1, 0, 1), command=command, extraArgs=extraArgs, scale=scale)
        self.initialiseoptions(NamedToonFrame)
        self.name = DirectButton(self, relief=None, text=name, text_scale=textScale, pos=textPos, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_align=TextNode.ALeft, text_wordwrap=10.5, text1_bg=(0.5, 0.9, 1, 1), text2_bg=(1, 1, 0, 1), command=command, extraArgs=extraArgs)
        return

    def destroy(self):
        RaceHeadFrame.destroy(self)
        self.name.destroy()
        del self.name