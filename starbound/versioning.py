
# Upgrade players from version 12 (v. Glad Giraffe) to version 25 (v. Cheerful Giraffe 1.0-1.1.1)
def upgrade_player_12_25(player):
    # Set player version. (Game internally adds by 1)
    player.version = 24
    
    #
    # Add new fields
    #
    
    # Add blank companion data
    player.data['companions'] = {
        'companions' : {},
        'scriptStorage' : {}
    }
    
    # 'log' field is basically new, but copy the
    # old death count and play time statistics here
    player.data['log'] = {
        'scannedObjects' : [],
        'cinematics' : [],
        'radioMessages' : [],
        'playTime' : player.data['playTime'],
        'deathCount' : player.data['log']['statistic']['deathCount'],
        'introComplete' : True
    }
    del player.data['playTime']
    
    #
    # Translate fields that need updating
    #
    
    # Update inventory
    
    # Add empty action bar data
    player.data['inventory']['selectedActionBar'] = None
    player.data['inventory']['customBarGroup'] = 0
    player.data['inventory']['customBar'] = [[[None, None]] * 6] * 2
    
    # For each bar
    for i in range(2):
        # For slots 1-6
        player.data['inventory']['customBar'].append([])
        for j in range(6):
            # Set both hands to empty
            player.data['inventory']['customBar'][i][j] = [None, None]
    
    # Delete old action bar selection data
    del player.data['inventory']['primaryHeldSlot']
    del player.data['inventory']['altHeldSlot']
    
    # Add inspection tool
    player.data['inventory']['inspectionTool'] = None
    
    # Translate old 'equipment' array into
    # the new named slots
    player.data['inventory']['headSlot'] = player.data['inventory']['equipment'][0]
    player.data['inventory']['chestSlot'] = player.data['inventory']['equipment'][1]
    player.data['inventory']['legsSlot'] = player.data['inventory']['equipment'][2]
    player.data['inventory']['backSlot'] = player.data['inventory']['equipment'][3]
    player.data['inventory']['headCosmeticSlot'] = player.data['inventory']['equipment'][4]
    player.data['inventory']['chestCosmeticSlot'] = player.data['inventory']['equipment'][5]
    player.data['inventory']['legsCosmeticSlot'] = player.data['inventory']['equipment'][6]
    player.data['inventory']['backCosmeticSlot'] = player.data['inventory']['equipment'][7]
    del player.data['inventory']['equipment']
    
    # Translate the old 'essentialbar' entry into
    # the named tool slots
    player.data['inventory']['beamAxe'] = player.data['inventory']['essentialBar'][0]
    player.data['inventory']['wireTool'] = player.data['inventory']['essentialBar'][1]
    player.data['inventory']['paintTool'] = player.data['inventory']['essentialBar'][2]
    del player.data['inventory']['essentialBar']
    
    # Translate bags
    player.data['inventory']['mainBag'] = player.data['inventory']['bag']
    player.data['inventory']['materialBag'] = player.data['inventory']['tileBag']
    # New bags
    player.data['inventory']['reagentBag'] = [None] * 40
    player.data['inventory']['foodBag'] = [None] * 40

    # Dump old action bar items in the reagent bag
    # since that storage  doesn't exist any more
    # and the reagent bag is guaranteed to be empty
    for i in range(10):
        player.data['inventory']['reagentBag'][i] = player.data['inventory']['actionBar'][i]
    del player.data['inventory']['actionBar']
    # Dump old primary/secondary slot items in the food bag
    # since that storage  doesn't exist any more
    # and the food bag is guaranteed to be empty
    for i in range(2):
        player.data['inventory']['foodBag'][i] = player.data['inventory']['wieldable'][i]
    del player.data['inventory']['wieldable']
    
    # Don't know what this slot is for but it's new
    player.data['inventory']['trashSlot'] = None
    
    # Translate ship upgrades
    
    # Crew size is 2 per level after level 2 (which is when you fully repair your ship)
    # with a minimum of 2
    player.data['shipUpgrades']['crewSize'] = 2 * max(1, (player.data['shipUpgrades']['shipLevel'] - 2))
    # Default fuel efficiency
    player.data['shipUpgrades']['fuelEfficiency'] = 1.0
    
    # Translate player status
    
    # Add hunger
    player.data['statusController']['food'] = 70.0
    player.data['statusController']['resourcesLocked']['food'] = False
    
    # Add immunities to status. Just check if the player
    # has the tech enabled or not.
    protectedStatus = []
    if "breathprotectionTech" in player.data['techs']['enabledTechs']:
        protectedStatus.append("breathProtection")
    if "radiationprotectionTech" in player.data['techs']['enabledTechs']:
        protectedStatus.append("biomeradiationImmunity")
    if "coldprotectionTech" in player.data['techs']['enabledTechs']:
        protectedStatus.append("biomecoldImmunity")
    if "heatprotectionTech" in player.data['techs']['enabledTechs']:
        protectedStatus.append("biomeheatImmunity")
    player.data['statusController']['persistentEffectCategories']['armor'] += [{'stat' : status, 'amount' : 1.0} for status in protectedStatus]
    
    #
    # Reset the following:
    #
    # - Blueprints
    # - Techs
    # - Quests
    # - Codexes
    # - AI state
    # - Bookmarks
    player.data['blueprints'] = {'knownBlueprints' : [], 'newBlueprints' : []}
    player.data['techs'] = {
        'enabledTechs' : [],
        'availableTechs' : [],
        'equippedTechs' : {}
    }
    player.data['techController'] = {'techModules' : []}
    player.data['quests'] = {'currentQuest' : None, 'quests' : {}}
    player.data['codexes'] = {}
    player.data['aiState'] = {'availableMissions' : [], 'completedMissions' : []}
    player.data['bookmarks'] = []
