# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.coghq.CashbotMintDuctRoom_Battle01_Cogs
from panda3d.core import Point3
from SpecImports import *
from toontown.toonbase import ToontownGlobals
CogParent = 10000
BattleCellId = 0
BattleCells = {BattleCellId: {'parentEntId': CogParent,
                'pos': Point3(0, 0, 0)}}
CogData = [{'parentEntId': CogParent,
  'boss': 1,
  'level': ToontownGlobals.CashbotMintBossLevel,
  'battleCell': BattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.CashbotMintCogLevel + 1,
  'battleCell': BattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.CashbotMintCogLevel + 1,
  'battleCell': BattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.CashbotMintCogLevel + 1,
  'battleCell': BattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0}]
ReserveCogData = []