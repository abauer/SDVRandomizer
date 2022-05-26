class RecipeData:

    def __init__(self, name, recipeString):
        self.name = name
        self.ingredientIDs = []
        self.ingredientQuantities = []
        self.unused = ""
        self.yieldID = 0
        self.yieldQuantity = 0
        self.objectType = ""
        self.learnLocation = ""
        self.learnLevel = 0
        self.learnType = ""
        self.translatedName = ""
      
        self.isCookingRecipe = False

        self.parseSettingString(recipeString)

    def parseSettingString(self, settingString):
        settings = settingString.split('/')
        self.isCookingRecipe = (len(settings) == 4)
      
        ingredients = settings[0].split(' ')
        self.ingredientIDs = [int(ing) for ing in ingredients[::2]]
        self.ingredientQuantities = [int(quantity) for quantity in ingredients[1::2]]
        self.unused = settings[1]
        yieldSettings = settings[2].split(' ')
        if len(yieldSettings) > 1:
            self.yieldID = int(yieldSettings[0])
            self.yieldQuantity = int(yieldSettings[1])
        else:
            self.yieldID = int(yieldSettings[0])

        learningData = []
        if self.isCookingRecipe:
            learningData = settings[3].split(' ')
        else:
            learningData = settings[4].split(' ')
            self.objectType = settings[3]

        if learningData[0] in ["f", "s"]:
            self.learnType = learningData[0]
            self.learnLocation = learningData[1]
            self.learnLevel = int(learningData[2])
        elif learningData[0] == "l":
            self.learnType = learningData[0]
            self.learnLevel = str(learningData[1])
        elif learningData[0] in ["none", "default", "null"]:
            self.learnLocation = learningData[0]
        else:
            self.learnType = "s"
            self.learnLocation = learningData[0]
            self.learnLevel = int(learningData[1])

    def toSettingString(self):
        settingsStrings = []
        ingredients = []
        for i in range(len(self.ingredientIDs)):
            ingredients.append(str(self.ingredientIDs[i]) + ' ' + str(self.ingredientQuantities[i]))
        settingsStrings.append(' '.join(ingredients))
        settingsStrings.append(self.unused)

        if self.yieldQuantity > 0:
            settingsStrings.append(str(self.yieldID) + ' ' + str(self.yieldQuantity))
        else:
            settingsStrings.append(str(self.yieldID))

        if not self.isCookingRecipe:
            settingsStrings.append(self.objectType)

        if self.learnLocation in ["none", "default", "null"]:
            settingsStrings.append(self.learnLocation)
        elif self.learnType == "l":
            settingsStrings.append(self.learnType + ' ' + str(self.learnLevel))
        else:
            settingsStrings.append(self.learnType + ' ' + self.learnLocation + ' ' + str(self.learnLevel))

        return "/".join(settingsStrings)