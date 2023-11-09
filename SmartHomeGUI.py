import tkinter as tk
import random

from automationSystem import automationSystem
from securityCamera import securityCamera
from smartLight import smartLight
from thermoStat import thermoStat


class SmartHomeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Control Panel")

        self.automation_system = automationSystem()

        # Initialize instance attributes for controls
        self.light_brightness_slider = None
        self.thermostat_temp_slider = None
        self.camera_toggle = None
        self.light_toggle = None
        self.thermostat_toggle = None
        self.random_motion_button = None
        self.camera_motion_status_label = None
        self.status_frame = None
        self.status_labels = {}

        # Create and discover IoT devices
        self.device_status_labels = []
        self.camera = securityCamera("Camera", "off", "secure")
        self.light = smartLight("Light", "off", 0)
        self.thermostat = thermoStat("Thermostat", "off", 68)

        self.automation_system.add_device(self.camera)
        self.automation_system.add_device(self.light)
        self.automation_system.add_device(self.thermostat)

        # Create GUI elements
        self.create_device_status_labels()
        self.create_device_controls()
        self.create_visualization()
        self.periodic_update()

        # Create the real-time status update section
        self.create_status_update_section()

        # Start the periodic update after GUI setup is complete
        self.root.after(1000, self.periodic_update)

    def create_device_status_labels(self):
        for device in self.automation_system.devices:
            device_frame = tk.LabelFrame(self.root, text=device.deviceID)
            device_frame.pack(padx=10, pady=5, fill="both", expand=1)

            device_status_label = tk.Label(device_frame, text=f"Status: {device.status}")
            device_status_label.pack()
            self.device_status_labels.append(device_status_label)

            if isinstance(device, thermoStat):
                temperature_label = tk.Label(device_frame, text=f"Temperature: {device.temperature}°C")
                temperature_label.pack()
            elif isinstance(device, securityCamera):
                motion_status_label = tk.Label(device_frame, text=f"Security Status: {device.security_status}")
                motion_status_label.pack()
            elif isinstance(device, smartLight):
                brightness_label = tk.Label(device_frame, text=f"Brightness: {device.brightness}")
                brightness_label.pack()

    def create_device_controls(self):
        control_frame = tk.LabelFrame(self.root, text="Controls")
        control_frame.pack(padx=10, pady=5, fill="both", expand=1)

        # Add sliders for brightness and temperature, and buttons for toggling devices
        self.light_brightness_slider = tk.Scale(control_frame, from_=0, to=100, orient="horizontal",
                                                label="Light Brightness")
        self.light_brightness_slider.pack(side="left", padx=10, pady=5)

        self.thermostat_temp_slider = tk.Scale(control_frame, from_=15, to=30, orient="horizontal",
                                               label="Thermostat Temperature (°C)")
        self.thermostat_temp_slider.pack(side="left", padx=10, pady=5)

        self.camera_toggle = tk.Button(control_frame, text="Toggle Camera", command=self.toggle_camera)
        self.camera_toggle.pack(side="left", padx=10, pady=5)

        self.light_toggle = tk.Button(control_frame, text="Toggle Light", command=self.toggle_light)
        self.light_toggle.pack(side="left", padx=10, pady=5)

        self.thermostat_toggle = tk.Button(control_frame, text="Toggle Thermostat", command=self.toggle_thermostat)
        self.thermostat_toggle.pack(side="left", padx=10, pady=5)

        # Button for simulating random motion detection
        self.random_motion_button = tk.Button(self.root, text="Random Detect Motion", command=self.random_detect_motion)
        self.random_motion_button.pack()

        # Label to display the camera motion status
        self.camera_motion_status_label = tk.Label(self.root, text=f"Camera Motion Status: OFF")

    def random_detect_motion(self):
        # Simulate random motion detection
        motion_detected = random.choice([True, False])
        motion_status = "YES" if motion_detected else "NO"
        self.camera_motion_status_label.config(text=f"Front Door Camera - Motion: {motion_status}")

        # If motion is detected and the light is off, turn on the light
        if motion_detected and self.light.status == "off":
            self.toggle_light()

    def toggle_camera(self):
        if self.camera.status == "on":
            self.camera.turn_off()
        else:
            self.camera.turn_on()
        self.update_device_status_labels()

    def toggle_light(self):
        # Toggle the light's status
        new_status = "off" if self.light.status == "on" else "on"
        self.light.status = new_status
        self.update_device_status_labels()  # Make sure this method updates the GUI appropriately

        # if self.light.status == "on":
        #     self.light.turn_off()
        # else:
        #     self.light.turn_on()
        # self.update_device_status_labels()

    def toggle_thermostat(self):
        if self.thermostat.status == "on":
            self.thermostat.turn_off()
        else:
            self.thermostat.turn_on()
        self.update_device_status_labels()

    def update_device_status_labels(self):
        for i, device in enumerate(self.automation_system.devices):
            self.device_status_labels[i].config(text=f"Status: {device.status}")
            if isinstance(device, thermoStat):
                self.thermostat_temp_slider.set(device.temperature)
            elif isinstance(device, smartLight):
                self.light_brightness_slider.set(device.brightness)

        for deviceID, label in self.status_labels.items():
            device = self.automation_system.get_device(deviceID)
            status_text = f"{device.deviceID}: Status: {device.status}"
            label.config(text=status_text)

    def create_visualization(self):
        # Placeholder for creating graphs for temperature and brightness levels
        pass

    def periodic_update(self):
        # Update the device status labels with the current device statuses
        self.update_device_status_labels()
        # Schedule the next update
        self.root.after(1000, self.periodic_update)

    def create_status_update_section(self):
        self.status_frame = tk.LabelFrame(self.root, text="Device Status Updates")
        self.status_frame.pack(padx=10, pady=5, fill="both", expand=1)

        # For each device, create a label and store it in a dictionary for later updates
        for device in self.automation_system.devices:
            status_text = f"{device.deviceID}: Status: {device.status}"
            self.status_labels[device.deviceID] = tk.Label(self.status_frame, text=status_text)
            self.status_labels[device.deviceID].pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeGUI(root)
    root.mainloop()
