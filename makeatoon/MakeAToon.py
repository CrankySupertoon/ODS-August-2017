# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.makeatoon.MakeAToon
from panda3d.core import Lens, ModelPool, Point3, SequenceNode, TextNode, Texture, TexturePool, Vec4, rotateTo
from direct.actor.Actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.fsm import StateData
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
import random
import BodyShop
import ColorShop
import GenderShop
from MakeAToonGlobals import *
import MakeClothesGUI
import NameShop
import ChallengeShop
from otp.avatar import Avatar
from otp.nametag.NametagConstants import *
from toontown.distributed.ToontownMsgTypes import *
from toontown.toon import LocalToon
from toontown.toon import Toon
from toontown.toon import ToonDNA
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TTDialog

class MakeAToon(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('MakeAToon')

    def __init__(self, parentFSM, avList, doneEvent, index):
        StateData.StateData.__init__(self, doneEvent)
        self.dna = None
        self.progressing = 0
        self.toonPosition = Point3(-1.62, -3.49, 0)
        self.toonScale = Point3(1, 1, 1)
        self.toonHpr = Point3(180, 0, 0)
        self.leftTime = 1.6
        self.rightTime = 1
        self.visitedGenderShop = False
        self.warp = 0
        for av in avList:
            if av.position == index:
                self.warp = 1
                self.namelessPotAv = av

        self.fsm = ClassicFSM.ClassicFSM('MakeAToon', [State.State('Init', self.enterInit, self.exitInit, ['GenderShop', 'NameShop']),
         State.State('GenderShop', self.enterGenderShop, self.exitGenderShop, ['BodyShop']),
         State.State('BodyShop', self.enterBodyShop, self.exitBodyShop, ['GenderShop', 'ColorShop']),
         State.State('ColorShop', self.enterColorShop, self.exitColorShop, ['BodyShop', 'ClothesShop']),
         State.State('ClothesShop', self.enterClothesShop, self.exitClothesShop, ['ColorShop', 'ChallengeShop']),
         State.State('ChallengeShop', self.enterChallengeShop, self.exitChallengeShop, ['ClothesShop', 'NameShop']),
         State.State('NameShop', self.enterNameShop, self.exitNameShop, ['ChallengeShop', 'Done']),
         State.State('Done', self.enterDone, self.exitDone, [])], 'Init', 'Done')
        self.parentFSM = parentFSM
        self.parentFSM.getStateNamed('createAvatar').addChild(self.fsm)
        self.gs = GenderShop.GenderShop(self, 'GenderShop-done')
        self.bs = BodyShop.BodyShop('BodyShop-done')
        self.cos = ColorShop.ColorShop('ColorShop-done')
        self.cls = MakeClothesGUI.MakeClothesGUI('ClothesShop-done')
        self.chs = ChallengeShop.ChallengeShop('ChallengeShop-done')
        self.ns = NameShop.NameShop(self, 'NameShop-done', avList, index)
        self.shop = GENDERSHOP
        self.music = None
        self.soundBack = None
        self.fsm.enterInitialState()
        self.hprDelta = -1
        self.dropIval = None
        self.roomSquishIval = None
        self.propSquishIval = None
        self.focusOutIval = None
        self.focusInIval = None
        self.toon = None
        return

    def getToon(self):
        return self.toon

    def enter(self):
        base.camLens.setMinFov(ToontownGlobals.MakeAToonCameraFov / (4.0 / 3.0))
        base.playMusic(self.music, looping=1, volume=self.musicVolume)
        camera.setPosHpr(-5.7, -12.3501, 2.15, -24.8499, 2.73, 0)
        if self.warp:
            self.toon.reparentTo(render)
            self.toon.loop('neutral')
            self.toon.setScale(self.toonScale)
            self.spotlight.setPos(2, -1.95, 0.41)
            self.toon.setPos(Point3(1.5, -4, 0))
            self.toon.setH(120)
        self.guiTopBar.show()
        self.guiBottomBar.show()
        self.guiCancelButton.show()
        if self.warp:
            self.progressing = 0
            self.guiLastButton.hide()
            self.fsm.request('NameShop')
        else:
            self.fsm.request('GenderShop')

    def exit(self):
        base.camLens.setMinFov(settings['fov'] / (4.0 / 3.0))
        self.guiTopBar.hide()
        self.guiBottomBar.hide()
        self.music.stop()
        self.fsm.request('Done')
        self.room.reparentTo(hidden)

    def load(self):
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        gui.flattenMedium()
        guiAcceptUp = gui.find('**/tt_t_gui_mat_okUp')
        guiAcceptUp.flattenStrong()
        guiAcceptDown = gui.find('**/tt_t_gui_mat_okDown')
        guiAcceptDown.flattenStrong()
        guiCancelUp = gui.find('**/tt_t_gui_mat_closeUp')
        guiCancelUp.flattenStrong()
        guiCancelDown = gui.find('**/tt_t_gui_mat_closeDown')
        guiCancelDown.flattenStrong()
        guiNextUp = gui.find('**/tt_t_gui_mat_nextUp')
        guiNextUp.flattenStrong()
        guiNextDown = gui.find('**/tt_t_gui_mat_nextDown')
        guiNextDown.flattenStrong()
        guiNextDisabled = gui.find('**/tt_t_gui_mat_nextDisabled')
        guiNextDisabled.flattenStrong()
        skipTutorialUp = gui.find('**/tt_t_gui_mat_skipUp')
        skipTutorialUp.flattenStrong()
        skipTutorialDown = gui.find('**/tt_t_gui_mat_skipDown')
        skipTutorialDown.flattenStrong()
        rotateUp = gui.find('**/tt_t_gui_mat_arrowRotateUp')
        rotateUp.flattenStrong()
        rotateDown = gui.find('**/tt_t_gui_mat_arrowRotateDown')
        rotateDown.flattenStrong()
        self.guiTopBar = DirectFrame(relief=None, text=TTLocalizer.CreateYourToon, text_font=ToontownGlobals.getSignFont(), text_fg=(0.0, 0.65, 0.35, 1), text_scale=0.18, text_pos=(0, -0.03), pos=(0, 0, 0.86))
        self.guiTopBar.hide()
        self.guiBottomBar = DirectFrame(relief=None, image_scale=(1.25, 1, 1), pos=(0.01, 0, -0.86))
        self.guiBottomBar.hide()
        self.guiCheckButton = DirectButton(parent=self.guiBottomBar, relief=None, image=(guiAcceptUp,
         guiAcceptDown,
         guiAcceptUp,
         guiAcceptDown), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(1.165, 0, -0.018), command=self.__handleNext, text=('', TTLocalizer.MakeAToonDone, TTLocalizer.MakeAToonDone), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_align=TextNode.ARight, text_pos=(0.075, 0.13), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.guiCheckButton.setPos(-0.13, 0, 0.13)
        self.guiCheckButton.reparentTo(base.a2dBottomRight)
        self.guiCheckButton.hide()
        self.guiCancelButton = DirectButton(parent=self.guiBottomBar, relief=None, image=(guiCancelUp,
         guiCancelDown,
         guiCancelUp,
         guiCancelDown), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-1.179, 0, -0.011), command=self.__handleCancel, text=('', TTLocalizer.MakeAToonCancel, TTLocalizer.MakeAToonCancel), text_font=ToontownGlobals.getInterfaceFont(), text_scale=TTLocalizer.MATguiCancelButton, text_pos=(0, 0.115), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.guiCancelButton.setPos(0.13, 0, 0.13)
        self.guiCancelButton.reparentTo(base.a2dBottomLeft)
        self.guiCancelButton.hide()
        self.guiNextButton = DirectButton(parent=self.guiBottomBar, relief=None, image=(guiNextUp,
         guiNextDown,
         guiNextUp,
         guiNextDisabled), image_scale=(0.3, 0.3, 0.3), image1_scale=(0.35, 0.35, 0.35), image2_scale=(0.35, 0.35, 0.35), pos=(1.165, 0, -0.018), command=self.__handleNext, text=('',
         TTLocalizer.MakeAToonNext,
         TTLocalizer.MakeAToonNext,
         ''), text_font=ToontownGlobals.getInterfaceFont(), text_scale=TTLocalizer.MATguiNextButton, text_pos=(0, 0.115), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.guiNextButton.setPos(-0.13, 0, 0.13)
        self.guiNextButton.reparentTo(base.a2dBottomRight)
        self.guiNextButton.hide()
        self.guiLastButton = DirectButton(parent=self.guiBottomBar, relief=None, image=(guiNextUp,
         guiNextDown,
         guiNextUp,
         guiNextDown), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), image_scale=(-0.3, 0.3, 0.3), image1_scale=(-0.35, 0.35, 0.35), image2_scale=(-0.35, 0.35, 0.35), pos=(0.825, 0, -0.018), command=self.__handleLast, text=('',
         TTLocalizer.MakeAToonLast,
         TTLocalizer.MakeAToonLast,
         ''), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_pos=(0, 0.115), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.guiLastButton.setPos(-0.37, 0, 0.13)
        self.guiLastButton.reparentTo(base.a2dBottomRight)
        self.guiLastButton.hide()
        self.rotateLeftButton = DirectButton(parent=self.guiBottomBar, relief=None, image=(rotateUp,
         rotateDown,
         rotateUp,
         rotateDown), image_scale=(-0.4, 0.4, 0.4), image1_scale=(-0.5, 0.5, 0.5), image2_scale=(-0.5, 0.5, 0.5), pos=(-0.355, 0, 0.36))
        self.rotateLeftButton.flattenMedium()
        self.rotateLeftButton.reparentTo(base.a2dBottomCenter)
        self.rotateLeftButton.hide()
        self.rotateLeftButton.bind(DGG.B1PRESS, self.rotateToonLeft)
        self.rotateLeftButton.bind(DGG.B1RELEASE, self.stopToonRotateLeftTask)
        self.rotateRightButton = DirectButton(parent=self.guiBottomBar, relief=None, image=(rotateUp,
         rotateDown,
         rotateUp,
         rotateDown), image_scale=(0.4, 0.4, 0.4), image1_scale=(0.5, 0.5, 0.5), image2_scale=(0.5, 0.5, 0.5), pos=(0.355, 0, 0.36))
        self.rotateRightButton.flattenStrong()
        self.rotateRightButton.reparentTo(base.a2dBottomCenter)
        self.rotateRightButton.hide()
        self.rotateRightButton.bind(DGG.B1PRESS, self.rotateToonRight)
        self.rotateRightButton.bind(DGG.B1RELEASE, self.stopToonRotateRightTask)
        gui.removeNode()
        self.roomDropActor = Actor()
        self.roomDropActor.loadModel('phase_3/models/makeatoon/roomAnim_model')
        self.roomDropActor.loadAnims({'drop': 'phase_3/models/makeatoon/roomAnim_roomDrop'})
        self.roomDropActor.reparentTo(render)
        self.dropJoint = self.roomDropActor.find('**/droppingJoint')
        self.roomSquishActor = Actor()
        self.roomSquishActor.loadModel('phase_3/models/makeatoon/roomAnim_model')
        self.roomSquishActor.loadAnims({'squish': 'phase_3/models/makeatoon/roomAnim_roomSquish'})
        self.roomSquishActor.reparentTo(render)
        self.squishJoint = self.roomSquishActor.find('**/scalingJoint')
        self.propSquishActor = Actor()
        self.propSquishActor.loadModel('phase_3/models/makeatoon/roomAnim_model')
        self.propSquishActor.loadAnims({'propSquish': 'phase_3/models/makeatoon/roomAnim_propSquish'})
        self.propSquishActor.reparentTo(render)
        self.propSquishActor.pose('propSquish', 0)
        self.propJoint = self.propSquishActor.find('**/propJoint')
        self.spotlightActor = Actor()
        self.spotlightActor.loadModel('phase_3/models/makeatoon/roomAnim_model')
        self.spotlightActor.loadAnims({'spotlightShake': 'phase_3/models/makeatoon/roomAnim_spotlightShake'})
        self.spotlightActor.reparentTo(render)
        self.spotlightJoint = self.spotlightActor.find('**/spotlightJoint')
        self.room = loader.loadModel('phase_3/models/makeatoon/tt_m_ara_mat_room')
        self.room.flattenMedium()
        self.genderWalls = self.room.find('**/genderWalls')
        self.genderWalls.flattenStrong()
        self.genderProps = self.room.find('**/genderProps')
        self.genderProps.flattenStrong()
        self.bodyWalls = self.room.find('**/bodyWalls')
        self.bodyWalls.flattenStrong()
        self.bodyProps = self.room.find('**/bodyProps')
        self.bodyProps.flattenStrong()
        self.colorWalls = self.room.find('**/colorWalls')
        self.colorWalls.flattenStrong()
        self.colorProps = self.room.find('**/colorProps')
        self.colorProps.flattenStrong()
        self.clothesWalls = self.room.find('**/clothWalls')
        self.clothesWalls.flattenMedium()
        self.clothesProps = self.room.find('**/clothProps')
        self.clothesProps.flattenMedium()
        self.nameWalls = self.room.find('**/nameWalls')
        self.nameWalls.flattenStrong()
        self.nameProps = self.room.find('**/nameProps')
        self.nameProps.flattenStrong()
        self.background = self.room.find('**/background')
        self.background.flattenStrong()
        self.background.reparentTo(render)
        self.floor = self.room.find('**/floor')
        self.floor.flattenStrong()
        self.floor.reparentTo(render)
        self.spotlight = self.room.find('**/spotlight')
        self.spotlight.reparentTo(self.spotlightJoint)
        self.spotlight.setColor(1, 1, 1, 0.3)
        self.spotlight.setPos(1.18, -1.27, 0.41)
        self.spotlight.setScale(2.6)
        self.spotlight.setHpr(0, 0, 0)
        smokeSeqNode = SequenceNode('smoke')
        smokeModel = loader.loadModel('phase_3/models/makeatoon/tt_m_ara_mat_smoke')
        smokeFrameList = list(smokeModel.findAllMatches('**/smoke_*'))
        smokeFrameList.reverse()
        for smokeFrame in smokeFrameList:
            smokeSeqNode.addChild(smokeFrame.node())

        smokeSeqNode.setFrameRate(12)
        self.smoke = render.attachNewNode(smokeSeqNode)
        self.smoke.setScale(1, 1, 0.75)
        self.smoke.hide()
        if self.warp:
            self.dna = ToonDNA.ToonDNA()
            self.dna.makeFromNetString(self.namelessPotAv.dna)
            self.toon = Toon.Toon()
            self.toon.setDNA(self.dna)
            self.toon.setNameVisible(0)
            self.toon.startBlink()
            self.toon.startLookAround()
        self.gs.load()
        self.bs.load()
        self.cos.load()
        self.cls.load()
        self.ns.load()
        self.music = loader.loadMusic('phase_3/audio/bgm/create_a_toon.ogg')
        self.musicVolume = config.GetFloat('makeatoon-music-volume', 1)
        self.sfxVolume = 0.4
        self.soundBack = loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_back.ogg')
        self.crashSounds = map(loader.loadSfx, ['phase_3/audio/sfx/tt_s_ara_mat_crash_boing.ogg',
         'phase_3/audio/sfx/tt_s_ara_mat_crash_glassBoing.ogg',
         'phase_3/audio/sfx/tt_s_ara_mat_crash_wood.ogg',
         'phase_3/audio/sfx/tt_s_ara_mat_crash_woodBoing.ogg',
         'phase_3/audio/sfx/tt_s_ara_mat_crash_woodGlass.ogg'])
        return

    def unload(self):
        self.exit()
        if self.toon:
            self.toon.stopBlink()
            self.toon.stopLookAroundNow()
        self.gs.unload()
        self.bs.unload()
        self.cos.unload()
        self.cls.unload()
        self.chs.unload()
        self.ns.unload()
        del self.gs
        del self.bs
        del self.cos
        del self.cls
        del self.chs
        del self.ns
        self.guiTopBar.destroy()
        self.guiBottomBar.destroy()
        self.guiCancelButton.destroy()
        self.guiCheckButton.destroy()
        self.guiNextButton.destroy()
        self.guiLastButton.destroy()
        self.rotateLeftButton.destroy()
        self.rotateRightButton.destroy()
        del self.guiTopBar
        del self.guiBottomBar
        del self.guiCancelButton
        del self.guiCheckButton
        del self.guiNextButton
        del self.guiLastButton
        del self.rotateLeftButton
        del self.rotateRightButton
        del self.music
        del self.soundBack
        del self.dna
        if self.toon:
            self.toon.delete()
        del self.toon
        self.cleanupDropIval()
        self.cleanupRoomSquishIval()
        self.cleanupPropSquishIval()
        self.cleanupFocusInIval()
        self.cleanupFocusOutIval()
        self.room.removeNode()
        del self.room
        self.genderWalls.removeNode()
        self.genderProps.removeNode()
        del self.genderWalls
        del self.genderProps
        self.bodyWalls.removeNode()
        self.bodyProps.removeNode()
        del self.bodyWalls
        del self.bodyProps
        self.colorWalls.removeNode()
        self.colorProps.removeNode()
        del self.colorWalls
        del self.colorProps
        self.clothesWalls.removeNode()
        self.clothesProps.removeNode()
        del self.clothesWalls
        del self.clothesProps
        self.nameWalls.removeNode()
        self.nameProps.removeNode()
        del self.nameWalls
        del self.nameProps
        self.background.removeNode()
        del self.background
        self.floor.removeNode()
        del self.floor
        self.spotlight.removeNode()
        del self.spotlight
        self.smoke.removeNode()
        del self.smoke
        while len(self.crashSounds):
            del self.crashSounds[0]

        self.parentFSM.getStateNamed('createAvatar').removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.ignoreAll()
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def __handleBodyShop(self):
        self.fsm.request('BodyShop')

    def __handleClothesShop(self):
        self.fsm.request('ClothesShop')

    def __handleColorShop(self):
        self.fsm.request('ColorShop')

    def __handleNameShop(self):
        self.fsm.request('NameShop')

    def __handleCancel(self):
        self.doneStatus = 'cancel'
        base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent))

    def goToNextShop(self):
        self.progressing = 1
        if self.shop == GENDERSHOP:
            self.fsm.request('BodyShop')
        elif self.shop == BODYSHOP:
            self.fsm.request('ColorShop')
        elif self.shop == COLORSHOP:
            self.fsm.request('ClothesShop')
        elif self.shop == CLOTHESSHOP:
            self.fsm.request('ChallengeShop')
        else:
            self.fsm.request('NameShop')

    def goToLastShop(self):
        self.progressing = 0
        if self.shop == BODYSHOP:
            self.fsm.request('GenderShop')
        elif self.shop == COLORSHOP:
            self.fsm.request('BodyShop')
        elif self.shop == CLOTHESSHOP:
            self.fsm.request('ColorShop')
        elif self.shop == CHALLENGESHOP:
            self.fsm.request('ClothesShop')
        else:
            self.fsm.request('ChallengeShop')

    def enterInit(self):
        pass

    def exitInit(self):
        pass

    def enterGenderShop(self):
        self.shop = GENDERSHOP
        if not self.visitedGenderShop:
            self.visitedGenderShop = True
            self.genderWalls.reparentTo(self.squishJoint)
            self.genderProps.reparentTo(self.propJoint)
            self.roomSquishActor.pose('squish', 0)
            self.guiNextButton['state'] = DGG.DISABLED
        else:
            self.dropRoom(self.genderWalls, self.genderProps)
        self.guiTopBar['text'] = TTLocalizer.CreateYourToonTitle
        self.guiTopBar['text_fg'] = (1, 0.92, 0.2, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterGenderShop
        base.transitions.fadeIn()
        self.accept('GenderShop-done', self.__handleGenderShopDone)
        self.gs.enter()
        self.guiNextButton.show()
        self.gs.showButtons()
        self.rotateLeftButton.hide()
        self.rotateRightButton.hide()
        if self.toon:
            self.toon.setHpr(self.toonHpr)

    def exitGenderShop(self):
        self.squishRoom(self.genderWalls)
        self.squishProp(self.genderProps)
        self.gs.exit()
        self.ignore('GenderShop-done')

    def __handleGenderShopDone(self):
        self.guiNextButton.hide()
        self.gs.hideButtons()
        self.goToNextShop()

    def enterBodyShop(self):
        self.toon.show()
        self.shop = BODYSHOP
        self.guiTopBar['text'] = TTLocalizer.ShapeYourToonTitle
        self.guiTopBar['text_fg'] = (0.0, 0.98, 0.5, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterBodyShop
        self.accept('BodyShop-done', self.__handleBodyShopDone)
        self.dropRoom(self.bodyWalls, self.bodyProps)
        self.colorShopOpening()
        self.bs.enter(self.toon)

    def exitBodyShop(self):
        self.squishRoom(self.bodyWalls)
        self.squishProp(self.bodyProps)
        self.bs.exit()
        self.ignore('BodyShop-done')

    def __handleBodyShopDone(self):
        self.guiNextButton.hide()
        self.guiLastButton.hide()
        if self.bs.doneStatus == 'next':
            self.goToNextShop()
        else:
            self.goToLastShop()

    def colorShopOpening(self):
        self.guiNextButton.show()
        self.guiLastButton.show()
        self.rotateLeftButton.show()
        self.rotateRightButton.show()

    def enterColorShop(self):
        self.shop = COLORSHOP
        self.guiTopBar['text'] = TTLocalizer.PaintYourToonTitle
        self.guiTopBar['text_fg'] = (0, 1, 1, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterColorShop
        self.accept('ColorShop-done', self.__handleColorShopDone)
        self.dropRoom(self.colorWalls, self.colorProps)
        self.toon.setPos(self.toonPosition)
        self.colorShopOpening()
        self.cos.enter(self.toon)

    def exitColorShop(self):
        self.squishRoom(self.colorWalls)
        self.squishProp(self.colorProps)
        self.cos.exit()
        self.ignore('ColorShop-done')

    def __handleColorShopDone(self):
        self.guiNextButton.hide()
        self.guiLastButton.hide()
        if self.cos.doneStatus == 'next':
            self.goToNextShop()
        else:
            self.goToLastShop()

    def clothesShopOpening(self):
        self.guiNextButton.show()
        self.guiLastButton.show()
        self.cls.showButtons()
        self.rotateLeftButton.show()
        self.rotateRightButton.show()

    def enterClothesShop(self):
        self.shop = CLOTHESSHOP
        self.guiTopBar['text'] = TTLocalizer.PickClothesTitle
        self.guiTopBar['text_fg'] = (1, 0.92, 0.2, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterClothesShop
        self.accept('ClothesShop-done', self.__handleClothesShopDone)
        self.dropRoom(self.clothesWalls, self.clothesProps)
        self.toon.setScale(self.toonScale)
        self.toon.setPos(self.toonPosition)
        if not self.progressing:
            self.toon.setHpr(self.toonHpr)
        self.clothesShopOpening()
        self.cls.enter(self.toon)

    def exitClothesShop(self):
        self.squishRoom(self.clothesWalls)
        self.squishProp(self.clothesProps)
        self.cls.exit()
        self.ignore('ClothesShop-done')

    def __handleClothesShopDone(self):
        self.guiNextButton.hide()
        self.guiLastButton.hide()
        if self.cls.doneStatus == 'next':
            self.cls.hideButtons()
            self.goToNextShop()
        else:
            self.cls.hideButtons()
            self.goToLastShop()

    def challengeShopOpening(self):
        self.guiNextButton.show()
        self.guiLastButton.show()

    def enterChallengeShop(self):
        self.shop = CHALLENGESHOP
        self.guiTopBar['text'] = TTLocalizer.PickChallengeTitle
        self.guiTopBar['text_fg'] = (0.258, 0.525, 0.95, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterChallengeShop
        self.accept('ChallengeShop-done', self.__handleChallengeShopDone)
        self.dropRoom(self.genderWalls, self.genderProps)
        self.toon.setScale(self.toonScale)
        self.toon.setPos(self.toonPosition)
        if not self.progressing:
            self.toon.setHpr(self.toonHpr)
        self.rotateLeftButton.show()
        self.rotateRightButton.show()
        self.challengeShopOpening()
        self.chs.enter(self.toon)

    def exitChallengeShop(self):
        self.squishRoom(self.genderWalls)
        self.squishProp(self.genderProps)
        self.chs.exit()
        self.ignore('ChallengeShop-done')

    def __handleChallengeShopDone(self):
        self.guiNextButton.hide()
        self.guiLastButton.hide()
        if self.chs.doneStatus == 'next':
            self.goToNextShop()
        else:
            self.goToLastShop()

    def nameShopOpening(self, task):
        self.guiCheckButton.show()
        self.guiLastButton.show()
        if self.warp:
            self.guiLastButton.hide()
        return Task.done

    def enterNameShop(self):
        self.shop = NAMESHOP
        self.guiTopBar['text'] = TTLocalizer.NameToonTitle
        self.guiTopBar['text_fg'] = (0.0, 0.98, 0.5, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterNameShop
        self.accept('NameShop-done', self.__handleNameShopDone)
        self.dropRoom(self.nameWalls, self.nameProps)
        self.spotlight.setPos(2, -1.95, 0.41)
        self.toon.setPos(Point3(1.5, -4, 0))
        self.toon.setH(120)
        self.rotateLeftButton.hide()
        self.rotateRightButton.hide()
        if self.progressing:
            waittime = self.leftTime
        else:
            waittime = 0.2
        self.ns.enter(self.toon, self.warp)
        taskMgr.doMethodLater(waittime, self.nameShopOpening, 'nameShopOpeningTask')

    def exitNameShop(self):
        self.squishRoom(self.nameWalls)
        self.squishProp(self.nameProps)
        self.spotlight.setPos(1.18, -1.27, 0.41)
        self.ns.exit()
        self.ignore('NameShop-done')
        taskMgr.remove('nameShopOpeningTask')

    def rejectName(self):
        self.ns.rejectName(TTLocalizer.RejectNameText)

    def __handleNameShopDone(self):
        self.guiLastButton.hide()
        self.guiCheckButton.hide()
        if self.ns.getDoneStatus() == 'last':
            self.ns.hideAll()
            self.goToLastShop()
        else:
            self.doneStatus = 'created'
            base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent))

    def __handleNext(self):
        if self.fsm.getCurrentState().getName() == 'ChallengeShop' and not self.chs.checkChallenges():
            return
        messenger.send('next')

    def __handleLast(self):
        messenger.send('last')

    def __handleSkipTutorial(self):
        messenger.send('skipTutorial')

    def enterDone(self):
        pass

    def exitDone(self):
        pass

    def squishRoom(self, room):
        if self.roomSquishIval and self.roomSquishIval.isPlaying():
            self.roomSquishIval.finish()
        squishDuration = self.roomSquishActor.getDuration('squish')
        self.roomSquishIval = Sequence(Func(self.roomSquishActor.play, 'squish'), Wait(squishDuration), Func(room.hide))
        self.roomSquishIval.start()

    def squishProp(self, prop):
        if not prop.isEmpty():
            if self.propSquishIval and self.propSquishIval.isPlaying():
                self.propSquishIval.finish()
            squishDuration = self.propSquishActor.getDuration('propSquish')
            self.propSquishIval = Sequence(Func(self.propSquishActor.play, 'propSquish'), Wait(squishDuration), Func(prop.hide))
            self.propSquishIval.start()

    def dropRoom(self, walls, props):

        def propReparentTo(props):
            if not props.isEmpty():
                props.reparentTo(self.propJoint)

        if self.dropIval and self.dropIval.isPlaying():
            self.dropIval.finish()
        walls.reparentTo(self.dropJoint)
        walls.show()
        if not props.isEmpty():
            props.reparentTo(self.dropJoint)
            props.show()
        dropDuration = self.roomDropActor.getDuration('drop')
        self.dropIval = Parallel(Sequence(Func(self.roomDropActor.play, 'drop'), Wait(dropDuration), Func(walls.reparentTo, self.squishJoint), Func(propReparentTo, props), Func(self.propSquishActor.pose, 'propSquish', 0), Func(self.roomSquishActor.pose, 'squish', 0)), Sequence(Wait(0.25), Func(self.smoke.show), Func(self.smoke.node().play), LerpColorScaleInterval(self.smoke, 0.5, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1)), Func(self.smoke.hide)), Func(self.spotlightActor.play, 'spotlightShake'), Func(self.playRandomCrashSound))
        self.dropIval.start()

    def startFocusOutIval(self):
        if self.focusInIval.isPlaying():
            self.focusInIval.pause()
        if not self.focusOutIval.isPlaying():
            self.focusOutIval = LerpScaleInterval(self.spotlight, 0.25, self.spotlightFinalScale)
            self.focusOutIval.start()

    def startFocusInIval(self):
        if self.focusOutIval.isPlaying():
            self.focusOutIval.pause()
        if not self.focusInIval.isPlaying():
            self.focusInIval = LerpScaleInterval(self.spotlight, 0.25, self.spotlightOriginalScale)
            self.focusInIval.start()

    def cleanupFocusOutIval(self):
        if self.focusOutIval:
            self.focusOutIval.finish()
            del self.focusOutIval

    def cleanupFocusInIval(self):
        if self.focusInIval:
            self.focusInIval.finish()
            del self.focusInIval

    def cleanupDropIval(self):
        if self.dropIval:
            self.dropIval.finish()
            del self.dropIval

    def cleanupRoomSquishIval(self):
        if self.roomSquishIval:
            self.roomSquishIval.finish()
            del self.roomSquishIval

    def cleanupPropSquishIval(self):
        if self.propSquishIval:
            self.propSquishIval.finish()
            del self.propSquishIval

    def setToon(self, toon):
        self.toon = toon

    def setNextButtonState(self, state):
        self.guiNextButton['state'] = state

    def playRandomCrashSound(self):
        index = random.randint(0, len(self.crashSounds) - 1)
        base.playSfx(self.crashSounds[index], volume=self.sfxVolume)

    def rotateToonLeft(self, event):
        taskMgr.add(self.rotateToonLeftTask, 'rotateToonLeftTask')

    def rotateToonLeftTask(self, task):
        self.toon.setH(self.toon.getH() + self.hprDelta)
        return task.cont

    def stopToonRotateLeftTask(self, event):
        taskMgr.remove('rotateToonLeftTask')

    def rotateToonRight(self, event):
        taskMgr.add(self.rotateToonRightTask, 'rotateToonRightTask')

    def rotateToonRightTask(self, task):
        self.toon.setH(self.toon.getH() - self.hprDelta)
        return task.cont

    def stopToonRotateRightTask(self, event):
        taskMgr.remove('rotateToonRightTask')