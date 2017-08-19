# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.building.RandomBuilding
from panda3d.core import Texture
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase
from toontown.dna.DNAParser import setupDoor
from ZoneBuilding import ZoneBuilding

def randomDNAItem(randomGen, category, findFunc):
    codeCount = assetStorage.getNumCatalogCodes(category)
    if codeCount < 1:
        return
    index = randomGen.randint(0, codeCount - 1)
    return findFunc(assetStorage.getCatalogCode(category, index))


class RandomBuilding(ZoneBuilding):

    def setup(self):
        pass

    def randomDNAItem(self, randomGen, category, findFunc):
        return randomDNAItem(randomGen, category, findFunc)

    def replaceRandomInModel(self, randomGen, colors, model):
        paths = model.findAllMatches('**/random_???_*')
        for i in xrange(paths.getNumPaths()):
            path = paths.getPath(i)
            name = path.getName()
            length = len('random_')
            category = name[length + 4:]
            key1 = name[length]
            key2 = name[length + 1]
            if category[-1].isdigit():
                category = category[:-1]
            if key1 == 'm':
                model = self.randomDNAItem(randomGen, category, assetStorage.findNode)
                if model:
                    path = model.copyTo(path)
                    if key2 == 'r':
                        self.replaceRandomInModel(randomGen, colors, path)
            elif key1 == 't':
                texture = self.randomDNAItem(randomGen, category, assetStorage.findTexture)
                if texture:
                    path.setTexture(texture, 100)
            if key2 == 'c':
                if 'TI_wallpaper' in category:
                    randomGen.seed(self.zoneId)
                path.setColorScale(randomGen.choice(colors[category]))

    def setupDoor(self, randomGen, colors, interior, doorYOffset = -0.025):
        doorColor = randomGen.choice(colors['TI_door'])
        door = assetStorage.findNode('door_double_round_ur')
        doorOrigins = render.findAllMatches('**/door_origin*')
        for doorOrigin in doorOrigins:
            doorNP = door.copyTo(doorOrigin)
            doorOrigin.setScale(0.8, 0.8, 0.8)
            doorOrigin.setPos(doorOrigin, 0, doorYOffset, 0)
            setupDoor(doorNP, interior, doorOrigin, base.cr.playGame.dnaStore, str(self.block), doorColor)
            doorFrame = doorNP.find('door_*_flat')
            doorFrame.wrtReparentTo(self.interior)
            doorFrame.setColor(doorColor)

    def resetNPCs(self):
        for npc in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npc.initToonState()