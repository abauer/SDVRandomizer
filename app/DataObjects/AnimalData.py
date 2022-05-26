class AnimalData:

   def __init__(self, name, animalString):
      self.name = name
      self.producePeriod = 0
      self.daysToMature = 0
      self.commonHarvestIndex = -1
      self.premiumHarvestIndex = -1
      self.cry = ""
      self.boundingBox = []
      self.harvestType = 0
      self.canChangeTexture = False
      self.buildingType = ""
      self.spriteDimensions = []
      self.hungerStep = 0
      self.happinessDrain = 0
      self.harvestTool = ""
      self.meatIndex = 0
      self.sellPrice = 0
      self.translatedName = ""
      self.translatedBuilding = ""

      self.parseSettingString(animalString)

   def parseSettingString(self, settingString):
      settings = settingString.split('/')
      self.producePeriod = int(settings[0])
      self.daysToMature = int(settings[1])
      self.commonHarvestIndex = int(settings[2])
      self.premiumHarvestIndex = int(settings[3])
      self.cry = settings[4]
      self.boundingBox = [int(s) for s in settings[5:13]]
      self.harvestType = int(settings[13])
      self.canChangeTexture = (settings[14] == "true")
      self.buildingType = settings[15]
      self.spriteDimensions = [int(s) for s in settings[16:20]]
      self.hungerStep = int(settings[20])
      self.happinessDrain = int(settings[21])
      self.harvestTool = settings[22]
      self.meatIndex = int(settings[23])
      self.sellPrice = int(settings[24])
      self.translatedName = settings[25]
      self.translatedBuilding = settings[26]

   def toSettingString(self):
      settingsStrings = []
      settingsStrings.append(str(self.producePeriod))
      settingsStrings.append(str(self.daysToMature))
      settingsStrings.append(str(self.commonHarvestIndex))
      settingsStrings.append(str(self.premiumHarvestIndex))
      settingsStrings.append(self.cry)
      for i in self.boundingBox:
         settingsStrings.append(str(i))
      settingsStrings.append(str(self.harvestType))
      if self.canChangeTexture:
         settingsStrings.append("true")
      else:
         settingsStrings.append("false")
      settingsStrings.append(self.buildingType)
      for i in self.spriteDimensions:
         settingsStrings.append(str(i))
      settingsStrings.append(str(self.hungerStep))
      settingsStrings.append(str(self.happinessDrain))
      settingsStrings.append(self.harvestTool)
      settingsStrings.append(str(self.meatIndex))
      settingsStrings.append(str(self.sellPrice))
      settingsStrings.append(self.translatedName)
      settingsStrings.append(self.translatedBuilding)

      return "/".join(settingsStrings)