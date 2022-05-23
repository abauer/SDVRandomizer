import json
from pathlib import Path

def generateContentJSONHelper():
    jsonHelper = { "Format" : "1.26.0", "Changes" : []}
    replacements = { "Data/Crops" : "assets/randomizedCrops.json", "Data/ObjectInformation" : "assets/updatedObjectInformation.json" }
    for target, replacement in replacements.items():
        changeDict = { "Action" : "Load", "Target" : target, "FromFile": replacement }
        jsonHelper["Changes"].append(changeDict)
    return jsonHelper

def writeContentJSON():
   CONTENT_JSON_FILE = Path.cwd() / "content.json"
   file = open(CONTENT_JSON_FILE, "w+")
   json.dump(generateContentJSONHelper(), file, indent=3)
