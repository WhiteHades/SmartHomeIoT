from securityCamera import securityCamera
from thermoStat import thermoStat
from smartLight import smartLight


class automationSystem:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def remove_device(self, device):
        self.devices.remove(device)

    def get_device(self, deviceID):
        for device in self.devices:
            if device.deviceID == deviceID:
                return device
        return None

    def execute_automation_jobs(self):
        for device in self.devices:
            if isinstance(device, securityCamera):
                if device.status == "on":
                    device.toggle_security_status()
            elif isinstance(device, smartLight):
                if device.status == "on" and device.brightness > 40:
                    device.gradual_brightness()
            elif isinstance(device, thermoStat):
                if device.status == "on" and 10 <= device.temperature <= 30:
                    device.randomise_temperature()

    # def simulation_loop(self, duration, interval):
    #     import time
    #     for i in range(duration):
    #         self.execute_automation_jobs()
    #         time.sleep(interval)