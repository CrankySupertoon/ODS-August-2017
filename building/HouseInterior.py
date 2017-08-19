# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.HouseInterior
from panda3d.core import Light, Texture
from toontown.toonbase.ToontownGlobals import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem
from toontown.catalog import CatalogSurfaceItem
from toontown.dna.DNAParser import *
from toontown.estate import HouseGlobals
WindowPlugNames = [ '**/windowcut_%s*' % x for x in ('b', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i') ]
RoomNames = [ '**/group%s' % x for x in (4, 3, 2, 1) ]
WallNames = ('ceiling*', 'wall_side_middle*', 'wall_front_middle*', 'windowcut_*')
MouldingNames = ('wall_side_top*', 'wall_front_top*')
FloorNames = ('floor*',)
WainscotingNames = ('wall_side_bottom*', 'wall_front_bottom*')
BorderNames = ('wall_side_middle*_border', 'wall_front_middle*_border', 'windowcut_*_border')
WallpaperPieceNames = (WallNames,
 MouldingNames,
 FloorNames,
 WainscotingNames,
 BorderNames)
ModelId2Name = {0: 'phase_5.5/models/estate/tt_m_ara_int_estateHouseB'}

class HouseInterior:

    def __init__(self):
        self.interior = None
        self.model = 0
        return

    def disable(self):
        self.interior.removeNode()
        del self.interior

    def getBlock(self):
        return 0

    def setup(self):
        if self.interior:
            return None
        else:
            self.interior = loader.loadModel(ModelId2Name[self.model])
            self.interior.reparentTo(render)
            door = assetStorage.findNode('door_double_round_ur')
            door_origin = self.interior.find('**/door_origin')
            door_origin.setPos(door_origin, 0, -0.025, 0)
            door_origin.setHpr(180, 0, 0)
            door_origin.setScale(0.8)
            doorNP = door.copyTo(door_origin)
            setupDoor(doorNP, door_origin, door_origin, base.cr.playGame.dnaStore, str(self.getBlock()), HouseGlobals.atticWood)
            doorFrame = doorNP.find('door_*_flat')
            doorFrame.setColor(HouseGlobals.atticWood)
            self.interior.flattenMedium()
            self.windowSlots = []
            for name in WindowPlugNames:
                plugNodes = self.interior.findAllMatches(name)
                if plugNodes.isEmpty():
                    self.windowSlots.append((None, None))
                    continue
                viewBase = plugNodes[0].getParent().attachNewNode('view')
                viewBase.setTransform(plugNodes[0].getTransform())
                plug = plugNodes[0].getParent().attachNewNode('plug')
                plugNodes.reparentTo(plug)
                plug.flattenLight()
                self.windowSlots.append((plug, viewBase))

            self.windowSlots[2][1].setPosHpr(-21.28, -37.15, 16.25, -90.4, 0, 0)
            self.windowSlots[4][1].setPosHpr(16.0, -12.0, 5.51, -90, 0, 0)
            self.windowSlots[6][1].setPosHpr(-12.0, 26.0, 5.51, 0, 0, 0)
            self.__colorWalls()
            self.__setupWindows()
            messenger.send('houseInteriorLoaded-%d' % self.zoneId)
            return None

    def __colorWalls(self):
        if not self.wallpaper:
            for name in WallNames + WainscotingNames:
                for node in self.interior.findAllMatches('**/%s' % name):
                    node.setTextureOff(1)

            return
        numSurfaceTypes = CatalogSurfaceItem.NUM_ST_TYPES
        numRooms = min(len(self.wallpaper) / numSurfaceTypes, len(RoomNames))
        for room in xrange(numRooms):
            roomNode = self.interior.find(RoomNames[room])
            if roomNode.isEmpty():
                continue
            for surface in xrange(numSurfaceTypes):
                slot = room * numSurfaceTypes + surface
                wallpaper = self.wallpaper[slot]
                color = wallpaper.getColor()
                texture = wallpaper.loadTexture()
                for name in WallpaperPieceNames[surface]:
                    for node in roomNode.findAllMatches('**/%s' % name):
                        if name == 'ceiling*':
                            r, g, b, a = color
                            node.setColorScale(r * 0.66, g * 0.66, b * 0.66, a)
                        else:
                            node.setColorScale(*color)
                            node.setTexture(texture, 1)

                    if wallpaper.getSurfaceType() == CatalogSurfaceItem.STWallpaper:
                        color2 = wallpaper.getBorderColor()
                        texture2 = wallpaper.loadBorderTexture()
                        for node in roomNode.findAllMatches('**/%s_border' % name):
                            node.setColorScale(*color2)
                            node.setTexture(texture2, 1)

        for node in self.interior.findAllMatches('**/arch*'):
            node.setColorScale(HouseGlobals.archWood)

    def __setupWindows(self):
        for plug, viewBase in self.windowSlots:
            if plug:
                plug.show()
            if viewBase:
                viewBase.getChildren().detach()

        if not self.windows:
            return
        for item in self.windows:
            plug, viewBase = self.windowSlots[item.placement]
            if plug:
                plug.hide()
            if viewBase:
                model = item.loadModel()
                model.reparentTo(viewBase)

    def setWallpaper(self, items):
        self.wallpaper = CatalogItemList.CatalogItemList(items, store=CatalogItem.Customization)
        if self.interior:
            self.__colorWalls()

    def setWindows(self, items):
        self.windows = CatalogItemList.CatalogItemList(items, store=CatalogItem.Customization | CatalogItem.WindowPlacement)
        if self.interior:
            self.__setupWindows()

    def setModel(self, model):
        self.model = model
        if self.interior:
            self.interior.removeNode()
            self.setup()