import json
from pathlib import Path

def generateContentJSONHelper():
    jsonHelper = { "Format" : "1.26.0", "Changes" : []}
    replacements = {
        "Data/Crops" : "assets/randomizedCrops.json", 
        "Data/ObjectInformation" : "assets/updatedObjectInformation.json",
        "Data/Bundles" : "assets/randomizedBundles.json",
        "Data/FarmAnimals" : "assets/randomizedAnimals.json",
        "Data/CookingRecipes" : "assets/randomizedCooking.json",
        "Data/CraftingRecipes" : "assets/randomizedCrafting.json",
        "Data/Fish" : "assets/randomizedFish.json",
        "Data/fruitTrees" : "assets/randomizedFruitTrees.json",
        "Data/Locations" : "assets/randomizedLocations.json",
        "Data/mail" : "assets/randomizedMail.json",
        "Data/Quests" : "assets/randomizedQuests.json",
        "Data/TV/TipChannel" : "assets/updatedTipChannel.json"
        }
    for target, replacement in replacements.items():
        changeDict = { "Action" : "Load", "Target" : target, "FromFile": replacement }
        jsonHelper["Changes"].append(changeDict)
    return jsonHelper

def writeContentJSON(outputFilePath):
   CONTENT_JSON_FILE = outputFilePath / "content.json"
   file = open(CONTENT_JSON_FILE, "w+")
   json.dump(generateContentJSONHelper(), file, indent=3)
