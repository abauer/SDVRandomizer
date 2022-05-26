#Note: Valid values for season include Island, which is either Summer or all year if planted on Ginger Island 
#Note: fruit trees do not support multiple growth seasons

class FruitTreeData:

   def __init__(self, id, fruitTreeString):
      self.id = int(id)
      self.spriteIndex = 0
      self.season = ""
      self.harvestIndex = 0
      self.unused = ""

      self.parseSettingString(fruitTreeString)

   def parseSettingString(self, settingString):
      settings = settingString.split('/')
      self.spriteIndex = int(settings[0])
      self.season = settings[1]
      self.harvestIndex = int(settings[2])
      self.unused = settings[3]

   def toSettingString(self):
      settingsStrings = []
      settingsStrings.append(str(self.spriteIndex))
      settingsStrings.append(self.season)
      settingsStrings.append(str(self.harvestIndex))
      settingsStrings.append(self.unused)

      return "/".join(settingsStrings)
