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
import DataObjects.QuestData as QuestData
import DataObjects.MailData as MailData
import DataObjects.TipChannelData as TipChannelData
import DataObjects.EventData as EventData

import ContentJSONHelper
import shufflingAlgorithms as sa

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
        opts, extra = getopt.getopt(argv[1:], "", ["shuffle-seasons", "all-seasons", "short-growth", "shuffle-harvest", "earlySeedMaker", "shuffle-fish", "shuffle-forage", "numVillagers=", "random-seed=", "Unpacked-folder="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    return opts

if __name__ == "__main__":
    cmdArgs = parseArgs(sys.argv)
    unpackedFilePath = Path("C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Content (unpacked)")

    setSeed = False
    for opt, arg in cmdArgs:
        if opt == "--random-seed":
            random.seed(int(arg))
            setSeed = True
        elif opt == "--Unpacked-folder":
            unpackedFilePath = Path(arg)

    if not setSeed:
        seed = random.getrandbits(64)
        random.seed(seed)
        print(seed)

    cropsSettings = readUnpackedXNB(CropData.CropData, unpackedFilePath / "Data" / "Crops.json")
    bundleSettings = readUnpackedXNB(BundleData.BundleData, unpackedFilePath / "Data" / "Bundles.json")
    fishSettings = readUnpackedXNB(FishData.FishData, unpackedFilePath / "Data" / "Fish.json")
    fruitTreeSettings = readUnpackedXNB(FruitTrees.FruitTreeData, unpackedFilePath / "Data" / "fruitTrees.json")
    animalSettings = readUnpackedXNB(AnimalData.AnimalData, unpackedFilePath / "Data" / "FarmAnimals.json")
    cookingSettings = readUnpackedXNB(RecipeData.RecipeData, unpackedFilePath / "Data" / "CookingRecipes.json")
    craftingSettings = readUnpackedXNB(RecipeData.RecipeData, unpackedFilePath / "Data" / "CraftingRecipes.json")    
    locationSettings = readUnpackedXNB(LocationData.LocationData, unpackedFilePath / "Data" / "Locations.json")
    objectInfo = readUnpackedXNB(ObjectInfoData.ObjectInfoData, unpackedFilePath / "Data" / "ObjectInformation.json")
    bigObjectInfo = readUnpackedXNB(ObjectInfoData.BigObjectInfoData, unpackedFilePath / "Data" / "BigCraftablesInformation.json")
    eventSettings = readUnpackedXNB(EventData.EventData, unpackedFilePath / "Data" / "Events" / "Farm.json")
    mailSettings = readUnpackedXNB(MailData.MailData, unpackedFilePath / "Data" / "mail.json")
    tipChannelSettings = readUnpackedXNB(TipChannelData.TipChannelData, unpackedFilePath / "Data" / "TV" / "TipChannel.json")

    numVillagers = 29
    shuffledFish = []
    shuffledForage = []
    for opt, arg in cmdArgs:
        if opt == "--shuffle-seasons":
            sa.shuffleCropSeasons(cropsSettings)
        elif opt == "--all-seasons":
            sa.setAllSeasons(cropsSettings)
        elif opt == "--short-growth":
            sa.shortenCropGrowth(cropsSettings)
        elif opt == "--shuffle-harvest":
            sa.randomizeHarvestDrops(cropsSettings)
        elif opt == "--earlySeedMaker":
            sa.setEarlySeedMaker(craftingSettings)
        elif opt == "--numVillagers":
            numVillagers = arg
        elif opt == "--shuffle-fish":
            shuffledFish = sa.randomizeFish(locationSettings, objectInfo)

    # Make sure we shuffle the forage after any crop shuffling
    for opt, arg in cmdArgs:
        if opt == "--shuffle-forage":
            listOfIDs = [req.id for req in sa.getAllPossibleRequirements(objectInfo, cropsSettings, shuffledFish, "Fish,AnimalProd,Forage,Artisan")]
            shuffledForage = sa.randomizeForage(locationSettings, listOfIDs)

    sa.shuffleBundleRequirements(bundleSettings, objectInfo, locationSettings, cropsSettings, shuffledFish)
    hints = sa.place8CrowRewards(bundleSettings, mailSettings, eventSettings, objectInfo, bigObjectInfo, numVillagers)
    sa.setHintsInTipChannel(tipChannelSettings, hints)
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
    writeDataFile(str(outputDirectory / "updatedFarmEvents.json"), eventSettings)
    writeDataFile(str(outputDirectory / "randomizedMail.json"), mailSettings)
    writeDataFile(str(outputDirectory / "updatedObjectInformation.json"), objectInfo)
    writeDataFile(str(outputDirectory / "updatedTipChannel.json"), tipChannelSettings)
    ContentJSONHelper.writeContentJSON(outputDirectory)
