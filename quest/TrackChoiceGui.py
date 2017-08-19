# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.quest.TrackChoiceGui
from panda3d.core import TextNode, Vec4
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import TTLocalizer

class TrackPoster(DirectFrame):
    normalTextColor = (0.3, 0.25, 0.2, 1)

    def __init__(self, trackId, callback):
        DirectFrame.__init__(self, relief=None, scale=0.8)
        self.initialiseoptions(TrackPoster)
        trackName = ToontownBattleGlobals.Tracks[trackId].capitalize()
        invModel = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        iconGeom = invModel.find('**/' + ToontownBattleGlobals.AvPropsNew[trackId][1])
        invModel.removeNode()
        self.poster = DirectFrame(parent=self, relief=None, image=Preloaded['questCard'], image_scale=(0.8, 0.58, 0.58))
        self.pictureFrame = DirectFrame(parent=self.poster, relief=None, image=Preloaded['questPictureFrame'], image_scale=0.25, image_color=(0.45, 0.8, 0.45, 1), text=trackName, text_font=ToontownGlobals.getInterfaceFont(), text_pos=(0, -0.16), text_fg=self.normalTextColor, text_scale=0.05, text_align=TextNode.ACenter, text_wordwrap=8.0, textMayChange=0, geom=iconGeom, pos=(-0.2, 0, 0.06))
        self.helpText = DirectFrame(parent=self.poster, relief=None, text=TTLocalizer.TrackChoiceGuiHelps[trackId], text_font=ToontownGlobals.getInterfaceFont(), text_fg=self.normalTextColor, text_scale=0.05, text_align=TextNode.ALeft, text_wordwrap=8.0, textMayChange=0, pos=(-0.05, 0, 0.14))
        self.chooseButton = DirectButton(parent=self.poster, relief=None, state=DGG.NORMAL, image=Preloaded['yellowButton'], image_scale=(0.7, 1, 1), text=TTLocalizer.TrackChoiceGuiChoose, text_scale=0.06, text_pos=(0, -0.02), command=callback, extraArgs=[trackId], pos=(0, 0, -0.16), scale=0.8)
        return


class TrackChoiceGui(DirectFrame):

    def __init__(self, timeout):
        DirectFrame.__init__(self, base.a2dBottomLeft, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=Vec4(0.8, 0.6, 0.4, 1), geom_scale=(1.5, 1, 1.5), geom_hpr=(0, 0, -90), pos=(0.85, 0, 1.075))
        self.initialiseoptions(TrackChoiceGui)
        self.cancelButton = DirectButton(parent=self, relief=None, image=Preloaded['yellowButton'], image_scale=(0.7, 1, 1), text=TTLocalizer.TrackChoiceGuiCancel, pos=(0.5, 0, -0.47), text_scale=0.06, text_pos=(0, -0.02), command=self.chooseTrack, extraArgs=[-1])
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self)
        self.timer.setScale(0.35)
        self.timer.setPos(-0.5, 0, -0.47)
        self.timer.countdown(timeout, self.timeout)
        self.trackChoicePosters = []
        tracks = [(0, (-0.33, 0, 0.47)),
         (1, (0.33, 0, 0.47)),
         (2, (-0.33, 0, 0)),
         (3, (0.33, 0, 0)),
         (6, (0, 0, -0.47))]
        for track in tracks:
            trackId, pos = track
            poster = TrackPoster(trackId, self.chooseTrack)
            poster.setPos(pos)
            poster.reparentTo(self)
            if base.localAvatar.hasTrackAccess(trackId):
                poster.setColorScale(0.6, 0.6, 0.6, 1)
                poster.chooseButton['state'] = DGG.DISABLED
            self.trackChoicePosters.append(poster)

        return

    def chooseTrack(self, trackId):
        self.timer.stop()
        messenger.send('chooseTrack', [trackId])

    def timeout(self):
        messenger.send('chooseTrack', [-1])