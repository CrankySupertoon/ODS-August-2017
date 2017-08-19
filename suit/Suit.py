# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.suit.Suit
from panda3d.core import CollideMask, GeomNode, NodePath, Point3, Texture, Vec4
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.task.Task import Task
from otp.avatar import Avatar
from otp.otpbase import OTPLocalizer
from toontown.battle import SuitBattleGlobals
from otp.nametag.NametagConstants import CFSpeech
from otp.nametag.NametagGroup import NametagGroup
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.suit import SuitGlobals
from toontown.effects import DustCloud
import SuitDNA, SuitHealthBar, string, random
aSize = 6.06
bSize = 5.29
cSize = 4.14
AllAnims = ['cigar-smoke',
 'drop-react',
 'effort',
 'finger-wag',
 'flail',
 'flatten',
 'fountain-pen',
 'glower',
 'golf-club-swing',
 'hold-eraser',
 'hold-pencil',
 'hypnotize',
 'jump',
 'landing',
 'lose',
 'lured',
 'magic1',
 'magic2',
 'magic3',
 'neutral',
 'pencil-sharpener',
 'phone',
 'pickpocket',
 'pie-small',
 'rake',
 'reach',
 'roll-o-dex',
 'rubber-stamp',
 'shredder',
 'sidestep-left',
 'sidestep-right',
 'sit',
 'sit-angry',
 'sit-eat-in',
 'sit-eat-loop',
 'sit-eat-out',
 'sit-hungry-left',
 'sit-hungry-right',
 'sit-lose',
 'slip-backward',
 'slip-forward',
 'smile',
 'soak',
 'song-and-dance',
 'speak',
 'squirt-large',
 'squirt-small',
 'stomp',
 'throw-object',
 'throw-paper',
 'tray-neutral',
 'tray-walk',
 'tug-o-war',
 'victory',
 'walk',
 'watercooler']
if not config.GetBool('want-new-cogs', 0):
    ModelDict = {'a': 'phase_3.5/models/char/suitA-',
     'b': 'phase_3.5/models/char/suitB-',
     'c': 'phase_3.5/models/char/suitC-'}
else:
    ModelDict = {'a': 'phase_3.5/models/char/tt_a_ene_cga_',
     'b': 'phase_3.5/models/char/tt_a_ene_cgb_',
     'c': 'phase_3.5/models/char/tt_a_ene_cgc_'}
AnimDict = {key:{anim:value + anim for anim in AllAnims} for key, value in ModelDict.iteritems()}
PreloadedHeads = {}
DialogTypes = ['grunt',
 'murmur',
 'statement',
 'question',
 'exclaim']
SkelSuitDialogArray = [ loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_%s.ogg' % dialog) for dialog in DialogTypes ]
SuitDialogArray = [ loader.loadSfx('phase_3.5/audio/dial/COG_VO_%s.ogg' % dialog) for dialog in DialogTypes ]

def loadModels():
    global PreloadedHeads
    if PreloadedHeads:
        return
    heads = loader.loadModel('phase_4/models/char/suit-heads')
    for head in heads.getChildren():
        head.flattenStrong()
        PreloadedHeads[head.getName()] = head

    customHeads = {'shotgun': 'phase_4/models/char/shotgun-head'}
    for name, path in customHeads.iteritems():
        head = loader.loadModel(path)
        head.flattenStrong()
        PreloadedHeads[name] = head


def attachSuitHead(node, suitName):
    properties = SuitGlobals.suitProperties[suitName]
    headTex = properties[SuitGlobals.HEAD_TEXTURE_INDEX]
    head = node.attachNewNode('head', 0)
    heads = properties[SuitGlobals.HEADS_INDEX]
    for headName in heads:
        headNode = NodePath(PreloadedHeads[headName].node().copySubgraph())
        headNode.reparentTo(head)
        if headTex:
            headNode.setTexture(loader.loadTexture('phase_3.5/maps/' + headTex), 1)
        if suitName == 'cc':
            headNode.setColor(SuitGlobals.ColdCallerHead)

    head.reparentTo(node)
    head.setDepthTest(True)
    head.setDepthWrite(True)
    p1 = Point3()
    p2 = Point3()
    head.calcTightBounds(p1, p2)
    d = p2 - p1
    biggest = max(d[0], d[2])
    column = SuitDNA.suitHeadTypes.index(suitName) % SuitDNA.suitsPerDept
    s = (0.2 + column / 100.0) / biggest
    pos = -0.14 + (SuitDNA.suitsPerDept - column - 1) / 135.0
    head.setPos(0, 0, pos)
    head.setScale(s)
    if 'shotgun' not in heads:
        head.setHpr(180, 0, 0)
    return head


class Suit(Avatar.Avatar):
    medallionColors = {'c': Vec4(0.863, 0.776, 0.769, 1.0),
     's': Vec4(0.843, 0.745, 0.745, 1.0),
     'l': Vec4(0.749, 0.776, 0.824, 1.0),
     'm': Vec4(0.749, 0.769, 0.749, 1.0),
     't': Vec4(0.556, 0.392, 0.541, 1.0)}

    def __init__(self):
        Avatar.Avatar.__init__(self)
        self.setFont(ToontownGlobals.getSuitFont())
        self.nametag.setSpeechFont(ToontownGlobals.getSuitFont())
        self.setPlayerType(NametagGroup.CCSuit)
        self.setPickable(1)
        self.leftHand = None
        self.rightHand = None
        self.shadowJoint = None
        self.nametagJoint = None
        self.headParts = []
        self.healthBar = SuitHealthBar.SuitHealthBar()
        self.isDisguised = 0
        self.isWaiter = 0
        self.isRental = 0
        self.isSkeleton = 0
        self.level = 0
        self.soundSequenceList = []
        return

    def delete(self):
        try:
            self.Suit_deleted
        except:
            self.Suit_deleted = 1
            if self.leftHand:
                self.leftHand.removeNode()
                self.leftHand = None
            if self.rightHand:
                self.rightHand.removeNode()
                self.rightHand = None
            if self.shadowJoint:
                self.shadowJoint.removeNode()
                self.shadowJoint = None
            if self.nametagJoint:
                self.nametagJoint.removeNode()
                self.nametagJoint = None
            for part in self.headParts:
                part.removeNode()

            for soundSequence in self.soundSequenceList:
                soundSequence.pause()

            self.soundSequenceList = []
            self.headParts = []
            self.healthBar.delete()
            Avatar.Avatar.delete(self)

        return

    def uniqueName(self, name):
        return 'Suit-%s-%s' % (id(self), name)

    def setHeight(self, height):
        Avatar.Avatar.setHeight(self, height)
        self.nametag3d.setPos(0, 0, height + 1.0)

    def getRadius(self):
        return 2

    def setDNAString(self, dnaString):
        self.dna = SuitDNA.SuitDNA()
        self.dna.makeFromNetString(dnaString)
        self.setDNA(self.dna)

    def setDNA(self, dna):
        if self.style:
            self.removePart('modelRoot')
            self.style = dna
            self.generateSuit(True)
            self.loop('neutral')
            self.healthBar.update(1)
            self.corpMedallion.hide()
            self.healthBar.geom.show()
        else:
            self.style = dna
            self.generateSuit()
        self.initializeDropShadow()
        self.initializeNametag3d()

    def getSkeleRevives(self):
        return 0

    def setDisplayLevel(self, level = None):
        if not hasattr(self.style, 'name'):
            return
        if not level:
            level = SuitDNA.getSuitType(self.style.name)
        level = str(level)
        if self.getSkeleRevives() > 0:
            level += TTLocalizer.SkeleRevivePostFix % (self.skeleRevives + 1)
        self.setDisplayName(TTLocalizer.SuitBaseNameWithLevel % {'name': self.name,
         'dept': self.getStyleDept(),
         'level': level})

    def getStyleDept(self):
        if hasattr(self, 'style') and self.style:
            return SuitDNA.getDeptFullname(self.style.dept)

    def generateSuit(self, dustCloud = False):
        if dustCloud:
            dustCloud = DustCloud.DustCloud(fBillboard=0, wantSound=1)
            dustCloud.setBillboardAxis(2.0)
            dustCloud.setZ(3)
            dustCloud.setScale(0.4)
            dustCloud.createTrack()
            dustCloud.reparentTo(render)
            dustCloud.setPos(self, 0, 0, 0)
            Sequence(dustCloud.track, Func(dustCloud.destroy)).start()
            if self.isSkeleton:
                self.makeSkeleton()
                return
        dna = self.style
        self.headParts = []
        self.headColor = None
        self.headTexture = None
        self.loseActor = None
        if dna.name in SuitGlobals.suitProperties:
            properties = SuitGlobals.suitProperties[dna.name]
            self.scale = properties[SuitGlobals.SCALE_INDEX]
            self.handColor = properties[SuitGlobals.HAND_COLOR_INDEX]
            if dna.name == 'cc':
                self.headColor = SuitGlobals.ColdCallerHead
            self.generateBody()
            if properties[SuitGlobals.HEAD_TEXTURE_INDEX]:
                self.headTexture = properties[SuitGlobals.HEAD_TEXTURE_INDEX]
            for head in properties[SuitGlobals.HEADS_INDEX]:
                self.generateHead(head)

            self.setHeight(properties[SuitGlobals.HEIGHT_INDEX])
        self.setName(SuitBattleGlobals.SuitAttributes[dna.name]['name'])
        self.getGeomNode().setScale(self.scale)
        self.generateHealthBar()
        self.generateCorporateMedallion()
        if dna.name == 'pp':
            self.setupPinchers()
        if settings['smoothAnimations']:
            self.setBlend(frameBlend=True)
        if dustCloud:
            if self.virtual:
                self.setVirtual(self.virtual)
            elif self.isWaiter:
                self.makeWaiter()
        return

    def setupPinchers(self):
        hands = loader.loadModel('phase_4/models/props/pinch_hands')
        lExpose = self.exposeJoint(None, 'modelRoot', 'Lh_wrist')
        rExpose = self.exposeJoint(None, 'modelRoot', 'Rh_wrist')
        lHand = hands.find('**/Lhand')
        rHand = hands.find('**/Rhand')
        rHand.setX(-0.75)
        if not self.isSkeleton:
            lHand.setColorScale(self.handColor)
            rHand.setColorScale(self.handColor)
        else:
            lHand.setColorScale(0.5, 0.5, 0.5, 1.0)
            rHand.setColorScale(0.5, 0.5, 0.5, 1.0)
        if not hands.isEmpty():
            hands.reparentTo(hidden)
        if not hands.isEmpty():
            if not lHand.isEmpty() and not rHand.isEmpty():
                lHand.reparentTo(self.leftHand)
                rHand.reparentTo(self.rightHand)
        return

    def getActualLevel(self):
        if hasattr(self, 'style'):
            return SuitBattleGlobals.getActualFromRelativeLevel(self.style.name, self.level) + 1
        else:
            self.notify.warning('called getActualLevel with no DNA, returning 1 for level')
            return 1

    def generateBody(self):
        animDict = self.getAnimDict()
        self.loadModel(loader.loadModel(ModelDict[self.style.body] + 'mod', customOptions={'flatten': 'medium'}))
        self.loadAnims(animDict)
        self.setSuitClothes()

    def getAnimDict(self):
        return AnimDict[self.style.body]

    def initializeBodyCollisions(self, collIdStr):
        Avatar.Avatar.initializeBodyCollisions(self, collIdStr)
        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)

    def setSuitClothes(self, modelRoot = None):
        if not modelRoot:
            modelRoot = self
        dept = self.style.dept
        torsoTex = loader.loadTexture('phase_3.5/maps/%s_blazer.jpg' % dept)
        torsoTex.setMinfilter(Texture.FTLinearMipmapLinear)
        torsoTex.setMagfilter(Texture.FTLinear)
        legTex = loader.loadTexture('phase_3.5/maps/%s_leg.jpg' % dept)
        legTex.setMinfilter(Texture.FTLinearMipmapLinear)
        legTex.setMagfilter(Texture.FTLinear)
        armTex = loader.loadTexture('phase_3.5/maps/%s_sleeve.jpg' % dept)
        armTex.setMinfilter(Texture.FTLinearMipmapLinear)
        armTex.setMagfilter(Texture.FTLinear)
        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)
        modelRoot.find('**/hands').setColorScale(self.handColor)
        self.leftHand = self.find('**/joint_Lhold')
        self.rightHand = self.find('**/joint_Rhold')
        self.shadowJoint = self.find('**/joint_shadow')
        self.nametagJoint = self.find('**/joint_nameTag')

    def makeWaiter(self, modelRoot = None):
        if not modelRoot:
            modelRoot = self
        self.isWaiter = 1
        torsoTex = loader.loadTexture('phase_3.5/maps/waiter_m_blazer.jpg')
        torsoTex.setMinfilter(Texture.FTLinearMipmapLinear)
        torsoTex.setMagfilter(Texture.FTLinear)
        legTex = loader.loadTexture('phase_3.5/maps/waiter_m_leg.jpg')
        legTex.setMinfilter(Texture.FTLinearMipmapLinear)
        legTex.setMagfilter(Texture.FTLinear)
        armTex = loader.loadTexture('phase_3.5/maps/waiter_m_sleeve.jpg')
        armTex.setMinfilter(Texture.FTLinearMipmapLinear)
        armTex.setMagfilter(Texture.FTLinear)
        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)

    def makeRentalSuit(self, suitType, modelRoot = None):
        if suitType != 's':
            return
        if not modelRoot:
            modelRoot = self.getGeomNode()
        torsoTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_blazer.jpg')
        legTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_leg.jpg')
        armTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_sleeve.jpg')
        handTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_hand.jpg')
        self.isRental = 1
        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)
        modelRoot.find('**/hands').setTexture(handTex, 1)

    def generateHead(self, headType):
        if headType not in PreloadedHeads:
            return
        head = NodePath(PreloadedHeads[headType].node().copySubgraph())
        head = self.instance(head, 'modelRoot', 'to_head' if self.find('**/to_head') else 'joint_head')
        if headType == 'shotgun':
            head.setH(180)
            head.setZ(-0.125)
        if self.headTexture:
            headTex = loader.loadTexture('phase_3.5/maps/%s' % self.headTexture)
            headTex.setMinfilter(Texture.FTLinearMipmapLinear)
            headTex.setMagfilter(Texture.FTLinear)
            head.setTexture(headTex, 1)
        if self.headColor:
            head.setColor(self.headColor)
        self.headParts.append(head)

    def generateCorporateTie(self, modelPath = None):
        if not modelPath:
            modelPath = self
        dept = self.style.dept
        tie = modelPath.find('**/tie')
        if tie.isEmpty():
            self.notify.warning('skelecog has no tie model!!!')
            return
        if dept == 'c':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_boss.jpg')
        elif dept == 's':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_sales.jpg')
        elif dept == 'l':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_legal.jpg')
        elif dept == 'm':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_money.jpg')
        elif dept == 't':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_tech.jpg')
        tieTex.setMinfilter(Texture.FTLinearMipmapLinear)
        tieTex.setMagfilter(Texture.FTLinear)
        tie.setTexture(tieTex, 1)

    def generateCorporateMedallion(self):
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        dept = self.style.dept
        if dept in SuitDNA.suitDeptModelPaths:
            self.corpMedallion = icons.find(SuitDNA.suitDeptModelPaths[dept]).copyTo(self.getMeterJoint())
        self.corpMedallion.setPosHprScale(0.02, 0.05, 0.04, 180.0, 0.0, 0.0, 0.51, 0.51, 0.51)
        self.corpMedallion.setColor(self.medallionColors[dept])
        icons.removeNode()

    def getMeterJoint(self):
        return self.find('**/joint_attachMeter')

    def generateHealthBar(self):
        self.healthBar.generate()
        self.healthBar.geom.reparentTo(self.getMeterJoint())
        self.healthBar.geom.setScale(3.0)

    def resetHealthBarForSkele(self):
        self.currHP = self.maxHP
        self.healthBar.geom.setPos(0.0, 0.1, 0.0)

    def updateHealthBar(self, hp, forceUpdate = 0):
        if hp > self.currHP:
            hp = self.currHP
        self.currHP -= hp
        self.healthBar.update(float(self.currHP) / float(self.maxHP))

    def getLoseActor(self):
        if self.loseActor == None:
            loseAnim = ModelDict[self.style.body] + 'lose'
            if not self.isSkeleton:
                self.loseActor = Actor.Actor(loseAnim + '-mod', {'lose': loseAnim})
                loseNeck = self.loseActor.find('**/joint_head')
                for part in self.headParts:
                    part.instanceTo(loseNeck)

                if self.isWaiter:
                    self.makeWaiter(self.loseActor)
                else:
                    self.setSuitClothes(self.loseActor)
                if self.style.name == 'pp':
                    hands = loader.loadModel('phase_4/models/props/pinch_hands')
                    lExpose = self.loseActor.exposeJoint(None, 'modelRoot', 'Lh_wrist')
                    rExpose = self.loseActor.exposeJoint(None, 'modelRoot', 'Rh_wrist')
                    lHand = hands.find('**/Lhand')
                    rHand = hands.find('**/Rhand')
                    lHand.setColorScale(self.handColor)
                    rHand.setColorScale(self.handColor)
                    if not hands.isEmpty():
                        hands.reparentTo(hidden)
                    if not hands.isEmpty():
                        if not lHand.isEmpty() and not rHand.isEmpty():
                            lHand.reparentTo(self.loseActor.find('**/joint_Lhold'))
                            rHand.reparentTo(self.loseActor.find('**/joint_Rhold'))
            else:
                loseModel = 'phase_3.5/models/char/cog' + string.upper(self.style.body) + '_robot-lose-mod'
                self.loseActor = Actor.Actor(loseModel, {'lose': loseAnim})
                self.generateCorporateTie(self.loseActor)
        self.loseActor.setScale(self.scale)
        self.loseActor.setPos(self.getPos())
        self.loseActor.setHpr(self.getHpr())
        shadowJoint = self.loseActor.find('**/joint_shadow')
        dropShadow = loader.loadModel('phase_3/models/props/drop_shadow')
        dropShadow.setScale(0.45)
        dropShadow.setColor(0.0, 0.0, 0.0, 0.5)
        dropShadow.reparentTo(shadowJoint)
        if settings['smoothAnimations']:
            self.loseActor.setBlend(frameBlend=True)
        return self.loseActor

    def cleanupLoseActor(self):
        if self.loseActor:
            self.loseActor.cleanup()
        self.loseActor = None
        return

    def makeSkeleton(self):
        if self.isSkeleton:
            return
        anims = self.getAnimDict()
        anim = self.getCurrentAnim()
        dropShadow = self.dropShadow
        if not dropShadow.isEmpty():
            dropShadow.reparentTo(hidden)
        self.removePart('modelRoot')
        self.loadModel(loader.loadModel('phase_3.5/models/char/cog' + string.upper(self.style.body) + '_robot-zero', customOptions={'flatten': 'medium'}))
        self.loadAnims(anims)
        self.getGeomNode().setScale(self.scale * 1.0173)
        self.generateHealthBar()
        self.generateCorporateMedallion()
        self.generateCorporateTie()
        self.setHeight(self.height)
        parts = self.findAllMatches('**/pPlane*')
        for partNum in xrange(0, parts.getNumPaths()):
            bb = parts.getPath(partNum)
            bb.setTwoSided(1)

        self.setName(TTLocalizer.Skeleton)
        nameInfo = TTLocalizer.SuitBaseNameWithLevel % {'name': self.name,
         'dept': self.getStyleDept(),
         'level': self.getActualLevel()}
        self.setDisplayName(nameInfo)
        self.leftHand = self.find('**/joint_Lhold')
        self.rightHand = self.find('**/joint_Rhold')
        self.shadowJoint = self.find('**/joint_shadow')
        self.nametagNull = self.find('**/joint_nameTag')
        if not dropShadow.isEmpty():
            dropShadow.setScale(0.75)
            if not self.shadowJoint.isEmpty():
                dropShadow.reparentTo(self.shadowJoint)
        self.loop(anim)
        self.isSkeleton = 1

    def getHeadParts(self):
        return self.headParts

    def getRightHand(self):
        return self.rightHand

    def getLeftHand(self):
        return self.leftHand

    def getShadowJoint(self):
        return self.shadowJoint

    def getNametagJoints(self):
        return []

    def getDialogueArray(self):
        if self.isSkeleton:
            return SkelSuitDialogArray
        else:
            return SuitDialogArray

    def getTypeText(self):
        if self.virtual:
            return TTLocalizer.CogPanelVirtual
        if self.isWaiter:
            return TTLocalizer.CogPanelWaiter
        if self.skeleRevives:
            return TTLocalizer.CogPanelRevives % (self.skeleRevives + 1)
        if self.isSkelecog:
            return TTLocalizer.CogPanelSkeleton
        return ''

    def playCurrentDialogue(self, dialogue, chatFlags, interrupt = 1, quiet = 0):
        if quiet:
            return
        else:
            if dialogue:
                base.playSfx(dialogue, node=self)
            elif chatFlags & CFSpeech != 0:
                if self.nametag is not None and self.nametag.getNumChatPages() > 0:
                    self.playDialogueForString(self.nametag.getChat())
                    if self.soundChatBubble != None:
                        base.playSfx(self.soundChatBubble, node=self)
            return

    def playDialogueForString(self, chatString, delay = 0.0):
        if len(chatString) == 0:
            return
        searchString = chatString.lower()
        if searchString.find(OTPLocalizer.DialogExclamation) >= 0:
            type = 'exclamation'
        elif searchString.find(OTPLocalizer.DialogQuestion) >= 0:
            type = 'question'
        elif random.randint(0, 1):
            type = 'statementA'
        else:
            type = 'statementB'
        stringLength = len(chatString)
        if stringLength <= OTPLocalizer.DialogLength1:
            length = 1
        elif stringLength <= OTPLocalizer.DialogLength2:
            length = 2
        elif stringLength <= OTPLocalizer.DialogLength3:
            length = 3
        else:
            length = 4
        self.playDialogue(type, length, delay)

    def playDialogue(self, type, length, delay = 0.0):
        dialogueArray = self.getDialogueArray()
        if dialogueArray == None:
            return
        else:
            sfxIndex = None
            if type == 'statementA' or type == 'statementB':
                if length == 1:
                    sfxIndex = 0
                elif length == 2:
                    sfxIndex = 1
                elif length >= 3:
                    sfxIndex = 2
            elif type == 'question':
                sfxIndex = 3
            elif type == 'exclamation':
                sfxIndex = 4
            else:
                notify.error('unrecognized dialogue type: ', type)
            if sfxIndex != None and sfxIndex < len(dialogueArray) and dialogueArray[sfxIndex] != None:
                soundSequence = Sequence(Wait(delay), Func(base.playSfx, dialogueArray[sfxIndex], listener=base.localAvatar))
                self.soundSequenceList.append(soundSequence)
                soundSequence.start()
                self.cleanUpSoundList()
            return

    def cleanUpSoundList(self):
        self.soundSequenceList = [ seq for seq in self.soundSequenceList if not seq.isStopped() ]