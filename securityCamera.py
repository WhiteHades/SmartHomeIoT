class securityCamera:
    def __init__(self, deviceID, status, security_status):
        self.deviceID = deviceID
        self.status = "off"
        self.security_status = security_status

    def set_security_status(self, security_status):
        self.security_status = security_status

    def toggle_security_status(self):
        if self.status == "on":
            print("Camera is on.")
            self.security_status = "secure"
        else:
            self.security_status = "unsecure"
            print("Camera is off.")

    def turn_on(self):
        self.status = "on"
        self.security_status = "secure"

    def turn_off(self):
        self.status = "off"
        self.security_status = "unsecure"
