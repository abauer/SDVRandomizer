# This class holds all settings for bundles
# Can parse the bundle data strings and write new bundle data strings
class BundleReward:
    def __init__(self, rewardType="", rewardID=0, numRewards=0):
        self.rewardType = str(rewardType)
        self.rewardID = int(rewardID)
        self.numRewards = int(numRewards)

class BundleRequirement:
    def __init__(self, reqID=0, numReq=0, minQuality=0):
        self.id = int(reqID)
        self.numReq = int(numReq)
        self.minQuality = int(minQuality)

class BundleData:

    def __init__(self, id, bundleSettingString):
        self.id = id
        self.name = ""
        self.reward = BundleReward()
        self.requirements = []
        self.colorIndex = 0
        self.numRequirementsToComplete = 0
        self.translatedName = ""
        
        self.parseSettingString(bundleSettingString)

    def parseSettingString(self, settingString):
        settings = settingString.split('/')
        
        self.name = settings[0]
        
        rewardData = settings[1].split(' ')
        if len(rewardData) > 1:
            self.reward = BundleReward(rewardData[0], rewardData[1], rewardData[2])

        requirementData = settings[2].split(' ')
        requirements = [["" for x in range(3)] for y in range(int(len(requirementData) / 3))]
        for i in range(len(requirementData)):
            requirements[int(i / 3)][i % 3] = requirementData[i]
        for reqs in requirements:
            self.requirements.append(BundleRequirement(reqs[0], reqs[1], reqs[2]))

        self.colorIndex = int(settings[3])
        if len(settings) >= 5 and settings[4].isdigit():
            self.numRequirementsToComplete = int(settings[4])
        elif len(settings) >= 5 and settings[4].isalpha():
            self.numRequirementsToComplete = len(self.requirements)
            self.translatedName = settings[4]
        elif len(settings) < 5:
            self.numRequirementsToComplete = len(self.requirements)

        if len(settings) >= 6 and settings[5].isalpha():
            self.translatedName = settings[5]

    def toSettingString(self):
        settingsStrings = []
        settingsStrings.append(self.name)
        if self.reward.rewardType != "":
            settingsStrings.append(self.reward.rewardType + ' ' + str(self.reward.rewardID) + ' ' + str(self.reward.numRewards))
        else:
            settingsStrings.append("")
        requirements = [str(req.id) + ' ' + str(req.numReq) + ' ' + str(req.minQuality) for req in self.requirements]
        settingsStrings.append(' '.join(requirements))
        settingsStrings.append(str(self.colorIndex))
        settingsStrings.append(str(self.numRequirementsToComplete))
        if self.translatedName != "":
            settingsStrings.append(str(self.translatedName))
        
        return "/".join(settingsStrings)
