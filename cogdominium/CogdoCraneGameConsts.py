# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.cogdominium.CogdoCraneGameConsts
from direct.fsm.StatePush import StateVar
from otp.level.EntityStateVarSet import EntityStateVarSet
from CogdoUtil import VariableContainer
from toontown.cogdominium.CogdoEntityTypes import CogdoCraneGameSettings, CogdoCraneCogSettings
Gameplay = VariableContainer()
Gameplay.SecondsUntilGameOver = 180.0
Gameplay.TimeRunningOutSeconds = 45.0
Audio = VariableContainer()
Audio.MusicFiles = {'normal': 'phase_9/audio/bgm/CHQ_FACT_bg.ogg',
 'end': 'phase_7/audio/bgm/encntr_toon_winning_indoor.ogg',
 'timeRunningOut': 'phase_7/audio/bgm/encntr_suit_winning_indoor.ogg'}
Settings = EntityStateVarSet(CogdoCraneGameSettings)
CogSettings = EntityStateVarSet(CogdoCraneCogSettings)
CranePosHprs = [(13.4, -136.6, 6, -45, 0, 0),
 (13.4, -91.4, 6, -135, 0, 0),
 (58.6, -91.4, 6, 135, 0, 0),
 (58.6, -136.6, 6, 45, 0, 0)]
MoneyBagPosHprs = [[-6.799999999999997,
  -128.3,
  0,
  -90,
  0,
  0],
 [-6.900000000000006,
  -101.69999999999999,
  0,
  -90,
  0,
  0],
 [81.69999999999999,
  -125.39999999999998,
  0,
  90,
  0,
  0],
 [81.5,
  -101.39999999999998,
  0,
  90,
  0,
  0],
 [23.799999999999997,
  -158.10000000000002,
  0,
  0,
  0,
  0],
 [49.900000000000006,
  -158.10000000000002,
  0,
  0,
  0,
  0],
 [23.0,
  -73.69999999999999,
  0,
  180,
  0,
  0],
 [50.19999999999999,
  -73.69999999999999,
  0,
  180,
  0,
  0]]
for i in xrange(len(MoneyBagPosHprs)):
    MoneyBagPosHprs[i][2] += 6