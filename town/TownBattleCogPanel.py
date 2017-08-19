# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.TownBattleCogPanel
from panda3d.core import Point3, Texture
from direct.gui.DirectGui import *
from toontown.battle import SuitBattleGlobals
from toontown.suit import SuitHealthBar
from toontown.toonbase import TTLocalizer, ToontownGlobals, ToontownBattleGlobals

class TownBattleCogPanel(DirectFrame):

    def __init__(self, battle):
        DirectFrame.__init__(self, relief=None, image=Preloaded['toonBattlePanel'], image_color=(0.86, 0.86, 0.86, 0.7), scale=0.8)
        self.initialiseoptions(TownBattleCogPanel)
        self.battle = battle
        self.levelText = DirectLabel(self, text='', pos=(-0.06, 0, -0.075), text_scale=0.055)
        self.typeText = DirectLabel(self, text='', pos=(0.12, 0, -0.075), text_scale=0.045)
        self.evolveText = DirectLabel(self, relief=None, text=TTLocalizer.CogPanelEvolved, text_font=ToontownGlobals.getMinnieFont(), text_scale=0.065, text_fg=(0, 1, 1, 1), text_shadow=(0, 0, 0, 1), pos=(0.025, 0, 0.13))
        self.evolveText.hide()
        self.healthBar = SuitHealthBar.SuitHealthBar()
        self.generateHealthBar()
        self.hoverButton = DirectButton(parent=self, relief=None, image_scale=(0.07, 0, 0.06), pos=(0.105, 0, 0.05), image=ToontownGlobals.getTransparentTexture(), pressEffect=0)
        self.hoverButton.setTransparency(True)
        self.hoverButton.bind(DGG.EXIT, self.battle.hideRolloverFrame)
        self.suit = None
        self.evolvedId = None
        self.hide()
        self.accept('reloadCogPanel', self.reloadPanel)
        return

    def cleanup(self):
        self.cleanupHead()
        self.levelText.removeNode()
        self.typeText.removeNode()
        self.evolveText.removeNode()
        self.healthBar.delete()
        self.hoverButton.removeNode()
        del self.levelText
        del self.typeText
        del self.evolveText
        del self.healthBar
        del self.hoverButton
        self.ignoreAll()
        DirectFrame.destroy(self)

    def cleanupHead(self):
        if hasattr(self, 'head'):
            self.head.removeNode()
            del self.head

    def setSuit(self, suit):
        self.cleanupHead()
        self.suit = suit
        self.generateSuitHead()
        self.updateHealthBar()
        self.levelText['text'] = TTLocalizer.CogPanelLevel % suit.getActualLevel()
        self.typeText['text'] = suit.getTypeText()
        self.updateRolloverBind()
        if self.suit.doId != self.evolvedId:
            self.evolveText.hide()

    def reloadPanel(self, suit):
        if self.suit == suit or suit == 'all' and self.suit != None:
            self.evolvedId = self.suit.doId
            self.setSuit(self.suit)
            if suit != 'all':
                self.evolveText.show()
        return

    def updateRolloverBind(self):
        if not self.suit:
            return
        attributes = SuitBattleGlobals.SuitAttributes[self.suit.getStyleName()]
        groupAttacks, singleAttacks = SuitBattleGlobals.getAttacksByType(attributes)
        level = self.suit.getLevel()
        motto = TTLocalizer.BattleCogPopupWeaknesses[self.suit.getStyleName()]
        info = TTLocalizer.BattleCogPopupHP % (self.suit.getHP(), self.suit.getMaxHP())
        info += TTLocalizer.BattleCogPopup % (self.getAttackStrings(groupAttacks, level), self.getAttackStrings(singleAttacks, level), motto)
        if TTLocalizer.BattleCogPopupDangerColor in info:
            info = TTLocalizer.BattleCogPopupDanger + info
        self.hoverButton.bind(DGG.ENTER, self.battle.showRolloverFrame, extraArgs=[self, ToontownBattleGlobals.BattleHoverCog, info])

    def getAttackStrings(self, attacks, level):
        attackStrings = []
        for attack in attacks:
            hp = attack[1][level]
            attackString = TTLocalizer.BattleCogPopupAttackDanger if self.battle.isAttackDangerous(hp) else TTLocalizer.BattleCogPopupAttack
            attackStrings.append(attackString % (TTLocalizer.SuitAttackNames[attack[0]], hp))

        if attackStrings:
            return '\n'.join(attackStrings)
        return TTLocalizer.SuitPageNoAttacks

    def generateSuitHead(self):
        self.cleanupHead()
        self.head = self.attachNewNode('head')
        for part in self.suit.headParts:
            part = part.copyTo(self.head)
            part.setDepthTest(True)
            part.setDepthWrite(True)

        p1, p2 = Point3(), Point3()
        self.head.calcTightBounds(p1, p2)
        distance = p2 - p1
        scale = 0.1 / max(0.01, max(distance[0], distance[1], distance[2]))
        self.head.setPosHprScale(0.1, 0, 0.01, 180, 0, 0, scale, scale, scale)

    def generateHealthBar(self):
        self.healthBar.generate()
        self.healthBar.geom.reparentTo(self)
        self.healthBar.geom.setScale(0.5)
        self.healthBar.geom.setPos(-0.065, 0, 0.05)
        self.healthBar.geom.show()

    def updateHealthBar(self):
        if not self.suit:
            return
        self.healthBar.update(float(self.suit.getHP()) / float(self.suit.getMaxHP()))