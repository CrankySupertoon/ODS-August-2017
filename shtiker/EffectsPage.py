# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.shtiker.EffectsPage
from panda3d.core import Shader, TextNode, Vec4
from direct.gui.DirectGui import *
from direct.showbase import PythonUtil
from toontown.toonbase import TTLocalizer
from toontown.toontowngui.FrameColorPicker import FrameColorPicker
from BookElements import *
import ShtikerPage
PageMode = PythonUtil.Enum('Bloom, Ink, Invert, Sharpen')
normalColor = (1.0, 1.0, 1.0, 1.0)
clickColor = (0.8, 0.8, 0.0, 1.0)
rolloverColor = (0.15, 0.82, 1.0, 1.0)
diabledColor = (1.0, 0.98, 0.15, 1.0)

class EffectsPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.loaded = False
        self.mode = PageMode.Bloom
        self.tabPages = []

    def load(self):
        if self.loaded:
            return
        else:
            gui = loader.loadModel('phase_3.5/models/gui/fishingBook')
            self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.EffectsPageTitle, text_scale=0.12, pos=(0, 0, 0.62))
            self.tabs = [DirectButton(parent=self, relief=None, pos=(-0.75, 0, 0.775), text=TTLocalizer.EffectsBloom, text_scale=0.08, text_align=TextNode.ALeft, image=gui.find('**/tabs/polySurface1'), image_pos=(0.55, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Bloom]),
             DirectButton(parent=self, relief=None, pos=(-0.33, 0, 0.775), text=TTLocalizer.EffectsInk, text_scale=0.07, text_pos=(-0.05, 0), text_align=TextNode.ALeft, image=gui.find('**/tabs/polySurface2'), image_pos=(0.12, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Ink]),
             DirectButton(parent=self, relief=None, pos=(0.09, 0, 0.775), text=TTLocalizer.EffectsInvert, text_scale=0.07, text_pos=(-0.0275, 0), text_align=TextNode.ALeft, image=gui.find('**/tabs/polySurface3'), image_pos=(-0.28, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Invert]),
             DirectButton(parent=self, relief=None, pos=(0.51, 0, 0.775), text=TTLocalizer.EffectsSharpen, text_scale=0.08, text_align=TextNode.ALeft, image=gui.find('**/tabs/polySurface3'), image_pos=(-0.28, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Sharpen])]
            self.tabPages = [BloomTabPage(self),
             InkTabPage(self),
             InvertTabPage(self),
             SharpenTabPage(self)]
            for page in self.tabPages:
                page.hide()

            gui.removeNode()
            self.loaded = True
            return

    def enter(self):
        self.setMode(self.mode, True)
        self.show()

    def exit(self):
        for page in self.tabPages:
            page.exit()

        self.ignoreAll()
        self.hide()

    def unload(self):
        if not self.loaded:
            return
        self.title.destroy()
        for tab in self.tabs:
            tab.destroy()

        for page in self.tabPages:
            page.unload()

        del self.tabs
        self.loaded = False
        ShtikerPage.ShtikerPage.unload(self)

    def setMode(self, mode, force = False):
        if self.mode == mode and not force:
            return
        messenger.send('wakeup')
        self.mode = mode
        for i, tab in enumerate(self.tabs):
            tab['state'] = DGG.DISABLED if i == mode else DGG.NORMAL

        for i, page in enumerate(self.tabPages):
            page.enter() if i == mode else page.exit()

        self.title['text'] = self.tabs[mode]['text']


class ShaderTabPage(DirectFrame):

    def __init__(self, parent = aspect2d):
        DirectFrame.__init__(self, parent=parent, relief=None)
        self.parent = parent
        self.loaded = False
        self.load()
        return

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)
        return

    def load(self):
        if self.loaded:
            return
        self.enabledLabel = Label(parent=self, row=0)
        self.enabledButton = Button(parent=self, row=0, command=self.__toggleEnable)
        self.loaded = True
        return True

    def unload(self):
        if not self.loaded:
            return
        self.enabledLabel.destroy()
        self.enabledButton.destroy()
        del self.enabledLabel
        del self.enabledButton
        self.loaded = False
        return True

    def enter(self):
        self.show()
        self.__updateEnabled()

    def exit(self):
        self.hide()

    def __updateEnabled(self):
        if settings[self.shader].get('enabled', False):
            self.enabledLabel['text'] = self.enabledText
            self.enabledButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.enabledLabel['text'] = self.disabledText
            self.enabledButton['text'] = TTLocalizer.OptionsPageToggleOn

    def __toggleEnable(self):
        base.shaderMgr.setValue(self.shader, 'enabled', not settings[self.shader].get('enabled', False))
        self.__updateEnabled()


class BloomTabPage(ShaderTabPage):
    shader = 'bloom'
    enabledText = TTLocalizer.EffectsBloomEnabled
    disabledText = TTLocalizer.EffectsBloomDisabled

    def load(self):
        if not ShaderTabPage.load(self):
            return
        self.minLabel = Label(parent=self, row=1, text=TTLocalizer.EffectsBloomMinTrigger)
        self.minSlider = Slider(parent=self, row=1, value=settings[self.shader].get('minTrigger', 0.6), range=(0.0, 1.0), command=self.__editMinTrigger)
        self.maxLabel = Label(parent=self, row=2, text=TTLocalizer.EffectsBloomMaxTrigger)
        self.maxSlider = Slider(parent=self, row=2, value=settings[self.shader].get('maxTrigger', 1.0), range=(0.0, 1.0), command=self.__editMaxTrigger)
        self.desatLabel = Label(parent=self, row=3, text=TTLocalizer.EffectsBloomDesaturation)
        self.desatSlider = Slider(parent=self, row=3, value=settings[self.shader].get('desaturation', 0.6), range=(0.0, 1.0), command=self.__editDesaturation)
        self.intensityLabel = Label(parent=self, row=4, text=TTLocalizer.EffectsBloomIntensity)
        self.intensitySlider = Slider(parent=self, row=4, value=settings[self.shader].get('intensity', 1.0), range=(0.0, 1.0), command=self.__editIntensity)

    def unload(self):
        if not ShaderTabPage.unload(self):
            return
        self.minLabel.destroy()
        self.minSlider.destroy()
        self.maxLabel.destroy()
        self.maxSlider.destroy()
        self.desatLabel.destroy()
        self.desatSlider.destroy()
        self.intensityLabel.destroy()
        self.intensitySlider.destroy()
        del self.minLabel
        del self.minSlider
        del self.maxLabel
        del self.maxSlider
        del self.desatLabel
        del self.desatSlider
        del self.intensityLabel
        del self.intensitySlider

    def exit(self):
        ShaderTabPage.exit(self)
        base.shaderMgr.reloadBloom()

    def __editMinTrigger(self):
        base.shaderMgr.setValue(self.shader, 'minTrigger', self.minSlider['value'])

    def __editMaxTrigger(self):
        base.shaderMgr.setValue(self.shader, 'maxTrigger', self.maxSlider['value'])

    def __editDesaturation(self):
        base.shaderMgr.setValue(self.shader, 'desaturation', self.desatSlider['value'])

    def __editIntensity(self):
        base.shaderMgr.setValue(self.shader, 'intensity', self.intensitySlider['value'])


class InkTabPage(ShaderTabPage):
    shader = 'ink'
    enabledText = TTLocalizer.EffectsInkEnabled
    disabledText = TTLocalizer.EffectsInkDisabled

    def load(self):
        if not ShaderTabPage.load(self):
            return
        else:
            self.colorPicker = None
            self.widthLabel = Label(parent=self, row=1, text=TTLocalizer.EffectsInkWidth)
            self.widthSlider = Slider(parent=self, row=1, value=settings[self.shader].get('width', 1.0), range=(0.3, 2.0), command=self.__editWidth)
            self.colorLabel = Label(parent=self, row=2, text=TTLocalizer.EffectsInkColor)
            self.colorButton = Button(parent=self, row=2, text=TTLocalizer.EffectsInkChoose, command=self.__openColor)
            return

    def unloadColorPicker(self):
        if self.colorPicker:
            self.colorPicker.destroy()
            self.colorPicker = None
        return

    def unload(self):
        if not ShaderTabPage.unload(self):
            return
        self.unloadColorPicker()
        self.widthLabel.destroy()
        self.widthSlider.destroy()
        self.colorLabel.destroy()
        self.colorButton.destroy()
        del self.widthLabel
        del self.widthSlider
        del self.colorLabel
        del self.colorButton

    def exit(self):
        ShaderTabPage.exit(self)
        self.unloadColorPicker()
        base.shaderMgr.reloadInk()

    def __editWidth(self):
        base.shaderMgr.setValue(self.shader, 'width', self.widthSlider['value'])

    def __openColor(self):
        if not self.colorPicker:
            self.colorPicker = FrameColorPicker(0, 1, 0, 1, self.__editColor)

    def __editColor(self, color):
        if color:
            base.shaderMgr.setValue(self.shader, 'color', color)
        self.colorPicker = None
        return


class InvertTabPage(ShaderTabPage):
    shader = 'invert'
    enabledText = TTLocalizer.EffectsInvertEnabled
    disabledText = TTLocalizer.EffectsInvertDisabled

    def exit(self):
        ShaderTabPage.exit(self)
        base.shaderMgr.reloadInvert()


class SharpenTabPage(ShaderTabPage):
    shader = 'sharpen'
    enabledText = TTLocalizer.EffectsSharpenEnabled
    disabledText = TTLocalizer.EffectsSharpenDisabled

    def load(self):
        if not ShaderTabPage.load(self):
            return
        self.amountLabel = Label(parent=self, row=1, text=TTLocalizer.EffectsSharpenAmount)
        self.amountSlider = Slider(parent=self, row=1, value=settings[self.shader].get('amount', 0.0), range=(-10, 10), command=self.__editAmount)

    def unload(self):
        if not ShaderTabPage.unload(self):
            return
        self.amountLabel.destroy()
        self.amountSlider.destroy()
        del self.amountLabel
        del self.amountSlider

    def exit(self):
        ShaderTabPage.exit(self)
        base.shaderMgr.reloadSharpen()

    def __editAmount(self):
        base.shaderMgr.setValue(self.shader, 'amount', self.amountSlider['value'])