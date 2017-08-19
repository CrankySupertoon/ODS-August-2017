# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.shtiker.DisguisePage
from panda3d.core import TextNode, Vec4
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.suit import SuitDNA
from toontown.battle import SuitBattleGlobals
from toontown.coghq import CogDisguiseGlobals
from toontown.suit.Suit import Suit
import ShtikerPage
DeptColors = (Vec4(0.647, 0.608, 0.596, 1.0),
 Vec4(0.588, 0.635, 0.671, 1.0),
 Vec4(0.596, 0.714, 0.659, 1.0),
 Vec4(0.761, 0.678, 0.69, 1.0),
 Vec4(0.556, 0.392, 0.541, 1.0))
PartTypeToNode = [('legs',),
 ('legs',),
 ('torso', 'joint_attachMeter'),
 ('arms',),
 ('arms',),
 ('to_head', 'joint_head')]

class DisguisePage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.title = DirectLabel(self, relief=None, text=TTLocalizer.DisguisePageTitle, text_scale=0.12, pos=(0, 0, 0.62))
        self.deptFrame = DirectFrame(self, relief=DGG.SUNKEN, frameSize=(-0.51, 0.51, -0.1, 0.08), frameColor=(0.85, 0.95, 1, 1), borderWidth=(0.01, 0.01), pos=(0, 0, 0.485))
        self.deptIcons = []
        self.suits = []
        iconModel = loader.loadModel('phase_3/models/gui/cog_icons')
        for i in xrange(len(SuitDNA.suitDepts)):
            icon = DirectButton(self.deptFrame, relief=None, geom=iconModel.find(SuitDNA.suitDeptModelPaths[i]), state=DGG.NORMAL, scale=0.15, pos=(-0.4 + i * 0.2, 0, -0.01), command=self.__chooseDept, extraArgs=[i])
            self.deptIcons.append(icon)

        self.cogLabel = DirectLabel(self, relief=None, text_font=ToontownGlobals.getSuitFont(), text='', text_scale=0.07, pos=(-0.45, 0, -0.525), text_shadow=(0.5, 0.5, 0.5, 1))
        self.rightFrame = DirectFrame(self, relief=None, pos=(0.43, 0, -0.15))
        self.meritBar = DirectWaitBar(self.rightFrame, relief=DGG.SUNKEN, frameSize=(-1.2, 1.2, -0.15, 0.15), borderWidth=(0.02, 0.02), scale=0.3, text='', text_scale=0.18, text_fg=(0, 0, 0, 1), text_align=TextNode.ALeft, text_pos=(-1.16, -0.05), pos=(0.005, 0, 0.125))
        self.promotionLabel = DirectLabel(self.rightFrame, relief=None, text_font=ToontownGlobals.getSuitFont(), text_shadow=(0, 0, 0, 1), text='', text_scale=0.065, text_wordwrap=11)
        self.dept = -1
        self.updatePage()
        self.__chooseDept(0)
        return

    def unload(self):
        ShtikerPage.ShtikerPage.unload(self)
        self.title.destroy()
        del self.title
        self.deptFrame.destroy()
        del self.deptFrame
        self.cogLabel.destroy()
        del self.cogLabel
        self.rightFrame.destroy()
        del self.rightFrame
        self.meritBar.destroy()
        del self.meritBar
        self.promotionLabel.destroy()
        del self.promotionLabel
        for icon in self.deptIcons:
            icon.destroy()

        del self.deptIcons
        for suit in self.suits:
            suit.delete()

        del self.suits

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)

    def updatePage(self):
        for suit in self.suits:
            suit.delete()

        self.suits = []
        for i in xrange(len(SuitDNA.suitDepts)):
            dna = SuitDNA.SuitDNA()
            dna.newSuit(self.getCogHead(i))
            suit = Suit()
            suit.setDNA(dna)
            suit.setDepthWrite(True)
            suit.setDepthTest(True)
            suit.setScale(0.08)
            suit.setPos(-0.45, 0, -0.4)
            suit.setH(190)
            suit.deleteDropShadow()
            suit.destroyNametag3d()
            suit.reparentTo(self)
            suit.loop('neutral')
            suit.setTransparency(True)
            suit.find('**/').removeNode()
            suit.hide()
            self.suits.append(suit)

        if self.dept != -1:
            self.update()

    def getCogIndex(self, dept):
        return base.localAvatar.cogTypes[dept] + SuitDNA.suitsPerDept * dept

    def getCogHead(self, dept):
        return SuitDNA.suitHeadTypes[self.getCogIndex(dept)]

    def getCogName(self, dept):
        return SuitBattleGlobals.SuitAttributes[self.getCogHead(dept)]['name']

    def getCogLevel(self, dept):
        return base.localAvatar.cogLevels[dept] + 1

    def setPromotionColor(self, color):
        self.promotionLabel['text_fg'] = color

    def update(self):
        for suit in self.suits:
            suit.hide()

        suit = self.suits[self.dept]
        suit.show()
        self.cogLabel['text'] = '%s\n%s' % (self.getCogName(self.dept), TTLocalizer.DisguisePageCogLevel % self.getCogLevel(self.dept))
        r, g, b, _ = DeptColors[self.dept]
        self.meritBar['frameColor'] = (r * 0.7,
         g * 0.7,
         b * 0.7,
         1)
        self.meritBar['barColor'] = (r,
         g,
         b,
         1)
        if CogDisguiseGlobals.isSuitComplete(base.localAvatar.cogParts, self.dept):
            totalMerits = CogDisguiseGlobals.getTotalMerits(base.localAvatar, self.dept)
            merits = base.localAvatar.cogMerits[self.dept]
            if totalMerits:
                self.meritBar['range'] = totalMerits
                self.meritBar['value'] = merits
                if merits == totalMerits:
                    self.meritBar['text'] = TTLocalizer.RewardPanelMeritAlert
                    promotionText = TTLocalizer.RewardPanelMeritAlert
                    promotionColor = Vec4(0, 0.8, 0, 1)
                else:
                    meritLabel = TTLocalizer.RewardPanelMeritBarLabels[self.dept]
                    self.meritBar['text'] = '%s/%s %s' % (merits, totalMerits, meritLabel)
                    promotionText = TTLocalizer.RewardPanelMissing % (totalMerits - merits, meritLabel)
                    promotionColor = Vec4(0.8, 0, 0, 1)
            else:
                self.meritBar['range'] = 1
                self.meritBar['value'] = 1
                self.meritBar['text'] = TTLocalizer.RewardPanelMeritsMaxed
                promotionText = TTLocalizer.RewardPanelMaxedMeritAlert
                promotionColor = Vec4(0, 0.7, 0, 1)
        else:
            totalParts = CogDisguiseGlobals.PartsPerSuit[self.dept]
            parts = CogDisguiseGlobals.getTotalParts(base.localAvatar.cogParts[self.dept])
            self.meritBar['range'] = totalParts
            self.meritBar['value'] = parts
            self.meritBar['text'] = '%s/%s %s' % (parts, totalParts, TTLocalizer.RewardPanelPartBarLabel)
            promotionText = TTLocalizer.RewardPanelMissing % (totalParts - parts, TTLocalizer.RewardPanelPartBarLabel)
            promotionColor = Vec4(0.8, 0, 0, 1)
        self.promotionLabel['text'] = promotionText
        self.setPromotionColor(promotionColor)
        for parts in PartTypeToNode:
            for part in parts:
                node = suit.find('**/' + part)
                if node:
                    node.clearColorScale()

        for i, parts in enumerate(PartTypeToNode):
            if not CogDisguiseGlobals.isPartComplete(base.localAvatar.cogParts, i, self.dept):
                for part in parts:
                    node = suit.find('**/' + part)
                    if node:
                        node.setColorScale(1, 1, 1, 0.1)

    def __chooseDept(self, dept):
        for icon in self.deptIcons:
            icon['state'] = DGG.NORMAL

        self.deptIcons[dept]['state'] = DGG.DISABLED
        self.dept = dept
        self.update()