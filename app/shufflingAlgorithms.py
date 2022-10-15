import DataObjects.CropData as CropData
import DataObjects.ObjectInfoData as ObjectInfoData
import DataObjects.BundleData as BundleData
import DataObjects.FishData as FishData
import DataObjects.FruitTreeData as FruitTrees
import DataObjects.AnimalData as AnimalData
import DataObjects.RecipeData as RecipeData
import DataObjects.LocationData as LocationData
import DataObjects.EventData as EventData
import DataObjects.MailData as MailData
import DataObjects.TipChannelData as TipChannelData

import random

class Reward:

    def __init__(self, typeString, id, quantity):
        self.typeString = typeString
        self.id = id
        self.quantity = quantity

def getNamesOfVillagers():
    return ['Alex', 'Elliot', 'Harvey', 'Sam', 'Sebastian', 'Shane', 'Abigail', 'Emily', 'Haley', 'Leah', 'Maru', 'Penny', 'Caroline', 'Clint', 'Demetrius', 'Evelyn', 'George', 'Gus', 'Jas', 'Jodi', 'Kent', 'Lewis', 'Linus', 'Marnie', 'Pam', 'Pierre', 'Robin', 'Vincent', 'Willy']

def createMail(nameString, reward, mailDataDictionary):
    mailString = ""
    if reward.typeString == "object":
        mailString = "Dear @,^Thank you for being my friend! I found this and thought you would like it.^  -" + nameString + "%item " + reward.typeString + " " + str(reward.id) + " " + str(reward.quantity) + " %%[#]" + nameString + " Friendship"
    else:
        mailString = "Dear @,^Thank you for being my friend! I found this and thought you would like it.^  -" + nameString + "%item " + reward.typeString + " " + str(reward.id) + " %%[#]" + nameString + " Friendship"
    mailDataDictionary[nameString + "_friend"] = MailData.MailData(nameString + "_friend", mailString)

def createEvent(id, nameString, eventDataDictionary):
    TARGET_FRIENDSHIP_VALUE = 250
    eventDataDictionary[EventData.generateFriendshipEventID(id, nameString, TARGET_FRIENDSHIP_VALUE)] = EventData.EventData(EventData.generateFriendshipEventID(id, nameString, TARGET_FRIENDSHIP_VALUE), "null")

# set the season a crop grows in to a random subset of the seasons
def shuffleCropSeasons(cropDataDictionary):
    seasons = ["spring", "summer", "fall", "winter"]
    
    for id, cropdata in cropDataDictionary.items():
        numSeasons = random.randint(1, len(seasons))
        cropdata.seasons = random.sample(seasons, numSeasons)

        #Parsnips must always grow in spring
        if id == "472":
            if not "spring" in cropdata.seasons:
                cropdata.seasons.append("spring")

# set all crops to grow in all seasons
def setAllSeasons(cropDataDictionary):
    seasons = ["spring", "summer", "fall", "winter"]
    for id, cropdata in cropDataDictionary.items():
        cropdata.seasons = seasons

# equivilent to randomizeCropGrowth with maxGrowthPeriod = 1
def shortenCropGrowth(cropDataDictionary):
    randomizeCropGrowth(cropDataDictionary, 1)

# crops grow in stages of various lengths; you see different sprites as they change stages.
# Randomize the number of days spent in each stage between 1 (theoretical minimum) and the specified max growth period per stage.
# If no max growth period is specified (<= 0), calculate the maximum number of days for each stage
# so that the crop can still grow once with in a season. This can be different for each crop; it depends on the number of growth stages.
# At this point I think it is still important to maintain the number of growth stages for each crop
def randomizeCropGrowth(cropDataDictionary, maxGrowthPeriod=-1):
    NUM_DAYS_PER_SEASON = 28
    maxGrowthPeriodPerStage = maxGrowthPeriod
    for id, cropdata in cropDataDictionary.items():
        if maxGrowthPeriod <= 0:
            maxGrowthPeriodPerStage = floor(NUM_DAYS_PER_SEASON / len(cropdata.growthStages))
        cropdata.growthStages = [random.randint(1, maxGrowthPeriod) for i in cropdata.growthStages]

# Shuffle the crop that gets harvested from each plant
# Only consider the items which are normally harvested from crops in the shuffling
def randomizeHarvestDrops(cropDataDictionary):
    allHarvestIds = [crop.harvestId for id, crop in cropDataDictionary.items()]
    for id, cropdata in cropDataDictionary.items():
        #pop removes and returns the item at the specified index
        cropdata.harvestId = allHarvestIds.pop(random.randint(0, len(allHarvestIds) - 1))

def chooseSpringCrops(cropDataDictionary, cropIDs):
    return [crop.harvestId for id, crop in cropDataDictionary.items() if crop.harvestId in cropIDs and "spring" in crop.seasons]

def chooseSpringFish(locationDataDict, fishIDs):
    allSpringFish = []
    for id, location in locationDataDict.items():
        if not id in ["Temp", "IslandSecret", "Woods", "Sewer", "BugLand", "WitchSwamp", "fishingGame"]:
            allSpringFish[len(allSpringFish):] = location.springFishIDs
    return [id for id in fishIDs if id in allSpringFish]

def chooseSpringForage(locationDataDict, forageIDs):
    allSpringForage = []
    for id, location in locationDataDict.items():
        if not id in ["Temp", "IslandSecret"]:
            allSpringForage[len(allSpringForage):] = location.springForageIDs
    return [forage for forage in forageIDs if forage in allSpringForage]

def getFishForRandomizing(fishDataDict):
    objects = [int(id) for id, obj in fishDataDict.items() if not obj.canCatchWithTrap]

    for x in [159, 160, 163, 682, 775, 898, 899, 900, 901, 902]:
        objects.remove(x)
    return objects

# Any basic item with category -15, -28, -16, -27, -26, -7, -75, -81, -4, -6, -5, -18, -79
# No radioactive, no legend fish (Crimsonfish, Angler, Legend, Glacierfish, Mutant Carp, son of Crimsonfish, ms. Angler, Legend 2, Glacierfish jr., Radioactive carp)
def getAllPossibleRequirementsForType(objectInfoDict, cropDataDictionary, fishDataDictionary, shuffledFishIDs, cat):
    VEGETABLE_ID = -75
    ORE_ID = -15
    FISH_ID = -4

    objects = [int(id) for id, obj in objectInfoDict.items() if (obj.category == cat)]

    #Make sure that all crops that we choose from will be in the seed
    if cat == VEGETABLE_ID:
        objects = [crop.harvestId for id, crop in cropDataDictionary.items()]

    if cat == FISH_ID and len(shuffledFishIDs) > 0:
        objects = shuffledFishIDs
    elif cat == FISH_ID and len(shuffledFishIDs) == 0:
        objects = getFishForRandomizing(fishDataDictionary)

    if cat == ORE_ID:
        for x in [909, 910]:
            objects.remove(x)

    requirements = []
    for id in objects:
        #Set random quality for vegetables
        if cat in [VEGETABLE_ID]:
            requirements.append(BundleData.BundleRequirement(id, 1, random.randint(0, 2)))
        else:
            requirements.append(BundleData.BundleRequirement(id, 1, 0))
    return requirements

def getEasyRequirementsForType(objectInfoDict, locationDataDict, cropDataDictionary, cat):
    VEGETABLE_ID = -75
    ORE_ID = -15
    FISH_ID = -4
    RESOURCE_ID = -16
    FORAGE_ID = -81
    EGG_ID = -5
    MILK_ID = -6

    objects = [int(id) for id, obj in objectInfoDict.items() if (obj.category == cat)]
    
    if cat == ORE_ID:
        #Remove iridium and radioactive
        for x in [909, 910, 337, 386]:
            objects.remove(x)
    elif cat == FISH_ID:
        #Remove boss fish, void salmon and slimejack
        for x in [159, 160, 163, 682, 775, 898, 899, 900, 901, 902, 795, 796]:
            objects.remove(x)
        objects = chooseSpringFish(locationDataDict, objects)
    elif cat == RESOURCE_ID:
        #Remove battery pack
        objects.remove(787)
    elif cat == EGG_ID:
        #Remove ostrich egg, void egg, duck egg and golden egg
        for x in [928, 289, 305, 442]:
            objects.remove(x)
    elif cat == MILK_ID:
        #Remove goat milk
        for x in [436, 438]:
            objects.remove(x)
    elif cat == FORAGE_ID:
        objects = chooseSpringForage(locationDataDict, objects)
    elif cat == VEGETABLE_ID:
        objects = chooseSpringCrops(cropDataDictionary, objects)

    requirements = []
    for id in objects:
        #Set random quality for vegetables
        if cat in [VEGETABLE_ID]:
            requirements.append(BundleData.BundleRequirement(id, 1, random.randint(0, 2)))
        else:
            requirements.append(BundleData.BundleRequirement(id, 1, 0))
    return requirements

def getAllPossibleRequirements(objectInfoDict, cropDataDictionary, fishDataDictionary, shuffledFishIDs, options):
    listOfCategories = []
    if "Crops" in options:
        listOfCategories.append(-75)
        listOfCategories.append(-79)
    if "Fish" in options:
        listOfCategories.append(-4)
    if "AnimalProd" in options:
        listOfCategories.append(-6)
        listOfCategories.append(-5)
        listOfCategories.append(-18)
    if "Cooking" in options:
        listOfCategories.append(-7)
    if "Forage" in options:
        listOfCategories.append(-16)
        listOfCategories.append(-81)
        listOfCategories.append(-27)
    if "Artisan" in options:
        listOfCategories.append(-26)
    if "Monster" in options:
        listOfCategories.append(-28)
    if "Ore" in options:
        listOfCategories.append(-15)

    requirements = []
    for cat in listOfCategories:
        requirements[len(requirements):] = getAllPossibleRequirementsForType(objectInfoDict, cropDataDictionary, fishDataDictionary, shuffledFishIDs, cat)
    return requirements

#An easy requirement is something that can be achieved in this first 2 weeks of spring (hopefully :) )
def getAllEasyRequirements(objectInfoDict, locationDataDict, cropDataDictionary, options):
    requirements = []
    listOfCategories= []
    if "Crops" in options:
        listOfCategories.append(-75)
    if "Fish" in options:
        listOfCategories.append(-4)
    if "AnimalProd" in options:
        listOfCategories.append(-6)
        listOfCategories.append(-5)
    if "Forage" in options:
        listOfCategories.append(-16)
        listOfCategories.append(-81)
        listOfCategories.append(-27)
    if "Monster" in options:
        listOfCategories.append(-28)
    if "Ore" in options:
        listOfCategories.append(-15)

    for cat in listOfCategories:
        requirements[len(requirements):] = getEasyRequirementsForType(objectInfoDict, locationDataDict, cropDataDictionary, cat)
    return requirements

def shuffleBundleRequirements(bundleDataDictionary, objectInfoDict, locationDataDict, cropDataDictionary, fishDataDictionary, shuffledFishIDs, options="Crops,Fish,AnimalProd,Forage,Artisan,Monster,Ore"):
    requirements = getAllPossibleRequirements(objectInfoDict, cropDataDictionary, fishDataDictionary, shuffledFishIDs, options)
    easyRequirements = getAllEasyRequirements(objectInfoDict, locationDataDict, cropDataDictionary, options)

    for id, bundle in bundleDataDictionary.items():
        if "Crafts Room" in id:
            bundle.numRequirementsToComplete = 1
            bundle.requirements = random.sample(easyRequirements, 4)
        elif not "Vault" in id:
            bundle.numRequirementsToComplete = 1
            bundle.requirements = random.sample(requirements, 4)

def setEarlySeedMaker(craftingDictionary):
    craftingDictionary["Seed Maker"].learnLevel = 1

def getAllIDsForCategory(objectInfoDict, catValue):
    return [int(id) for id, obj in objectInfoDict.items() if (obj.category == catValue)]

def get8CrowRewardsList(objectInfoDict, bigObjectDict, numVillagers):
    SEED_CATEGORY_VALUE = -74
    STARDROP_ID = 434
    FARM_TOTEM_ID = 688
    ISLAND_TOTEM_ID = 886
    DESERT_TOTEM_ID = 261
    SEA_DISH_ID = 242
    MINE_DISH_ID = 243
    LUCK_DISH_ID = 204
    CRAB_CAKE_ID = 732
    LIGHTNING_ROD_ID = 9
    DIAMOND_ID = 72
    TOTAL_CHECKS = 38 + numVillagers

    listRarecrowID = [id for id, obj in bigObjectDict.items() if (obj.name == "Rarecrow")]
    listSeedIDs = getAllIDsForCategory(objectInfoDict, SEED_CATEGORY_VALUE)

    rewards = []
    for id in listRarecrowID:
        rewards.append(Reward("bigobject", id, 1))
    rewards.append(Reward("object", STARDROP_ID, 1))
    rewards.append(Reward("object", STARDROP_ID, 1))
    rewards.append(Reward("object", STARDROP_ID, 1))
    rewards.append(Reward("object", STARDROP_ID, 1))
    rewards.append(Reward("object", STARDROP_ID, 1))
    rewards.append(Reward("object", FARM_TOTEM_ID, 999))
    rewards.append(Reward("object", FARM_TOTEM_ID, 999))
    rewards.append(Reward("object", FARM_TOTEM_ID, 999))
    rewards.append(Reward("object", ISLAND_TOTEM_ID, 100))
    rewards.append(Reward("object", ISLAND_TOTEM_ID, 100))
    rewards.append(Reward("object", ISLAND_TOTEM_ID, 100))
    rewards.append(Reward("object", DESERT_TOTEM_ID, 100))
    rewards.append(Reward("object", DESERT_TOTEM_ID, 100))
    rewards.append(Reward("object", DESERT_TOTEM_ID, 100))
    rewards.append(Reward("object", SEA_DISH_ID, 100))
    rewards.append(Reward("object", MINE_DISH_ID, 100))
    rewards.append(Reward("object", LUCK_DISH_ID, 100))
    rewards.append(Reward("object", CRAB_CAKE_ID, 100))
    rewards.append(Reward("bigobject", LIGHTNING_ROD_ID, 1))
    rewards.append(Reward("bigobject", LIGHTNING_ROD_ID, 1))
    rewards.append(Reward("bigobject", LIGHTNING_ROD_ID, 1))

    for id in random.sample(listSeedIDs, numVillagers):
        rewards.append(Reward("object", id, 100))

    #Fill the rest of the slots with 100 Diamonds (functions as cash or friendship items)
    for i in range(TOTAL_CHECKS - len(rewards)):
        rewards.append(Reward("object", DIAMOND_ID, 100))

    return rewards

def place8CrowRewards(bundleDataDictionary, mailDataDictionary, eventDataDictionary, objectInfoDict, bigObjectDict, numVillagers):
    rewards = get8CrowRewardsList(objectInfoDict, bigObjectDict, numVillagers)
    hints = []
    rewardString = ""

    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["mom1"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad1"].setRewardString(reward.typeString, reward.id, reward.quantity)

    if reward.typeString == "object":
        rewardString = objectInfoDict[str(reward.id)].name
    else:
        rewardString = bigObjectDict[str(reward.id)].name
    hints.append("Oh, Mom and Dad are on TV. Sounds like they are sending me " + rewardString)
    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["mom2"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad2"].setRewardString(reward.typeString, reward.id, reward.quantity)

    if reward.typeString == "object":
        rewardString = objectInfoDict[str(reward.id)].name
    else:
        rewardString = bigObjectDict[str(reward.id)].name
    hints.append("Oh, Mom and Dad are on TV. Sounds like they are sending me " + rewardString)
    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["mom3"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad3"].setRewardString(reward.typeString, reward.id, reward.quantity)

    if reward.typeString == "object":
        rewardString = objectInfoDict[str(reward.id)].name
    else:
        rewardString = bigObjectDict[str(reward.id)].name
    hints.append("Oh, Mom and Dad are on TV. Sounds like they are sending me " + rewardString)
    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["mom4"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad4"].setRewardString(reward.typeString, reward.id, reward.quantity)

    if reward.typeString == "object":
        rewardString = objectInfoDict[str(reward.id)].name
    else:
        rewardString = bigObjectDict[str(reward.id)].name
    hints.append("Oh, Mom and Dad are on TV. Sounds like they are sending me " + rewardString)

    for mail in ["QiChallengeComplete", "fishing2", "fishing6", "ccBulletinThankYou"]:
        reward = rewards.pop(random.randint(0, len(rewards)-1))
        mailDataDictionary[mail].setRewardString(reward.typeString, reward.id, reward.quantity)

        if reward.typeString == "object":
            rewardString = objectInfoDict[str(reward.id)].name
        else:
            rewardString = bigObjectDict[str(reward.id)].name
        hints.append("Check your mail! " + mail + " gives " + rewardString)

    villagers = getNamesOfVillagers()
    i = 420
    for name in random.sample(villagers, numVillagers):
        reward = rewards.pop(random.randint(0, len(rewards)-1))
        createEvent(i, name, eventDataDictionary)
        createMail(name, reward, mailDataDictionary)
        if reward.typeString == "money":
            rewardString = str(reward.quantity) + 'g'
        elif reward.typeString == "object":
            rewardString = objectInfoDict[str(reward.id)].name
        else:
            rewardString = bigObjectDict[str(reward.id)].name
        hints.append(name + " here! I'll give ya " + rewardString + " if you help me out.")
        i = i + 1

    for id, bundle in bundleDataDictionary.items():
        if not id == "Abandoned Joja Mart/36":
            reward = rewards.pop(random.randint(0, len(rewards)-1))
            if reward.typeString == "object":
                bundle.reward = BundleData.BundleReward("O", reward.id, reward.quantity)
            else:
                bundle.reward = BundleData.BundleReward("BO", reward.id, reward.quantity)
            if reward.typeString == "object":
                hints.append("This just in! Completing " + bundle.name + " bundle gives " + objectInfoDict[str(reward.id)].name)
            else:
                hints.append("This just in! Completing " + bundle.name + " bundle gives " + bigObjectDict[str(reward.id)].name)
    return hints

def setHintsInTipChannel(tipChannelDict, listOfHints):
    tipChannelKeys = list(tipChannelDict.keys())
    numHintsToSet = 0
    if len(tipChannelKeys) < len(listOfHints):
        numHintsToSet = len(tipChannelKeys)
    else:
        numHintsToSet = len(listOfHints)
    for i in range(numHintsToSet):
        tipChannelDict[tipChannelKeys[i]].setHintString(listOfHints.pop(random.randint(0, len(listOfHints)-1)))

def randomizeFish(locationDataDict, fishDataDict):
    fishList = []
    fishIDList = getFishForRandomizing(fishDataDict)
    for id, location in locationDataDict.items():
        if not id in ["Temp"]:
            if len(location.springFishChance) > 0:
                location.springFishIDs = random.sample(fishIDList, len(location.springFishIDs))
                fishList = fishList + location.springFishIDs
            if len(location.summerFishChance) > 0:
                location.summerFishIDs = random.sample(fishIDList, len(location.summerFishIDs))
                fishList = fishList + location.summerFishIDs
            if len(location.fallFishChance) > 0:
                location.fallFishIDs = random.sample(fishIDList, len(location.fallFishIDs))
                fishList = fishList + location.fallFishIDs
            if len(location.winterFishChance) > 0:
                location.winterFishIDs = random.sample(fishIDList, len(location.winterFishIDs))
                fishList = fishList + location.winterFishIDs
    #Convert to a set to uniquify the list
    return list(set(fishList))

def randomizeForage(locationDataDict, forageIDList):
    forage = []
    for id, location in locationDataDict.items():
        if not id in ["Temp", ]:
            if len(location.springForageChance) > 0:
                location.springForageIDs = random.sample(forageIDList, len(location.springForageIDs))
                forage = forage + location.springForageIDs
            if len(location.summerForageChance) > 0:
                location.summerForageIDs = random.sample(forageIDList, len(location.summerForageIDs))
                forage = forage + location.summerForageIDs
            if len(location.fallForageChance) > 0:
                location.fallForageIDs = random.sample(forageIDList, len(location.fallForageIDs))
                forage = forage + location.fallForageIDs
            if len(location.winterForageChance) > 0:
                location.winterForageIDs = random.sample(forageIDList, len(location.winterForageIDs))
                forage = forage + location.winterForageIDs
    #Convert to a set to uniquify the list
    return list(set(forage))

#Uses a different hint system than 
def place8CrowRewardsV2(bundleDataDictionary, mailDataDictionary, eventDataDictionary, objectInfoDict, bigObjectDict, numVillagers):
    rewards = get8CrowRewardsList(objectInfoDict, bigObjectDict, numVillagers)
    hints = []
    RARECROW_IDS = [110, 113, 126, 136, 137, 138, 139, 140]
    rewardString = ""
    rarecrowPlaced = False

    reward = rewards.pop(random.randint(0, len(rewards)-1))
    if reward.typeString != "object" and reward.id in RARECROW_IDS:
        rarecrowPlaced = True
    mailDataDictionary["mom1"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad1"].setRewardString(reward.typeString, reward.id, reward.quantity)

    reward = rewards.pop(random.randint(0, len(rewards)-1))
    if reward.typeString != "object" and reward.id in RARECROW_IDS:
        rarecrowPlaced = True
    mailDataDictionary["mom2"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad2"].setRewardString(reward.typeString, reward.id, reward.quantity)

    reward = rewards.pop(random.randint(0, len(rewards)-1))
    if reward.typeString != "object" and reward.id in RARECROW_IDS:
        rarecrowPlaced = True
    mailDataDictionary["mom3"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad3"].setRewardString(reward.typeString, reward.id, reward.quantity)

    reward = rewards.pop(random.randint(0, len(rewards)-1))
    if reward.typeString != "object" and reward.id in RARECROW_IDS:
        rarecrowPlaced = True
    mailDataDictionary["mom4"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad4"].setRewardString(reward.typeString, reward.id, reward.quantity)

    if rarecrowPlaced:
        hints.append("Your grandfather gave a Rarecrow to your parents to give you when you are ready. Check your mail!")
        rarecrowPlaced = False
    else:
        hints.append("Mail from your parents does not give a Rarecrow")

    for mail in ["fishing2", "fishing6"]:
        reward = rewards.pop(random.randint(0, len(rewards)-1))
        mailDataDictionary[mail].setRewardString(reward.typeString, reward.id, reward.quantity)

        if reward.typeString != "object" and reward.id in RARECROW_IDS:
            rarecrowPlaced = True

    if rarecrowPlaced:
        hints.append("Did I ever tell you about the time your grandfather caught a Rarecrow while fishing? He was reel talented, he was.")
        rarecrowPlaced = False
    else:
        hints.append("There are no rarecrows from fishing levels")

    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["QiChallengeComplete"].setRewardString(reward.typeString, reward.id, reward.quantity)

    if reward.typeString != "object" and reward.id in RARECROW_IDS:
        hints.append("Did I ever tell you about the time your grandfather completed Qi's challenge? He told me he found a Rarecrow at the end of it.")
    else:
        hints.append("Qi's Challenge does not give a Rarecrow.")

    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["ccBulletinThankYou"].setRewardString(reward.typeString, reward.id, reward.quantity)

    if reward.typeString != "object" and reward.id in RARECROW_IDS:
        hints.append("Did I ever tell you about the time your grandfather completed all the bulletin board bundles? Mayor Lewis was so happy he gave your grandfather a Rarecrow.")
    else:
        hints.append("The bulletin board thank you letter does not contain a Rarecrow.")
        
    villagers = getNamesOfVillagers()
    i = 420
    for name in random.sample(villagers, numVillagers):
        reward = rewards.pop(random.randint(0, len(rewards)-1))
        createEvent(i, name, eventDataDictionary)
        createMail(name, reward, mailDataDictionary)
        if reward.typeString != "object" and reward.id in RARECROW_IDS:
            rarecrowPlaced = True
        i += 1

    if rarecrowPlaced:
        hints.append("Did I ever tell you about the time your grandfather helped the villagers? They were so greatful, they gave him a Rarecrow.")
        rarecrowPlaced = False
    else:
        hints.append("Villager friendship does not give a Rarecrow.")

    importantBundles = { "Pantry":False, "Fish Tank":False, "Crafts Room":False, "Boiler Room":False, "Vault":False, "Bulletin Board":False}
    for id, bundle in bundleDataDictionary.items():
        if not id == "Abandoned Joja Mart/36":
            reward = rewards.pop(random.randint(0, len(rewards)-1))
            if reward.typeString == "object":
                bundle.reward = BundleData.BundleReward("O", reward.id, reward.quantity)
            else:
                bundle.reward = BundleData.BundleReward("BO", reward.id, reward.quantity)
                if reward.id in RARECROW_IDS:
                    importantBundles[id.split('/')[0]] = True

    for b, isImportant in importantBundles.items():
        if isImportant:
            hints.append("Your grandfather put a Rarecrow in one of the " + b + " bundles.")
        else:
            hints.append("There are no Rarecrows in the " + b + " bundles.")

    return hints 