from iot import iot

class thermoStat(iot):
    def __init__(self, deviceID, status, temperature):
        super().__init__(deviceID, status)
        self.temperature = temperature

    def set_temperature(self, temperature):
        self.temperature = temperature

    def randomise_temperature(self):
        import random
        if self.status == "on":
            self.temperature += random.uniform(-1, 1)