from iot import iot

class securityCamera(iot):
    def __init__(self, deviceID, status, security_status):
        super().__init__(deviceID, status)
        self.security_status = security_status

    def set_security_status(self, security_status):
        self.security_status = security_status

    def randomise_security_status(self):
        import random
        if self.status == "on":
            self.security_status = random.choice(["secure", "alert"])