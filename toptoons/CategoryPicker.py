# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toptoons.CategoryPicker
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals, TTLocalizer
import math

class CategoryPicker(DirectFrame):

    def __init__(self, successCallback, failCallback, period, *args, **kwargs):
        self.successCallback = successCallback
        self.failCallback = failCallback
        self.period = period
        baseArgs = {'relief': None,
         'geom': DGG.getDefaultDialogGeom(),
         'geom_color': ToontownGlobals.GlobalDialogColor,
         'geom_scale': (1.6, 1, 1.35),
         'text': TTLocalizer.TopToonsPeriodTitle,
         'text_scale': 0.1,
         'text_pos': (0, 0.525)}
        kwargs.update(baseArgs)
        DirectFrame.__init__(self, *args, **kwargs)
        self.initialiseoptions(CategoryPicker)
        jarGui = loader.loadModel('phase_3.5/models/gui/jar_gui')
        sosGui = loader.loadModel('phase_3.5/models/gui/sos_textures')
        bookGui = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        cdrGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui')
        golfGui = loader.loadModel('phase_6/models/golf/golf_gui')
        cardGui = loader.loadModel('phase_3.5/models/gui/playingCard')
        inventoryGui = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        friendsGui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        gear = sosGui.find('**/gui_gear')
        self.buttons = []
        text = TTLocalizer.TopToonsMost + TTLocalizer.Stats[0]
        for pos in [(-0.295, 0, 0.275),
         (0.295, 0, 0.275),
         (-0.295, 0, -0.275),
         (0.295, 0, -0.275)]:
            button = DirectButton(self, relief=None, state=DGG.NORMAL, image=gear, image_scale=0.3, image_color=(1, 1, 1, 1), text_pos=(0, -0.25), text_scale=0.075, text2_scale=0.085, text_wordwrap=7, text=text, pos=pos, command=self.__choose)
            button.setTransparency(True)
            self.buttons.append(button)

        self.stopButton = DirectButton(self, relief=None, state=DGG.NORMAL, image=Preloaded['circleButton'], image_color=(1, 0.55, 0, 1), image_scale=0.5, pos=(0.65, 0, 0.56), text='X', text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.05, text_pos=(-0.005, -0.01), command=self.__close)
        self.leftArrow = DirectButton(self, relief=None, state=DGG.NORMAL, image=Preloaded['yellowArrow'], pos=(-0.68, 0, 0), command=self.__increaseIndex, extraArgs=[-1])
        self.rightArrow = DirectButton(self, relief=None, state=DGG.NORMAL, image=Preloaded['yellowArrow'], pos=(0.68, 0, 0), scale=(-1, 1, 1), command=self.__increaseIndex, extraArgs=[1])
        self.stats = [{'extraArgs': [ToontownGlobals.STAT_COGS],
          'image': gear},
         {'extraArgs': [ToontownGlobals.STAT_V2],
          'image': bookGui.find('**/CogArmIcon2')},
         {'extraArgs': [ToontownGlobals.STAT_SKELE],
          'image': sosGui.find('**/disguiseIcon')},
         {'extraArgs': [ToontownGlobals.STAT_UNIQUE],
          'image': sosGui.find('**/disguises')},
         {'extraArgs': [ToontownGlobals.STAT_VP],
          'image': bookGui.find('**/BossHead3Icon')},
         {'extraArgs': [ToontownGlobals.STAT_CFO],
          'image': 'phase_3.5/maps/cfo_icon.png',
          'image_scale': 0.175},
         {'extraArgs': [ToontownGlobals.STAT_CJ],
          'image': 'phase_3.5/maps/cj_icon.png',
          'image_scale': 0.175},
         {'extraArgs': [ToontownGlobals.STAT_CEO],
          'image': 'phase_3.5/maps/ceo_icon.png',
          'image_scale': 0.175},
         {'extraArgs': [ToontownGlobals.STAT_SOLO_VP],
          'image': bookGui.find('**/BossHead3Icon'),
          'color': (1, 0.5, 0.5, 1)},
         {'extraArgs': [ToontownGlobals.STAT_SOLO_CFO],
          'image': 'phase_3.5/maps/cfo_icon.png',
          'image_scale': 0.175,
          'color': (1, 0.5, 0.5, 1)},
         {'extraArgs': [ToontownGlobals.STAT_SOLO_CJ],
          'image': 'phase_3.5/maps/cj_icon.png',
          'image_scale': 0.175,
          'color': (1, 0.5, 0.5, 1)},
         {'extraArgs': [ToontownGlobals.STAT_SOLO_CEO],
          'image': 'phase_3.5/maps/ceo_icon.png',
          'image_scale': 0.175,
          'color': (1, 0.5, 0.5, 1)},
         {'extraArgs': [ToontownGlobals.STAT_BEANS_EARNT],
          'image': jarGui.find('**/Jar'),
          'image_scale': 0.6},
         {'extraArgs': [ToontownGlobals.STAT_TASKS],
          'image': bookGui.find('**/questCard')},
         {'extraArgs': [ToontownGlobals.STAT_BLDG],
          'image': bookGui.find('**/COG_building')},
         {'extraArgs': [ToontownGlobals.STAT_COGDO],
          'image': 'phase_3.5/maps/cogdo_icon.jpg',
          'image_scale': 0.175},
         {'extraArgs': [ToontownGlobals.STAT_ITEMS],
          'image': bookGui.find('**/package')},
         {'extraArgs': [ToontownGlobals.STAT_GIFTS],
          'image': cdrGui.find('**/tt_t_gui_sbk_cdrPresent')},
         {'extraArgs': [ToontownGlobals.STAT_FISH],
          'image': sosGui.find('**/fish')},
         {'extraArgs': [ToontownGlobals.STAT_FLOWERS],
          'image': sosGui.find('**/gardenIcon')},
         {'extraArgs': [ToontownGlobals.STAT_RACES_WON],
          'image': sosGui.find('**/kartIcon')},
         {'extraArgs': [ToontownGlobals.STAT_GOLF],
          'image': golfGui.find('**/score_card_icon')},
         {'extraArgs': [ToontownGlobals.STAT_HOLES_IN_ONE],
          'image': sosGui.find('**/teleportIcon')},
         {'extraArgs': [ToontownGlobals.STAT_COURSES_UNDER_PAR],
          'image': golfGui.find('**/score_card_icon'),
          'image_scale': (-0.3, 1, 0.3)},
         {'extraArgs': [ToontownGlobals.STAT_SOS],
          'image': cardGui.find('**/card_back'),
          'image_scale': 0.1},
         {'extraArgs': [ToontownGlobals.STAT_UNITES_USED],
          'image': inventoryGui.find('**/inventory_pixiedust'),
          'image_scale': 2.5,
          'color': (0, 0, 1, 1)},
         {'extraArgs': [ToontownGlobals.STAT_SLIPS],
          'image': loader.loadModel('phase_4/models/minigames/toon_cannon'),
          'image_scale': 0.07,
          'image_pos': (0, 0, -0.1),
          'image_hpr': (0, 10, 0)},
         {'extraArgs': [ToontownGlobals.STAT_GAGS],
          'image': inventoryGui.find('**/inventory_whistle'),
          'image_scale': 2.5},
         {'extraArgs': [ToontownGlobals.STAT_TROLLEY],
          'image': bookGui.find('**/trolley')},
         {'extraArgs': [ToontownGlobals.STAT_FRIENDS],
          'image': friendsGui.find('**/FriendsBox_Closed'),
          'image_scale': 1}]
        self.maxIndex = int(math.ceil(len(self.stats) / 4.0)) - 1
        self.index = 0
        self.openStats(0)
        return

    def destroy(self):
        DirectFrame.destroy(self)
        if not hasattr(self, 'buttons'):
            return
        for button in self.buttons:
            button.destroy()

        self.stopButton.destroy()
        del self.stopButton
        self.leftArrow.destroy()
        del self.leftArrow
        self.rightArrow.destroy()
        del self.rightArrow

    def __choose(self, period):
        for button in self.buttons + [self.stopButton, self.leftArrow, self.rightArrow]:
            button['state'] = DGG.DISABLED

        self.disappearSequence = Sequence(self.posInterval(1.5, (0, 0, -2.5), (0, 0, 0), blendType='easeInOut'), Func(self.destroy), Func(self.successCallback, self.period, period))
        self.disappearSequence.start()

    def __close(self):
        self.failCallback()
        self.destroy()

    def __increaseIndex(self, index):
        self.index += index
        self.openStats(self.index)

    def openStats(self, index):
        start = index * 4
        stats = self.stats[start:start + 4]
        for button in self.buttons:
            button.hide()

        for i, stat in enumerate(stats):
            button = self.buttons[i]
            statName = stat['extraArgs'][0]
            allStats = {'image_scale': 0.3,
             'image_pos': (0, 0, 0),
             'image_hpr': (0, 0, 0)}
            allStats.update(stat)
            if 'color' in allStats:
                button.setColorScale(*allStats['color'])
            else:
                button.setColorScale(1, 1, 1, 1)
            for key, value in allStats.iteritems():
                if key != 'color':
                    button[key] = value

            button['text'] = (TTLocalizer.TopToonsMost + TTLocalizer.Stats[statName]).title()
            button.show()

        if self.index <= 0:
            self.leftArrow.hide()
        else:
            self.leftArrow.show()
        if self.index >= self.maxIndex:
            self.rightArrow.hide()
        else:
            self.rightArrow.show()