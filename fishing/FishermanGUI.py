# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.fishing.FishermanGUI
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toon import NPCToons
from FishSellGUI import FishSellGUI
from FishBrowser import FishBrowser
import FishGlobals, math

class BaitGUI:

    def __init__(self, buyCallback, cancelCallback):
        self.loaded = False
        self.buyCallback = buyCallback
        self.cancelCallback = cancelCallback

    def load(self):
        if self.loaded:
            return
        else:
            self.frame = DirectFrame(relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(1.3, 1, 1.5), pos=(0, 0, 0.14))
            self.browser = FishBrowser(self.frame, pos=(0, 0, 0.15), scale=0.8, command=self.updateFish)
            self.title = DirectLabel(self.frame, relief=None, text=TTLocalizer.BaitBuyTitle, text_scale=0.08, pos=(0, 0, 0.65))
            self.slider = DirectSlider(self.frame, state=DGG.NORMAL, thumb_relief=None, pageSize=5, thumb_geom=Preloaded['circle'], thumb_geom_scale=2, scale=0.4, pos=(0, 0, -0.35), range=(1, 1.01), command=self.updateSliderLabel)
            self.sliderLabel = DirectLabel(self.frame, relief=None, text_scale=0.045, text=TTLocalizer.BaitBuyUnknownText, pos=(0, 0, -0.44))
            self.buyButton = DirectButton(self.frame, state=DGG.NORMAL, relief=None, geom=Preloaded['yellowButton'], geom_scale=(0.6, 1, 1), text=TTLocalizer.BaitBuyText, text_scale=0.06, text_pos=(0, -0.01), pos=(-0.3, 0, -0.65), command=self.__buy)
            self.cancelButton = DirectButton(self.frame, relief=None, geom=Preloaded['yellowButton'], geom_scale=(0.6, 1, 1), text=TTLocalizer.lCancel, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, -0.65), command=self.__cancel)
            self.beanBank = DirectLabel(self.frame, relief=None, pos=(-0.3, 0, -0.62), scale=0.5, image=Preloaded['beanBank'], text='', text_align=TextNode.ARight, text_scale=0.11, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_pos=(0.75, -0.81), text_font=ToontownGlobals.getSignFont())
            self.loaded = True
            return

    def destroy(self):
        if not self.loaded:
            return
        self.frame.destroy()
        self.browser.destroy()
        del self.frame
        del self.browser
        del self.title
        del self.slider
        del self.sliderLabel
        del self.buyButton
        del self.cancelButton
        del self.beanBank
        self.loaded = False

    def getBaitNum(self):
        return int(math.floor(self.slider['value']))

    def getCurrentBaitNum(self, bait):
        return base.localAvatar.fishingBaits.get(bait, 0)

    def getBait(self):
        if not hasattr(self, 'browser'):
            return 0
        return self.browser.index * 2

    def isUnlocked(self, genus):
        return len(FishGlobals.getSpecies(genus)) == 1 or base.localAvatar.fishCollection.hasGenus(genus)

    def disableGui(self, text):
        self.slider['state'] = DGG.DISABLED
        self.buyButton['state'] = DGG.DISABLED
        self.sliderLabel['text'] = text
        self.beanBank['text'] = str(base.localAvatar.getBankMoney())

    def updateFish(self):
        if not hasattr(self, 'slider'):
            return
        bait = self.getBait()
        if not self.isUnlocked(bait):
            self.disableGui(TTLocalizer.BaitBuyUnknownText)
            return
        maxValue = min(65535 - self.getCurrentBaitNum(bait), FishGlobals.MaxBaitBuy)
        maxValue = min(maxValue, int(math.floor(base.localAvatar.getBankMoney() / FishGlobals.BaitPrice[bait])))
        if maxValue <= 0:
            self.disableGui(TTLocalizer.BaitBuyFullText)
            return
        self.slider['range'] = (1, maxValue + 0.01)
        self.slider['value'] = 1
        self.slider['state'] = DGG.NORMAL
        self.buyButton['state'] = DGG.NORMAL
        self.updateSliderLabel()

    def enter(self):
        self.updateFish()

    def updateSliderLabel(self):
        bait = self.getBait()
        baitNum = self.getBaitNum()
        name = TTLocalizer.FishGenusNames[bait]
        currentBait = self.getCurrentBaitNum(bait)
        jellybeanCost = int(math.ceil(baitNum * FishGlobals.BaitPrice[bait]))
        if self.isUnlocked(bait):
            self.sliderLabel['text'] = TTLocalizer.BaitBuyHelpText % (baitNum,
             name,
             jellybeanCost,
             currentBait)
        self.beanBank['text'] = str(base.localAvatar.getBankMoney() - jellybeanCost)

    def __buy(self):
        self.buyCallback(self.getBait(), self.getBaitNum())
        self.destroy()

    def __cancel(self):
        self.destroy()
        self.cancelCallback()


class RepairGUI:

    def __init__(self, repairCallback, cancelCallback):
        self.loaded = False
        self.repairCallback = repairCallback
        self.cancelCallback = cancelCallback

    def load(self):
        if self.loaded:
            return
        else:
            self.frame = DirectFrame(relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(1, 1, 0.6))
            self.title = DirectLabel(self.frame, relief=None, text='', text_scale=0.07, text_wordwrap=13, pos=(0, 0, 0.2))
            self.slider = DirectSlider(self.frame, thumb_relief=None, pageSize=5, thumb_geom=Preloaded['circle'], thumb_geom_scale=2, scale=0.4, pos=(0, 0, 0.025), command=self.updateSliderLabel)
            self.sliderLabel = DirectLabel(self.frame, relief=None, text_scale=0.045, text='', pos=(0, 0, -0.065))
            self.repairButton = DirectButton(self.frame, relief=None, geom=Preloaded['yellowButton'], geom_scale=(0.6, 1, 1), text=TTLocalizer.RodRepairText, text_scale=0.06, text_pos=(0, -0.01), pos=(-0.3, 0, -0.2), command=self.__repair)
            self.cancelButton = DirectButton(self.frame, relief=None, geom=Preloaded['yellowButton'], geom_scale=(0.6, 1, 1), text=TTLocalizer.lCancel, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, -0.2), command=self.__cancel)
            self.beanBank = DirectLabel(self.frame, relief=None, pos=(-0.35, 0, -0.12), scale=0.6, image=Preloaded['beanBank'], text='', text_align=TextNode.ARight, text_scale=0.11, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_pos=(0.75, -0.81), text_font=ToontownGlobals.getSignFont())
            self.loaded = True
            return

    def destroy(self):
        if not self.loaded:
            return
        self.frame.destroy()
        del self.frame
        del self.title
        del self.slider
        del self.sliderLabel
        del self.repairButton
        del self.cancelButton
        del self.beanBank
        self.loaded = False

    def getDurability(self, rod):
        return (base.localAvatar.getFishingRodDurability()[rod], FishGlobals.Rod2Durability[rod], FishGlobals.Rod2RepairJellybean[rod])

    def enter(self):
        rod = base.localAvatar.getFishingRod()
        durability, maxDurability, jellybeanCost = self.getDurability(rod)
        durabilityCeil = min(maxDurability - durability, int(math.floor(base.localAvatar.getBankMoney() / jellybeanCost)))
        self.title['text'] = TTLocalizer.RodRepairTitle % TTLocalizer.FishingRodNameDict[rod]
        self.slider['range'] = (1, durabilityCeil + 0.01)
        self.slider['value'] = 1
        self.updateSliderLabel()

    def getDurabilityRecover(self):
        return int(math.floor(self.slider['value']))

    def updateSliderLabel(self):
        rod = base.localAvatar.getFishingRod()
        durability, maxDurability, jellybeanCost = self.getDurability(rod)
        durabilityRecover = self.getDurabilityRecover()
        jellybeanCost = int(math.ceil(durabilityRecover * jellybeanCost))
        self.sliderLabel['text'] = '%s/%s\n%s' % (durability + durabilityRecover, maxDurability, TTLocalizer.PaintGUINotice % jellybeanCost)
        self.beanBank['text'] = str(base.localAvatar.getBankMoney() - jellybeanCost)

    def __repair(self):
        self.repairCallback(self.getDurabilityRecover())
        self.destroy()

    def __cancel(self):
        self.destroy()
        self.cancelCallback()


class FishermanGUI:

    def __init__(self, saleCallback, repairCallback, upgradeCallback, buyBaitCallback, pos = (0, 0, 0)):
        self.loaded = False
        self.saleCallback = saleCallback
        self.repairCallback = repairCallback
        self.upgradeCallback = upgradeCallback
        self.buyBaitCallback = buyBaitCallback
        self.pos = pos

    def load(self):
        if self.loaded:
            return
        else:
            self.frame = DirectFrame(relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(0.9, 1, 1), pos=self.pos)
            i = 0.375
            self.repairButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(0, 0.5, 1, 1), text=TTLocalizer.FishermanRepair, text_scale=0.08, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, i), command=self.__repair)
            self.sellButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(0, 0.5, 1, 1), text=TTLocalizer.PetshopSell, text_scale=0.08, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, i - 0.12), command=self.__sell)
            self.buyRodButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(0, 0.5, 1, 1), text=TTLocalizer.FishermanBuyRod, text_scale=0.08, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, i - 0.24), command=self.__buyRod)
            self.upgradeTankButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(0, 0.5, 1, 1), text=TTLocalizer.FishermanUpgradeTank, text_scale=0.08, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, i - 0.36), command=self.__upgradeTank)
            self.buyLureButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(0, 0.5, 1, 1), text=TTLocalizer.FishermanBuyLure, text_scale=0.08, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, i - 0.48), command=self.__buyLure)
            self.buyBaitButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(0, 0.5, 1, 1), text=TTLocalizer.FishermanBuyBaits, text_scale=0.08, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, i - 0.6), command=self.__buyBait)
            self.cancelButton = DirectButton(self.frame, relief=None, state=DGG.NORMAL, geom=Preloaded['squareBox'], geom_scale=(0.75, 1, 0.1), geom_color=(1, 0, 0, 1), text=TTLocalizer.lCancel, text_scale=0.08, text_pos=(0, -0.02), text_shadow=(0, 0, 0, 1), text_fg=(1, 1, 1, 1), pos=(0, 0, i - 0.72), command=self.__cancel)
            self.gui = None
            self.loaded = True
            return

    def destroy(self):
        if self.gui:
            self.gui.destroy()
            self.gui = None
        if not self.loaded:
            return
        else:
            self.frame.destroy()
            del self.frame
            del self.repairButton
            del self.sellButton
            del self.buyRodButton
            del self.upgradeTankButton
            del self.buyLureButton
            del self.cancelButton
            self.loaded = False
            return

    def enter(self):
        rod = base.localAvatar.getFishingRod()
        self.setButtonState(self.repairButton, base.localAvatar.getBankMoney() >= 1 and base.localAvatar.getFishingRodDurability()[rod] < FishGlobals.Rod2Durability[rod])
        self.setButtonState(self.sellButton, base.localAvatar.fishTank.getTotalValue() > 0)
        self.setButtonState(self.buyRodButton, base.localAvatar.getMaxFishingRod() < FishGlobals.MaxRodId)
        self.setButtonState(self.upgradeTankButton, base.localAvatar.getMaxFishTank() < FishGlobals.MaxTank)
        self.setButtonState(self.buyLureButton, base.localAvatar.getMaxFishingLure() < FishGlobals.MaxLureId)
        self.setButtonState(self.buyBaitButton, base.localAvatar.getBankMoney() >= 3)

    def setButtonState(self, button, state):
        state = DGG.NORMAL if state else DGG.DISABLED
        button['geom_color'] = (0, 0.5, 1, 1) if state == DGG.NORMAL else (0.5, 0.5, 0.5, 1)
        button['state'] = state

    def __repair(self):
        self.destroy()
        self.gui = RepairGUI(self.repairCallback, lambda : self.saleCallback(False))
        self.gui.load()
        self.gui.enter()

    def __buyBait(self):
        self.destroy()
        self.gui = BaitGUI(self.buyBaitCallback, lambda : self.saleCallback(False))
        self.gui.load()
        self.gui.enter()

    def __dialogAnswer(self, upgradeType, answer):
        if answer < 0:
            self.__cancel()
        else:
            self.upgradeCallback(upgradeType)
            self.destroy()

    def __buyRod(self):
        next = base.localAvatar.getMaxFishingRod() + 1
        self.__buy(next, FishGlobals.Rod2RequiredFish, TTLocalizer.FishermanRod, FishGlobals.RodPriceDict, '%s %s' % (TTLocalizer.FishingRodNameDict[next], TTLocalizer.FishermanRod), NPCToons.SELL_MOVIE_NEWROD)

    def __upgradeTank(self):
        priceDict = sorted(FishGlobals.TankPriceDict.keys())
        next = priceDict[priceDict.index(base.localAvatar.getMaxFishTank()) + 1]
        self.__buy(next, FishGlobals.Tank2RequiredFish, TTLocalizer.TankTypeName, FishGlobals.TankPriceDict, TTLocalizer.FishTank % next, NPCToons.SELL_MOVIE_NEWTANK)

    def __buyLure(self):
        next = base.localAvatar.getMaxFishingLure() + 1
        self.__buy(next, FishGlobals.Lure2RequiredFish, TTLocalizer.LureTypeName, FishGlobals.LurePriceDict, '%s %s' % (TTLocalizer.FishingLureColors[next], TTLocalizer.FishermanLure), NPCToons.SELL_MOVIE_NEWLURE)

    def __buy(self, next, requiredFishDict, name, priceDict, fullName, upgradeType):
        self.destroy()
        currentFish = len(base.localAvatar.fishCollection)
        requiredFish = requiredFishDict[next]
        if currentFish < requiredFish:
            self.gui = TTDialog.TTDialog(style=TTDialog.Acknowledge, fadeScreen=True, text_wordwrap=15, text=TTLocalizer.FishermanUnlockMessage % (name.lower(), requiredFish, requiredFish - currentFish), command=self.__cancel)
            return
        price = priceDict[next]
        bankMoney = base.localAvatar.getBankMoney()
        if bankMoney < price:
            self.gui = TTDialog.TTDialog(style=TTDialog.Acknowledge, fadeScreen=True, text_wordwrap=15, text=TTLocalizer.FishermanNotEnough % (price, bankMoney), command=self.__cancel)
            return
        self.gui = TTDialog.TTDialog(style=TTDialog.TwoChoice, fadeScreen=True, text_wordwrap=15, text=TTLocalizer.FishermanBuyQuestion % (fullName, price, bankMoney), command=lambda answer: self.__dialogAnswer(upgradeType, answer))

    def __sell(self):
        self.destroy()
        self.gui = FishSellGUI(self.saleCallback)

    def __cancel(self, _ = None):
        self.saleCallback(False)
        self.destroy()