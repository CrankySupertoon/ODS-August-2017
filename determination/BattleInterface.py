# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.determination.BattleInterface
from BattleArea import *
from toontown.battle.BattleBase import CLIENT_MINIGAME_TIMEOUT, MINIGAME_MIN_MAX_HP, MINIGAME_MAX_HITS, getMinigameSquish
from toontown.toonbase import ToontownGlobals, TTLocalizer, ToontownTimer
import random

class BattleInterface(DrawnSquare):

    def __init__(self, doneCallback = None, stopCallback = None, game = None):
        DrawnSquare.__init__(self, pos=(-0.75, 0, -0.8), scale=(1.5, 0, 1.1))
        self.card.setScale(self.scale)
        if not game:
            game = getRandomGame()
        self.game = game(shakeCallback=self.updateHitLabel, endCallback=doneCallback, stopCallback=stopCallback, pos=(-0.525, 0, -0.645))
        self.nameLabel = DirectLabel(relief=None, pos=(-0.025, 0, 0.175), text=self.game.getName(), text_fg=self.game.HEART_COLOR, text_shadow=(0.5, 0.5, 0.5, 1), text_scale=0.12, text_font=ToontownGlobals.getSuitFont())
        self.winLabel = DirectLabel(relief=None, pos=(-0.025, 0, -0.745), text='', text_fg=self.game.HEART_COLOR, text_shadow=(0.5, 0.5, 0.5, 1), text_scale=0.07, text_font=ToontownGlobals.getSuitFont())
        self.hitLabel = DirectLabel(relief=None, pos=(-0.64, 0, -0.25), text='', text_fg=self.game.HEART_COLOR, text_shadow=(0.5, 0.5, 0.5, 1), text_scale=0.05, text_font=ToontownGlobals.getSuitFont())
        self.controlLabel = DirectLabel(relief=None, pos=(0.61, 0, -0.2), text='', text_fg=self.game.HEART_COLOR, text_shadow=(0.5, 0.5, 0.5, 1), text_scale=0.035, text_font=ToontownGlobals.getSuitFont())
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.setScale(0.4)
        self.timer.countdown(CLIENT_MINIGAME_TIMEOUT)
        self.updateHitLabel(False)
        self.updateControlLabel()
        self.game.initGameSequence()
        return

    def destroy(self):
        if not DrawnSquare.destroy(self):
            return
        for label in (self.nameLabel,
         self.winLabel,
         self.hitLabel,
         self.controlLabel):
            label.removeNode()

        self.timer.destroy()
        self.game.destroy()
        del self.nameLabel
        del self.winLabel
        del self.hitLabel
        del self.controlLabel
        del self.timer

    def updateHitLabel(self, squish = True):
        self.hitLabel['text'] = TTLocalizer.MinigameHits % self.game.hits
        if squish and self.game.hits <= MINIGAME_MAX_HITS and base.localAvatar.getMaxHp() >= MINIGAME_MIN_MAX_HP:
            base.localAvatar.d_squish(getMinigameSquish(base.localAvatar.getHp()))

    def updateControlLabel(self):
        self.controlLabel['text'] = TTLocalizer.MinigameControls % tuple([ TTLocalizer.getFancyButtonName(base.getKey(ToontownGlobals.CONTROL_INPUT_STATES[key])) for key in ALL_KEYS ])