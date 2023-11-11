import random


# from iot import iot

class thermoStat:
    def __init__(self, deviceID, status, temperature):
        self.deviceID = deviceID
        self.status = status
        self.temperature = temperature

    def set_temperature(self, temperature):
        if self.status == "on":
            self.temperature = temperature
        else:
            print("Thermostat is off.")

    # def toggle_thermostat(self):
    #     if self.status == "on":
    #         self.turn_off()
    #     else:
    #         self.turn_on()

    def turn_on(self):
        self.status = "on"
        self.set_temperature(20)  # Default temperature when turning on
        print("Thermostat turned on.")
        print("Default temperature: 20°C.")

    def turn_off(self):
        self.status = "off"
        self.set_temperature(15)  # Reset temperature when turning off
        print("Thermostat turned off.")

    def randomise_temperature(self):
        # Define the range for random temperature adjustment
        temp_range = (10, 30)

        # Generate a random temperature within the range
        new_temperature = random.randint(*temp_range)

        # Set the new temperature
        self.set_temperature(new_temperature)

