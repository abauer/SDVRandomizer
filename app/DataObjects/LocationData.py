#Location data has information on forageables and fish that spawn in each region
class LocationData:

    def __init__(self, name, locationString):
        self.name = name
        self.springForageIDs = []
        self.springForageChance = []
        self.summerForageIDs = []
        self.summerForageChance = []
        self.fallForageIDs = []
        self.fallForageChance = []
        self.winterForageIDs = []
        self.winterForageChance = []
        self.springFishIDs = []
        self.springFishChance = []
        self.summerFishIDs = []
        self.summerFishChance = []
        self.fallFishIDs = []
        self.fallFishChance = []
        self.winterFishIDs = []
        self.winterFishChance = []
        self.artifactIDs = []
        self.artifactChance = []

        self.parseSettingString(locationString)

    def splitIDandChance(string):
        idList = []
        chanceList = []
        subStrings = string.split(' ')
        if len(subStrings) <= 1:
            idList = [int(subStrings[0])]
        else:
            idList = [int(s) for s in subStrings[::2]]
            chanceList = [float(s) for s in subStrings[1::2]]
        return idList, chanceList

    def idAndChanceToString(idList, chanceList):
        if len(chanceList) == 0:
            return str(idList[0])
        else:
            stringList = []
            for i in range(len(idList)):
                stringList.append(str(idList[i]) + ' ' + str(chanceList[i]))
            return ' '.join(stringList)

    def parseSettingString(self, settingString):
        settings = settingString.split('/')
        self.springForageIDs, self.springForageChance = LocationData.splitIDandChance(settings[0])
        self.summerForageIDs, self.summerForageChance = LocationData.splitIDandChance(settings[1])
        self.fallForageIDs, self.fallForageChance = LocationData.splitIDandChance(settings[2])
        self.winterForageIDs, self.winterForageChance = LocationData.splitIDandChance(settings[3])
        self.springFishIDs, self.springFishChance = LocationData.splitIDandChance(settings[4])
        self.summerFishIDs, self.summerFishChance = LocationData.splitIDandChance(settings[5])
        self.fallFishIDs, self.fallFishChance = LocationData.splitIDandChance(settings[6])
        self.winterFishIDs, self.winterFishChance = LocationData.splitIDandChance(settings[7])
        self.artifactIDs, self.artifactChance = LocationData.splitIDandChance(settings[8])


    def toSettingString(self):
        settingsStrings = []
        settingsStrings.append(LocationData.idAndChanceToString(self.springForageIDs, self.springForageChance))
        settingsStrings.append(LocationData.idAndChanceToString(self.summerForageIDs, self.summerForageChance))
        settingsStrings.append(LocationData.idAndChanceToString(self.fallForageIDs, self.fallForageChance))
        settingsStrings.append(LocationData.idAndChanceToString(self.winterForageIDs, self.winterForageChance))
        settingsStrings.append(LocationData.idAndChanceToString(self.springFishIDs, self.springFishChance))
        settingsStrings.append(LocationData.idAndChanceToString(self.summerFishIDs, self.summerFishChance))
        settingsStrings.append(LocationData.idAndChanceToString(self.fallFishIDs, self.fallFishChance))
        settingsStrings.append(LocationData.idAndChanceToString(self.winterFishIDs, self.winterFishChance))
        settingsStrings.append(LocationData.idAndChanceToString(self.artifactIDs, self.artifactChance))

        return "/".join(settingsStrings)
