class QuestData:

    def __init__(self, id, settingString):
        self.id = int(id)
        self.type = ""
        self.name = ""
        self.flavorText = ""
        self.hint = ""
        self.completion - ""
        self.nextQuest = ""
        self.goldReward = 0
        self.rewardDescription = ""
        self.cancellable = False
        self.reactionText = ""

        self.parseSettingsString(settingString)

    def parseSettingsString(self, settingString):
        settings = settingString.split('/')

        self.type = settings[0]
        self.name = settings[1]
        self.flavorText = settings[2]
        self.hint = settings[3]
        self.completion = settings[4]
        self.nextQuest = settings[5]
        self.goldReward = int(settings[6])
        self.rewardDescription = settings[7]
        self.cancellable = (settings[8] == "true")
        if len(settings) > 9:
            self.reactionText = settings[9]

    def toSettingsString(self):
        settingsStrings = []
        settingsStrings.append(self.type)
        settingsStrings.append(self.name)
        settingsStrings.append(self.flavorText)
        settingsStrings.append(self.hint)
        settingsStrings.append(self.completion)
        settingsStrings.append(self.nextQuest)
        settingsStrings.append(str(self.goldReward))
        settingsStrings.append(self.rewardDescription)
        if self.cancellable:
            settingsStrings.append("true")
        else:
            settingsStrings.append("false")
        if not self.reactionText == "":
            settingsStrings.append(self.reactionText)
        return '/'.join(settingsStrings)

# Reaction text is useful for inserting a random item for completing a quest
    def setRewardOnCompletion(self, typeString, id, quantity):
        rewardString = ""
        if typeString == "money":
            rewardString = "%item money" + str(quantity) + ' ' + str(quantity + 1) + ' %%'
        else
            rewardString = "%item " + typeString + ' ' + str(id) + ' ' + str(quantity) + ' %%'
        self.reactionText = self.reactionText + rewardString