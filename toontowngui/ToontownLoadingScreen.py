# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toontowngui.ToontownLoadingScreen
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.hood import ZoneUtil
from toontown.racing import RaceGlobals
import GUIUtils
import random, colorsys
zone2Picture = {ToontownGlobals.GoofySpeedway: 'gs',
 ToontownGlobals.ToontownCentral: 'ttc',
 ToontownGlobals.SillyStreet: 'ttc_ss',
 ToontownGlobals.LoopyLane: 'ttc_ll',
 ToontownGlobals.PunchlinePlace: 'ttc_pp',
 ToontownGlobals.DonaldsDock: 'dd',
 ToontownGlobals.BarnacleBoulevard: 'dd_bb',
 ToontownGlobals.SeaweedStreet: 'dd_ss',
 ToontownGlobals.LighthouseLane: 'dd_ll',
 ToontownGlobals.DaisyGardens: 'dg',
 ToontownGlobals.ElmStreet: 'dg_es',
 ToontownGlobals.MapleStreet: 'dg_ms',
 ToontownGlobals.OakStreet: 'dg_os',
 ToontownGlobals.MinniesMelodyland: 'mml',
 ToontownGlobals.AltoAvenue: 'mml_aa',
 ToontownGlobals.BaritoneBoulevard: 'mml_bb',
 ToontownGlobals.TenorTerrace: 'mml_tt',
 ToontownGlobals.TheBrrrgh: 'tb',
 ToontownGlobals.WalrusWay: 'tb_ww',
 ToontownGlobals.SleetStreet: 'tb_ss',
 ToontownGlobals.PolarPlace: 'tb_pp',
 ToontownGlobals.DonaldsDreamland: 'ddl',
 ToontownGlobals.LullabyLane: 'ddl_ll',
 ToontownGlobals.PajamaPlace: 'ddl_pp',
 ToontownGlobals.BedtimeBoulevard: 'ddl_bb',
 ToontownGlobals.OutdoorZone: 'oz',
 ToontownGlobals.GolfZone: 'gz',
 ToontownGlobals.SellbotHQ: 'sbhq',
 ToontownGlobals.CashbotHQ: 'cbhq',
 ToontownGlobals.LawbotHQ: 'lbhq',
 ToontownGlobals.BossbotHQ: 'bbhq',
 ToontownGlobals.SellbotFactoryInt: 'sbhq_fact',
 ToontownGlobals.SellbotFatalInt: 'sbhq_fact',
 ToontownGlobals.LawbotOfficeInt: 'lbhq_fact',
 ToontownGlobals.MyEstate: 'estate',
 RaceGlobals.RT_Speedway_1: 'gs_s1',
 RaceGlobals.RT_Speedway_1_rev: 'gs_s1',
 RaceGlobals.RT_Rural_1: 'gs_r1',
 RaceGlobals.RT_Rural_1_rev: 'gs_r1',
 RaceGlobals.RT_Speedway_2: 'gs_s2',
 RaceGlobals.RT_Speedway_2_rev: 'gs_s2',
 RaceGlobals.RT_Rural_2: 'gs_r1',
 RaceGlobals.RT_Rural_2_rev: 'gs_r2'}

class ToontownLoadingScreen(DirectObject):

    def __init__(self, loader):
        self.images = loader.scanDirectory('phase_3/maps/loading', ['png', 'jpg'])
        self.gui = None
        self.image = None
        self.head = None
        self.connectingLabel = DirectLabel(base.a2dpBottomCenter, relief=None, text='', text_scale=0.07, text_fg=(1, 1, 0.5, 1), text_shadow=(0, 0, 0, 1), pos=(0, 0, 0.05))
        self.connectingLabel.hide()
        self.headingLabel = DirectLabel(base.a2dpBottomCenter, relief=None, text='', text_scale=0.11, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_font=ToontownGlobals.getMinnieFont(), text_wordwrap=15, pos=(0.12, 0, 0.6))
        self.headingLabel.hide()
        self.tipLabel = DirectLabel(base.a2dpBottomCenter, text='', relief=None, text_scale=0.06, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), pos=(0, 0, 0.05))
        self.tipLabel.hide()
        self.logo = OnscreenImage(parent=base.a2dpTopCenter, image='phase_3/maps/toontown-logo.png')
        self.logo.setTransparency(True)
        self.logo.hide()
        return

    def destroyModel(self, model):
        if model:
            if hasattr(model, 'delete'):
                model.delete()
            else:
                model.removeNode()

    def getImage(self, zoneId):
        if zoneId in zone2Picture:
            return 'phase_3/maps/loading/%s.jpg' % zone2Picture[zoneId]
        else:
            return random.choice(loader.scanDirectory('phase_3/maps/loading/default', ['jpg', 'png']))

    def destroy(self):
        for model in [self.gui] + self.getModels():
            self.destroyModel(model)

        self.gui = None
        self.logo = None
        self.image = None
        self.head = None
        self.connectingLabel = None
        self.headingLabel = None
        self.tipLabel = None
        return

    def setLogoScale(self, scale, zAxis = 0):
        self.logo.setScale(scale * 2.0, 1, scale)
        self.logo.setPos(0, 0, -scale + zAxis)

    def getMusic(self):
        return loader.loadMusic('phase_3/audio/bgm/loading.ogg')

    def getModels(self):
        return [self.logo,
         self.connectingLabel,
         self.headingLabel,
         self.tipLabel,
         self.head,
         self.image]

    def getTip(self, tipCategory):
        return TTLocalizer.TipTitle + ' ' + random.choice(TTLocalizer.TipDict.get(tipCategory))

    def getToonDNA(self):
        from toontown.toon import ToonDNA
        toon = base.cr.avData
        dna = ToonDNA.ToonDNA(toon.dna)
        hue, sat, val = colorsys.rgb_to_hsv(*dna.getHeadColor()[:3])
        return (toon,
         dna,
         hue,
         sat,
         val)

    def begin(self, label, gui, tipCategory, zoneId):
        if gui == 2:
            self.gui = OnscreenImage(parent=render2d, image='phase_3/maps/loading_bg_clouds.jpg')
            self.gui.setBin('gui-popup', 0)
            self.setLogoScale(0.5625, -0.125)
            self.headingLabel['text_wordwrap'] = 15
            self.headingLabel.setX(0.12)
            self.accept('setConnectingText', self.__setConnectingText)
        elif gui == 0:
            from toontown.toon import ToonHead
            toon, dna, hue, sat, val = self.getToonDNA()
            self.gui = GUIUtils.loadRandomGradient(render2d, (-1, 1, -1, 1), hue, 0.85, 0.4)
            self.gui.setBin('gui-popup', 0)
            self.connectingLabel.hide()
            self.headingLabel.setX(0)
            self.setLogoScale(0.3)
            self.head = ToonHead.ToonHead()
            self.head.setupHead(dna, forGui=True)
            self.head.reparentTo(base.a2dpTopCenter)
            self.head.setH(random.choice([135, 180, 225]))
            self.head.setScale(0.35)
            self.head.setPos(0, 0, -1.025)
            label = label % toon.name
            self.headingLabel['text_wordwrap'] = 15
        else:
            self.setLogoScale(0.4, -0.15)
            self.headingLabel.setPos(0, 0, 0.65)
            self.headingLabel['text_wordwrap'] = 100
            self.image = OnscreenImage(parent=render2d, image=self.getImage(zoneId))
            self.image.setBin('gui-popup', 0)
        self.headingLabel['text'] = label
        for model in self.getModels():
            if model:
                model.show()

        if gui != 2:
            self.connectingLabel.hide()
            self.tipLabel['text'] = self.getTip(tipCategory)
            base.playMusic(self.getMusic(), looping=True, volume=0.8)
        else:
            self.tipLabel.hide()

    def __setConnectingText(self, text):
        self.connectingLabel['text'] = text
        if text:
            base.graphicsEngine.renderFrame()

    def end(self):
        self.destroyModel(self.gui)
        self.destroyModel(self.head)
        for model in self.getModels():
            if model:
                model.hide()

        self.gui = None
        self.ignore('setConnectingText')
        self.getMusic().stop()
        return