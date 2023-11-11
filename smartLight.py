class smartLight:
    def __init__(self, deviceID, status, brightness):
        self.deviceID = deviceID
        self.status = status
        self.brightness = brightness

    def set_brightness(self, brightness):
        if self.status == "on":
            self.brightness = brightness

    def gradual_brightness(self):
        if self.status == "on" and self.brightness > 50:
            self.brightness -= 5
            print(f"Brightness decreased to {self.brightness}%")
        else:
            print("Light is off")

    def turn_on(self):
        self.status = "on"
        self.set_brightness(60)  # Default brightness when turning on
        print("Light turned on.")

    def turn_off(self):
        self.status = "off"
        self.set_brightness(0)  # Reset brightness when turning off
        print("Light turned off.")
