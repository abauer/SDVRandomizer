class FishData:

    def __init__(self, id, fishSettingsString):
        self.id = int(id)
        self.name = ""
        self.canCatchWithTrap = False
        self.trapChance = 0.0
        self.trapLocation = ""
        self.minSize = 0
        self.maxSize = 0
        self.dartingChance = 0
        self.dartingBehavior = ""
        self.spawnTimeWindow = []
        self.weather = ""
        self.maxDepth = 0
        self.spawnMultiplier = 0.0
        self.depthMultiplier = 0.0
        self.minFishingLevel = 0

        #According to modding notes, these values not unused from the Fish.xnb file
        self.fishLocationAndChance = ""
        self.seasons = []

        self.parseSettingString(fishSettingsString)

    def parseSettingString(self, settingString):
        settings = settingString.split('/')
        self.name = settings[0]

        if settings[1].isdigit():
            #This is fish data
            self.dartingChance = int(settings[1])
            self.dartingBehavior = settings[2]
            self.minSize = int(settings[3])
            self.maxSize = int(settings[4])
            self.spawnTimeWindow = [int(time) for time in settings[5].split(' ')]
            self.seasons = settings[6].split(' ')
            self.weather = settings[7]
            self.fishLocationAndChance = settings[8]
            self.maxDepth = int(settings[9])
            self.spawnMultiplier = float(settings[10])
            self.depthMultiplier = float(settings[11])
            self.minFishingLevel = int(settings[12])

        elif settings[1] == "trap":
            self.canCatchWithTrap = True
            self.trapChance = float(settings[2])
            self.fishLocationAndChance = settings[3]
            self.trapLocation = settings[4]
            self.minSize = int(settings[5])
            self.maxSize = int(settings[6])

    def toSettingString(self):
        settingsStrings = []
        settingsStrings.append(self.name)
        if self.canCatchWithTrap:
            settingsStrings.append("trap")
            if self.trapChance == 0:
                settingsStrings.append("0")
            else:
                settingsStrings.append(str(self.trapChance)[1:])
            settingsStrings.append(self.fishLocationAndChance)
            settingsStrings.append(self.trapLocation)
            settingsStrings.append(str(self.minSize))
            settingsStrings.append(str(self.maxSize))
        else:
            settingsStrings.append(str(self.dartingChance))
            settingsStrings.append(self.dartingBehavior)
            settingsStrings.append(str(self.minSize))
            settingsStrings.append(str(self.maxSize))
            settingsStrings.append(' '.join([str(time) for time in self.spawnTimeWindow]))
            settingsStrings.append(' '.join(self.seasons))
            settingsStrings.append(self.weather)
            settingsStrings.append(self.fishLocationAndChance)
            settingsStrings.append(str(self.maxDepth))
            if self.spawnMultiplier == 0:
                settingsStrings.append("0")
            else:
                settingsStrings.append(str(self.spawnMultiplier)[1:])
            if self.depthMultiplier == 0:
                settingsStrings.append("0")
            else:
                settingsStrings.append(str(self.depthMultiplier)[1:])
            settingsStrings.append(str(self.minFishingLevel))

        return "/".join(settingsStrings)
