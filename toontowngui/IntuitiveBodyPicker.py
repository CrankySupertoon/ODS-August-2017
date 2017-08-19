# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toontowngui.IntuitiveBodyPicker
from panda3d.core import Texture
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toon import ToonDNA, Toon, ToonHead

class IntuitiveBodyPicker(DirectFrame):

    def __init__(self, parent, pos = (0, 0, 0)):
        DirectFrame.__init__(self, parent, relief=None, image=Preloaded['squareBox'], image_color=(0.16, 0.69, 1, 1), image_pos=(0.33, 0, -0.57), image_scale=(1.05, 1, 1.55), pos=pos)
        self.initialiseoptions(IntuitiveBodyPicker)
        torsoZ = -0.225 * len(ToonDNA.toonSpeciesTypes) / 4 - 0.315
        self.toonHeads = []
        self.torsos = []
        self.legs = []
        self.headButtons = []
        self.torsoButtons = []
        self.legsButtons = []
        self.animalLabel = DirectLabel(self, relief=None, text=TTLocalizer.BodyShopAnimal, text_scale=0.1, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_font=ToontownGlobals.getMinnieFont(), pos=(0.36, 0, 0.045))
        self.bodyLabel = DirectLabel(self, relief=None, text=TTLocalizer.BodyShopBody, text_scale=0.1, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_font=ToontownGlobals.getMinnieFont(), pos=(0.36, 0, torsoZ + 0.145))
        dna = ToonDNA.ToonDNA()
        dna.gender = 'm'
        dna.headColor = (1, 1, 1, 1)
        for i, species in enumerate(ToonDNA.toonSpeciesTypes):
            button = self.getNewButton(self.__swapHead, [i], (i % 4 * 0.22, 0, -0.225 * (i / 4) - 0.1))
            dna.head = species + 'ss'
            head = ToonHead.ToonHead()
            head.setupHead(dna, forGui=True)
            head.fitAndCenterHead(0.7, forGui=True)
            head.reparentTo(button)
            head.setH(135)
            self.toonHeads.append(head)
            self.headButtons.append(button)

        for i in xrange(3):
            button = self.getNewButton(self.__swapTorso, [i], (i * 0.22 + 0.125, 0, torsoZ))
            self.torsoButtons.append(button)

        for i, leg in enumerate(ToonDNA.toonLegTypes):
            button = self.getNewButton(self.__swapLegs, [i], (i * 0.22 + 0.125, 0, torsoZ - 0.225))
            leg = loader.loadModel(Toon.LegDict.get(leg) + '1000')
            leg.reparentTo(button)
            leg.find('**/shoes').removeNode()
            leg.setPos(0, 0, -0.4)
            self.legs.append(leg)
            self.legsButtons.append(button)
            for part in leg.findAllMatches('**/boots_*'):
                part.removeNode()

        for part in self.torsos + self.legs:
            self.setupPart(part)

        return

    def setupPart(self, part):
        part.setScale(0.3)
        part.setH(180)
        part.setDepthTest(True)
        part.setDepthWrite(True)

    def getNewButton(self, command, extraArgs, pos):
        return DirectButton(self, relief=None, image=Preloaded['squareBox'], image_color=(1, 1, 1, 1), scale=0.235, pos=pos, command=command, extraArgs=extraArgs)

    def removeNode(self):
        self.destroy()

    def destroy(self):
        if not self.animalLabel:
            return
        else:
            DirectFrame.destroy(self)
            for button in self.headButtons + self.torsoButtons + self.legsButtons:
                button.destroy()

            for head in self.toonHeads:
                head.delete()

            for part in self.torsos + self.legs:
                part.removeNode()

            self.animalLabel.destroy()
            self.bodyLabel.destroy()
            self.animalLabel = None
            self.bodyLabel = None
            self.toonHeads = None
            self.torsos = None
            self.headButtons = None
            self.torsoButtons = None
            self.legsButtons = None
            self.legs = None
            self.lastTorsos = None
            self.callback = None
            return

    def setToon(self, toon):
        for head in self.toonHeads:
            head.generateToonColor(toon.style)

        for leg in self.legs:
            leg.setColor(toon.style.getLegColor())

        shirtTex = ToonDNA.Shirts[toon.style.topTex]
        if toon.style.getGender() == 'm':
            bottomTex = ToonDNA.BoyShorts[toon.style.botTex]
        else:
            bottomTex = ToonDNA.GirlBottoms[toon.style.botTex][0]
        shirtTex = loader.loadTexture(shirtTex)
        bottomTex = loader.loadTexture(bottomTex)
        if toon.style.gender == 'm' or ToonDNA.GirlBottoms[toon.style.botTex][1] == ToonDNA.SHORTS:
            torsos = ToonDNA.toonTorsoTypes[:3]
        else:
            torsos = ToonDNA.toonTorsoTypes[3:6]
        if not self.torsos or torsos != self.lastTorsos:
            for torso in self.torsos:
                torso.removeNode()

            self.torsos = []
            for i, type in enumerate(torsos):
                torso = loader.loadModel(Toon.TorsoDict.get(type) + '1000')
                torso.reparentTo(self.torsoButtons[i])
                torso.setPos(0, 0, -0.2 if type[0] == 'l' else -0.14)
                self.setupPart(torso)
                self.torsos.append(torso)
                for part in ('arms', 'hands', 'neck', 'sleeves'):
                    part = torso.find('**/' + part)
                    if part:
                        part.removeNode()

        self.lastTorsos = torsos
        for torso in self.torsos:
            top = torso.find('**/torso-top')
            top.setTexture(shirtTex, 1)
            top.setColor(*toon.style.topTexColor)
            for bottom in torso.findAllMatches('**/torso-bot'):
                bottom.setTexture(bottomTex, 1)
                bottom.setColor(*toon.style.botTexColor)

        self.setIndex(self.headButtons, ToonDNA.toonSpeciesTypes.index(toon.style.head[0]))
        self.setIndex(self.torsoButtons, self.lastTorsos.index(toon.style.torso))
        self.setIndex(self.legsButtons, ToonDNA.toonLegTypes.index(toon.style.legs))
        self.toon = toon

    def setIndex(self, buttons, index):
        if buttons[index]['image_color'] == (1, 0.5, 0, 1):
            return False
        for i, button in enumerate(buttons):
            button['image_color'] = (1, 0.5, 0, 1) if i == index else (1, 1, 0, 1)

        return True

    def initToon(self):
        self.toon.loop('neutral', 0)
        self.toon.swapToonColor(self.toon.style)

    def __swapHead(self, i):
        self.setIndex(self.headButtons, i)
        species = ToonDNA.toonSpeciesTypes[i]
        headList = ToonDNA.getHeadList(species)
        headSize = self.toon.style.head[1:3]
        if species + headSize in headList:
            index = headList.index(species + headSize) + 1
        else:
            index = 0
        if index >= len(headList):
            index = 0
        head = headList[index]
        self.toon.style.head = head
        self.toon.swapToonHead(head)
        self.initToon()

    def __swapTorso(self, i):
        if not self.setIndex(self.torsoButtons, i):
            return
        torso = self.lastTorsos[i]
        self.toon.style.torso = torso
        self.toon.swapToonTorso(torso)
        self.initToon()

    def __swapLegs(self, i):
        if not self.setIndex(self.legsButtons, i):
            return
        legs = ToonDNA.toonLegTypes[i]
        self.toon.style.legs = legs
        self.toon.swapToonLegs(legs)
        self.initToon()