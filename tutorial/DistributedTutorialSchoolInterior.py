# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.DistributedTutorialSchoolInterior
from panda3d.core import GeomNode, headsUp
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from otp.nametag.NametagConstants import CFSpeech, CFTimeout
from toontown.building.DistributedToonHouseInterior import DistributedToonHouseInterior
from toontown.estate.DistributedChair import DistributedChair
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toon import NPCToons, ToonDNA, LaffMeter, InventoryNew
import random

class DistributedTutorialSchoolInterior(DistributedToonHouseInterior):

    def __init__(self, cr):
        DistributedToonHouseInterior.__init__(self, cr)
        self.bellSfx = loader.loadSfx('phase_3.5/audio/sfx/telephone_ring.ogg')
        self.alarmSfx = loader.loadSfx('phase_3.5/audio/sfx/alarm_warning.ogg')
        self.initVariables()

    def disable(self):
        DistributedToonHouseInterior.disable(self)
        render.setColorScale(1, 1, 1, 1)
        taskMgr.remove(self.professorPete.uniqueName('comeHowMessage'))
        taskMgr.remove(self.uniqueName('lowerHp'))
        taskMgr.remove(self.uniqueName('blackout'))
        for obj in self.toons + [self.professorPete]:
            if obj:
                obj.delete()

        for obj in [self.tutorialGui, self.tutorialGuiPiece]:
            if obj:
                obj.removeNode()

        for obj in [self.laffMeter, self.blackoutText]:
            if obj:
                obj.destroy()

        for obj in [self.inventory]:
            if obj:
                obj.unload()

        for obj in [self.lectureSeq, self.inventoryPulseSeq, self.alarmSeq]:
            if obj:
                obj.pause()

        self.bellSfx.stop()
        self.alarmSfx.stop()
        self.initVariables()

    def initVariables(self):
        self.toons = []
        self.professorPete = None
        self.tutorialGui = None
        self.tutorialGuiPiece = None
        self.laffMeter = None
        self.inventory = None
        self.lectureSeq = None
        self.inventoryPulseSeq = None
        self.alarmSeq = None
        self.myChair = None
        self.blackoutText = None
        return

    def getDoor(self):
        return base.cr.doFind('DistributedDoor')

    def setup(self):
        DistributedToonHouseInterior.setup(self)
        base.localAvatar.setPosHpr(-12.1, -28, 0.08, 0, 0, 0)
        base.playSfx(self.bellSfx, volume=0.5)
        self.professorPete = NPCToons.createLocalNPC(2003)
        self.professorPete.reparentTo(render)
        self.professorPete.setPosHpr(*self.posIndices[0])
        self.professorPete.setChatAbsolute(TTLocalizer.TutorialComeMessage % base.localAvatar.getName(), CFSpeech)
        self.professorPete.headsUp(base.localAvatar)
        self.professorPete.permanentLookAt(base.localAvatar)
        self.professorPete.initializeBodyCollisions(self.uniqueName('distAvatarCollNode'))
        self.professorPete.addActive()
        self.accept('houseItemGenerated', self.__houseItemGenerated)
        taskMgr.doMethodLater(10, lambda task: self.professorPete.setChatAbsolute(TTLocalizer.TutorialComeHowMessage, CFSpeech), self.professorPete.uniqueName('comeHowMessage'))

    def loadChair(self, chair):
        if not chair.locked:
            if chair.item.furnitureType == 110:
                chair.setTutorialCallback(self.startLecture)
            return
        chairInfo = chair.getChair()
        toon = NPCToons.createRandomNPC()
        toon.addActive()
        toon.reparentTo(chair)
        toon.setPos(chairInfo[0])
        toon.getGeomNode().setHpr(chairInfo[1])
        toon.animFSM.request('Sit')
        self.toons.append(toon)
        self.accept('enter%s' % chair.uniqueName('Chair'), self.__talkWithClassmate, [toon])

    def switchTutorialGuiPiece(self, guiName = None):
        if self.tutorialGuiPiece:
            self.tutorialGuiPiece.removeNode()
        if not guiName:
            self.tutorialGui.removeNode()
            self.tutorialGui = None
            self.tutorialGuiPiece = None
            return
        else:
            if not self.tutorialGui:
                self.tutorialGui = loader.loadModel('phase_3.5/models/gui/tutorial_gui')
            self.tutorialGuiPiece = self.tutorialGui.find('**/' + guiName)
            self.tutorialGuiPiece.reparentTo(self.professorPete)
            self.tutorialGuiPiece.setPosHprScale(3, 4, 3.3, 180, 0, 0, 2, 2, 2)
            return

    def pulseTrackRow(self, pulseRow = None):
        if self.inventoryPulseSeq:
            self.inventoryPulseSeq.finish()
            self.inventoryPulseSeq = None
        for row in self.inventory.trackRows:
            row.setBin('background', 10)
            row.setScale(1)

        if pulseRow == None:
            return
        else:
            pulseRow = self.inventory.trackRows[pulseRow]
            pulseRow.clearBin()
            self.inventoryPulseSeq = Sequence(pulseRow.scaleInterval(1, 1.3, 1, blendType='easeInOut'), pulseRow.scaleInterval(1, 1, 1.3, blendType='easeInOut'))
            self.inventoryPulseSeq.loop()
            return

    def startLecture(self, chair):
        if self.lectureSeq:
            return
        self.myChair = chair
        taskMgr.remove(self.professorPete.uniqueName('comeHowMessage'))
        taskMgr.remove(self.uniqueName('lowerHp'))
        self.professorPete.stopPermanentLookAt()
        self.professorPete.setPosHpr(*self.posIndices[0])
        for toon in [self.professorPete] + self.toons:
            toon.clearChat()

        camera.setPosHpr(camera.getPos(render), camera.getHpr(render))
        camera.reparentTo(render)
        base.playSfx(self.bellSfx, volume=0.5)
        base.localAvatar.setPreventSleepWatch(True)
        self.lectureSeq = Sequence(camera.posHprInterval(1.5, (3.9, -12, 3.7525), (90, 0, 0)), Wait(1), Func(self.professorPete.setLocalPageChat, TTLocalizer.TutorialLectureMessage, 0))
        self.lectureSeq.start()
        self.ignore('houseItemGenerated')
        self.accept(self.professorPete.uniqueName('nextChatPage'), self.__lectureNext)
        self.acceptOnce(self.professorPete.uniqueName('doneChatPage'), self.__lectureDone)

    def __lectureNext(self, pageNumber, elapsed):
        if pageNumber == 5:
            self.switchTutorialGuiPiece('suits')
        elif pageNumber == 8:
            self.switchTutorialGuiPiece('toon_buildings')
        elif pageNumber == 9:
            self.switchTutorialGuiPiece('suit_buildings')
        elif pageNumber == 10:
            self.switchTutorialGuiPiece('squirt1')
        elif pageNumber == 11:
            self.switchTutorialGuiPiece('squirt2')
        elif pageNumber == 12:
            self.switchTutorialGuiPiece()
            self.laffMeter = LaffMeter.LaffMeter(base.localAvatar.style, base.localAvatar.maxHp, base.localAvatar.maxHp)
            self.laffMeter.setAvatar(base.localAvatar)
            self.laffMeter.reparentTo(self.professorPete)
            self.laffMeter.setPosHprScale(3, 4, 3.3, 180, 0, 0, 1, 1, 1)
            self.laffMeter.setBin('fixed', 40)
            self.laffMeter.setDepthWrite(False)
            self.laffMeter.start()
        elif pageNumber == 13:
            taskMgr.doMethodLater(0.01, self.__lowerHp, self.uniqueName('lowerHp'))
        elif pageNumber == 14:
            taskMgr.remove(self.uniqueName('lowerHp'))
            self.laffMeter.adjustFace(self.laffMeter.maxHp, self.laffMeter.maxHp)
        elif pageNumber == 16:
            self.laffMeter.destroy()
            self.laffMeter = None
            base.localAvatar.laffMeter.obscure(False)
            self.inventory = InventoryNew.InventoryNew(base.localAvatar, base.localAvatar.inventory.invString)
            self.inventory.setActivateMode('book')
            self.inventory.updateGUI()
            self.inventory.invFrame.reparentTo(aspect2d)
            self.inventory.invFrame.setPos(-0.66, 0, 0)
            self.inventory.invFrame.setScale(0.6)
            trackInfo = DirectFrame(self.inventory.detailFrame, relief=None, pos=(0, 0, -0.18), scale=(0.35, 1, 0.45), text='', geom=DGG.getDefaultDialogGeom(), geom_scale=(1.4, 1, 1), geom_color=ToontownGlobals.GlobalDialogColor)
            trackInfo.setBin('background', 10)
        elif pageNumber == 19:
            self.pulseTrackRow(0)
        elif pageNumber == 22:
            self.pulseTrackRow(1)
        elif pageNumber == 25:
            self.pulseTrackRow(2)
        elif pageNumber == 27:
            self.pulseTrackRow(3)
        elif pageNumber == 28:
            self.pulseTrackRow(4)
        elif pageNumber == 30:
            self.pulseTrackRow(5)
        elif pageNumber == 31:
            self.pulseTrackRow(6)
        elif pageNumber == 34:
            self.pulseTrackRow()
            self.inventory.unload()
            self.inventory = None
        return

    def __lectureDone(self, elapsed):
        self.alarmSeq = Sequence(render.colorScaleInterval(1.5, (0.5, 0, 0, 1)), render.colorScaleInterval(1.5, (1, 1, 1, 1)))
        self.lectureSeq = Sequence(Wait(2), Func(self.professorPete.setChatAbsolute, TTLocalizer.TutorialLectureEndMessage1, CFSpeech), Wait(3), Func(self.professorPete.setChatAbsolute, TTLocalizer.TutorialLectureEndMessage2, CFSpeech), Wait(1.5), Func(base.cr.tutorialManager.d_requestStage, 'schoolAlarm'), Func(base.cr.playGame.hood.loader.activityMusic.stop), Func(base.playSfx, self.alarmSfx, looping=1, volume=1.25), Func(self.alarmSeq.loop), Func(self.professorPete.clearChat), Wait(2.5), Func(self.professorPete.setChatAbsolute, TTLocalizer.TutorialLectureEndMessage3, CFSpeech), Wait(2), Func(self.professorPete.loop, 'walk'), self.professorPete.hprInterval(1, (180, 0, 0)), Func(self.professorPete.loop, 'neutral'), Wait(2), Func(self.professorPete.loop, 'walk'), self.professorPete.hprInterval(1, (270, 0, 0)), Func(self.professorPete.loop, 'neutral'), Func(self.professorPete.setChatAbsolute, TTLocalizer.TutorialLectureEndMessage4, CFSpeech), Wait(4), Func(self.professorPete.setChatAbsolute, TTLocalizer.TutorialLectureEndMessage5, CFSpeech), Func(self.professorPete.loop, 'walk'), self.professorPete.hprInterval(1, (180, 0, 0)), Func(self.professorPete.loop, 'run'), self.professorPete.posInterval(1.5, (-15.5, -31.5, 0.056)), Func(self.professorPete.delete), Func(self.myChair.setupGui), Func(taskMgr.doMethodLater, 90, self.__blackOut, self.uniqueName('blackout')), Func(base.localAvatar.setPreventSleepWatch, False))
        self.lectureSeq.start()

    def __lowerHp(self, task):
        if not self.laffMeter or self.laffMeter.hp <= 0:
            return task.done
        self.laffMeter.adjustFace(self.laffMeter.hp - 1, self.laffMeter.maxHp)
        return task.again

    def __setBlackoutText(self, sfx, text):
        base.playSfx(loader.loadSfx(sfx), volume=0.7)
        self.blackoutText['text'] = self.blackoutText['text'] + text + '\n\n'

    def __blackOut(self, task):
        base.cr.playGame.getPlace().setState('stopped')
        base.transitions.fadeOut(5)
        base.localAvatar.setPreventSleepWatch(True)
        self.blackoutText = DirectLabel(relief=None, pos=(0, 0, 0.8), text_scale=0.11, text='', text_fg=(1, 1, 1, 1), sortOrder=2000)
        self.lectureSeq = Sequence(Wait(5), Func(self.alarmSfx.stop), Wait(2), Func(self.__setBlackoutText, 'phase_3.5/audio/dial/AV_dog_question.ogg', TTLocalizer.TutorialPassOutMessage1), Wait(2), Func(self.__setBlackoutText, 'phase_3.5/audio/dial/COG_VO_statement.ogg', TTLocalizer.TutorialPassOutMessage2), Wait(2), Func(self.__setBlackoutText, 'phase_3.5/audio/dial/AV_dog_long.ogg', TTLocalizer.TutorialPassOutMessage3), Wait(2), Func(self.__setBlackoutText, 'phase_3.5/audio/dial/AV_dog_long.ogg', TTLocalizer.TutorialPassOutMessage4), Wait(2), Func(self.__setBlackoutText, 'phase_3.5/audio/dial/AV_dog_exclaim.ogg', TTLocalizer.TutorialPassOutMessage5), Wait(3), Func(base.localAvatar.getGeomNode().setHpr, 0, 0, 0), Func(self.getDoor().doorTrigger), Wait(1), Func(self.blackoutText.destroy), Func(base.transitions.fadeIn, 1.5))
        self.lectureSeq.start()
        return

    def __talkWithClassmate(self, toon, collEntry):
        if toon.isTalking():
            return
        if self.myChair:
            messages = TTLocalizer.TutorialScaredMessages
        else:
            messages = TTLocalizer.TutorialHelloMessages
        toon.setChatAbsolute(random.choice(messages), CFSpeech | CFTimeout)

    def __houseItemGenerated(self, item):
        if isinstance(item, DistributedChair):
            self.loadChair(item)