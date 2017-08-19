# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.shtiker.BookElements
from panda3d.core import NodePath, Plane, PlaneNode, TextNode
from direct.gui.DirectGui import *
from direct.task.Task import Task
import __builtin__
__builtin__.Preloaded = {}

def loadModels():
    if Preloaded:
        return
    print 'Preloading shticker book elements...'
    circleModel = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop')
    whiteCircleModel = loader.loadModel('phase_3/models/gui/nameshop_gui')
    buttonModel = loader.loadModel('phase_3/models/gui/quit_button')
    friendModel = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
    dialogModel = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
    matModel = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
    stickerModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
    speedchatModel = loader.loadModel('phase_3.5/models/gui/speedChatGui')
    houseModel = loader.loadModel('phase_5.5/models/gui/house_design_gui')
    battleModel = loader.loadModel('phase_3.5/models/gui/battle_gui')
    catModel = loader.loadModel('phase_3/models/gui/create_a_toon_gui')
    sosModel = loader.loadModel('phase_3.5/models/gui/playingCard')
    panelModel = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
    helpModel = loader.loadModel('phase_3.5/models/gui/tt_m_gui_brd_help')
    petModel = loader.loadModel('phase_3.5/models/gui/PetControlPannel')
    boardingModel = loader.loadModel('phase_3.5/models/gui/tt_m_gui_brd_avatarPanelBg')
    boardingInvModel = loader.loadModel('phase_3.5/models/gui/tt_m_gui_brd_inviteButton')
    inventoryModel = loader.loadModel('phase_3.5/models/gui/inventory_gui')
    trashcanModel = loader.loadModel('phase_3/models/gui/trashcan_gui')
    cogdoModel = loader.loadModel('phase_5/models/cogdominium/tt_m_gui_csa_flyThru')
    castModel = loader.loadModel('phase_4/models/gui/fishingGui')
    matchingModel = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
    catalogModel = loader.loadModel('phase_5.5/models/gui/catalog_gui')
    Preloaded['star'] = loader.loadModel('phase_3.5/models/gui/name_star')
    Preloaded['squareBox'] = speedchatModel.find('**/menuBG')
    Preloaded['paperNote'] = stickerModel.find('**/paper_note')
    Preloaded['circle'] = circleModel.find('**/tt_t_gui_mat_namePanelCircle')
    Preloaded['whiteCircle'] = whiteCircleModel.find('**/namePanelCircle')
    Preloaded['blueCircle'] = catalogModel.find('**/cover/blue_circle')
    Preloaded['playCard'] = sosModel.find('**/card_back')
    Preloaded['playCardFront'] = sosModel.find('**/card_front')
    Preloaded['evidence'] = stickerModel.find('**/summons')
    Preloaded['questCard'] = stickerModel.find('**/questCard')
    Preloaded['questPictureFrame'] = stickerModel.find('**/questPictureFrame')
    Preloaded['toonBattlePanel'] = battleModel.find('**/ToonBtl_Status_BG')
    Preloaded['blueFrame'] = matModel.find('**/tt_t_gui_mat_shuffleFrame')
    Preloaded['yellowButton'] = [ buttonModel.find('**/QuitBtn_' + name) for name in ('UP', 'DN', 'RLVR') ]
    Preloaded['blueButton'] = [ matModel.find('**/tt_t_gui_mat_shuffle' + name) for name in ('Up', 'Down') ]
    Preloaded['closeButton'] = [ dialogModel.find('**/CloseBtn_' + name) for name in ('UP', 'DN', 'Rllvr') ]
    Preloaded['okButton'] = [ dialogModel.find('**/ChtBx_OKBtn_' + name) for name in ('UP', 'DN', 'Rllvr') ]
    Preloaded['purpleHelpButton'] = [ helpModel.find('**/tt_t_gui_brd_help' + name) for name in ('Up', 'Down', 'Hover', 'Down') ]
    Preloaded['exitButton'] = [ castModel.find('**/exit_button' + name) for name in ('Up', 'Down', 'Rollover') ]
    Preloaded['blueArrow'] = [ friendModel.find('**/Horiz_Arrow_' + name) for name in ('UP', 'DN', 'Rllvr', 'UP') ]
    Preloaded['yellowArrow'] = [ matModel.find('**/tt_t_gui_mat_shuffleArrow' + name) for name in ('Up', 'Down', 'Up', 'Disabled') ]
    Preloaded['slimBlueArrow'] = [ battleModel.find('**/PckMn_BackBtn' + name) for name in ('', '_Dn', '_Rlvr') ]
    Preloaded['fatYellowArrow'] = [ catModel.find('**/CrtATn_R_Arrow_' + name) for name in ('UP', 'DN', 'RLVR', 'UP') ]
    Preloaded['scrollBlueArrow'] = [ friendModel.find('**/FndsLst_Scroll' + name) for name in ('Up', 'DN', 'Up_Rllvr', 'Up') ]
    Preloaded['circleButton'] = matchingModel.find('**/minnieCircle')
    Preloaded['furnitureButton'] = [ houseModel.find('**/bu_attic/bu_attic_' + name) for name in ('up', 'down', 'rollover', 'up') ]
    Preloaded['furnitureAttic'] = houseModel.find('**/attic')
    Preloaded['furnitureRoofTile'] = houseModel.find('**/rooftile')
    Preloaded['friendButton'] = [ friendModel.find('**/FriendsBox_' + name) for name in ('Closed', 'Rollover', 'Rollover') ]
    Preloaded['petIcon'] = petModel.find('**/PetBattleIcon')
    Preloaded['callButton'] = [ inventoryModel.find('**/InventoryButton' + name) for name in ('Up', 'Down', 'Rollover', 'Up') ]
    Preloaded['trashcan'] = [ trashcanModel.find('**/TrashCan_' + name) for name in ('CLSD', 'OPEN', 'RLVR') ]
    Preloaded['friendGui'] = friendModel.find('**/FriendsBox_Open')
    Preloaded['beanBank'] = catalogModel.find('**/bean_bank')
    Preloaded['detailInfoPanel'] = panelModel.find('**/avatarInfoPanel')
    Preloaded['detailPanel'] = panelModel.find('**/avatar_panel')
    Preloaded['detailStar'] = panelModel.find('**/avatarStar')
    Preloaded['detailFriends'] = [ panelModel.find('**/Frnds_Btn_' + name) for name in ('UP', 'DN', 'RLVR', 'UP') ]
    Preloaded['detailGo'] = [ panelModel.find('**/Go2_Btn_' + name) for name in ('UP', 'DN', 'RLVR', 'UP') ]
    Preloaded['detailWhisper'] = [ panelModel.find('**/ChtBx_ChtBtn_' + name) for name in ('UP', 'DN', 'RLVR', 'UP') ]
    Preloaded['detailTrueFriends'] = [ panelModel.find('**/Amuse_Btn_' + name) for name in ('UP', 'DN', 'RLVR', 'UP') ]
    Preloaded['detailIgnore'] = [ panelModel.find('**/Ignore_Btn_' + name) for name in ('UP', 'DN', 'RLVR', 'UP') ]
    Preloaded['detailReport'] = [ panelModel.find('**/report_Btn' + name) for name in ('UP', 'DN', 'RLVR', 'UP') ]
    Preloaded['detailDetail'] = [ panelModel.find('**/ChtBx_BackBtn_' + name) for name in ('UP', 'DN', 'Rllvr', 'UP') ]
    Preloaded['detailPet'] = [ petModel.find('**/PetControlToonButton%s1' % name) for name in ('Up', 'Down', 'Rollover') ]
    Preloaded['boardingBg'] = boardingModel.find('**/tt_t_gui_brd_avatar_panel_party')
    Preloaded['inviteButton'] = [ boardingInvModel.find('**/tt_t_gui_brd_invite' + name) for name in ('Up', 'Down', 'Hover', 'Up') ]
    Preloaded['kickButton'] = [ boardingInvModel.find('**/tt_t_gui_brd_kickout' + name) for name in ('Up', 'Down', 'Hover', 'Up') ]
    Preloaded['inviteDisabledButton'] = boardingInvModel.find('**/tt_t_gui_brd_inviteDisabled')
    Preloaded['cogdoChatBg'] = cogdoModel.find('**/background')
    Preloaded['cogdoChatBubble'] = cogdoModel.find('**/chatBubble')
    Preloaded['cogdoChatButton'] = [ cogdoModel.find('**/button' + name) for name in ('Up', 'Down', 'Hover') ]
    circleModel.removeNode()
    whiteCircleModel.removeNode()
    buttonModel.removeNode()
    friendModel.removeNode()
    dialogModel.removeNode()
    matModel.removeNode()
    stickerModel.removeNode()
    speedchatModel.removeNode()
    houseModel.removeNode()
    battleModel.removeNode()
    catModel.removeNode()
    sosModel.removeNode()
    panelModel.removeNode()
    helpModel.removeNode()
    petModel.removeNode()
    boardingModel.removeNode()
    boardingInvModel.removeNode()
    inventoryModel.removeNode()
    trashcanModel.removeNode()
    cogdoModel.removeNode()
    castModel.removeNode()
    matchingModel.removeNode()
    catalogModel.removeNode()
    del circleModel
    del whiteCircleModel
    del buttonModel
    del friendModel
    del dialogModel
    del matModel
    del stickerModel
    del speedchatModel
    del houseModel
    del battleModel
    del catModel
    del sosModel
    del panelModel
    del helpModel
    del petModel
    del boardingModel
    del boardingInvModel
    del inventoryModel
    del trashcanModel
    del cogdoModel
    del castModel
    del matchingModel
    del catalogModel


def copyFromPreload(preloadName):
    if preloadName in Preloaded:
        return NodePath(Preloaded[preloadName].node().copySubgraph())


loadModels()
textStartHeight = 0.45
textRowHeight = 0.145
leftMargin = -0.72
buttonbase_xcoord = 0.35
buttonbase_ycoord = 0.45
button_image_scale = (0.7, 1, 1)
button_textpos = (0, -0.02)
options_text_scale = 0.052

class Slider(DirectSlider):

    def __init__(self, parent = aspect2d, row = 0, x = buttonbase_xcoord, **kw):
        optiondefs = (('thumb_relief', None, None),
         ('pos', (x, 0, buttonbase_ycoord - row * textRowHeight), None),
         ('pageSize', 5, None),
         ('thumb_geom', Preloaded['circle'], None),
         ('thumb_geom_scale', 2, None),
         ('scale', 0.25, None))
        self.defineoptions(kw, optiondefs)
        DirectSlider.__init__(self, parent)
        self.initialiseoptions(Slider)
        return


class Label(DirectLabel):

    def __init__(self, parent = aspect2d, row = 0, zPadding = 0, align = 'left', **kw):
        optiondefs = (('relief', None, None),
         ('text', '', None),
         ('text_align', TextNode.ALeft, None),
         ('text_scale', options_text_scale, None),
         ('text_wordwrap', 16, None),
         ('pos', (leftMargin if align == 'left' else buttonbase_xcoord, 0, buttonbase_ycoord - row * textRowHeight + zPadding), None))
        self.defineoptions(kw, optiondefs)
        DirectLabel.__init__(self, parent)
        self.initialiseoptions(Label)
        return


class Button(DirectButton):

    def __init__(self, parent = aspect2d, row = 0, x = buttonbase_xcoord, xPadding = 0, zPadding = 0, type = 'yellowButton', **kw):
        optiondefs = (('relief', None, None),
         ('image', Preloaded[type], None),
         ('image_scale', button_image_scale, None),
         ('text', '', None),
         ('text_scale', options_text_scale, None),
         ('text_pos', button_textpos, None),
         ('pos', (x + xPadding, 0, buttonbase_ycoord - row * textRowHeight + zPadding), None),
         ('state', DGG.NORMAL, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initialiseoptions(Button)
        return


class TaskedScrollList(DirectScrolledList):

    def __init__(self, parent = aspect2d, clipperPos = (0.2, 0, 0), **kw):
        optiondefs = (('relief', None, None),
         ('incButton_relief', None, None),
         ('decButton_relief', None, None),
         ('itemFrame_relief', None, None),
         ('items', [], None),
         ('incButton_image', Preloaded['scrollBlueArrow'], None),
         ('decButton_image', Preloaded['scrollBlueArrow'], None))
        self.defineoptions(kw, optiondefs)
        DirectScrolledList.__init__(self, parent)
        self.initialiseoptions(TaskedScrollList)
        clipper = PlaneNode('clipper')
        clipper.setPlane(Plane((-1, 0, 0), clipperPos))
        self.setClipPlane(self.attachNewNode(clipper))
        self.pressTask = 'pressTask-%s' % id(self)
        self.decButton.bind(DGG.B1PRESS, self.__pressTaskUpdate, extraArgs=[-1])
        self.incButton.bind(DGG.B1PRESS, self.__pressTaskUpdate, extraArgs=[1])
        for button in (self.decButton, self.incButton):
            button.bind(DGG.B1RELEASE, self.__pressTaskDone)

        return

    def destroy(self):
        taskMgr.remove(self.pressTask)
        DirectScrolledList.destroy(self)

    def offsetListIndex(self, offset):
        newIndex = self.index + offset
        hitLimit = False
        if newIndex < 0:
            newIndex = 0
            hitLimit = True
        else:
            index = len(self['items']) - self['numItemsVisible'] + 1
            if newIndex >= index:
                newIndex = index
                hitLimit = True
        self.index = newIndex
        self.refresh()
        return hitLimit

    def __pressTaskDone(self, task = None):
        messenger.send('wakeup')
        taskMgr.remove(self.pressTask)

    def __pressTaskUpdate(self, offset, event = None):
        if self.offsetListIndex(offset):
            return
        task = Task(self.__runPressTask)
        task.delayTime = 0.2
        task.prevTime = 0.0
        task.delta = offset
        messenger.send('wakeup')
        taskMgr.add(task, self.pressTask)

    def __runPressTask(self, task):
        if task.time - task.prevTime < task.delayTime:
            return task.cont
        task.delayTime = max(0.05, task.delayTime * 0.75)
        task.prevTime = task.time
        if self.offsetListIndex(task.delta):
            return task.done
        return task.cont