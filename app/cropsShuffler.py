import sys
import getopt
import random
from pathlib import Path
import json

import DataObjects.CropData as CropData
import DataObjects.ObjectInfoData as ObjectInfoData
import DataObjects.BundleData as BundleData
import DataObjects.FishData as FishData
import DataObjects.FruitTreeData as FruitTrees
import DataObjects.AnimalData as AnimalData
import DataObjects.RecipeData as RecipeData
import DataObjects.LocationData as LocationData

import ContentJSONHelper
import shufflingAlgorithms

def readUnpackedXNB(DataClassType, filePath):
    file = open(filePath, "r")
    stardewJsonData = json.load(file)
    
    settingsDictionary = {}
    for key, val in stardewJsonData.items():
        settingsDictionary[key] = DataClassType(key, val)
    return settingsDictionary

def writeDataFile(filepath, settingsDictionary):
    file = open(filepath, "w+")

    jsonData = {}
    for id, settingsObject in settingsDictionary.items():
        jsonData[id] = settingsObject.toSettingString()
    json.dump(jsonData, file, indent=2)



def parseArgs(argv):

    try:
        opts, extra = getopt.getopt(argv[1:], "saghr:f:", ["shuffle-seasons", "all-seasons", "short-growth", "shuffle-harvest", "random-seed=", "Unpacked-folder="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    return opts

if __name__ == "__main__":
    cmdArgs = parseArgs(sys.argv)
    unpackedFilePath = Path("C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Content (unpacked)")

    setSeed = False
    for opt, arg in cmdArgs:
        if opt in ["-r", "--random-seed"]:
            random.seed(int(arg))
            setSeed = True
        elif opt in ["-f", "--Unpacked-folder"]:
            unpackedFilePath = Path(arg)

    if not setSeed:
        seed = random.getrandbits(64)
        random.seed(seed)
        print(seed)

    cropsSettings = readUnpackedXNB(CropData.CropData, unpackedFilePath / "Data" / "Crops.json")
    
    for opt, arg in cmdArgs:
        if opt in ["-s", "--shuffle-seasons"]:
            shuffleCropSeasons(cropsSettings)
        elif opt in ["-a", "--all-seasons"]:
            setAllSeasons(cropsSettings)
        elif opt in ["-g", "--short-growth"]:
            shortenCropGrowth(cropsSettings)
        elif opt in ["-h", "--shuffle-harvest"]:
            randomizeHarvestDrops(cropsSettings)

    bundleSettings = readUnpackedXNB(BundleData.BundleData, unpackedFilePath / "Data" / "Bundles.json")
    fishSettings = readUnpackedXNB(FishData.FishData, unpackedFilePath / "Data" / "Fish.json")
    fruitTreeSettings = readUnpackedXNB(FruitTrees.FruitTreeData, unpackedFilePath / "Data" / "fruitTrees.json")
    animalSettings = readUnpackedXNB(AnimalData.AnimalData, unpackedFilePath / "Data" / "FarmAnimals.json")
    cookingSettings = readUnpackedXNB(RecipeData.RecipeData, unpackedFilePath / "Data" / "CookingRecipes.json")
    craftingSettings = readUnpackedXNB(RecipeData.RecipeData, unpackedFilePath / "Data" / "CraftingRecipes.json")
    locationSettings = readUnpackedXNB(LocationData.LocationData, unpackedFilePath / "Data" / "Locations.json")
    objectInfo = readUnpackedXNB(ObjectInfoData.ObjectInfoData, unpackedFilePath / "Data" / "ObjectInformation.json")
    ObjectInfoData.updateCropDescriptions(cropsSettings, objectInfo)

    outputDirectory = Path.cwd() / "bin"
    outputDirectory.mkdir(exist_ok=True)

    writeDataFile(str(outputDirectory / "randomizedBundles.json"), bundleSettings)
    writeDataFile(str(outputDirectory / "randomizedCrops.json"), cropsSettings)
    writeDataFile(str(outputDirectory / "randomizedFish.json"), fishSettings)
    writeDataFile(str(outputDirectory / "randomizedFruitTrees.json"), fruitTreeSettings)
    writeDataFile(str(outputDirectory / "randomizedAnimals.json"), animalSettings)
    writeDataFile(str(outputDirectory / "randomizedCooking.json"), cookingSettings)
    writeDataFile(str(outputDirectory / "randomizedCrafting.json"), craftingSettings)
    writeDataFile(str(outputDirectory / "randomizedLocations.json"), locationSettings)
    writeDataFile(str(outputDirectory / "updatedObjectInformation.json"), objectInfo)
    ContentJSONHelper.writeContentJSON(outputDirectory)
