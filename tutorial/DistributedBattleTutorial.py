# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.DistributedBattleTutorial
from toontown.battle.DistributedBattle import DistributedBattle
from direct.directnotify import DirectNotifyGlobal

class DistributedBattleTutorial(DistributedBattle):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleTutorial')

    def __init__(self, cr):
        DistributedBattle.__init__(self, cr)

    def startTimer(self, ts = 0):
        self.townBattle.timer.hide()

    def playReward(self, ts):
        self.movie.playTutorialReward(ts, self.uniqueName('reward'), self.handleRewardDone)

    def removeLocalToon(self):
        base.localAvatar.earnedExperience = None
        self.localToonFsm.request('NoLocalToon')
        base.cr.playGame.place.tutorial.startIntroAftermatch()
        return