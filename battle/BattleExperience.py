# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.battle.BattleExperience


def genRewardDicts(entries):
    toonRewardDicts = []
    for toonId, origExp, earnedExp, origQuests, items, missedItems, origMerits, merits, parts in entries:
        if toonId == -1:
            continue
        toon = base.cr.doId2do.get(toonId)
        if toon:
            toonRewardDicts.append({'toon': toon,
             'origExp': origExp,
             'earnedExp': earnedExp,
             'origQuests': origQuests,
             'items': items,
             'missedItems': missedItems,
             'origMerits': origMerits,
             'merits': merits,
             'parts': parts})

    return toonRewardDicts