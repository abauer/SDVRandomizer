import json
from pathlib import Path

def generateContentJSONHelper():
    jsonHelper = { "Format" : "1.26.0", "Changes" : []}
    replacements = {
        "Data/Crops" : "assets/randomizedCrops.json", 
        "Data/ObjectInformation" : "assets/updatedObjectInformation.json",
        "Data/Bundles" : "assets/randomizedBundles.json"
        }
    for target, replacement in replacements.items():
        changeDict = { "Action" : "Load", "Target" : target, "FromFile": replacement }
        jsonHelper["Changes"].append(changeDict)
    return jsonHelper

def writeContentJSON(outputFilePath):
   CONTENT_JSON_FILE = outputFilePath / "content.json"
   file = open(CONTENT_JSON_FILE, "w+")
   json.dump(generateContentJSONHelper(), file, indent=3)
