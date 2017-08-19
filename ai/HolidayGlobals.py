# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.ai.HolidayGlobals
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.parties import ToontownTimeZone
import calendar, datetime
TIME_ZONE = ToontownTimeZone.ToontownTimeZone()
TRICK_OR_TREAT = 0
WINTER_CAROLING = 1
CAROLING_REWARD = 100
SCAVENGER_HUNT_LOCATIONS = 6
Holidays = {ToontownGlobals.GRAND_PRIX: {'weekDay': 0,
                              'startMessage': TTLocalizer.CircuitRaceStart,
                              'ongoingMessage': TTLocalizer.CircuitRaceOngoing,
                              'endMessage': TTLocalizer.CircuitRaceEnd},
 ToontownGlobals.FISH_BINGO: {'weekDay': 2,
                              'startMessage': TTLocalizer.FishBingoStart,
                              'ongoingMessage': TTLocalizer.FishBingoOngoing,
                              'endMessage': TTLocalizer.FishBingoEnd},
 ToontownGlobals.SILLY_SATURDAY: {'weekDay': 5,
                                  'startMessage': TTLocalizer.SillySaturdayStart,
                                  'ongoingMessage': TTLocalizer.SillySaturdayOngoing,
                                  'endMessage': TTLocalizer.SillySaturdayEnd},
 ToontownGlobals.BLACK_CAT_DAY: {'startMonth': 10,
                                 'startDay': 31,
                                 'endMonth': 10,
                                 'endDay': 31,
                                 'startMessage': TTLocalizer.BlackCatHolidayStart,
                                 'ongoingMessage': TTLocalizer.BlackCatHolidayStart,
                                 'endMessage': TTLocalizer.BlackCatHolidayEnd},
 ToontownGlobals.APRIL_TOONS_WEEK: {'startMonth': 4,
                                    'startDay': 1,
                                    'endMonth': 4,
                                    'endDay': 7,
                                    'startMessage': TTLocalizer.AprilToonsWeekStart,
                                    'ongoingMessage': TTLocalizer.AprilToonsWeekStart,
                                    'endMessage': TTLocalizer.AprilToonsWeekEnd},
 ToontownGlobals.IDES_OF_MARCH: {'startMonth': 3,
                                 'startDay': 14,
                                 'endMonth': 3,
                                 'endDay': 20,
                                 'startMessage': TTLocalizer.IdesOfMarchStart,
                                 'ongoingMessage': TTLocalizer.IdesOfMarchStart,
                                 'endMessage': TTLocalizer.IdesOfMarchEnd,
                                 'speedchatIndexes': [30450],
                                 'effectMessage': TTLocalizer.GreenToonEffectMsg,
                                 'effectDelay': 10},
 ToontownGlobals.CHRISTMAS: {'startMonth': 12,
                             'startDay': 14,
                             'endMonth': 1,
                             'endDay': 4,
                             'startMessage': TTLocalizer.WinterCarolingStart,
                             'ongoingMessage': TTLocalizer.WinterCarolingStart,
                             'endMessage': TTLocalizer.WinterCarolingEnd,
                             'speedchatIndexes': range(30200, 30206),
                             'effectDelay': 15,
                             'scavengerHunt': WINTER_CAROLING},
 ToontownGlobals.HALLOWEEN: {'startMonth': 10,
                             'startDay': 21,
                             'endMonth': 11,
                             'endDay': 1,
                             'startMessage': TTLocalizer.TrickOrTreatStart,
                             'ongoingMessage': TTLocalizer.TrickOrTreatStart,
                             'endMessage': TTLocalizer.TrickOrTreatEnd,
                             'speedchatIndexes': [10003],
                             'effectDelay': 15,
                             'scavengerHunt': TRICK_OR_TREAT},
 ToontownGlobals.SUMMER_FIREWORKS: {'startMonth': 6,
                                    'startDay': 29,
                                    'endMonth': 7,
                                    'endDay': 16,
                                    'startMessage': TTLocalizer.SummerFireworksStart,
                                    'ongoingMessage': TTLocalizer.SummerFireworksStart,
                                    'endMessage': TTLocalizer.SummerFireworksEnd},
 ToontownGlobals.NEW_YEAR_FIREWORKS: {'startMonth': 12,
                                      'startDay': 30,
                                      'endMonth': 1,
                                      'endDay': 2,
                                      'startMessage': TTLocalizer.NewYearFireworksStart,
                                      'ongoingMessage': TTLocalizer.NewYearFireworksStart,
                                      'endMessage': TTLocalizer.NewYearFireworksEnd},
 ToontownGlobals.VALENTOONS_DAY: {'startMonth': 2,
                                  'startDay': 8,
                                  'endMonth': 2,
                                  'endDay': 23,
                                  'startMessage': TTLocalizer.ValentinesDayStart,
                                  'ongoingMessage': TTLocalizer.ValentinesDayStart,
                                  'endMessage': TTLocalizer.ValentinesDayEnd},
 ToontownGlobals.MORE_XP_HOLIDAY: {'weekDay': 4,
                                   'startMessage': TTLocalizer.MoreXpHolidayStart,
                                   'ongoingMessage': TTLocalizer.MoreXpHolidayOngoing,
                                   'endMessage': TTLocalizer.MoreXpHolidayEnd},
 ToontownGlobals.BOSS_HOLIDAY: {'weekDay': 6,
                                'startMessage': TTLocalizer.BossHolidayStart,
                                'ongoingMessage': TTLocalizer.BossHolidayOngoing,
                                'endMessage': TTLocalizer.BossHolidayEnd}}

def getHoliday(id):
    return Holidays.get(id, {})


def getServerTime(date):
    epoch = datetime.datetime.fromtimestamp(0, TIME_ZONE)
    delta = date - epoch
    return delta.total_seconds()


def getStartDate(holiday, rightNow = None):
    if not rightNow:
        rightNow = datetime.datetime.now()
    startMonth = holiday['startMonth'] if 'startMonth' in holiday else rightNow.month
    startDay = holiday['startDay'] if 'startDay' in holiday else (rightNow.day if 'weekDay' in holiday else calendar.monthrange(rightNow.year, startMonth)[0])
    startDate = datetime.datetime(rightNow.year, startMonth, startDay, tzinfo=TIME_ZONE)
    return startDate


def getEndDate(holiday, rightNow = None):
    if not rightNow:
        rightNow = datetime.datetime.now()
    endMonth = holiday['endMonth'] if 'endMonth' in holiday else rightNow.month
    endDay = holiday['endDay'] if 'endDay' in holiday else (rightNow.day if 'weekDay' in holiday else calendar.monthrange(rightNow.year, endMonth)[1])
    endYear = rightNow.year
    if 'startMonth' in holiday and holiday['startMonth'] > endMonth:
        endYear += 1
    endDate = datetime.datetime(endYear, endMonth, endDay, tzinfo=TIME_ZONE)
    return endDate