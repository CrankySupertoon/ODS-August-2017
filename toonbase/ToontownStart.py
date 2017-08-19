# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toonbase.ToontownStart
from panda3d.core import AntialiasAttrib, ConfigVariable, ConfigVariableList, ConfigVariableString, Filename, FrameRateMeter, NodePath, PandaSystem, VirtualFile, VirtualFileSystem, loadPrcFile, loadPrcFileData
from datetime import datetime
import __builtin__
import sys, os

def convertVersion(version):
    return tuple([ int(part) for part in version.split('.') ])


if sys.version_info < (2, 7, 13):
    print 'Your Python version is too old. Please upgrade to 2.7.13.'
    sys.exit()
elif convertVersion(PandaSystem.getVersionString()) < (1, 10, 0):
    print 'Your Panda3D version is too old. Please upgrade to 1.10.0.'
    sys.exit()
for dtool in ('children', 'parent', 'name'):
    del NodePath.DtoolClassDict[dtool]

startPath = 'user/' if sys.platform != 'android' else '/sdcard/ods/user/'
if not os.path.exists(startPath):
    os.makedirs(startPath)
from direct.directnotify.DirectNotifyGlobal import directNotify
notify = directNotify.newCategory('ToontownStart')
notify.setInfo(True)
from otp.settings.Settings import Settings
from otp.otpbase import OTPGlobals
preferencesFilename = ConfigVariableString('preferences-filename', startPath + 'preferences.json').getValue()
notify.info('Reading %s...' % preferencesFilename)
__builtin__.settings = Settings(preferencesFilename)
defaultSettings = {'res': (1280, 720),
 'fullscreen': False,
 'musicVol': 1.0,
 'sfxVol': 1.0,
 'loadDisplay': 'pandagl',
 'toonChatSounds': True,
 'language': 'English',
 'cogInterface': True,
 'tpTransition': True,
 'smoothAnimations': True,
 'patTransition': True,
 'fov': OTPGlobals.DefaultCameraFov,
 'fpsMeter': False,
 'customControls': False,
 'antiAliasing': True,
 'bulletHell': True,
 'greenScreen': False,
 'musicEasterEgg': True,
 'ttoAspectRatio': False,
 'bloom': {},
 'ink': {},
 'invert': {},
 'sharpen': {},
 'savedProfiles': {}}
for key, value in defaultSettings.iteritems():
    if key not in settings:
        settings[key] = value

del defaultSettings
loadPrcFileData('Settings: res', 'win-size %d %d' % tuple(settings['res']))
loadPrcFileData('Settings: fullscreen', 'fullscreen %s' % settings['fullscreen'])
if sys.platform == 'android':
    loadPrcFileData('Settings: android-loadDisplay', 'load-display pandagles2')
else:
    loadPrcFileData('Settings: loadDisplay', 'load-display %s' % settings['loadDisplay'])
if sys.platform != 'android':
    import argparse
    parser = argparse.ArgumentParser(description='Process some particularly interesting settings.')
    parser.add_argument('--username', '-u')
    __builtin__.arguments = parser.parse_args()
    del parser
from toontown.launcher.TTLauncher import TTLauncher
__builtin__.launcher = TTLauncher()
notify.info('Starting the game...')
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
notify.info('Setting the default font...')
import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
import ToonBase
ToonBase.ToonBase()
if base.win is None:
    notify.error('Unable to open window; aborting.')
import ToontownLoader
base.loader = ToontownLoader.ToontownLoader(base)
__builtin__.loader = base.loader
if settings['antiAliasing'] and sys.platform != 'android':
    render.setAntialias(AntialiasAttrib.MMultisample)
else:
    render.clearAntialias()
if settings['ttoAspectRatio']:
    base.applyForcedAspectRatio(1.33)
DirectGuiGlobals.setDefaultRolloverSound(loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
import TTLocalizer
if base.musicManagerIsValid:
    vol = settings['sfxVol']
    for man in base.sfxManagerList:
        man.setVolume(vol)

    base.sfxActive = True
    vol = settings['musicVol']
    base.musicManager.setVolume(vol)
    base.musicActive = True
    notify.info('Loading the default GUI sounds...')
    DirectGuiGlobals.setDefaultRolloverSound(loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
    DirectGuiGlobals.setDefaultClickSound(loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
import random
from toontown.suit import Suit
Suit.loadModels()
from toontown.dna import DNAParser
DNAParser.setupAssetStorage()
from toontown.distributed import ToontownClientRepository
base.cr = ToontownClientRepository.ToontownClientRepository(base.getServerVersion())
base.initNametagGlobals()
base.setFrameRateMeter(settings['fpsMeter'])
base.startShow(base.cr)
try:
    base.run()
except SystemExit:
    pass
except:
    import traceback
    traceback.print_exc()