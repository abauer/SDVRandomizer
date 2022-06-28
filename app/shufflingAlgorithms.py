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

def chooseRewards(bigObjectDict, objectDict, options="8Crow"):
    listRarecrowID = [id for id, obj in bigObjectDict.items() if (obj.name == "Rarecrow")]
    listBigObjectID = [id for id, obj in bigObjectDict.items()]
    listObjectID = [id for id, obj in objectDict.items() if (obj.type in ["Seeds", "Fish", "Crafting"])]

    NUM_BUNDLES_TO_SHUFFLE = 30
    if "8Crow" in options:
        NUM_BUNDLES_TO_SHUFFLE = NUM_BUNDLES_TO_SHUFFLE - len(listRarecrowID)
    numBigRewards = random.randint(0, NUM_BUNDLES_TO_SHUFFLE)
    numSmallRewards = NUM_BUNDLES_TO_SHUFFLE - numBigRewards

    #remove rarecrows from general pool because we will add them at the end
    if "8Crow" in options:
        for id in listRarecrowID:
            listBigObjectID.remove(id)

    rewards = [BundleData.BundleReward("BO", id, 1) for id in random.sample(listBigObjectID, numBigRewards)]
    rewards[len(rewards):] = [BundleData.BundleReward("O", id, random.randint(1, 30)) for id in random.sample(listObjectID, numSmallRewards)]
    if "8Crow" in options:
        rewards[len(rewards):] = [BundleData.BundleReward("B0", id, 1) for id in listRarecrowID]
    return rewards

def shuffleBundleRewards(bundleDataDictionary, possibleRewards):
    for id, bundleData in bundleDataDictionary.items():
        if not id == "Abandoned Joja Mart/36":
            bundleData.reward = possibleRewards.pop(random.randint(0, len(possibleRewards) -1))

# Any basic item with category -15, -28, -16, -27, -26, -7, -75, -81, -4, -6, -5, -18, -79
# No radioactive, no legend fish (Crimsonfish, Angler, Legend, Glacierfish, Mutant Carp, son of Crimsonfish, ms. Angler, Legend 2, Glacierfish jr., Radioactive carp)
def getAllObjectsForType(objectInfoDict, cat):
    VEGETABLE_ID = -75
    FRUIT_ID = -79
    ORE_ID = -15
    FISH_ID = -4

    objects = [int(id) for id, obj in objectInfoDict.items() if (obj.category == cat)]
    
    if cat == ORE_ID:
        for x in [909, 910]:
            objects.remove(x)
    elif cat == FISH_ID:
        for x in [159, 160, 163, 682, 775, 898, 899, 900, 901, 902]:
            objects.remove(x)

    requirements = []
    for id in objects:
        if cat in [VEGETABLE_ID, FRUIT_ID]:
            requirements.append(BundleData.BundleRequirement(id, random.randint(1, 3) * 5, random.randint(0, 2)))
        else:
            requirements.append(BundleData.BundleRequirement(id, random.randint(1, 3) * 5, 0))
    return requirements

def shuffleBundleRequirements(bundleDataDictionary, objectInfoDict, options="Crops,Fish,AnimalProd,Forage,Artisan,Monster,Ore"):
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
        requirements[len(requirements):] = getAllObjectsForType(objectInfoDict, cat)

    for id, bundle in bundleDataDictionary.items():
        if not "Vault" in id:
            bundle.numRequirementsToComplete = random.randint(2, 6)
            bundle.requirements = random.sample(requirements, random.randint(bundle.numRequirementsToComplete, 10))

def setEarlySeedMaker(craftingDictionary):
    craftingDictionary["Seed Maker"].learnLevel = 1

def getAllIDsForCategory(objectInfoDict, catValue):
    return [int(id) for id, obj in objectInfoDict.items() if (obj.category == catValue)]

def get8CrowRewardsList(objectInfoDict, bigObjectDict):
    SEED_CATEGORY_VALUE = -74
    STARDROP_ID = 434
    FARM_TOTEM_ID = 688
    ISLAND_TOTEM_ID = 886
    DESERT_TOTEM_ID = 261
    SEA_DISH_ID = 242
    MINE_DISH_ID = 243
    LUCK_DISH_ID = 204
    LIGHTNING_ROD_ID = 9
    TRASH_ID = 168

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
    rewards.append(Reward("bigobject", LIGHTNING_ROD_ID, 1))
    rewards.append(Reward("bigobject", LIGHTNING_ROD_ID, 1))
    rewards.append(Reward("bigobject", LIGHTNING_ROD_ID, 1))
    rewards.append(Reward("bigobject", LIGHTNING_ROD_ID, 1))

    for id in random.sample(listSeedIDs, 26):
        rewards.append(Reward("object", id, 100))

    #Fill the rest of the slots with trash
    for i in range(67 - len(rewards)):
        rewards.append(Reward("object", TRASH_ID, 1))

    return rewards

def place8CrowRewards(bundleDataDictionary, mailDataDictionary, eventDataDictionary, objectInfoDict, bigObjectDict):
    rewards = get8CrowRewardsList(objectInfoDict, bigObjectDict)
    hints = []

    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["mom1"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad1"].setRewardString(reward.typeString, reward.id, reward.quantity)
    if reward.typeString == "object":
        hints.append("Oh, mom and dad are on TV. Sounds like they are sending me " + objectInfoDict[str(reward.id)].name)
    else:
        hints.append("Oh, mom and dad are on TV. Sounds like they are sending me " + bigObjectDict[str(reward.id)].name)
    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["mom2"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad2"].setRewardString(reward.typeString, reward.id, reward.quantity)
    if reward.typeString == "object":
        hints.append("Oh, mom and dad are on TV. Sounds like they are sending me " + objectInfoDict[str(reward.id)].name)
    else:
        hints.append("Oh, mom and dad are on TV. Sounds like they are sending me " + bigObjectDict[str(reward.id)].name)
    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["mom3"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad3"].setRewardString(reward.typeString, reward.id, reward.quantity)
    if reward.typeString == "object":
        hints.append("Oh, mom and dad are on TV. Sounds like they are sending me " + objectInfoDict[str(reward.id)].name)
    else:
        hints.append("Oh, mom and dad are on TV. Sounds like they are sending me " + bigObjectDict[str(reward.id)].name)
    reward = rewards.pop(random.randint(0, len(rewards)-1))
    mailDataDictionary["mom4"].setRewardString(reward.typeString, reward.id, reward.quantity)
    mailDataDictionary["dad4"].setRewardString(reward.typeString, reward.id, reward.quantity)
    if reward.typeString == "object":
        hints.append("Oh, mom and dad are on TV. Sounds like they are sending me " + objectInfoDict[str(reward.id)].name)
    else:
        hints.append("Oh, mom and dad are on TV. Sounds like they are sending me " + bigObjectDict[str(reward.id)].name)

    for mail in ["QiChallengeComplete", "fishing2", "fishing6", "ccBulletinThankYou"]:
        reward = rewards.pop(random.randint(0, len(rewards)-1))
        mailDataDictionary[mail].setRewardString(reward.typeString, reward.id, reward.quantity)
        if reward.typeString == "object":
            hints.append("Check your mail! " + mail + " gives " + objectInfoDict[str(reward.id)].name)
        else:
            hints.append("Check your mail! " + mail + " gives " + bigObjectDict[str(reward.id)].name)

    villagers = getNamesOfVillagers()
    i = 420
    for name in villagers:
        reward = rewards.pop(random.randint(0, len(rewards)-1))
        createEvent(i, name, eventDataDictionary)
        createMail(name, reward, mailDataDictionary)
        if reward.typeString == "object":
            hints.append(name + " gives " + objectInfoDict[str(reward.id)].name)
        else:
            hints.append(name + " gives " + bigObjectDict[str(reward.id)].name)
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