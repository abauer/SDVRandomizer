import DataObjects.CropData as CropData
import DataObjects.ObjectInfoData as ObjectInfoData
import DataObjects.BundleData as BundleData
import DataObjects.FishData as FishData
import DataObjects.FruitTreeData as FruitTrees
import DataObjects.AnimalData as AnimalData
import DataObjects.RecipeData as RecipeData
import DataObjects.LocationData as LocationData

import random

# set the season a crop grows in to a random subset of the seasons
def shuffleCropSeasons(cropDataDictionary):
    seasons = ["spring", "summer", "fall", "winter"]
    
    for id, cropdata in cropDataDictionary.items():
        numSeasons = random.randint(1, len(seasons))
        cropdata.seasons = random.sample(seasons, numSeasons)

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

# Any basic item with category -15 except radioactive
# Any basic item with category -28, -16, -27, -26, -7, -75, -81, -4, -6, -5, -18, -79
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

def shuffleBundleRequirements(bundleDataDictionary, objectInfoDict, options="Crops,Fish,AnimalProd,Cooking,Forage,Artisan,Monster,Ore"):
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
    