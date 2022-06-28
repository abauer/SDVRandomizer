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
            endIndex = settingsString.find('[')
            self.firstPart = settingsString[:startIndex]
            self.itemBlock = settingsString[startIndex:endIndex]
            self.secondPart = settingsString[endIndex:]
        else:
            splitIndex = settingsString.find('[')
            self.firstPart = settingsString[:splitIndex]
            self.secondPart = settingsString[splitIndex:]
            

    def toSettingString(self):
        return self.firstPart + self.itemBlock + self.secondPart

    def setRewardString(self, typeString, id, quantity):
        if typeString == "money":
            self.itemBlock = "%item money" + str(quantity) + ' ' + str(quantity + 1) + ' %%'
        elif typeString == "object":
            self.itemBlock = "%item " + typeString + ' ' + str(id) + ' ' + str(quantity) + ' %%'
        else:
            self.itemBlock = "%item " + typeString + ' ' + str(id) + ' %%'
