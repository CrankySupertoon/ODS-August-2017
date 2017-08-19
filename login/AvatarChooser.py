# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.login.AvatarChooser
from panda3d.core import GeomNode
from direct.interval.IntervalGlobal import *
from direct.fsm.StateData import StateData
from direct.gui.DirectGui import *
from otp.avatar import Emote
from otp.otpbase import OTPGlobals, OTPLocalizer
from otp.nametag import NametagGroup, NametagGlobals
from toontown.safezone import SZUtil
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toon import NPCToons, Toon, ToonDNA, TTEmote
from toontown.estate import HouseGlobals
import random, time

class AvatarChooser(StateData):

    def __init__(self, avList, doneEvent):
        StateData.__init__(self, doneEvent)
        self.avList = avList
        self.doneEvent = doneEvent
        self.loaded = False
        self.specialToon = None
        self.playground = random.choice(ToontownGlobals.LOGIN_SCREEN_SZ.keys())
        return

    def getRandomDNA(self, color):
        color = HouseGlobals.houseColors[color]
        dna = ToonDNA.ToonDNA()
        dna.newToonRandomColor(0, [0,
         color,
         0,
         color,
         0,
         color])
        return dna

    def getAvatar(self, position):
        if self.specialToon:
            return self.specialToon
        for av in self.avList:
            if av.position == position:
                return av

    def enter(self):
        self.toonIndex = -1
        self.deletedIndex = -1
        self.deletedToons = []
        self.load()
        camera.setHpr(*self.cameraPos[3:6])
        base.applyMinAspectRatio(self.minAspectRatio)
        allToons = self.toons + self.deletedToons + self.emptyToons.values()
        for element in [self.title,
         self.quitButton,
         self.playgroundNode,
         self.sky] + allToons:
            if element:
                element.show()

        self.__setDeletedAvatars()
        Sequence(camera.posInterval(1.5, self.cameraPos[0:3], self.cameraPos[6:9], blendType='easeInOut'), Func(NametagGlobals.setMasterNametagsActive, True)).start()

    def exit(self):
        if not self.loaded:
            return
        self.ignoreAll()
        self.hideAll()
        base.unapplyMinAspectRatio()

    def unload(self):
        if not self.loaded:
            return
        self.ignoreAll()
        self.loaded = False
        for element in [self.playgroundNode,
         self.sky,
         self.snowRender,
         self.title,
         self.quitButton,
         self.backButton,
         self.deleteButton,
         self.lastButton,
         self.nextButton,
         self.playLabel,
         self.nameLabel,
         self.passwordEntry,
         self.passwordButton,
         self.popup]:
            if element:
                element.removeNode()

        for toon in self.toons:
            if toon:
                toon.delete()

        if self.snow:
            self.snow.cleanup()
        self.toons = []
        self.deleteDeletedToons()
        self.deleteEmptyToons()

    def load(self):
        if self.loaded:
            return
        else:
            self.toons = [None] * 6
            matGui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
            gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
            arrowImage = [ matGui.find('**/tt_t_gui_mat_next' + name) for name in ('Up', 'Down', 'Up', 'Down') ]
            cancelImage = [ matGui.find('**/tt_t_gui_mat_close' + name) for name in ('Up', 'Down', 'Up', 'Down') ]
            self.cameraPos, self.toonPos, self.minAspectRatio, removedElements = ToontownGlobals.LOGIN_SCREEN_SZ[self.playground]
            self.dnaStore, self.playgroundNode, self.sky, self.snow, self.snowRender = SZUtil.loadPlayground(self.playground)
            self.title = OnscreenText(TTLocalizer.AvatarChooserPickAToon, scale=TTLocalizer.ACtitle, font=ToontownGlobals.getSignFont(), fg=(1, 0.9, 0.1, 1), pos=(0.0, 0.82))
            self.quitButton = DirectButton(base.a2dBottomRight, image=gui.find('**/QuitBtn_RLVR'), relief=None, text=TTLocalizer.AvatarChooserQuit, text_font=ToontownGlobals.getSignFont(), text_fg=(0.977, 0.816, 0.133, 1), text_pos=TTLocalizer.ACquitButtonPos, text_scale=TTLocalizer.ACquitButton, image_scale=1, scale=1.05, pos=(-0.25, 0, 0.075), command=self.__handleQuit)
            self.backButton = DirectButton(base.a2dBottomLeft, relief=None, image=cancelImage, image_scale=0.9, pos=(0.15, 0, 0.15), text=('',
             TTLocalizer.MakeAToonLast,
             TTLocalizer.MakeAToonLast,
             ''), text_fg=(1, 1, 1, 1), text_scale=0.1, text_shadow=(0, 0, 0, 1), text_pos=(0, 0.15), command=self.__panBack)
            self.deleteButton = DirectButton(base.a2dBottomLeft, relief=None, image=Preloaded['trashcan'], image_scale=0.9, pos=(0.5, 0, 0.2), text=('',
             '',
             TTLocalizer.AvatarChoiceDelete,
             TTLocalizer.AvatarChoiceDelete), text_fg=(1, 1, 1, 1), text_scale=0.13, text_shadow=(0, 0, 0, 1), text_pos=(0, -0.1), command=self.__delete)
            self.lastButton = DirectButton(base.a2dBottomRight, relief=None, image=arrowImage, image_scale=(-0.5, 0.5, 0.5), pos=(-0.45, 0, 0.15), text=('',
             TTLocalizer.LastCheckBox,
             TTLocalizer.LastCheckBox,
             ''), text_scale=0.11, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, 0.15), command=self.__panToon, extraArgs=[-1])
            self.nextButton = DirectButton(base.a2dBottomRight, relief=None, image=arrowImage, image_scale=0.5, pos=(-0.15, 0, 0.15), text=('',
             TTLocalizer.lNext,
             TTLocalizer.lNext,
             ''), text_scale=0.11, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, 0.15), command=self.__panToon, extraArgs=[1])
            self.playLabel = DirectLabel(relief=6, frameColor=(0, 0, 0, 0.5), text=TTLocalizer.MinigameRulesPanelPlay, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.11, text_font=ToontownGlobals.getMinnieFont(), pos=(0, 0, -0.3))
            self.nameLabel = DirectButton(relief=None, pressEffect=None, clickSound=None, pos=(0.8, 0, -0.25), text=TTLocalizer.AvatarChooserRename, text_wordwrap=10, text_scale=0.11, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
            self.leftButton = DirectButton(relief=None, image=Preloaded['fatYellowArrow'], image_scale=(-1, 1, 1), pos=(-0.5, 0, -0.265), command=self.__increaseRecoverIndex, extraArgs=[-1])
            self.rightButton = DirectButton(relief=None, image=Preloaded['fatYellowArrow'], pos=(0.5, 0, -0.265), command=self.__increaseRecoverIndex, extraArgs=[1])
            self.passwordEntry = None
            self.passwordButton = None
            self.popup = None
            for element in removedElements:
                self.playgroundNode.find(element).removeNode()

            self.playgroundNode.reparentTo(render)
            for av in self.avList:
                self.createToonByDNA(av.name, av.dna, av.position)

            self.emptyToons = {index:self.createRandomToon(index) for index in xrange(6) if not self.toons[index]}
            self.hideAll()
            matGui.removeNode()
            gui.removeNode()
            self.loaded = True
            return

    def hideAll(self):
        for element in [self.title,
         self.quitButton,
         self.playgroundNode,
         self.sky] + self.toons:
            if element and not element.isEmpty():
                element.hide()

        self.setToonVisibility(False)

    def deleteDeletedToons(self):
        for toon in self.deletedToons:
            toon.delete()

        self.deletedToons = []

    def deleteEmptyToons(self):
        for toon in self.emptyToons.values():
            toon.delete()

        self.emptyToons = {}

    def setToonVisibility(self, visible):
        for element in [self.backButton,
         self.deleteButton,
         self.lastButton,
         self.nextButton,
         self.playLabel,
         self.nameLabel,
         self.leftButton,
         self.rightButton]:
            if element:
                element.show() if visible else element.hide()

        NametagGlobals.setMasterNametagsActive(visible)

    def showToonGUI(self):
        self.setToonVisibility(True)
        self.title.show()
        base.transitions.noTransitions()
        self.nameLabel['text'] = ''
        self.nameLabel['command'] = None
        self.nameLabel['extraArgs'] = []
        av = self.getAvatar(self.toonIndex)
        if not av:
            self.decideRecoverButtons()
            self.deleteButton.hide()
            return
        else:
            if av.wantName:
                self.nameLabel['text'] = TTLocalizer.AvatarChooserReviewing % av.wantName
            elif av.approvedName:
                self.nameLabel['text'] = TTLocalizer.AvatarChooserAccepted % av.approvedName
            elif av.rejectedName:
                self.nameLabel['text'] = TTLocalizer.AvatarChooserRejected % av.rejectedName
            elif av.allowedName:
                self.nameLabel['text'] = TTLocalizer.AvatarChooserRename
                self.nameLabel['command'] = self.__playWithAnim
                self.nameLabel['extraArgs'] = ['create']
            self.playLabel['text'] = TTLocalizer.MinigameRulesPanelPlay
            self.deleteButton.show()
            self.leftButton.hide()
            self.rightButton.hide()
            return

    def createToon(self, name, dna, position, setToon = True):
        toon = Toon.Toon()
        toon.setName(name)
        toon.setPickable(True)
        toon.setPlayerType(NametagGroup.CCNormal)
        toon.setDNAString(dna.makeNetString())
        toon.animFSM.request('neutral')
        toon.reparentTo(render)
        toon.setPosHpr(*self.toonPos[position])
        toon.deleteShadowPlacer()
        self.accept(toon.nametag.getUniqueId(), self.__clickedNametag, [toon])
        if setToon:
            self.toons[position] = toon
        return toon

    def createToonByDNA(self, name, dna, position, setToon = True):
        return self.createToon(name, ToonDNA.ToonDNA(dna), position, setToon)

    def createRandomToon(self, position, setToon = True):
        return self.createToon(TTLocalizer.AvatarChooserNewToon, self.getRandomDNA(position), position, setToon)

    def transitionToToon(self, toon):
        pos = toon.getPos()
        hpr = toon.getHpr()
        h = hpr[0]
        if h in (-90, 270):
            pos[0] += 15.5
        elif h in (90,):
            pos[0] -= 15.5
        elif h in (0,):
            pos[1] += 15.5
        elif h in (180,):
            pos[1] -= 15.5
        pos[2] += toon.getHeight()
        hpr[0] -= 180
        self.toonIndex = self.toons.index(toon)
        self.setToonVisibility(False)
        self.load()
        Sequence(camera.posHprInterval(1.5, pos, hpr, blendType='easeInOut'), Func(self.showToonGUI)).start()

    def __panToon(self, offset):
        self.deletedIndex = -1
        self.decideRecoverToon()
        self.toonIndex += offset
        if self.toonIndex == 6:
            self.toonIndex = 0
        elif self.toonIndex == -1:
            self.toonIndex = 5
        self.transitionToToon(self.toons[self.toonIndex])

    def __panBack(self):
        self.deletedIndex = -1
        self.decideRecoverToon()
        self.toonIndex = -1
        self.setToonVisibility(False)
        Sequence(camera.posHprInterval(1.5, self.cameraPos[0:3], self.cameraPos[3:6], blendType='easeInOut'), Func(NametagGlobals.setMasterNametagsActive, True), Func(self.quitButton.show), Func(self.decideRecoverToon)).start()

    def __play(self, mode = None):
        if not mode:
            mode = 'chose' if self.getAvatar(self.toonIndex) else 'create'
        base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent, [mode]))

    def __playWithAnim(self, mode = None):
        self.setToonVisibility(False)
        self.title.hide()
        toon = self.toons[self.toonIndex]
        if not settings['patTransition']:
            self.__play(mode)
            return
        Sequence(toon.actorInterval('jump'), Func(toon.loop, 'neutral'), Wait(0.5), Func(toon.animFSM.request, 'TeleportOut'), Wait(3.5), Func(self.__play, mode)).start()

    def __clickedNametag(self, toon):
        NametagGlobals.setMasterNametagsActive(False)
        if toon in self.deletedToons:
            self.__recoverToon()
        elif self.toonIndex == self.toons.index(toon):
            self.__playWithAnim()
        else:
            self.quitButton.hide()
            self.transitionToToon(toon)

    def __delete(self):
        self.setToonVisibility(False)
        if len(base.cr.deletedAvList) >= OTPGlobals.MAX_DELETED_AVATARS:
            self.popup = TTDialog.TTDialog(style=TTDialog.Acknowledge, text_wordwrap=10, text=TTLocalizer.AvatarChooserCantDelete, command=self.__handleDeleteCancel)
            self.popup.show()
        else:
            self.title.hide()
            self.__openDelete()

    def __recoverToon(self):
        av = base.cr.deletedAvList[self.deletedIndex]
        secondsLeft = self.getSecondsLeft(av.position)
        base.transitions.noTransitions()
        self.setToonVisibility(False)
        if secondsLeft:
            self.popup = TTDialog.TTDialog(style=TTDialog.Acknowledge, text_wordwrap=17, text=TTLocalizer.AvatarChooserCantRecover % TTLocalizer.getHumanTime(secondsLeft, 5), command=self.__handleDeleteCancel)
            self.popup.show()
            return
        if not settings['patTransition']:
            self.unload()
            self.__actuallyRecover(av)
            return
        toon = self.deletedToons[self.deletedIndex]
        Sequence(toon.actorInterval('wave'), Func(toon.delete), Func(self.__actuallyRecover, av)).start()

    def __actuallyRecover(self, av):
        self.specialToon = av
        messenger.send(self.doneEvent, ['chose', [av.id, self.toonIndex]])

    def __openDelete(self):
        toonName = self.toons[self.toonIndex].name
        deleteText = TTLocalizer.AvatarChoiceDeleteConfirmText % {'name': toonName}
        gui = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        boxImage = loader.loadModel('phase_3/models/props/chatbox_input')
        okImage = [ gui.find('**/ChtBx_OKBtn_' + name) for name in ('UP', 'DN', 'Rllvr') ]
        cancelImage = [ gui.find('**/CloseBtn_' + name) for name in ('UP', 'DN', 'Rllvr') ]
        self.popup = DirectFrame(aspect2dp, relief=None, image=DGG.getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.4, 1.0, 1.0), pos=(0.0, 0.1, 0.2), text=deleteText, text_wordwrap=19, text_scale=TTLocalizer.ACdeleteWithPasswordFrame, text_pos=(0, 0.25), sortOrder=NO_FADE_SORT_INDEX)
        self.popup.hide()
        self.passwordEntry = DirectEntry(self.popup, relief=None, image=boxImage, image1_color=(0.8, 0.8, 0.8, 1.0), pos=(-0.45, 0.0, -0.2), scale=0.1, text_pos=(0, 0.7), text_scale=0.75, width=12, numLines=2, focus=1, cursorKeys=1, command=self.__handleDelete, extraArgs=[toonName])
        self.passwordButton = DirectButton(self.popup, image=okImage, relief=None, pos=(-0.22, 0.0, -0.35), text=TTLocalizer.AvatarChoiceDeletePasswordOK, text_scale=0.05, text_pos=(0.0, -0.1), command=self.__handleDelete, extraArgs=[None, toonName])
        DirectLabel(self.popup, relief=None, pos=(0, 0, 0.35), text=TTLocalizer.AvatarChoiceDeletePasswordTitle, text_scale=0.08)
        DirectButton(self.popup, relief=None, image=cancelImage, pos=(0.2, 0.0, -0.35), text=TTLocalizer.AvatarChoiceDeletePasswordCancel, text_scale=0.05, text_pos=(0.0, -0.1), command=self.__handleDeleteCancel)
        gui.removeNode()
        boxImage.removeNode()
        base.transitions.fadeScreen(0.5)
        self.popup.show()
        return

    def __handleDelete(self, passEntry, name):
        if self.passwordEntry.get().lower() != name.lower():
            self.popup['text'] = TTLocalizer.AvatarChoiceDeleteWrongConfirm % {'name': name}
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')
            return
        self.popup.destroy()
        taskMgr.doMethodLater(0.1, self.__handleDeletePopup, 'deletePopup')

    def __handleDeletePopup(self, task = None):
        self.popup = TTDialog.TTDialog(style=TTDialog.YesNo, text_wordwrap=23, text=TTLocalizer.AvatarChooserDeleteConfirm, command=self.__handleDeleteConfirm)
        self.popup.show()

    def __handleDeleteConfirm(self, value):
        base.transitions.noTransitions()
        self.popup.destroy()
        if value <= 0:
            self.showToonGUI()
            return
        toon = self.toons[self.toonIndex]
        if not settings['patTransition']:
            self.unload()
            messenger.send(self.doneEvent, ['delete'])
            return
        randomToon = self.createRandomToon(self.toonIndex, False)
        randomToon.hide()
        emoteSeq = Emote.globalEmote.doEmote(toon, TTEmote.Emotes.index('cry'), 0, start=False)[0]
        seq = Sequence(Parallel(emoteSeq, toon.doToonGhostColorScale((1, 1, 1, 0), 3.5), toon.nametag3d.colorScaleInterval(3.5, (1, 1, 1, 0), (1, 1, 1, 1))), Func(toon.hide), Wait(0.5), Func(randomToon.show), Func(randomToon.animFSM.request, 'TeleportIn'), Wait(1.65), Func(randomToon.animFSM.request, 'neutral'), Wait(1), Func(randomToon.delete), Func(self.__resetBackButton), Func(messenger.send, self.doneEvent, ['delete']))
        self.backButton['command'] = self.__cancelDelete
        self.backButton['extraArgs'] = [emoteSeq,
         seq,
         toon,
         randomToon]
        self.backButton.show()
        seq.start()

    def __resetBackButton(self):
        self.backButton['extraArgs'] = []
        self.backButton['command'] = self.__panBack
        self.backButton.hide()

    def __cancelDelete(self, emoteSequence, sequence, toon, randomToon):
        emoteSequence.finish()
        sequence.pause()
        randomToon.delete()
        toon.getGeomNode().clearColorScale()
        toon.nametag3d.clearColorScale()
        toon.getGeomNode().show()
        toon.loop('neutral')
        toon.show()
        self.__resetBackButton()
        self.showToonGUI()

    def __handleDeleteCancel(self, value = None):
        self.popup.destroy()
        self.showToonGUI()

    def __handleQuit(self):
        messenger.send(self.doneEvent, ['exit'])

    def __setDeletedAvatars(self):
        self.deleteDeletedToons()
        self.deletedIndex = -1
        self.deletedToons = []
        for av in base.cr.deletedAvList:
            toon = self.createToonByDNA(av.name, av.dna, 0, False)
            toon.setPos(0, 0, -600)
            self.deletedToons.append(toon)

    def getSecondsLeft(self, avatarTime):
        return max(0, avatarTime - int(time.time()))

    def decideRecoverButtons(self):
        if self.deletedIndex == -1:
            self.playLabel['text'] = TTLocalizer.AvatarChooserCreate
        else:
            av = base.cr.deletedAvList[self.deletedIndex]
            secondsLeft = self.getSecondsLeft(av.position)
            if not secondsLeft:
                self.playLabel['text'] = TTLocalizer.AvatarChooserRecover
            else:
                self.playLabel['text'] = TTLocalizer.AvatarChooserQueued
        if self.deletedIndex <= -1:
            self.leftButton.hide()
        else:
            self.leftButton.show()
        if self.deletedIndex >= len(self.deletedToons) - 1:
            self.rightButton.hide()
        else:
            self.rightButton.show()

    def __increaseRecoverIndex(self, index):
        self.deletedIndex += index
        self.decideRecoverButtons()
        self.decideRecoverToon()

    def decideRecoverToon(self):
        for toon in self.deletedToons:
            toon.setPos(0, 0, -600)

        if self.toonIndex not in self.emptyToons:
            return
        emptyToon = self.emptyToons[self.toonIndex]
        if self.deletedIndex == -1:
            toon = emptyToon
        else:
            emptyToon.setPos(0, 0, -600)
            toon = self.deletedToons[self.deletedIndex]
        toon.reparentTo(render)
        toon.setPosHpr(*self.toonPos[self.toonIndex])