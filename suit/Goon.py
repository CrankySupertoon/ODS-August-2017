# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.suit.Goon
from panda3d.core import CollideMask, GeomNode, Point3
from direct.actor import Actor
from otp.avatar import Avatar
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import GoonGlobals
import SuitDNA
import math
AnimList = ['walk', 'collapse', 'recovery']
ModelDict = {'pg': 'phase_9/models/char/Cog_Goonie',
 'fg1': 'phase_9/models/char/Cog_Goonie',
 'sg': 'phase_9/models/char/Cog_Goonie'}

class Goon(Avatar.Avatar):

    def __init__(self, dnaName = None, hideNametag = True):
        try:
            self.Goon_initialized
        except:
            self.Goon_initialized = 1
            Avatar.Avatar.__init__(self)
            self.ignore('nametagAmbientLightChanged')
            self.hFov = 70
            self.attackRadius = 15
            self.strength = 15
            self.velocity = 4
            self.scale = 1.0
            self.hat = None
            if dnaName is not None:
                self.initGoon(dnaName, hideNametag)

        return

    def initGoon(self, dnaName, hideNametag = True):
        self.type = dnaName
        dna = SuitDNA.SuitDNA()
        dna.newGoon(dnaName)
        self.setDNA(dna)
        self.find('**/actorGeom').setH(180)
        if hideNametag:
            self.nametag3d.hide()

    def initializeBodyCollisions(self, collIdStr):
        Avatar.Avatar.initializeBodyCollisions(self, collIdStr)
        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)

    def setDNAString(self, dnaString):
        self.dna = SuitDNA.SuitDNA()
        self.dna.makeFromNetString(dnaString)
        self.setDNA(self.dna)

    def setDNA(self, dna):
        if self.style:
            return
        self.style = dna
        self.generateGoon()
        self.createHead()
        self.initializeDropShadow()
        self.initializeNametag3d()
        self.nametag3d.setZ(3)

    def generateGoon(self):
        filePrefix = ModelDict[self.style.name] + '-'
        self.loadModel(filePrefix + 'zero')
        self.loadAnims({anim:filePrefix + anim for anim in AnimList})
        if settings['smoothAnimations']:
            self.setBlend(frameBlend=True)

    def getShadowJoint(self):
        return self.getGeomNode()

    def getNametagJoints(self):
        return []

    def createHead(self):
        self.headHeight = 3.0
        head = self.find('**/joint35')
        if head.isEmpty():
            head = self.find('**/joint40')
        self.hat = self.find('**/joint8')
        parentNode = head.getParent()
        self.head = parentNode.attachNewNode('headRotate')
        head.reparentTo(self.head)
        self.hat.reparentTo(self.head)
        if self.type == 'pg':
            self.hat.find('**/security_hat').hide()
        elif self.type == 'sg':
            self.hat.find('**/hard_hat').hide()
        elif self.type == 'fg1':
            self.hat.find('**/security_hat').hide()
            self.hat.setColor(0.862745, 0.517647, 0.0941177, 1)
        else:
            self.hat.find('**/security_hat').hide()
            self.hat.find('**/hard_hat').hide()
        self.eye = self.find('**/eye')
        self.eye.setColorScale(1, 1, 1, 1)
        self.eye.setColor(1, 1, 0, 1)
        self.radar = None
        return

    def scaleRadar(self):
        if self.radar:
            self.radar.removeNode()
        self.radar = self.eye.attachNewNode('radar')
        model = loader.loadModel('phase_9/models/cogHQ/alphaCone2')
        beam = self.radar.attachNewNode('beam')
        transformNode = model.find('**/transform')
        transformNode.getChildren().reparentTo(beam)
        self.radar.setPos(0, -0.5, 0.4)
        self.radar.setTransparency(1)
        self.radar.setDepthWrite(0)
        self.halfFov = self.hFov / 2.0
        fovRad = self.halfFov * math.pi / 180.0
        self.cosHalfFov = math.cos(fovRad)
        kw = math.tan(fovRad) * self.attackRadius / 10.5
        kl = math.sqrt(self.attackRadius * self.attackRadius + 9.0) / 25.0
        beam.setScale(kw / self.scale, kl / self.scale, kw / self.scale)
        beam.setHpr(0, self.halfFov, 0)
        p = self.radar.getRelativePoint(beam, Point3(0, -6, -1.8))
        self.radar.setSz(-3.5 / p[2])
        self.radar.flattenMedium()
        self.radar.setColor(1, 1, 1, 0.2)

    def colorHat(self):
        if self.type == 'pg':
            colorList = GoonGlobals.PG_COLORS
        elif self.type == 'sg':
            colorList = GoonGlobals.SG_COLORS
        elif self.type == 'fg1':
            colorList = GoonGlobals.FG1_COLORS_FATAL
        else:
            return
        if self.strength >= 20:
            self.hat.setColorScale(colorList[0])
        elif self.strength >= 15:
            self.hat.setColorScale(colorList[1])
        else:
            self.hat.clearColorScale()