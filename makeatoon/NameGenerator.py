# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.makeatoon.NameGenerator
from panda3d.core import DSearchPath, Filename, StreamReader
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
import random

class NameGenerator:
    notify = DirectNotifyGlobal.directNotify.newCategory('NameGenerator')
    boyTitles = []
    girlTitles = []
    neutralTitles = []
    boyFirsts = []
    girlFirsts = []
    neutralFirsts = []
    capPrefixes = []
    lastPrefixes = []
    lastSuffixes = []

    def __init__(self):
        self.generateLists()

    def generateLists(self):
        self.boyTitles = []
        self.girlTitles = []
        self.neutralTitles = []
        self.boyFirsts = []
        self.girlFirsts = []
        self.neutralFirsts = []
        self.capPrefixes = []
        self.lastPrefixes = []
        self.lastSuffixes = []
        self.nameDictionary = {}
        searchPath = DSearchPath()
        searchPath.appendDirectory(Filename('resources/phase_3/etc'))
        searchPath.appendDirectory(Filename('/phase_3/etc'))
        filename = Filename(TTLocalizer.NameShopNameMaster)
        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            self.notify.error("NameGenerator: Error opening name list text file '%s.'" % TTLocalizer.NameShopNameMaster)
        input = StreamReader(vfs.openReadFile(filename, 1), 1)
        currentLine = input.readline().strip()
        while currentLine:
            if currentLine.lstrip()[0:1] != '#':
                a1 = currentLine.find('*')
                a2 = currentLine.find('*', a1 + 1)
                self.nameDictionary[int(currentLine[0:a1])] = (int(currentLine[a1 + 1:a2]), currentLine[a2 + 1:len(currentLine)])
            currentLine = input.readline().strip()

        masterList = [self.boyTitles,
         self.girlTitles,
         self.neutralTitles,
         self.boyFirsts,
         self.girlFirsts,
         self.neutralFirsts,
         self.capPrefixes,
         self.lastPrefixes,
         self.lastSuffixes]
        for tu in self.nameDictionary.values():
            masterList[tu[0]].append(tu[1])

        return 1

    def _getNameParts(self, cat2part):
        nameParts = [{},
         {},
         {},
         {}]
        for id, tpl in self.nameDictionary.iteritems():
            cat, str = tpl
            if cat in cat2part:
                nameParts[cat2part[cat]][str] = id

        return nameParts

    def getMaleNameParts(self):
        return self._getNameParts({0: 0,
         2: 0,
         3: 1,
         5: 1,
         6: 2,
         7: 2,
         8: 3})

    def getFemaleNameParts(self):
        return self._getNameParts({1: 0,
         2: 0,
         4: 1,
         5: 1,
         6: 2,
         7: 2,
         8: 3})

    def returnUniqueID(self, name, listnumber):
        newtu = [(), (), ()]
        if listnumber == 0:
            newtu[0] = (0, name)
            newtu[1] = (1, name)
            newtu[2] = (2, name)
        elif listnumber == 1:
            newtu[0] = (3, name)
            newtu[1] = (4, name)
            newtu[2] = (5, name)
        elif listnumber == 2:
            newtu[0] = (6, name)
            newtu[1] = (7, name)
        else:
            newtu[0] = (8, name)
        for tu in self.nameDictionary.items():
            for g in newtu:
                if tu[1] == g:
                    return tu[0]

        return -1

    def randomNameMoreinfo(self, boy = 0, girl = 0, randomGen = None):
        if boy and girl:
            self.error("A name can't be both boy and girl!")
        if not randomGen:
            randomGen = random
        if not boy and not girl:
            boy = randomGen.choice([0, 1])
            girl = not boy
        uberFlag = randomGen.choice(['title-first',
         'title-last',
         'first',
         'last',
         'first-last',
         'title-first-last'])
        titleFlag = 0
        if uberFlag == 'title-first' or uberFlag == 'title-last' or uberFlag == 'title-first-last':
            titleFlag = 1
        firstFlag = 0
        if uberFlag == 'title-first' or uberFlag == 'first' or uberFlag == 'first-last' or uberFlag == 'title-first-last':
            firstFlag = 1
        lastFlag = 0
        if uberFlag == 'title-last' or uberFlag == 'last' or uberFlag == 'first-last' or uberFlag == 'title-first-last':
            lastFlag = 1
        retString = ''
        uberReturn = [0,
         0,
         0,
         '',
         '',
         '',
         '']
        uberReturn[0] = titleFlag
        uberReturn[1] = firstFlag
        uberReturn[2] = lastFlag
        titleList = self.neutralTitles[:]
        if boy:
            titleList += self.boyTitles
        elif girl:
            titleList += self.girlTitles
        else:
            self.error('Must be boy or girl.')
        uberReturn[3] = randomGen.choice(titleList)
        firstList = self.neutralFirsts[:]
        if boy:
            firstList += self.boyFirsts
        elif girl:
            firstList += self.girlFirsts
        else:
            self.error('Must be boy or girl.')
        uberReturn[4] = randomGen.choice(firstList)
        lastPrefix = randomGen.choice(self.lastPrefixes)
        lastSuffix = randomGen.choice(self.lastSuffixes)
        if lastPrefix in self.capPrefixes:
            lastSuffix = lastSuffix.capitalize()
        uberReturn[5] = lastPrefix
        uberReturn[6] = lastSuffix
        if titleFlag:
            retString += uberReturn[3] + ' '
        if firstFlag:
            retString += uberReturn[4]
            if lastFlag:
                retString += ' '
        if lastFlag:
            retString += uberReturn[5] + uberReturn[6]
        uberReturn.append(retString)
        return uberReturn