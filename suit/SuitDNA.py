# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.suit.SuitDNA
from panda3d.core import Datagram, DatagramIterator, VBase4
import random
from direct.directnotify.DirectNotifyGlobal import *
from toontown.toonbase import TTLocalizer, ToontownGlobals
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
notify = directNotify.newCategory('SuitDNA')
suitHeadTypes = ['f',
 'p',
 'ym',
 'mm',
 'ds',
 'hh',
 'cr',
 'tbc',
 'bf',
 'b',
 'dt',
 'ac',
 'bs',
 'sd',
 'le',
 'bw',
 'sc',
 'pp',
 'tw',
 'bc',
 'nc',
 'mb',
 'ls',
 'rb',
 'cc',
 'tm',
 'nd',
 'gh',
 'ms',
 'tf',
 'm',
 'mh',
 'sk',
 'cm',
 'vp',
 'db',
 'kc',
 'ss',
 'iw',
 'ru']
suitATypes = ['ym',
 'hh',
 'tbc',
 'dt',
 'bs',
 'le',
 'bw',
 'pp',
 'nc',
 'rb',
 'nd',
 'tf',
 'm',
 'mh',
 'vp',
 'ss',
 'ru']
suitBTypes = ['p',
 'ds',
 'b',
 'ac',
 'sd',
 'bc',
 'ls',
 'tm',
 'ms',
 'kc',
 'iw']
suitCTypes = ['f',
 'mm',
 'cr',
 'bf',
 'sc',
 'tw',
 'mb',
 'cc',
 'gh',
 'sk',
 'cm',
 'db']
suitDepts = ['c',
 'l',
 'm',
 's',
 't']
suitDeptZones = [ToontownGlobals.BossbotHQ,
 ToontownGlobals.LawbotHQ,
 ToontownGlobals.CashbotHQ,
 ToontownGlobals.SellbotHQ,
 ToontownGlobals.TechbotHQ]
suitDeptFullnames = {'c': TTLocalizer.Bossbot,
 'l': TTLocalizer.Lawbot,
 'm': TTLocalizer.Cashbot,
 's': TTLocalizer.Sellbot,
 't': TTLocalizer.Techbot}
suitDeptFullnamesP = {'c': TTLocalizer.BossbotP,
 'l': TTLocalizer.LawbotP,
 'm': TTLocalizer.CashbotP,
 's': TTLocalizer.SellbotP,
 't': TTLocalizer.TechbotP}
suitDeptFilenames = {'c': 'boss',
 'l': 'law',
 'm': 'cash',
 's': 'sell',
 't': 'tech'}
suitDeptModelPaths = {'c': '**/CorpIcon',
 0: '**/CorpIcon',
 'l': '**/LegalIcon',
 1: '**/LegalIcon',
 'm': '**/MoneyIcon',
 2: '**/MoneyIcon',
 's': '**/SalesIcon',
 3: '**/SalesIcon',
 't': '**/TechIcon',
 4: '**/TechIcon'}
corpPolyColor = VBase4(0.95, 0.75, 0.75, 1.0)
legalPolyColor = VBase4(0.75, 0.75, 0.95, 1.0)
moneyPolyColor = VBase4(0.65, 0.95, 0.85, 1.0)
salesPolyColor = VBase4(0.95, 0.75, 0.95, 1.0)
techPolyColor = VBase4(0.6, 0.48, 0.7, 1.0)
suitDeptColors = {'c': corpPolyColor,
 'l': legalPolyColor,
 'm': moneyPolyColor,
 's': salesPolyColor,
 't': techPolyColor}
suitsPerLevel = [1,
 1,
 1,
 1,
 1,
 1,
 1,
 1]
suitsPerDept = 8
goonTypes = ['pg', 'sg', 'fg1']

def getSuitBodyType(name):
    if name in suitATypes:
        return 'a'
    if name in suitBTypes:
        return 'b'
    if name in suitCTypes:
        return 'c'
    print 'Unknown body type for suit name: ', name


def getSuitDept(name):
    index = suitHeadTypes.index(name)
    for dept in xrange(len(suitDepts)):
        if index < suitsPerDept * (dept + 1):
            return suitDepts[dept]

    print 'Unknown dept for suit name: ', name


def getDeptFullname(dept):
    return suitDeptFullnames[dept]


def getDeptFullnameP(dept):
    return suitDeptFullnamesP[dept]


def getSuitDeptFullname(name):
    return suitDeptFullnames[getSuitDept(name)]


def getSuitType(name):
    index = suitHeadTypes.index(name)
    return index % suitsPerDept + 1


def getSuitName(deptIndex, typeIndex):
    return suitHeadTypes[suitsPerDept * deptIndex + typeIndex]


def getRandomSuitType(level, rng = random):
    return random.randint(max(level - 4, 1), min(level, 8))


def getRandomIndexByDept(dept):
    return suitsPerDept * suitDepts.index(dept) + random.randint(0, suitsPerDept - 1)


def getRandomSuitByDept(dept):
    return suitHeadTypes[getRandomIndexByDept(dept)]


def getSuitsInDept(dept):
    start = dept * suitsPerDept
    end = start + suitsPerDept
    return suitHeadTypes[start:end]


def getLevelByIndex(index):
    return index % suitsPerDept + 1


class SuitDNA:

    def __init__(self, str = None, type = None, dna = None, r = None, b = None, g = None):
        if str != None:
            self.makeFromNetString(str)
        elif type != None:
            if type == 's':
                self.newSuit()
        else:
            self.type = 'u'
        return

    def __str__(self):
        if self.type == 's':
            return 'type = %s\nbody = %s, dept = %s, name = %s' % ('suit',
             self.body,
             self.dept,
             self.name)
        elif self.type == 'b':
            return 'type = boss cog\ndept = %s' % self.dept
        else:
            return 'type undefined'

    def makeNetString(self):
        dg = PyDatagram()
        dg.addFixedString(self.type, 1)
        if self.type == 's':
            dg.addFixedString(self.name, 3)
            dg.addFixedString(self.dept, 1)
        elif self.type == 'b':
            dg.addFixedString(self.dept, 1)
        elif self.type == 'u':
            notify.error('undefined avatar')
        else:
            notify.error('unknown avatar type: ', self.type)
        return dg.getMessage()

    def makeFromNetString(self, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if self.type == 's':
            self.name = dgi.getFixedString(3)
            self.dept = dgi.getFixedString(1)
            self.body = getSuitBodyType(self.name)
        elif self.type == 'b':
            self.dept = dgi.getFixedString(1)
        else:
            notify.error('unknown avatar type: ', self.type)
        return None

    def __defaultGoon(self):
        self.type = 'g'
        self.name = goonTypes[0]

    def __defaultSuit(self):
        self.type = 's'
        self.name = 'ds'
        self.dept = getSuitDept(self.name)
        self.body = getSuitBodyType(self.name)

    def newSuit(self, name = None):
        if name == None:
            self.__defaultSuit()
        else:
            self.type = 's'
            self.name = name
            self.dept = getSuitDept(self.name)
            self.body = getSuitBodyType(self.name)
        return

    def newBossCog(self, dept):
        self.type = 'b'
        self.dept = dept

    def newSuitRandom(self, level = None, dept = None):
        self.type = 's'
        if level == None:
            level = random.choice(range(1, len(suitsPerLevel)))
        elif level < 0 or level > len(suitsPerLevel):
            notify.error('Invalid suit level: %d' % level)
        if dept == None:
            dept = random.choice(suitDepts)
        self.dept = dept
        index = suitDepts.index(dept)
        base = index * suitsPerDept
        offset = 0
        if level > 1:
            for i in xrange(1, level):
                offset = offset + suitsPerLevel[i - 1]

        bottom = base + offset
        top = bottom + suitsPerLevel[level - 1]
        self.name = suitHeadTypes[random.choice(range(bottom, top))]
        self.body = getSuitBodyType(self.name)
        return

    def newGoon(self, name = None):
        if type == None:
            self.__defaultGoon()
        else:
            self.type = 'g'
            if name in goonTypes:
                self.name = name
            else:
                notify.error('unknown goon type: ', name)
        return

    def getType(self):
        if self.type == 's':
            type = 'suit'
        elif self.type == 'b':
            type = 'boss'
        else:
            notify.error('Invalid DNA type: ', self.type)
        return type