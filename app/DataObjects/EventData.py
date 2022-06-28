def generateFriendshipEventID(id, nameString, friendShipValue):
    return str(id) + '/' + 'f ' + nameString + ' ' + str(friendShipValue) + '/x ' + nameString + '_friend'

class EventData:

    def __init__(self, id, settingsString):
        self.id = id
        self.eventScript = settingsString

    def toSettingString(self):
        return self.eventScript

