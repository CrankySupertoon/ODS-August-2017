# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.fishing.FishCollection
import FishBase
import FishGlobals

class FishCollection:

    def __init__(self):
        self.fishList = []

    def __len__(self):
        return len(self.fishList)

    def getFish(self):
        return self.fishList

    def makeFromNetLists(self, genusList, speciesList, weightList):
        self.fishList = []
        for genus, species, weight in zip(genusList, speciesList, weightList):
            self.fishList.append(FishBase.FishBase(genus, species, weight))

    def getNetLists(self):
        genusList = []
        speciesList = []
        weightList = []
        for fish in self.fishList:
            genusList.append(fish.getGenus())
            speciesList.append(fish.getSpecies())
            weightList.append(fish.getWeight())

        return [genusList, speciesList, weightList]

    def hasFish(self, genus, species):
        for fish in self.fishList:
            if fish.getGenus() == genus and fish.getSpecies() == species:
                return 1

        return 0

    def hasGenus(self, genus):
        for fish in self.fishList:
            if fish.getGenus() == genus:
                return 1

        return 0

    def __collect(self, newFish, updateWeight = 1, updateNew = 1):
        for fish in self.fishList:
            if fish.getGenus() == newFish.getGenus() and fish.getSpecies() == newFish.getSpecies():
                if fish.getWeight() < newFish.getWeight():
                    if updateWeight:
                        fish.setWeight(newFish.getWeight())
                    return FishGlobals.COLLECT_NEW_RECORD
                else:
                    return FishGlobals.COLLECT_NO_UPDATE

        if updateNew:
            self.fishList.append(newFish)
        return FishGlobals.COLLECT_NEW_ENTRY

    def collectNewEntry(self, newFish):
        for fish in self.fishList:
            if fish.getGenus() == newFish.getGenus() and fish.getSpecies() == newFish.getSpecies():
                return

        self.fishList.append(newFish)

    def collectFish(self, newFish):
        return self.__collect(newFish, updateWeight=1, updateNew=0)

    def getCollectResult(self, newFish):
        return self.__collect(newFish, updateWeight=0, updateNew=0)

    def __str__(self):
        numFish = len(self.fishList)
        txt = 'Fish Collection (%s fish):' % numFish
        for fish in self.fishList:
            txt += '\n' + str(fish)

        return txt