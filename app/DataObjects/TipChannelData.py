class TipChannelData:

    def __init__(self, id, settingsString):
        self.id = id
        self.stringData = settingsString

    def toSettingString(self):
        return self.stringData

    def setHintString(self, hintString):
        self.stringData = hintString