from securityCamera import securityCamera
from thermoStat import thermoStat
from smartLight import smartLight
from automationSystem import automationSystem

automation_system = automationSystem()

camera = securityCamera("camera", "on", "secure")
thermostat = thermoStat("thermostat", "on", 20)
light = smartLight("light", "on", 100)

automation_system.add_device(camera)
automation_system.add_device(light)
automation_system.add_device(thermostat)

automation_system.simulation_loop(10, 1)