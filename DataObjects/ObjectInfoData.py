import json
from pathlib import Path
from .CropData import CropData

#Class to store information from ObjectInformation.xnb
#Mostly used to update item descriptions

class ObjectInfoData:

    def __init__(self, id, settingString):
        self.id = int(id)
        self.name = ""
        self.price = 0
        self.edibility = -300 #Stands for inedible
        self.type = "Basic"
        self.category = 1 # this number is always negative for valid entries
        self.translatedName = ""
        self.description = ""
        
        #The next attributes are only used for food and drinks
        self.foodType = ""
        self.buffs = []
        self.buffDuration = 0

        #The next attribute is only for geodes
        self.geodeDropTable = []

        #The following are only for artifacts
        self.artSpawnLocations = []
        self.artSpawnChances = []
        self.artifactOtherStuff = ""

        #The following are only for fish
        self.fishTimeOfDay = []
        self.fishLocations = []

        self.parseSettingsString(settingString)

    def parseSettingsString(self, settingString):
        settings = settingString.split('/')
        self.name = settings[0]
        self.price = int(settings[1])
        self.edibility = int(settings[2])
        typeAndCategory = settings[3].split(' ')
        if len(typeAndCategory) > 1:
            self.type = typeAndCategory[0]
            self.category = int(typeAndCategory[1])
        else:
            self.type = typeAndCategory[0]
        self.translatedName = settings[4]
        self.description = settings[5]
        
        if "Dwarf Scroll" in self.name:
            self.artifactOtherStuff = settings[7]
        elif "Geode" in self.name or self.name == "Artifact Trove":
            self.geodeDropTable = [int(s) for s in settings[6].split(' ')]
        elif self.name == "Vinegar":
            self.foodType = settings[6]

        elif (len(settings) >= 7 and self.type in ["Arch", "asdf"]) or (self.id >= 820 and self.id <= 828):
            #Artifact data
            artifactSpawnData = settings[6].split(' ')
            for i in range(int(len(artifactSpawnData) / 2)):
                self.artSpawnLocations.append(artifactSpawnData[i * 2])
                self.artSpawnChances.append(float(artifactSpawnData[(i * 2) + 1]))
            
            if len(settings) == 8:
                self.artifactOtherStuff = settings[7]

        elif len(settings) == 7 and (self.type == "Fish" or self.name == "Treasure Chest"):
            #Fish data
            fishSpawnData = settings[6].split('^')
            self.fishTimeOfDay = fishSpawnData[0].split(' ')
            self.fishLocations = fishSpawnData[1].split(' ')

        elif len(settings) == 9:
            #Food/Drink data
            self.foodType = settings[6]
            self.buffs = [int(buff) for buff in settings[7].split(' ')]
            self.buffDuration = int(settings[8])




    def toSettingString(self):
        settingsStrings = []
        settingsStrings.append(self.name)
        settingsStrings.append(str(self.price))
        settingsStrings.append(str(self.edibility))
        if self.category > 0:
            settingsStrings.append(self.type)
        else:
            settingsStrings.append(self.type + ' ' + str(self.category))
        settingsStrings.append(self.translatedName)
        settingsStrings.append(self.description)

        # append the special data
        if self.name == "Vinegar":
            settingsStrings.append(self.foodType)
        elif len(self.geodeDropTable) > 0:
            settingsStrings.append(" ".join([str(s) for s in self.geodeDropTable]))
        elif self.foodType != "":
            settingsStrings.append(self.foodType)
            settingsStrings.append(" ".join([str(s) for s in self.buffs]))
            settingsStrings.append(str(self.buffDuration))
        elif len(self.fishTimeOfDay) > 0 and len(self.fishLocations) > 0:
            settingsStrings.append(' '.join(self.fishTimeOfDay) + '^' + ' '.join(self.fishLocations))
        else:
            if len(self.artSpawnLocations) > 0 and len(self.artSpawnChances) > 0:
                artSpawnInfo = []
                for i in range(len(self.artSpawnLocations)):
                    artSpawnInfo.append(self.artSpawnLocations[i] + ' ' + str(self.artSpawnChances[i]))
                settingsStrings.append(' '.join(artSpawnInfo))
            elif self.artifactOtherStuff != "":
                settingsStrings.append("")
            if self.artifactOtherStuff != "":    
                settingsStrings.append(self.artifactOtherStuff)
        return "/".join(settingsStrings)

def readObjectInfoFile(rootFilePath):
    OBJECT_INFO_FILE = rootFilePath + "\Data\ObjectInformation.json"
    file = open(OBJECT_INFO_FILE, "r")
    stardewJsonData = json.load(file)
    
    settingsDictionary = {}
    for key, val in stardewJsonData.items():
        settingsDictionary[key] = ObjectInfoData(key, val)
    return settingsDictionary

def updateCropDescriptions(cropsDataDictionary, objectInfoDictionary):
    for id, cropdata in cropsDataDictionary.items():
        descriptionString = "Plant these in the " + " or ".join(cropdata.seasons) + ". "
        descriptionString = descriptionString + "Takes " + str(sum(cropdata.growthStages)) + " days to mature. "
        descriptionString = descriptionString + "Produces " + objectInfoDictionary[str(cropdata.harvestId)].name + "."

        objectInfo = objectInfoDictionary[id]
        objectInfo.description = descriptionString