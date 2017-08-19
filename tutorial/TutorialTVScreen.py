# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.tutorial.TutorialTVScreen
from toontown.television.TVScreen import TVScreen
from toontown.television.TVScenes import *
from toontown.television.TVEffects import *
from toontown.toonbase import ToontownGlobals
from TutorialTVScenes import *

class TutorialTVScreen(TVScreen):

    def __init__(self, screen):
        TVScreen.__init__(self, screen, True)
        self.registerScene('ceo', CEOScene([FlickerEffect('ceo', 'static', [0, 2]), FontEffect(ToontownGlobals.getSuitFont(), (0.7, 0.7, 0.7, 1))]))
        self.registerScene('scientist', ScientistScene())
        self.registerScene('gyro', TwoDScene('phase_3.5/maps/gyro_gearloose.png', [FlickerEffect('gyro', 'static', [0, 2]), FontEffect(ToontownGlobals.getSuitFont(), (0.7, 0.7, 0.7, 1))]))
        self.chatGui.registerSounds(*[ (name, 'phase_3.5/audio/dial/COG_VO_%s.ogg' % name) for name in ('grunt', 'murmur', 'statement', 'question', 'exclaim') ])
        self.chatGui.registerSounds(('furious', 'phase_4/audio/sfx/furious_03.ogg'))
        self.loadToonSounds('duck')

    def loadToonSounds(self, species):
        self.chatGui.registerSounds(*[ ('%s_%s' % (species, name), 'phase_3.5/audio/dial/AV_%s_%s.ogg' % (species, name)) for name in ('exclaim', 'howl', 'long', 'med', 'question', 'short') ])