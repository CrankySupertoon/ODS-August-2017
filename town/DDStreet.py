# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.town.DDStreet
from panda3d.core import Fog
from toontown.town import Street

class DDStreet(Street.Street):

    def enter(self, requestStatus):
        Street.Street.enter(self, requestStatus)
        self.loader.hood.setWhiteFog()

    def exit(self):
        Street.Street.exit(self)
        self.loader.hood.setNoFog()