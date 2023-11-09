class iot:
    def __init__(self, deviceID, status):
        self.deviceID = deviceID
        self.status = status

    def turn_on(self):
        self.status = "on"

    def turn_off(self):
        self.status = "off"
