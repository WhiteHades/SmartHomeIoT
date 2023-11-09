from iot import iot

class smartLight(iot):
    def __init__(self, deviceID, status, brightness):
        super().__init__(deviceID, status)
        self.brightness = brightness

    def set_brightness(self, brightness):
        self.brightness = brightness

    def gradual_brightness(self, brightness):
        if self.status == "on" and self.brightness > 0:
            self.brightness -= 10
        else:
            print("Light is off")