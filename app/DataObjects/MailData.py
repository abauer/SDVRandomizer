class MailData:

    def __init__(self, id, settingsString):
        self.id = id
        self.firstPart = ""
        self.itemBlock = ""
        self.secondPart = ""

        self.parseSettingsString(settingsString)

    def parseSettingsString(self, settingsString):
        if '%' in settingsString:
            startIndex = settingsString.find('%')
            endIndex = settingsString.rfind('%')
            self.firstPart = settingsString[:startIndex - 1]
            self.itemBlock = settingsString[startIndex:endIndex]
            self.secondPart = settingsString[endIndex+1:]
        else:
            self.firstPart = settingsString

    def toSettingsString(self)
        return self.firstPart + self.itemBlock + self.secondPart

    def setRewardString(self, typeString, id, quantity):
        if typeString == "money":
            self.itemBlock = "%item money" + str(quantity) + ' ' + str(quantity + 1) + ' %%'
        else
            self.itemBlock = "%item " + typeString + ' ' + str(id) + ' ' + str(quantity) + ' %%'