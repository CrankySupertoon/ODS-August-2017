# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.catalog.CatalogBasketItem
from panda3d.core import Datagram
import CatalogItem
from toontown.estate import GardenGlobals
from toontown.toonbase import ToontownGlobals
from direct.actor import Actor
from toontown.toonbase import TTLocalizer
from direct.interval.IntervalGlobal import *

class CatalogBasketItem(CatalogItem.CatalogItem):
    sequenceNumber = 0

    def makeNewItem(self, maxBasket):
        self.maxBasket = maxBasket
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        return 1

    def reachedPurchaseLimit(self, avatar):
        return avatar.getMaxFlowerBasket() >= self.maxBasket or self in avatar.onOrder or self in avatar.mailboxContents

    def saveHistory(self):
        return 1

    def getTypeName(self):
        return TTLocalizer.BasketTypeName

    def getName(self):
        return TTLocalizer.FlowerBasket % TTLocalizer.FlowerBasketNameDict[self.maxBasket]

    def recordPurchase(self, avatar, optional):
        if self.maxBasket <= avatar.getMaxFlowerBasket():
            return ToontownGlobals.P_ItemUnneeded
        avatar.b_setMaxFlowerBasket(self.maxBasket)
        return ToontownGlobals.P_ItemAvailable

    def isGift(self):
        return 0

    def getDeliveryTime(self):
        return 1

    def getPicture(self, avatar):
        basket = loader.loadModel('phase_5.5/models/estate/flowerBasket')
        basket.setScale(2.3)
        basket.setPos(0, 0, 0.12)
        frame = self.makeFrame()
        basket.reparentTo(frame)
        return (frame, None)

    def getAcceptItemErrorText(self, retcode):
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptBasket
        if retcode == ToontownGlobals.P_ItemUnneeded:
            return TTLocalizer.CatalogAcceptBasketUnneeded
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def output(self, store = -1):
        return 'CatalogBasketItem(%s%s)' % (self.maxBasket, self.formatOptionalData(store))

    def compareTo(self, other):
        return self.maxBasket - other.maxBasket

    def getHashContents(self):
        return self.maxBasket

    def getBasePrice(self):
        return GardenGlobals.BasketPriceDict[self.maxBasket]

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.maxBasket = di.getUint8()

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.maxBasket)


def nextAvailableBasket(avatar, duplicateItems):
    basket = avatar.getMaxFlowerBasket()
    if basket in GardenGlobals.NextBasket:
        return CatalogBasketItem(GardenGlobals.NextBasket[basket])


def getAllBaskets():
    return [ CatalogBasketItem(basket) for basket in GardenGlobals.NextBasket.values() ]