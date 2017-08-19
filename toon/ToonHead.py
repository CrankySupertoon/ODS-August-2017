# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toon.ToonHead
from panda3d.core import CSDefault, GeomNode, Mat3, Mat4, NodePath, Point3, Texture, VBase3, Vec3, composeMatrix, decomposeMatrix, lookAt
from direct.interval.IntervalGlobal import *
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.actor import Actor
from direct.task import Task
from toontown.toonbase import ToontownGlobals
import random
if not config.GetBool('want-new-anims', 1):
    HeadDict = {'dls': 'phase_3.5/models/char/dogMM_Shorts-head-',
     'dss': 'phase_3.5/models/char/dogMM_Skirt-head-',
     'dsl': 'phase_3.5/models/char/dogSS_Shorts-head-',
     'dll': 'phase_3.5/models/char/dogLL_Shorts-head-',
     'c': 'phase_3.5/models/char/cat-heads-',
     'h': 'phase_3.5/models/char/horse-heads-',
     'm': 'phase_3.5/models/char/mouse-heads-',
     'r': 'phase_3.5/models/char/rabbit-heads-',
     'f': 'phase_3.5/models/char/duck-heads-',
     'p': 'phase_3.5/models/char/monkey-heads-',
     'b': 'phase_3.5/models/char/bear-heads-',
     'j': 'phase_3.5/models/char/cow-heads-',
     's': 'phase_3.5/models/char/pig-heads-',
     'a': 'phase_3.5/models/char/deer-heads-'}
else:
    HeadDict = {'dls': 'phase_3.5/models/char/tt_a_chr_dgm_shorts_head_',
     'dss': 'phase_3.5/models/char/tt_a_chr_dgm_skirt_head_',
     'dsl': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_head_',
     'dll': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_head_',
     'c': 'phase_3.5/models/char/cat-heads-',
     'h': 'phase_3.5/models/char/horse-heads-',
     'm': 'phase_3.5/models/char/mouse-heads-',
     'r': 'phase_3.5/models/char/rabbit-heads-',
     'f': 'phase_3.5/models/char/duck-heads-',
     'p': 'phase_3.5/models/char/monkey-heads-',
     'b': 'phase_3.5/models/char/bear-heads-',
     'j': 'phase_3.5/models/char/cow-heads-',
     's': 'phase_3.5/models/char/pig-heads-',
     'a': 'phase_3.5/models/char/deer-heads-'}
EyelashDict = {'d': 'phase_3.5/models/char/dog-lashes',
 'c': 'phase_3.5/models/char/cat-lashes',
 'h': 'phase_3.5/models/char/horse-lashes',
 'm': 'phase_3.5/models/char/mouse-lashes',
 'r': 'phase_3.5/models/char/rabbit-lashes',
 'f': 'phase_3.5/models/char/duck-lashes',
 'p': 'phase_3.5/models/char/monkey-lashes',
 'b': 'phase_3.5/models/char/bear-lashes',
 'j': 'phase_3.5/models/char/cow-lashes',
 's': 'phase_3.5/models/char/pig-lashes',
 'a': 'phase_3.5/models/char/deer-lashes'}
DogMuzzleDict = {'dls': 'phase_3.5/models/char/dogMM_Shorts-headMuzzles-',
 'dss': 'phase_3.5/models/char/dogMM_Skirt-headMuzzles-',
 'dsl': 'phase_3.5/models/char/dogSS_Shorts-headMuzzles-',
 'dll': 'phase_3.5/models/char/dogLL_Shorts-headMuzzles-'}

class ToonHead(Actor.Actor):
    EyesOpen = loader.loadTexture('phase_3/maps/eyes.jpg', 'phase_3/maps/eyes_a.rgb')
    EyesOpen.setMinfilter(Texture.FTLinear)
    EyesOpen.setMagfilter(Texture.FTLinear)
    EyesClosed = loader.loadTexture('phase_3/maps/eyesClosed.jpg', 'phase_3/maps/eyesClosed_a.rgb')
    EyesClosed.setMinfilter(Texture.FTLinear)
    EyesClosed.setMagfilter(Texture.FTLinear)
    EyesSadOpen = loader.loadTexture('phase_3/maps/eyesSad.jpg', 'phase_3/maps/eyesSad_a.rgb')
    EyesSadOpen.setMinfilter(Texture.FTLinear)
    EyesSadOpen.setMagfilter(Texture.FTLinear)
    EyesSadClosed = loader.loadTexture('phase_3/maps/eyesSadClosed.jpg', 'phase_3/maps/eyesSadClosed_a.rgb')
    EyesSadClosed.setMinfilter(Texture.FTLinear)
    EyesSadClosed.setMagfilter(Texture.FTLinear)
    EyesAngryOpen = loader.loadTexture('phase_3/maps/eyesAngry.jpg', 'phase_3/maps/eyesAngry_a.rgb')
    EyesAngryOpen.setMinfilter(Texture.FTLinear)
    EyesAngryOpen.setMagfilter(Texture.FTLinear)
    EyesAngryClosed = loader.loadTexture('phase_3/maps/eyesAngryClosed.jpg', 'phase_3/maps/eyesAngryClosed_a.rgb')
    EyesAngryClosed.setMinfilter(Texture.FTLinear)
    EyesAngryClosed.setMagfilter(Texture.FTLinear)
    EyesSurprised = loader.loadTexture('phase_3/maps/eyesSurprised.jpg', 'phase_3/maps/eyesSurprised_a.rgb')
    EyesSurprised.setMinfilter(Texture.FTLinear)
    EyesSurprised.setMagfilter(Texture.FTLinear)
    LeftA = Point3(0.06, 0.0, 0.14)
    LeftB = Point3(-0.13, 0.0, 0.1)
    LeftC = Point3(-0.05, 0.0, 0.0)
    LeftD = Point3(0.06, 0.0, 0.0)
    RightA = Point3(0.13, 0.0, 0.1)
    RightB = Point3(-0.06, 0.0, 0.14)
    RightC = Point3(-0.06, 0.0, 0.0)
    RightD = Point3(0.05, 0.0, 0.0)
    LeftAD = Point3(LeftA[0] - LeftA[2] * (LeftD[0] - LeftA[0]) / (LeftD[2] - LeftA[2]), 0.0, 0.0)
    LeftBC = Point3(LeftB[0] - LeftB[2] * (LeftC[0] - LeftB[0]) / (LeftC[2] - LeftB[2]), 0.0, 0.0)
    RightAD = Point3(RightA[0] - RightA[2] * (RightD[0] - RightA[0]) / (RightD[2] - RightA[2]), 0.0, 0.0)
    RightBC = Point3(RightB[0] - RightB[2] * (RightC[0] - RightB[0]) / (RightC[2] - RightB[2]), 0.0, 0.0)

    def __init__(self):
        Actor.Actor.__init__(self)
        self.toonName = 'ToonHead-' + str(self.this)
        self.__blinkName = 'blink-' + self.toonName
        self.__stareAtName = 'stareAt-' + self.toonName
        self.__lookName = 'look-' + self.toonName
        self.lookAtTrack = None
        self.__eyes = None
        self.__eyelashOpen = None
        self.__eyelashClosed = None
        self.__lpupil = None
        self.__rpupil = None
        self.__eyesOpen = ToonHead.EyesOpen
        self.__eyesClosed = ToonHead.EyesClosed
        self.__height = 0.0
        self.__eyelashesHiddenByGlasses = False
        self.randGen = random.Random()
        self.randGen.seed(random.random())
        self.eyelids = ClassicFSM('eyelids', [State('off', self.enterEyelidsOff, self.exitEyelidsOff, ['open', 'closed', 'surprised']),
         State('open', self.enterEyelidsOpen, self.exitEyelidsOpen, ['closed', 'surprised', 'off']),
         State('surprised', self.enterEyelidsSurprised, self.exitEyelidsSurprised, ['open', 'closed', 'off']),
         State('closed', self.enterEyelidsClosed, self.exitEyelidsClosed, ['open', 'surprised', 'off'])], 'off', 'off')
        self.eyelids.enterInitialState()
        self.muzzles = None
        self.specialHead = None
        self.__stareAtNode = NodePath()
        self.__defaultStarePoint = Point3(0, 0, 0)
        self.__stareAtPoint = self.__defaultStarePoint
        self.__stareAtTime = 0
        self.lookAtPositionCallbackArgs = None
        return

    def delete(self):
        try:
            self.ToonHead_deleted
        except:
            self.ToonHead_deleted = 1
            taskMgr.remove(self.__blinkName)
            taskMgr.remove(self.__lookName)
            taskMgr.remove(self.__stareAtName)
            if self.lookAtTrack:
                self.lookAtTrack.finish()
                self.lookAtTrack = None
            del self.eyelids
            del self.__stareAtNode
            del self.__stareAtPoint
            if self.__eyes:
                del self.__eyes
            if self.__lpupil:
                del self.__lpupil
            if self.__rpupil:
                del self.__rpupil
            if self.__eyelashOpen:
                del self.__eyelashOpen
            if self.__eyelashClosed:
                del self.__eyelashClosed
            self.lookAtPositionCallbackArgs = None
            Actor.Actor.delete(self)

        return

    def setupHead(self, dna, forGui = 0):
        self.__height = self.generateToonHead(dna, forGui)
        self.generateToonColor(dna)
        animalStyle = dna.getAnimal()
        bodyScale = ToontownGlobals.toonBodyScales[animalStyle]
        headScale = ToontownGlobals.toonHeadScales[animalStyle]
        self.getGeomNode().setScale(headScale[0] * bodyScale * 1.3, headScale[1] * bodyScale * 1.3, headScale[2] * bodyScale * 1.3)
        if forGui:
            self.getGeomNode().setDepthWrite(True)
            self.getGeomNode().setDepthTest(True)
        if dna.getAnimal() == 'dog':
            self.loop('neutral')
        if settings['smoothAnimations']:
            self.setBlend(frameBlend=True)

    def fitAndCenterHead(self, maxDim, forGui = 0):
        p1 = Point3()
        p2 = Point3()
        self.calcTightBounds(p1, p2)
        if forGui:
            h = 180
            t = p1[0]
            p1.setX(-p2[0])
            p2.setX(-t)
        else:
            h = 0
        d = p2 - p1
        biggest = max(d[0], d[2])
        s = maxDim / biggest
        mid = (p1 + d / 2.0) * s
        self.setPosHprScale(-mid[0], -mid[1] + 1, -mid[2], h, 0, 0, s, s, s)

    def setLookAtPositionCallbackArgs(self, argTuple):
        self.lookAtPositionCallbackArgs = argTuple

    def getHeight(self):
        return self.__height

    def getRandomForwardLookAtPoint(self):
        x = self.randGen.choice((-0.8, -0.5, 0, 0.5, 0.8))
        z = self.randGen.choice((-0.5, 0, 0.5, 0.8))
        return Point3(x, 1.5, z)

    def findSomethingToLookAt(self):
        if self.lookAtPositionCallbackArgs != None:
            pnt = self.lookAtPositionCallbackArgs[0].getLookAtPosition(self.lookAtPositionCallbackArgs[1], self.lookAtPositionCallbackArgs[2])
            self.startStareAt(self, pnt)
            return
        else:
            if self.randGen.random() < 0.33:
                lookAtPnt = self.getRandomForwardLookAtPoint()
            else:
                lookAtPnt = self.__defaultStarePoint
            self.lerpLookAt(lookAtPnt, blink=1)
            return

    def generateToonHead(self, style, forGui = 0):
        headStyle = style.head
        filePrefix = HeadDict[headStyle if headStyle in HeadDict else headStyle[0]]
        headHeight = 0.5 if headStyle[1:3] in ('sl', 'ss') else 0.75
        self.loadModel(loader.loadModel(filePrefix + '1000', customOptions={'flatten': 'medium'}), 'head')
        self.__fixHead(style)
        self.__style = style
        self.__headStyle = headStyle
        self.__fixEyes(style, forGui)
        self.setupEyelashes(style)
        self.eyelids.request('closed')
        self.eyelids.request('open')
        self.setupMuzzles(style)
        return headHeight

    def removeSpecialHead(self):
        if self.specialHead:
            self.specialHead.removeNode()
            self.specialHead = None
        return

    def setupSpecialHead(self):
        self.specialHead.setZ(-0.5)
        self.specialHead.setH(180)
        self.specialHead.reparentTo(self.getHeadJoint())
        self.getPart('head').stash()

    def loadPumpkin(self, type):
        self.specialHead = loader.loadModel('phase_4/models/estate/pumpkin_' + type)
        self.specialHead.setScale(0.5)
        for node in ('floorShadow_plane', 'collision_pSphere1', 'pPlane1'):
            self.specialHead.findAllMatches('**/' + node).detach()

        self.setupSpecialHead()

    def loadSnowman(self, type):
        self.specialHead = loader.loadModel('phase_4/models/props/tt_m_efx_snowmanHead_' + type)
        self.setupSpecialHead()

    def enablePumpkins(self, enable):
        self.removeSpecialHead()
        if enable:
            self.loadPumpkin('tall' if self.__headStyle[1] == 'l' else 'short')
        else:
            self.getPart('head').unstash()

    def enableSnowman(self, enable):
        self.removeSpecialHead()
        if enable:
            self.loadSnowman('tall' if self.__headStyle[1] == 'l' else 'short')
        else:
            self.getPart('head').unstash()

    def hideEars(self):
        self.findAllMatches('**/ears*;+s').stash()

    def showEars(self):
        self.findAllMatches('**/ears*;+s').unstash()

    def hideEyelashes(self):
        if self.__eyelashOpen:
            self.__eyelashOpen.stash()
        if self.__eyelashClosed:
            self.__eyelashClosed.stash()
        self.__eyelashesHiddenByGlasses = True

    def showEyelashes(self):
        if self.__eyelashOpen:
            self.__eyelashOpen.unstash()
        if self.__eyelashClosed:
            self.__eyelashClosed.unstash()
        self.__eyelashesHiddenByGlasses = False

    def generateToonColor(self, style):
        self.findAllMatches('**/head*').setColor(style.getHeadColor())
        if style.getAnimal() in ('cat', 'rabbit', 'bear', 'mouse', 'pig', 'deer', 'cow'):
            self.findAllMatches('**/ear?-*').setColorScale(style.getHeadColor())

    def __fixEyes(self, style, forGui = 0):
        self.__eyes = self.find('**/eyes*')
        if self.__eyes.isEmpty():
            return
        self.__eyes.setColorOff()
        self.drawInFront('eyes*', 'head-front*', -3)
        if not self.find('joint_pupil*').isEmpty():
            self.drawInFront('joint_pupil*', 'eyes*', -1)
        else:
            self.drawInFront('def_*_pupil', 'eyes*', -1)
        if not self.find('**/joint_pupilL*').isEmpty():
            leftPupil = self.find('**/joint_pupilL*')
            rightPupil = self.find('**/joint_pupilR*')
        else:
            leftPupil = self.find('**/def_left_pupil*')
            rightPupil = self.find('**/def_right_pupil*')
        leftEye = self.__eyes.attachNewNode('leftEye')
        rightEye = self.__eyes.attachNewNode('rightEye')
        leftEye.setMat(Mat4(0.8, 0.6, 0, 0, -0.59, 0.79, 0.19, 0, 0.11, -0.15, 0.98, 0, -0.23, 0.41, 0.02, 1))
        rightEye.setMat(Mat4(0.79, -0.62, 0, 0, 0.6, 0.77, 0.21, 0, -0.13, -0.17, 0.98, 0, 0.23, 0.42, 0.02, 1))
        self.__lpupil = leftEye.attachNewNode('leftPupil')
        self.__rpupil = rightEye.attachNewNode('rightPupil')
        lPoint = self.__eyes.attachNewNode('')
        rPoint = self.__eyes.attachNewNode('')
        lPoint.wrtReparentTo(self.__lpupil)
        rPoint.wrtReparentTo(self.__rpupil)
        leftPupil.reparentTo(lPoint)
        rightPupil.reparentTo(rPoint)
        for pupil in (leftPupil, rightPupil):
            pupil.adjustAllPriorities(1)
            if not forGui:
                pupil.setPos(0, 0.02, 0)
            if style.getAnimal() != 'dog':
                pupil.flattenStrong()

    def __setPupilDirection(self, x, y):
        if y < 0.0:
            y2 = -y
            left1 = self.LeftAD + (self.LeftD - self.LeftAD) * y2
            left2 = self.LeftBC + (self.LeftC - self.LeftBC) * y2
            right1 = self.RightAD + (self.RightD - self.RightAD) * y2
            right2 = self.RightBC + (self.RightC - self.RightBC) * y2
        else:
            y2 = y
            left1 = self.LeftAD + (self.LeftA - self.LeftAD) * y2
            left2 = self.LeftBC + (self.LeftB - self.LeftBC) * y2
            right1 = self.RightAD + (self.RightA - self.RightAD) * y2
            right2 = self.RightBC + (self.RightB - self.RightBC) * y2
        left0 = Point3(0.0, 0.0, left1[2] - left1[0] * (left2[2] - left1[2]) / (left2[0] - left1[0]))
        right0 = Point3(0.0, 0.0, right1[2] - right1[0] * (right2[2] - right1[2]) / (right2[0] - right1[0]))
        if x < 0.0:
            x2 = -x
            left = left0 + (left2 - left0) * x2
            right = right0 + (right2 - right0) * x2
        else:
            x2 = x
            left = left0 + (left1 - left0) * x2
            right = right0 + (right1 - right0) * x2
        self.__lpupil.setPos(left)
        self.__rpupil.setPos(right)

    def __lookPupilsAt(self, node, point):
        if node != None:
            mat = node.getMat(self.__eyes)
            point = mat.xformPoint(point)
        distance = 1.0
        recip_z = 1.0 / max(0.1, point[1])
        x = distance * point[0] * recip_z
        y = distance * point[2] * recip_z
        x = min(max(x, -1), 1)
        y = min(max(y, -1), 1)
        self.__setPupilDirection(x, y)
        return

    def __lookHeadAt(self, node, point, frac = 1.0):
        reachedTarget = 1
        head = self.getPart('head')
        if node != None:
            headParent = head.getParent()
            mat = node.getMat(headParent)
            point = mat.xformPoint(point)
        rot = Mat3(0, 0, 0, 0, 0, 0, 0, 0, 0)
        lookAt(rot, Vec3(point), Vec3(0, 0, 1), CSDefault)
        scale = VBase3(0, 0, 0)
        hpr = VBase3(0, 0, 0)
        if decomposeMatrix(rot, scale, hpr, CSDefault):
            hpr = VBase3(min(max(hpr[0], -60), 60), min(max(hpr[1], -20), 30), 0)
            if frac != 1:
                currentHpr = head.getHpr()
                reachedTarget = abs(hpr[0] - currentHpr[0]) < 1.0 and abs(hpr[1] - currentHpr[1]) < 1.0
                hpr = currentHpr + (hpr - currentHpr) * frac
            head.setHpr(hpr)
        return reachedTarget

    def setupEyelashes(self, style):
        if style.getGender() == 'm':
            if self.__eyelashOpen:
                self.__eyelashOpen.removeNode()
                self.__eyelashOpen = None
            if self.__eyelashClosed:
                self.__eyelashClosed.removeNode()
                self.__eyelashClosed = None
        else:
            if self.__eyelashOpen:
                self.__eyelashOpen.removeNode()
            if self.__eyelashClosed:
                self.__eyelashClosed.removeNode()
            animal = style.head[0]
            model = loader.loadModel(EyelashDict[animal])
            head = self.getPart('head')
            length = style.head[1]
            if length == 'l':
                openString = 'open-long'
                closedString = 'closed-long'
            else:
                openString = 'open-short'
                closedString = 'closed-short'
            self.__eyelashOpen = model.find('**/' + openString)
            self.__eyelashClosed = model.find('**/' + closedString)
            for eyelash in (self.__eyelashOpen, self.__eyelashOpen):
                eyelash.reparentTo(head)

            model.removeNode()
        return

    def __fixHead(self, style):
        if style.head in ('dls', 'dss', 'dsl', 'dll'):
            return
        headStyle = style.head[1:3]
        if headStyle == 'ls':
            self.__fixHeadMismatch(style, 'long', 'short')
        elif headStyle == 'sl':
            self.__fixHeadMismatch(style, 'short', 'long')
        else:
            for part in self.findAllMatches('**/*%s*' % ('long' if headStyle == 'ss' else 'short')):
                part.removeNode()

    def __fixHeadMismatch(self, style, short, long):
        animalType = style.getAnimal()
        if animalType not in ('duck', 'horse'):
            self.find('**/ears-' + (short if animalType == 'rabbit' else long)).removeNode()
        if animalType != 'rabbit':
            self.find('**/eyes-' + long).removeNode()
        self.find('**/joint_pupilL_' + long).removeNode()
        self.find('**/joint_pupilR_' + long).removeNode()
        self.find('**/head-' + long).removeNode()
        self.find('**/head-front-' + long).removeNode()
        for part in self.findAllMatches('**/muzzle-%s*' % (long if animalType == 'rabbit' else short)):
            part.removeNode()

    def __blinkOpenEyes(self, task):
        if self.eyelids.getCurrentState().getName() == 'closed':
            self.eyelids.request('open')
        r = self.randGen.random()
        if r < 0.1:
            t = 0.2
        else:
            t = r * 4.0 + 1.0
        taskMgr.doMethodLater(t, self.__blinkCloseEyes, self.__blinkName)
        return Task.done

    def __blinkCloseEyes(self, task):
        if self.eyelids.getCurrentState().getName() != 'open':
            taskMgr.doMethodLater(4.0, self.__blinkCloseEyes, self.__blinkName)
        else:
            self.eyelids.request('closed')
            taskMgr.doMethodLater(0.125, self.__blinkOpenEyes, self.__blinkName)
        return Task.done

    def startBlink(self):
        taskMgr.remove(self.__blinkName)
        if self.__eyes:
            self.openEyes()
        taskMgr.doMethodLater(self.randGen.random() * 4.0 + 1, self.__blinkCloseEyes, self.__blinkName)

    def stopBlink(self):
        taskMgr.remove(self.__blinkName)
        if self.__eyes:
            self.eyelids.request('open')

    def closeEyes(self):
        if hasattr(self, 'eyelids') and self.eyelids:
            self.eyelids.request('closed')

    def openEyes(self):
        if hasattr(self, 'eyelids') and self.eyelids:
            self.eyelids.request('open')

    def surpriseEyes(self):
        if hasattr(self, 'eyelids') and self.eyelids:
            self.eyelids.request('surprised')

    def sadEyes(self):
        self.__eyesOpen = ToonHead.EyesSadOpen
        self.__eyesClosed = ToonHead.EyesSadClosed

    def angryEyes(self):
        self.__eyesOpen = ToonHead.EyesAngryOpen
        self.__eyesClosed = ToonHead.EyesAngryClosed

    def normalEyes(self):
        self.__eyesOpen = ToonHead.EyesOpen
        self.__eyesClosed = ToonHead.EyesClosed

    def blinkEyes(self):
        taskMgr.remove(self.__blinkName)
        if hasattr(self, 'eyelids') and self.eyelids:
            self.eyelids.request('closed')
            taskMgr.doMethodLater(0.1, self.__blinkOpenEyes, self.__blinkName)

    def __stareAt(self, task):
        frac = 2 * globalClock.getDt()
        reachedTarget = self.__lookHeadAt(self.__stareAtNode, self.__stareAtPoint, frac)
        self.__lookPupilsAt(self.__stareAtNode, self.__stareAtPoint)
        if reachedTarget and self.__stareAtNode == None:
            return Task.done
        else:
            return Task.cont
            return

    def doLookAroundToStareAt(self, node, point):
        self.startStareAt(node, point)
        self.startLookAround()

    def startStareAtHeadPoint(self, point):
        self.startStareAt(self, point)

    def startStareAt(self, node, point):
        taskMgr.remove(self.__stareAtName)
        if self.lookAtTrack:
            self.lookAtTrack.finish()
            self.lookAtTrack = None
        self.__stareAtNode = node
        if point != None:
            self.__stareAtPoint = point
        else:
            self.__stareAtPoint = self.__defaultStarePoint
        self.__stareAtTime = globalClock.getFrameTime()
        taskMgr.add(self.__stareAt, self.__stareAtName)
        return

    def lerpLookAt(self, point, time = 1.0, blink = 0):
        taskMgr.remove(self.__stareAtName)
        if self.lookAtTrack:
            self.lookAtTrack.finish()
            self.lookAtTrack = None
        head = self.getPart('head')
        startHpr = head.getHpr()
        startLpupil = self.__lpupil.getPos()
        startRpupil = self.__rpupil.getPos()
        self.__lookHeadAt(None, point)
        self.__lookPupilsAt(None, point)
        endHpr = head.getHpr()
        endLpupil = self.__lpupil.getPos() * 0.5
        endRpupil = self.__rpupil.getPos() * 0.5
        head.setHpr(startHpr)
        self.__lpupil.setPos(startLpupil)
        self.__rpupil.setPos(startRpupil)
        if startHpr.almostEqual(endHpr, 10):
            return 0
        else:
            if blink:
                self.blinkEyes()
            lookToTgt_TimeFraction = 0.2
            lookToTgtTime = time * lookToTgt_TimeFraction
            returnToEyeCenterTime = time - lookToTgtTime - 0.5
            origin = Point3(0, 0, 0)
            blendType = 'easeOut'
            self.lookAtTrack = Parallel(Sequence(LerpPosInterval(self.__lpupil, lookToTgtTime, endLpupil, blendType=blendType), Wait(0.5), LerpPosInterval(self.__lpupil, returnToEyeCenterTime, origin, blendType=blendType)), Sequence(LerpPosInterval(self.__rpupil, lookToTgtTime, endRpupil, blendType=blendType), Wait(0.5), LerpPosInterval(self.__rpupil, returnToEyeCenterTime, origin, blendType=blendType)), name=self.__stareAtName)
            self.lookAtTrack.append(LerpHprInterval(head, time, endHpr, blendType='easeInOut'))
            self.lookAtTrack.start()
            return 1

    def stopStareAt(self):
        self.lerpLookAt(Vec3.forward())

    def stopStareAtNow(self):
        taskMgr.remove(self.__stareAtName)
        if self.lookAtTrack:
            self.lookAtTrack.finish()
            self.lookAtTrack = None
        if self.__lpupil and self.__rpupil:
            self.__setPupilDirection(0, 0)
        head = self.getPart('head')
        head.setHpr(0, 0, 0)
        return

    def __lookAround(self, task):
        self.findSomethingToLookAt()
        t = self.randGen.random() * 4.0 + 3.0
        taskMgr.doMethodLater(t, self.__lookAround, self.__lookName)
        return Task.done

    def startLookAround(self):
        taskMgr.remove(self.__lookName)
        t = self.randGen.random() * 5.0 + 2.0
        taskMgr.doMethodLater(t, self.__lookAround, self.__lookName)

    def stopLookAround(self):
        taskMgr.remove(self.__lookName)
        self.stopStareAt()

    def stopLookAroundNow(self):
        taskMgr.remove(self.__lookName)
        self.stopStareAtNow()

    def enterEyelidsOff(self):
        pass

    def exitEyelidsOff(self):
        pass

    def enterEyelidsOpen(self):
        if not self.__eyes.isEmpty():
            self.__eyes.setTexture(self.__eyesOpen, 1)
            self.openEyelash()

    def exitEyelidsOpen(self):
        pass

    def enterEyelidsClosed(self):
        if not self.__eyes.isEmpty() and self.__eyesClosed:
            self.__eyes.setTexture(self.__eyesClosed, 1)
            self.closeEyelash()

    def exitEyelidsClosed(self):
        pass

    def enterEyelidsSurprised(self):
        if not self.__eyes.isEmpty() and ToonHead.EyesSurprised:
            self.__eyes.setTexture(ToonHead.EyesSurprised, 1)
            self.showMuzzle('surprise')
            self.hideEyelash()

    def exitEyelidsSurprised(self):
        self.showMuzzle('neutral')

    def hideEyelash(self):
        if self.__eyelashOpen:
            self.__eyelashOpen.hide()
        if self.__eyelashClosed:
            self.__eyelashClosed.hide()
        if self.__lpupil:
            self.__lpupil.show()
            self.__rpupil.show()

    def openEyelash(self):
        if self.__eyelashOpen:
            self.__eyelashOpen.show()
        if self.__eyelashClosed:
            self.__eyelashClosed.hide()
        if self.__lpupil:
            self.__lpupil.show()
            self.__rpupil.show()

    def closeEyelash(self):
        if self.__eyelashOpen:
            self.__eyelashOpen.hide()
        if self.__eyelashClosed:
            self.__eyelashClosed.show()
        if self.__lpupil:
            self.__lpupil.hide()
            self.__rpupil.hide()

    def getHeadJoint(self):
        if not self.find('**/def_head').isEmpty():
            return self.find('**/def_head')
        else:
            return self.find('**/joint_toHead')

    def setupMuzzles(self, style):
        if style.getAnimal() != 'dog':
            muzzle = self.find('**/muzzle*neutral')
        else:
            muzzle = self.find('**/muzzle*')
            filePrefix = DogMuzzleDict[style.head]
            loader.loadModel(filePrefix + '1000').reparentTo(self.getHeadJoint())
        self.muzzles = {'neutral': muzzle}
        for type in ('surprise', 'angry', 'sad', 'smile', 'laugh'):
            muzzle = self.find('**/muzzle*' + type)
            if muzzle:
                self.muzzles[type] = muzzle

        self.showMuzzle('neutral')

    def showMuzzle(self, type):
        if type not in self.muzzles:
            self.showMuzzle('neutral')
            return
        for muzzle in self.muzzles.values():
            muzzle.hide()

        self.muzzles[type].show()