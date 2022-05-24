import sys
import getopt
import random

import DataObjects.CropData as CropData
import DataObjects.ObjectInfoData as ObjectInfoData
import DataObjects.BundleData as BundleData
import ContentJSONHelper

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

def parseArgs(argv):

    try:
        opts, extra = getopt.getopt(argv[1:], "saghr:", ["shuffle-seasons", "all-seasons", "short-growth", "shuffle-harvest", "random-seed="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    return opts

if __name__ == "__main__":
    cmdArgs = parseArgs(sys.argv)
    cropsSettings = CropData.readCropsFile()

    setSeed = False
    for opt, arg in cmdArgs:
        if opt in ["-r", "--random-seed"]:
            random.seed(int(arg))
            setSeed = True

    if not setSeed:
        seed = random.getrandbits(64)
        random.seed(seed)
        print(seed)

    
    for opt, arg in cmdArgs:
        if opt in ["-s", "--shuffle-seasons"]:
            shuffleCropSeasons(cropsSettings)
            
        elif opt in ["-a", "--all-seasons"]:
            setAllSeasons(cropsSettings)
        elif opt in ["-g", "--short-growth"]:
            shortenCropGrowth(cropsSettings)
        elif opt in ["-h", "--shuffle-harvest"]:
            randomizeHarvestDrops(cropsSettings)

    bundleSettings = BundleData.readBundlesFile()
    BundleData.writeBundlesFile(bundleSettings)
    CropData.writeCropsFile(cropsSettings)
    
    objectInfo = ObjectInfoData.readObjectInfoFile()
    ObjectInfoData.updateCropDescriptions(cropsSettings, objectInfo)
    ObjectInfoData.writeObjectInfoFile(objectInfo)
    ContentJSONHelper.writeContentJSON()
