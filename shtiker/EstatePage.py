# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.shtiker.EstatePage
from direct.gui.DirectGui import *
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui.NamedToonFrame import NamedToonFrame
from ShtikerPage import ShtikerPage

class EstateScrolledList(DirectScrolledList):

    def __init__(self, *args, **kwargs):
        DirectScrolledList.__init__(self, *args, **kwargs)
        self.initialiseoptions(EstateScrolledList)

    def setItems(self, items):
        index = self.getSelectedIndex()
        self.removeAndDestroyAllItems(False)
        for item in items:
            self.addItem(item, False)

        self.scrollTo(index)

    def scrollTo(self, *args, **kwargs):
        DirectScrolledList.scrollTo(self, *args, **kwargs)
        for item in self['items']:
            item.setX(0.045)
            item.setZ(item.getZ() - 0.03)


class EstatePage(ShtikerPage):

    def load(self):
        self.title = DirectLabel(self, relief=None, text=TTLocalizer.EstatePageTitle, text_scale=0.12, pos=(0, 0, 0.62))
        self.instructions = DirectLabel(self, relief=None, text=TTLocalizer.EstatePageInstructions, text_scale=0.055, text_wordwrap=11, pos=(0.4, 0, 0.325), text_font=ToontownGlobals.getNametagFont(3))
        self.list = EstateScrolledList(self, relief=None, pos=(-0.5, 0, 0.03), incButton_image=Preloaded['scrollBlueArrow'], incButton_relief=None, incButton_scale=(1.3, 1.3, -1.3), incButton_pos=(0.045, 0, -0.6), incButton_image3_color=(1, 1, 1, 0.2), decButton_image=Preloaded['scrollBlueArrow'], decButton_relief=None, decButton_scale=1.3, decButton_pos=(0.045, 0, 0.5), decButton_image3_color=(1, 1, 1, 0.2), itemFrame_pos=(-0.247, 0, 0.365), itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(-0.05, 0.65, -0.9, 0.08), itemFrame_frameColor=(0.85, 0.95, 1, 1), itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=5, forceHeight=0.19, items=[])
        return

    def getEstateManager(self):
        return base.cr.doFind('EstateManager')

    def enter(self):
        self.getEstateManager().b_requestEstates(True)
        self.accept('namedEstatesUpdated', self.__namedEstatesUpdated)
        self.__namedEstatesUpdated()
        self.show()

    def exit(self):
        self.ignoreAll()
        self.list.removeAndDestroyAllItems()
        self.getEstateManager().b_requestEstates(False)
        self.hide()

    def unload(self):
        self.title.destroy()
        del self.title
        self.instructions.destroy()
        del self.instructions
        self.list.destroy()
        del self.list
        ShtikerPage.unload(self)

    def __namedEstatesUpdated(self):
        if self.isHidden():
            return
        estates = self.getEstateManager().getNamedEstates()
        items = []
        for estate in estates:
            name, dna, avId, zoneId = estate
            items.append(NamedToonFrame(ToonDNA(dna), name, self.__clickedEstate, [avId, zoneId, name]))

        self.list.setItems(items)

    def __clickedEstate(self, avId, zoneId, name):
        base.localAvatar.book.exit()
        base.localAvatar.b_setAnimState('CloseBook', 1, callback=self.__handleBookClose, extraArgs=[avId, zoneId, name])

    def __handleBookClose(self, avId, zoneId, name):
        requestStatus = {'hoodId': ToontownGlobals.MyEstate,
         'zoneId': zoneId,
         'skipEstateMgr': True,
         'shardId': None,
         'ownerId': avId,
         'ownerName': name,
         'avId': -1}
        if avId != base.localAvatar.doId:
            requestStatus['ownerName'] = name
        base.cr.playGame.place.fsm.request('teleportOut', [requestStatus])
        return