import json
from pathlib import Path 

# This class holds all settings for crops
# Can parse the crop data strings and write new crop data strings

class CropData:

    def __init__(self, id, cropsSettingString):
        self.id = int(id)
        self.growthStages = []
        self.seasons = []
        self.spriteIndex = 0
        self.harvestId = 0
        self.regrowPeriod = -1
        self.harvestMethod = 0
        self.canExtraHarvest = False
        self.extraHarvestRange = []
        self.extraHarvestChance = 0.0
        self.raisedSeed = False
        self.hasTintColor = False
        self.tintColor = []
        
        self.parseSettingString(cropsSettingString)

    def parseSettingString(self, settingString):
        settings = settingString.split('/')
        extraHarvestStrings = settings[6].split(' ')
        
        self.growthStages = [int(growthStage) for growthStage in settings[0].split(' ')]
        self.seasons = [str for str in settings[1].split(' ')]
        self.spriteIndex = int(settings[2])
        self.harvestId = int(settings[3])
        self.regrowPeriod = int(settings[4])
        self.harvestMethod = int(settings[5])
        self.canExtraHarvest = (extraHarvestStrings[0] == "true")
        if self.canExtraHarvest:
            self.extraHarvestRange = [int(str) for str in extraHarvestStrings[1:4]]
            self.extraHarvestChance = float(extraHarvestStrings[4])
        self.raisedSeed = (settings[7] == "true")
        self.hasTintColor = (settings[8].split(' ')[0] == "true")
        if self.hasTintColor:
            self.tintColor = [int(str) for str in settings[8].split(' ')[1:]]

    def toSettingString(self):
        settingsStrings = []
        settingsStrings.append(" ".join([str(gs) for gs in self.growthStages]))
        settingsStrings.append(" ".join(self.seasons))
        settingsStrings.append(str(self.spriteIndex))
        settingsStrings.append(str(self.harvestId))
        settingsStrings.append(str(self.regrowPeriod))
        settingsStrings.append(str(self.harvestMethod))
        if self.canExtraHarvest:
            settingsStrings.append("true " + " ".join([str(setting) for setting in self.extraHarvestRange]) + " " + str(self.extraHarvestChance))
        else:
            settingsStrings.append("false")
        settingsStrings.append(str(self.raisedSeed).lower())
        if self.hasTintColor:
            settingsStrings.append("true " + " ".join([str(setting) for setting in self.tintColor]))
        else:
            settingsStrings.append("false")
        
        return "/".join(settingsStrings)

def readCropsFile(rootFilePath):
    CROPS_FILE = rootFilePath + "\Data\Crops.json"
    file = open(CROPS_FILE, "r")
    stardewJsonData = json.load(file)
    
    settingsDictionary = {}
    for key, val in stardewJsonData.items():
        settingsDictionary[key] = CropData(key, val)
    return settingsDictionary

def writeCropsFile(settingsDictionary):
    RANDOMIZED_CROPS_FILE = Path.cwd() / "randomizedCrops.json"
    file = open(RANDOMIZED_CROPS_FILE, "w+")

    cropsJSONData = {}
    for id, settingsObject in settingsDictionary.items():
        cropsJSONData[id] = settingsObject.toSettingString()
    json.dump(cropsJSONData, file, indent=2)