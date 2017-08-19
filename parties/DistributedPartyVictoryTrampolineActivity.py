# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.parties.DistributedPartyVictoryTrampolineActivity
from toontown.parties.DistributedPartyTrampolineActivity import DistributedPartyTrampolineActivity

class DistributedPartyVictoryTrampolineActivity(DistributedPartyTrampolineActivity):

    def __init__(self, cr, doJellyBeans = True, doTricks = False, texture = None):
        DistributedPartyTrampolineActivity.__init__(self, cr, doJellyBeans, doTricks, 'phase_13/maps/tt_t_ara_pty_trampolineVictory.jpg')