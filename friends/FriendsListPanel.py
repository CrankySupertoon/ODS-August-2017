# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.friends.FriendsListPanel
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from direct.fsm import StateData
from toontown.toon import ToonAvatarPanel
from toontown.friends import ToontownFriendSecret
from toontown.toonbase import ToontownGlobals, TTLocalizer
from otp.nametag.NametagGroup import *
from otp.nametag.NametagConstants import *
from otp.otpbase import OTPGlobals
from toontown.shtiker.BookElements import TaskedScrollList
FLPPets = 0
FLPOnline = 1
FLPAll = 2
FLPSearch = 3
globalFriendsList = None

def determineFriendName(friendId):
    handle = base.cr.identifyFriend(friendId)
    if handle:
        return handle.getName()
    return ''


def showFriendsList():
    global globalFriendsList
    if not globalFriendsList:
        globalFriendsList = FriendsListPanel()
    globalFriendsList.enter()


def hideFriendsList():
    if globalFriendsList:
        globalFriendsList.exit()


def showFriendsListTutorial():
    global globalFriendsList
    if not globalFriendsList:
        globalFriendsList = FriendsListPanel()
    globalFriendsList.enter()
    globalFriendsList.closeCommand = globalFriendsList.close['command']
    globalFriendsList.close['command'] = None
    return


def hideFriendsListTutorial():
    if globalFriendsList:
        if hasattr(globalFriendsList, 'closeCommand'):
            globalFriendsList.close['command'] = globalFriendsList.closeCommand
        globalFriendsList.exit()


def isFriendsListShown():
    return globalFriendsList != None and globalFriendsList.isEntered


def unloadFriendsList():
    global globalFriendsList
    if globalFriendsList:
        globalFriendsList.unload()
        globalFriendsList = None
    return


class FriendsListPanel(DirectFrame, StateData.StateData):

    def __init__(self):
        DirectFrame.__init__(self, parent=base.a2dTopRight, pos=(-0.233, 0, -0.46), geom=Preloaded['friendGui'], relief=None)
        StateData.StateData.__init__(self, 'friends-list-done')
        self.initialiseoptions(FriendsListPanel)
        self.friends = {}
        self.minPanel = FLPPets
        self.maxPanel = FLPSearch
        self.panelType = FLPOnline
        self.lastIndex = [0] * (self.maxPanel + 1)
        return

    def load(self):
        if self.isLoaded:
            return
        else:
            self.title = DirectLabel(parent=self, relief=None, text='', text_scale=TTLocalizer.FLPtitle, text_fg=(0, 0.1, 0.4, 1), pos=(0.007, 0.0, 0.2))
            self.scrollList = TaskedScrollList(parent=self, incButton_pos=(0.0, 0.0, -0.316), incButton_image3_color=(0.6, 0.6, 0.6, 0.6), incButton_scale=(1.0, 1.0, -1.0), decButton_pos=(0.0, 0.0, 0.117), decButton_image3_color=(0.6, 0.6, 0.6, 0.6), itemFrame_pos=(-0.17, 0.0, 0.06), numItemsVisible=8)
            self.close = DirectButton(parent=self, relief=None, image=Preloaded['closeButton'], pos=(0.01, 0, -0.38), command=self.__close)
            self.left = DirectButton(parent=self, relief=None, image=Preloaded['blueArrow'], image3_color=(0.6, 0.6, 0.6, 0.6), pos=(-0.15, 0.0, -0.38), scale=(-1.0, 1.0, 1.0), command=self.__offsetIndex, extraArgs=[-1])
            self.right = DirectButton(parent=self, relief=None, image=Preloaded['blueArrow'], image3_color=(0.6, 0.6, 0.6, 0.6), pos=(0.17, 0, -0.38), command=self.__offsetIndex, extraArgs=[1])
            self.newFriend = DirectButton(parent=self, relief=None, pos=(-0.14, 0.0, 0.14), image=Preloaded['detailFriends'], text=('', TTLocalizer.FriendsListPanelNewFriend, TTLocalizer.FriendsListPanelNewFriend), text_scale=TTLocalizer.FLPnewFriend, text_fg=(0, 0, 0, 1), text_bg=(1, 1, 1, 1), text_pos=(0.1, -0.085), textMayChange=0, command=self.__newFriend)
            self.trueFriends = DirectButton(parent=self, relief=None, pos=TTLocalizer.FLPtruefriendsPos, image=Preloaded['detailWhisper'], text=('',
             TTLocalizer.FriendsListPanelTrueFriends,
             TTLocalizer.FriendsListPanelTrueFriends,
             ''), text_scale=TTLocalizer.FLPtruefriends, text_fg=(0, 0, 0, 1), text_bg=(1, 1, 1, 1), text_pos=(-0.04, -0.085), textMayChange=0, command=self.__trueFriends)
            self.searchEntry = DirectEntry(parent=self, relief=DGG.GROOVE, scale=0.065, pos=(-0.185, 0, -0.48), borderWidth=(0.05, 0.05), frameColor=((1, 1, 1, 1), (1, 1, 1, 1), (0.5, 0.5, 0.5, 0.5)), state=DGG.NORMAL, text_align=TextNode.ALeft, text_scale=0.5, width=12, numLines=1, focus=1, backgroundFocus=1, cursorKeys=1, text_fg=(0, 0, 0, 1), suppressMouse=1, autoCapitalize=0)
            self.searchEntry.bind(DGG.TYPE, self.__search)
            self.searchEntry.bind(DGG.ERASE, self.__search)
            self.isLoaded = True
            return

    def unload(self):
        if not self.isLoaded:
            return
        self.exit()
        del self.title
        del self.scrollList
        del self.close
        del self.left
        del self.right
        del self.friends
        del self.searchEntry
        self.isLoaded = False
        DirectFrame.destroy(self)

    def enter(self):
        if self.isEntered:
            return
        else:
            self.isEntered = True
            if not self.isLoaded:
                self.load()
            if ToonAvatarPanel.ToonAvatarPanel.currentAvatarPanel:
                ToonAvatarPanel.ToonAvatarPanel.currentAvatarPanel.cleanup()
                ToonAvatarPanel.ToonAvatarPanel.currentAvatarPanel = None
            base.localAvatar.obscureFriendsListButton(1)
            if not self.friends:
                base.cr.sendGetFriendsListRequest()
            self.__updateTitle()
            self.__updateArrows()
            self.__updateScrollList()
            self.show()
            self.accept('friendOnline', self.__onlineFriendsChanged)
            self.accept('friendOffline', self.__onlineFriendsChanged)
            self.accept('friendsListChanged', self.__friendsListChanged)
            self.accept('friendsMapComplete', self.__friendsListChanged)
            self.searchEntry.enterText('')
            return

    def exit(self):
        if not self.isEntered:
            return
        self.isEntered = False
        self.lastIndex[self.panelType] = self.scrollList.index
        self.hide()
        base.cr.cleanPetsFromFriendsMap()
        self.ignoreAll()
        base.localAvatar.obscureFriendsListButton(-1)
        messenger.send(self.doneEvent)
        localAvatar.chatMgr.fsm.request('mainMenu')

    def __close(self):
        messenger.send('wakeup')
        self.exit()

    def __offsetIndex(self, offset):
        messenger.send('wakeup')
        self.lastIndex[self.panelType] = self.scrollList.index
        self.panelType += offset
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()

    def __trueFriends(self):
        messenger.send('wakeup')
        ToontownFriendSecret.showFriendSecret()

    def __newFriend(self):
        messenger.send('wakeup')
        messenger.send('friendAvatar', [None, None, None])
        return

    def __choseFriend(self, friendId):
        messenger.send('wakeup')
        handle = base.cr.identifyFriend(friendId)
        if handle:
            messenger.send('clickedNametag', [handle])

    def createButtons(self, avatars, nametag):
        for av in sorted(avatars, key=lambda x: x.getName()):
            button = DirectButton(relief=None, text=av.getName(), text_scale=0.04, text_align=TextNode.ALeft, text_fg=nametag, text_shadow=None, text1_bg=(0.5, 0.9, 1, 1), text2_bg=(1, 1, 0, 1), text3_fg=(0.4, 0.8, 0.4, 1), text_font=ToontownGlobals.getToonFont(), command=self.__choseFriend, extraArgs=[av.doId])
            self.scrollList.addItem(button, refresh=0)
            self.friends[av.doId] = button

        return

    def removeButtons(self):
        for button in self.friends.values():
            self.scrollList.removeItem(button, refresh=0)
            button.destroy()

        self.friends = {}

    def __updateScrollList(self):
        self.searchFriends = set()
        requeryFriendsList = False
        if self.panelType == FLPSearch:
            for friendId in base.localAvatar.friendsList:
                handle = base.cr.identifyFriend(friendId)
                if not handle:
                    requeryFriendsList = True
                    continue
                self.searchFriends.add(handle)

            localAvatar.chatMgr.fsm.request('otherDialog')
            self.searchEntry['focus'] = 1
            self.searchEntry.enterText('')
            self.searchEntry.show()
            self.removeButtons()
            self.scrollList.index = 0
            self.scrollList.refresh()
            return
        petFriends, friends, trueFriends = set(), set(), set()
        if self.panelType == FLPAll or self.panelType == FLPOnline:
            if base.wantPets and base.localAvatar.hasPet():
                handle = base.cr.identifyFriend(base.localAvatar.getPetId())
                if handle:
                    petFriends.add(handle)
            for friendId in base.localAvatar.friendsList:
                if self.panelType != FLPOnline or base.cr.isFriendOnline(friendId):
                    handle = base.cr.identifyFriend(friendId)
                    if not handle:
                        requeryFriendsList = True
                        continue
                    if base.localAvatar.isTrueFriends(friendId):
                        trueFriends.add(handle)
                    else:
                        friends.add(handle)

        elif self.panelType == FLPPets and base.wantPets:
            from toontown.pets import DistributedPet
            for av in base.cr.doId2do.values():
                if isinstance(av, DistributedPet.DistributedPet):
                    petFriends.add(av)

        self.removeButtons()
        self.createButtons(petFriends, NAMETAG_COLORS[CCNonPlayer][0][0])
        self.createButtons(trueFriends, NAMETAG_COLORS[CCNormal][0][0])
        self.createButtons(friends, NAMETAG_COLORS[CCSpeedChat][0][0])
        localAvatar.chatMgr.fsm.request('mainMenu')
        self.scrollList.index = self.lastIndex[self.panelType]
        self.scrollList.refresh()
        self.searchEntry.hide()
        if requeryFriendsList:
            base.cr.sendGetFriendsListRequest()

    def __updateTitle(self):
        if self.panelType == FLPOnline:
            self.title['text'] = TTLocalizer.FriendsListPanelOnlineFriends
        elif self.panelType == FLPAll:
            self.title['text'] = TTLocalizer.FriendsListPanelAllFriends
        elif self.panelType == FLPSearch:
            self.title['text'] = TTLocalizer.FriendsListPanelSearch
        else:
            self.title['text'] = TTLocalizer.FriendsListPanelPets
        self.title.resetFrameSize()

    def __updateArrows(self):
        self.left['state'] = 'inactive' if self.panelType == self.minPanel else 'normal'
        self.right['state'] = 'inactive' if self.panelType == self.maxPanel else 'normal'

    def __onlineFriendsChanged(self, doId):
        if self.panelType == FLPOnline:
            self.__updateScrollList()

    def __friendsListChanged(self, arg1 = None, arg2 = None):
        self.__updateScrollList()

    def __search(self, event = None):
        friends, trueFriends = set(), set()
        searchWord = self.searchEntry.get(plain=True)
        for result in [ friend for friend in self.searchFriends if searchWord.lower() in friend.getName().lower() ]:
            if base.localAvatar.isTrueFriends(result.doId):
                trueFriends.add(result)
            else:
                friends.add(result)

        self.removeButtons()
        self.createButtons(trueFriends, NAMETAG_COLORS[CCNormal][0][0])
        self.createButtons(friends, NAMETAG_COLORS[CCSpeedChat][0][0])
        self.scrollList.index = 0
        self.scrollList.refresh()