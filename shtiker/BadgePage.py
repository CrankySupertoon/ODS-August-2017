# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.shtiker.BadgePage
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer, ToontownGlobals
from BookElements import *
import ShtikerPage
import math

class BadgePage(ShtikerPage.ShtikerPage):

    def load(self):
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.BadgePageTitle, text_scale=0.12, textMayChange=0, pos=(0, 0, 0.62))
        self.bar = DirectWaitBar(parent=self, relief=DGG.SUNKEN, scale=0.45, pos=(-0.225, 0, -0.6), frameSize=(-1, 2, -0.1, 0.1), borderWidth=(0.025, 0.025), frameColor=(0.95, 0.9, 0.55, 1), barColor=(1, 0.55, 0, 1), range=ToontownGlobals.BADGE_MAX, text='', text_fg=(0.05, 0.14, 0.2, 1), text_align=TextNode.ACenter, text_pos=(0.47, -0.035))
        self.leftArrow = DirectButton(parent=self, relief=None, pos=(-0.835, 0, -0.45), image=Preloaded['yellowArrow'], image_scale=0.8, command=self.switchPage, extraArgs=[-1])
        self.rightArrow = DirectButton(parent=self, relief=None, pos=(-0.05, 0, -0.45), image=Preloaded['yellowArrow'], image_scale=-0.8, command=self.switchPage, extraArgs=[1])
        self.pageCount = DirectLabel(parent=self, relief=None, pos=(-0.45, 0, -0.465), text='', text_scale=0.07)
        self.info = DirectFrame(parent=self, relief=None, pos=(0.435, 0, 0.04), geom=Preloaded['squareBox'], geom_scale=(0.7, 0, 1.1), text='', text_wordwrap=8, text_scale=0.08, text_pos=(0, 0.4))
        self.equipButton = DirectButton(parent=self.info, relief=None, pos=(0, 0, -0.37), image=Preloaded['blueButton'], text='', text_scale=0.11, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, -0.02), command=self.equip)
        self.currentPage = 0
        self.currentBadge = 0
        self.equippedBadge = base.localAvatar.getEquippedBadge()
        self.chosenBadge = False
        self.pages = int(math.ceil(ToontownGlobals.BADGE_COUNT / 4.0))
        self.badges = []
        for i in xrange(4):
            badge = DirectButton(parent=self, relief=None, pos=ToontownGlobals.BADGE_POSITIONS[i], geom=Preloaded['paperNote'], geom_scale=0.45, text='', text_scale=0.047, text_wordwrap=8.5, text_pos=(0, 0.05), text_font=ToontownGlobals.getMinnieFont(), command=self.openBadge)
            badge.setTransparency(True)
            self.badges.append(badge)

        self.openBadge(0)
        return

    def enter(self):
        self.equippedBadge = base.localAvatar.getEquippedBadge()
        self.chosenBadge = False
        self.updateBadges()
        self.show()
        self.accept('badgeHistoryUpdated', self.updateBadges)

    def exit(self):
        self.ignoreAll()
        if self.chosenBadge:
            base.localAvatar.sendUpdate('requestEquippedBadge', [self.equippedBadge])
        self.hide()

    def unload(self):
        self.title.destroy()
        del self.title
        self.bar.destroy()
        del self.bar
        self.leftArrow.destroy()
        del self.leftArrow
        self.rightArrow.destroy()
        del self.rightArrow
        self.pageCount.destroy()
        del self.pageCount
        self.info.destroy()
        del self.info
        self.equipButton.destroy()
        del self.equipButton
        for badge in self.badges:
            badge.destroy()

        del self.badges
        ShtikerPage.ShtikerPage.unload(self)

    def updateBadges(self):
        self.pageCount['text'] = '%s/%s' % (self.currentPage + 1, self.pages)
        if self.currentPage == 0:
            self.leftArrow.hide()
        else:
            self.leftArrow.show()
        if self.currentPage == self.pages - 1:
            self.rightArrow.hide()
        else:
            self.rightArrow.show()
        currentProgress = base.localAvatar.getAllBadgeProgress()
        self.bar['value'] = currentProgress
        self.bar['text'] = '%s/%s' % (currentProgress, ToontownGlobals.BADGE_MAX)
        index = self.currentPage * 4
        for i, badge in enumerate(self.badges):
            realIndex = index + i
            if realIndex >= ToontownGlobals.BADGE_COUNT:
                badge.hide()
                continue
            name = TTLocalizer.Badges[realIndex][1]
            task, current, required, done = base.localAvatar.getBadgeProgress(realIndex)
            badge.show()
            badge['text'] = name if done else '%s\n%s/%s' % (name, current, required)
            badge['extraArgs'] = [realIndex]
            badge.setColor(ToontownGlobals.BADGE_PROGRESS_COLORS[current >= required])

        self.openBadge(self.currentBadge)

    def switchPage(self, index):
        self.currentPage += index
        self.updateBadges()

    def openBadge(self, badge):
        self.currentBadge = badge
        name = TTLocalizer.getFullBadgeName(badge)
        task, current, required, done = base.localAvatar.getBadgeProgress(badge)
        taskName = TTLocalizer.getBadgeTaskName(task, required)
        progress = '\x01%s\x01%s\x02' % ('forestGreen' if done else 'red', TTLocalizer.BadgeReady if done else '%s/%s' % (current, required))
        self.info['geom_color'] = ToontownGlobals.BADGE_COLORS[task]
        self.info['text'] = '%s\n\n%s\n\n%s' % (name, taskName, progress)
        if not done:
            self.equipButton.hide()
            return
        equipped = self.equippedBadge == badge + 1
        self.equipButton.show()
        self.equipButton['text'] = TTLocalizer.BadgeUnequip if equipped else TTLocalizer.BadgeEquip
        self.equipButton['extraArgs'] = [badge]

    def equip(self, badge):
        if self.equippedBadge == badge + 1:
            self.equippedBadge = 0
            self.equipButton['text'] = TTLocalizer.BadgeEquip
        else:
            self.equippedBadge = badge + 1
            self.equipButton['text'] = TTLocalizer.BadgeUnequip
        self.chosenBadge = True