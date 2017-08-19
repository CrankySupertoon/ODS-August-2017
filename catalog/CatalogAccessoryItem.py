# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.catalog.CatalogAccessoryItem
from panda3d.core import Datagram, Filename, Light, Texture, VBase4, Vec4
import CatalogItem
from CatalogAccessoryItemGlobals import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toon import ToonDNA
import random, types
from direct.showbase import PythonUtil
from direct.gui.DirectGui import *

class CatalogAccessoryItem(CatalogItem.CatalogItem):

    def makeNewItem(self, accessoryType, isSpecial = False):
        self.accessoryType = accessoryType
        self.isSpecial = isSpecial
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        return 1

    def reachedPurchaseLimit(self, avatar):
        if self in avatar.onOrder or self in avatar.onGiftOrder or self in avatar.mailboxContents:
            return True
        str = AccessoryTypes[self.accessoryType][ATString]
        if self.isHat():
            hat = ToonDNA.HatStyles[str]
            if avatar.getStyle().getHat() == hat or hat in avatar.hatList:
                return True
        elif self.areGlasses():
            glasses = ToonDNA.GlassesStyles[str]
            if avatar.getStyle().getGlasses() == glasses or glasses in avatar.glassesList:
                return True
        elif self.isBackpack():
            backpack = ToonDNA.BackpackStyles[str]
            if avatar.getStyle().getBackpack() == backpack or backpack in avatar.backpackList:
                return True
        else:
            shoes = ToonDNA.ShoesStyles[str]
            if avatar.getStyle().getShoes() == shoes or shoes in avatar.shoesList:
                return True
        return False

    def getTypeName(self):
        return TTLocalizer.AccessoryTypeName

    def getName(self):
        typeName = TTLocalizer.AccessoryTypeNames.get(self.accessoryType, 0)
        if typeName:
            return typeName
        else:
            article = AccessoryTypes[self.accessoryType][ATArticle]
            return TTLocalizer.AccessoryArticleNames[article]

    def getType(self):
        if self.isHat():
            return ToonDNA.HAT
        elif self.areGlasses():
            return ToonDNA.GLASSES
        elif self.isBackpack():
            return ToonDNA.BACKPACK
        else:
            return ToonDNA.SHOES

    def recordPurchase(self, avatar, optional):
        if avatar.isTrunkFull():
            return ToontownGlobals.P_NoRoomForItem
        str = AccessoryTypes[self.accessoryType][ATString]
        dna = avatar.getStyle().clone()
        if self.isHat():
            oldAccessory = avatar.getStyle().getHat()
            dna.hat = ToonDNA.HatStyles[str]
        elif self.areGlasses():
            oldAccessory = avatar.getStyle().getGlasses()
            dna.glasses = ToonDNA.GlassesStyles[str]
        elif self.isBackpack():
            oldAccessory = avatar.getStyle().getBackpack()
            dna.backpack = ToonDNA.BackpackStyles[str]
        else:
            oldAccessory = avatar.getStyle().getShoes()
            dna.shoes = ToonDNA.ShoesStyles[str]
        if not avatar.b_setDNAString(dna.makeNetString()):
            return ToontownGlobals.P_ItemUnneeded
        avatar.addToAccessoriesList(self.getType(), oldAccessory)
        return ToontownGlobals.P_ItemAvailable

    def getDeliveryTime(self):
        return 60

    def getPicture(self, avatar):
        model = self.loadModel()
        spin = 1
        model.setBin('unsorted', 0, 1)
        self.hasPicture = True
        return self.makeFrameModel(model, spin)

    def applyColor(self, model, color):
        if model == None or color == None:
            return
        else:
            if isinstance(color, types.StringType):
                tex = loader.loadTexture(color)
                tex.setMinfilter(Texture.FTLinearMipmapLinear)
                tex.setMagfilter(Texture.FTLinear)
                model.setTexture(tex, 1)
            else:
                needsAlpha = color[3] != 1
                color = VBase4(color[0], color[1], color[2], color[3])
                model.setColorScale(color, 1)
                if needsAlpha:
                    model.setTransparency(1)
            return

    def loadModel(self):
        modelPath = self.getFilename()
        if self.areShoes():
            str = AccessoryTypes[self.accessoryType][ATString]
            defn = ToonDNA.ShoesStyles[str]
            legModel = loader.loadModel('phase_3.5/models/char/tt_a_chr_dgm_shorts_legs_1000')
            model = legModel.find('**/' + modelPath)
        else:
            model = loader.loadModel(modelPath)
        texture = self.getTexture()
        if texture:
            self.applyColor(model, texture)
        colorVec4 = self.getColor()
        if colorVec4:
            modelColor = (colorVec4.getX(), colorVec4.getY(), colorVec4.getZ())
            self.applyColor(model, modelColor)
        model.flattenLight()
        return model

    def requestPurchase(self, phone, callback):
        from toontown.toontowngui import TTDialog
        avatar = base.localAvatar
        accessoriesOnOrder = 0
        for item in avatar.onOrder + avatar.mailboxContents + avatar.onGiftOrder:
            if hasattr(item, 'isHat'):
                accessoriesOnOrder += 1

        if avatar.isTrunkFull(accessoriesOnOrder):
            self.requestPurchaseCleanup()
            buttonCallback = PythonUtil.Functor(self.__handleFullPurchaseDialog, phone, callback)
            text = TTLocalizer.CatalogPurchaseTrunkFull
            self.dialog = TTDialog.TTDialog(style=TTDialog.YesNo, text=text, text_wordwrap=15, command=buttonCallback)
            self.dialog.show()
        else:
            CatalogItem.CatalogItem.requestPurchase(self, phone, callback)

    def requestPurchaseCleanup(self):
        if hasattr(self, 'dialog'):
            self.dialog.cleanup()
            del self.dialog

    def __handleFullPurchaseDialog(self, phone, callback, buttonValue):
        from toontown.toontowngui import TTDialog
        self.requestPurchaseCleanup()
        if buttonValue == DGG.DIALOG_OK:
            CatalogItem.CatalogItem.requestPurchase(self, phone, callback)
        else:
            callback(ToontownGlobals.P_UserCancelled, self)

    def getAcceptItemErrorText(self, retcode):
        if retcode == ToontownGlobals.P_ItemAvailable:
            if self.isHat():
                return TTLocalizer.CatalogAcceptHat
            elif self.areGlasses():
                return TTLocalizer.CatalogAcceptGlasses
            elif self.isBackpack():
                return TTLocalizer.CatalogAcceptBackpack
            else:
                return TTLocalizer.CatalogAcceptShoes
        elif retcode == ToontownGlobals.P_NoRoomForItem:
            return TTLocalizer.CatalogAcceptTrunkFull
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def isHat(self):
        return AccessoryTypes[self.accessoryType][ATArticle] == AHat

    def areGlasses(self):
        return AccessoryTypes[self.accessoryType][ATArticle] == AGlasses

    def isBackpack(self):
        return AccessoryTypes[self.accessoryType][ATArticle] == ABackpack

    def areShoes(self):
        return AccessoryTypes[self.accessoryType][ATArticle] == AShoes

    def output(self, store = -1):
        return 'CatalogAccessoryItem(%s%s)' % (self.accessoryType, self.formatOptionalData(store))

    def getFilename(self):
        str = AccessoryTypes[self.accessoryType][ATString]
        if self.isHat():
            defn = ToonDNA.HatStyles[str]
            modelPath = ToonDNA.HatModels[defn[0]]
        elif self.areGlasses():
            defn = ToonDNA.GlassesStyles[str]
            modelPath = ToonDNA.GlassesModels[defn[0]]
        elif self.isBackpack():
            defn = ToonDNA.BackpackStyles[str]
            modelPath = ToonDNA.BackpackModels[defn[0]]
        else:
            defn = ToonDNA.ShoesStyles[str]
            modelPath = ToonDNA.ShoesModels[defn[0]]
        return modelPath

    def getTexture(self):
        str = AccessoryTypes[self.accessoryType][ATString]
        if self.isHat():
            defn = ToonDNA.HatStyles[str]
            modelPath = ToonDNA.HatTextures[defn[1]]
        elif self.areGlasses():
            defn = ToonDNA.GlassesStyles[str]
            modelPath = ToonDNA.GlassesTextures[defn[1]]
        elif self.isBackpack():
            defn = ToonDNA.BackpackStyles[str]
            modelPath = ToonDNA.BackpackTextures[defn[1]]
        else:
            defn = ToonDNA.ShoesStyles[str]
            modelPath = ToonDNA.ShoesTextures[defn[1]]
        return modelPath

    def getColor(self):
        return None

    def compareTo(self, other):
        return self.accessoryType - other.accessoryType

    def getHashContents(self):
        return self.accessoryType

    def getBasePrice(self):
        return AccessoryTypes[self.accessoryType][ATBasePrice]

    def getEmblemPrices(self):
        result = ()
        info = AccessoryTypes[self.accessoryType]
        if ATEmblemPrices <= len(info) - 1:
            result = info[ATEmblemPrices]
        return result

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.accessoryType = di.getUint16()
        self.isSpecial = di.getBool()

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.accessoryType)
        dg.addBool(self.isSpecial)

    def isGift(self):
        return not self.getEmblemPrices()


def getAllAccessories(*accessoryTypes):
    list = []
    for accessoryType in accessoryTypes:
        base = CatalogAccessoryItem(accessoryType)
        list.append(base)

    return list