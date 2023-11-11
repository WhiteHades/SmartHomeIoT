import sys
import tkinter as tk
import random
from datetime import datetime
from tkinter import scrolledtext, ttk
# import threading

from automationSystem import automationSystem
from securityCamera import securityCamera
from smartLight import smartLight
from thermoStat import thermoStat


class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
        self.buffer = ""

    def write(self, message):
        if '\n' in message:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            log_message = f"{timestamp} {self.buffer}{message}"
            self.widget.insert(tk.END, log_message)
            self.widget.see(tk.END)
            self.buffer = ""
        else:
            self.buffer += message

    def flush(self):
        pass


class SmartHomeGUI:
    def __init__(self, root):
        self.simulation_toggle = None
        self.thermostat_temp_label = None
        self.light_brightness_label = None
        self.log_frame = None
        self.log_text = None
        self.root = root
        self.root.title("Smart Home Control Panel")

        self.automation_system = automationSystem()
        # self.duration = duration
        # self.interval = interval
        self.simulation_running = False  # Flag to indicate if the simulation is running
        # self.update_event = threading.Event()  # Event to signal the main thread to update the GUI

        # Initialize instance attributes for controls
        self.light_brightness_slider = None
        self.thermostat_temp_slider = None
        self.camera_toggle = None
        self.light_toggle = None
        self.thermostat_toggle = None
        self.random_motion_button = None
        self.camera_motion_status_label = None
        self.brightness_label = None
        self.temperature_label = None
        self.brightness_labels = []
        self.temperature_labels = []
        self.motion_status_labels = []
        self.temp_canvas = None
        self.temp_plot = None
        self.temp_figure = None
        self.thermostat_temp_slider = None
        self.light_brightness_slider = None
        self.status_frame = None
        self.status_labels = {}

        # Create and discover IoT devices
        self.device_status_labels = []
        camera_status = random.choice(["on", "off"])
        security_status = "secure" if camera_status == "on" else "unsecure"
        light_status = random.choice(["on", "off"])
        light_brightness = random.randint(0, 100) if light_status == "on" else 0
        thermostat_status = random.choice(["on", "off"])
        thermostat_temperature = random.randint(10, 30) if thermostat_status == "on" else 0

        self.camera = securityCamera("Camera", camera_status, security_status)
        self.light = smartLight("Light", light_status, light_brightness)
        self.thermostat = thermoStat("Thermostat", thermostat_status, thermostat_temperature)

        self.automation_system.add_device(self.camera)
        self.automation_system.add_device(self.light)
        self.automation_system.add_device(self.thermostat)

        # Create GUI elements
        self.create_device_status_labels()
        self.create_device_controls()

        self.periodic_update()

        sys.stdout = TextRedirector(self.log_text)

    def create_device_status_labels(self):
        for device in self.automation_system.devices:
            device_frame = ttk.LabelFrame(self.root, text=device.deviceID)
            device_frame.pack(padx=10, pady=5, fill="both", expand=1)

            device_status_label = tk.Label(device_frame, text=f"Status: {device.status}")
            device_status_label.pack()
            self.device_status_labels.append(device_status_label)

            if isinstance(device, thermoStat):
                temperature_label = tk.Label(device_frame, text=f"Temperature: {device.temperature}°C")
                temperature_label.pack()
                self.temperature_labels.append(temperature_label)
                self.thermostat_temp_label = temperature_label
            elif isinstance(device, securityCamera):
                motion_status_label = tk.Label(device_frame, text=f"Security Status: {device.security_status}")
                motion_status_label.pack()
                self.motion_status_labels.append(motion_status_label)
            elif isinstance(device, smartLight):
                brightness_label = tk.Label(device_frame, text=f"Brightness: {device.brightness}")
                brightness_label.pack()
                self.brightness_labels.append(brightness_label)

    @staticmethod
    def add_Slider(frame, from_, to, command, initial_value):
        scale = ttk.Scale(frame, from_=from_, to=to, orient=tk.HORIZONTAL, command=command)
        scale.set(initial_value)
        scale.pack(padx=10, pady=5)
        return scale

    def update_light_brightness(self, brightness):
        self.light.set_brightness(int(float(brightness)))
        self.light_brightness_label.config(text=f"Brightness: {int(float(brightness))}")
        print(f"Brightness set to {int(float(brightness))}")

    def update_thermostat_temperature(self, temperature):
        self.thermostat.set_temperature(int(float(temperature)))
        self.thermostat_temp_label.config(text=f"Temperature: {int(float(temperature))}°C")
        print(f"Temperature set to {int(float(temperature))}°C")

    def create_device_controls(self):
        control_frame = ttk.LabelFrame(self.root, text="Controls")
        control_frame.pack(padx=10, pady=5, fill="both", expand=1)

        # Add sliders for brightness and temperature, and buttons for toggling devices
        self.light_brightness_label = tk.Label(control_frame, text="Brightness")
        self.light_brightness_label.pack(side="left", padx=10, pady=5)
        self.light_brightness_slider = SmartHomeGUI.add_Slider(
            control_frame, 0, 100, self.update_light_brightness, self.light.brightness)
        self.light_brightness_slider.pack(side="left", padx=10, pady=5)

        self.thermostat_temp_label = tk.Label(control_frame, text="Temperature (°C)")
        self.thermostat_temp_label.pack(side="left", padx=10, pady=5)
        self.thermostat_temp_slider = SmartHomeGUI.add_Slider(
            control_frame, 10, 30, self.update_thermostat_temperature, self.thermostat.temperature)
        self.thermostat_temp_slider.pack(side="left", padx=10, pady=5)

        self.camera_toggle = ttk.Button(control_frame, text="Toggle Camera", command=self.toggle_camera)
        self.camera_toggle.pack(side="left", padx=10, pady=5)

        self.light_toggle = ttk.Button(control_frame, text="Toggle Light", command=self.toggle_light)
        self.light_toggle.pack(side="left", padx=10, pady=5)

        self.thermostat_toggle = ttk.Button(control_frame, text="Toggle Thermostat", command=self.toggle_thermostat)
        self.thermostat_toggle.pack(side="left", padx=10, pady=5)

        # Button for simulating random motion detection
        self.random_motion_button = ttk.Button(control_frame, text="Random Detect Motion",
                                               command=self.random_detect_motion)
        self.random_motion_button.pack()

        # Add a toggle button for the simulation
        self.simulation_toggle = ttk.Button(control_frame, text="Toggle Simulation", command=self.toggle_simulation)
        self.simulation_toggle.pack()

        # Label to display the camera motion status
        self.camera_motion_status_label = tk.Label(control_frame, text="Front Door Camera - Motion: OFF")
        self.camera_motion_status_label.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, width=40, height=10)
        self.log_text.pack(fill="both", expand=True)

    def toggle_simulation(self):
        self.simulation_running = not self.simulation_running
        self.periodic_update()

        # button_text = "Stop Simulation" if self.simulation_running else "Start Simulation"
        # self.simulation_toggle.config(text=button_text)

        # if self.simulation_running and self.light.status == "on" and self.thermostat.status == "on" and self.camera.status == "on":
        #     self.simulation_thread = threading.Thread(target=self.run_simulation)
        #     self.simulation_thread.daemon = True  # Make the thread a daemon to stop it when the main program exits
        #     self.simulation_thread.start()
        # else:
        #     print("Turn on camera, light, and thermostat for simulation to run.")

    # def run_simulation(self):
    #     while self.simulation_running:
    #         self.automation_system.simulation_loop(self.duration, self.interval)
    #         # Signal the main thread to update the GUI
    #         self.update_event.set()
    #         # Sleep for a short interval to avoid high CPU usage
    #         time.sleep(0.1)
    #
    #         if not self.simulation_running:
    #             break  # Exit the loop if simulation is stopped
    #
    #             # Schedule the next simulation step
    #         self.root.after(1000, self.run_simulation_step)

    # def run_simulation_step(self):
    #     if self.simulation_running:
    #         # Continue the simulation loop with a delay of 1 second
    #         self.run_simulation()

    def random_detect_motion(self):
        # Simulate random motion detection
        motion_detected = random.choice([True, False])
        motion_status = "YES" if motion_detected else "NO"
        self.camera_motion_status_label.config(text=f"Front Door Camera - Motion: {motion_status}")
        print("Motion detected." if motion_detected else "No motion detected.")

        # If motion is detected and the light is off, turn on the light
        if motion_detected:
            self.light.turn_on()
            self.update_device_status_labels()

            self.camera.turn_on()
            self.update_device_status_labels()

    def toggle_camera(self):
        if self.camera.status == "on":
            self.camera.turn_off()
            self.camera.security_status = "unsecure"
        else:
            self.camera.turn_on()
            self.camera.security_status = "secure"

        self.update_device_status_labels()

    def toggle_light(self):
        # Toggle the light's status
        self.light.status = "off" if self.light.status == "on" else "on"
        self.light.set_brightness(100 if self.light.status == 'on' else 0)
        self.update_device_status_labels()

    def toggle_thermostat(self):
        self.thermostat.status = 'off' if self.thermostat.status == 'on' else 'on'
        self.thermostat.set_temperature(22 if self.thermostat.status == 'on' else 0)  # Set a default temperature
        self.update_device_status_labels()

    def update_device_status_labels(self):
        for i, device in enumerate(self.automation_system.devices):
            self.device_status_labels[i].config(text=f"Status: {device.status}")
            if isinstance(device, thermoStat):
                self.thermostat_temp_slider.set(device.temperature)
                # Disable the thermostat slider if the thermostat is off
                slider_state = tk.NORMAL if device.status == "on" else tk.DISABLED
                self.thermostat_temp_slider.configure(state=slider_state)
            elif isinstance(device, smartLight):
                self.light_brightness_slider.set(device.brightness)
                # Disable the light brightness slider if the light is off
                slider_state = tk.NORMAL if device.status == "on" else tk.DISABLED
                self.light_brightness_slider.configure(state=slider_state)
            elif isinstance(device, securityCamera):
                self.camera_motion_status_label.config(text=f"Front Door Camera - Motion: {device.security_status}")

        for brightness_label in self.brightness_labels:
            brightness_label.config(text=f"Brightness: {self.light.brightness}")

        for temperature_label in self.temperature_labels:
            temperature_label.config(text=f"Temperature: {self.thermostat.temperature}°C")

        for motion_status_label in self.motion_status_labels:
            motion_status_label.config(text=f"Security Status: {self.camera.security_status}")

        for deviceID, label in self.status_labels.items():
            device = self.automation_system.get_device(deviceID)
            if isinstance(device, smartLight):
                label.config(text=f"{device.deviceID} - Brightness: {device.brightness}%")
            elif isinstance(device, thermoStat):
                label.config(text=f"{device.deviceID} - Temperature: {device.temperature}°C")
            elif isinstance(device, securityCamera):
                label.config(text=f"{device.deviceID} - Security Status: {device.security_status}")

    def periodic_update(self):
        if self.simulation_running and self.light.status == "on" and self.thermostat.status == "on" and self.camera.status == "on":
            # Execute automation jobs
            self.automation_system.execute_automation_jobs()

            # Update the device status labels with the current device statuses
            self.update_device_status_labels()

            # Schedule the next update
            self.root.after(1000, self.periodic_update)  # Update every 1000 milliseconds
        else:
            print("Turn on camera, light and thermostat for simulation to run.")

        # if self.simulation_running:
        #     # Wait for the event to be set by the simulation thread
        #     self.update_event.wait()
        #     # Reset the event for the next update
        #     self.update_event.clear()
        #
        #     # Update the device status labels with the current device statuses
        #     self.update_device_status_labels()
        #
        #     # Schedule the next update
        # self.root.after(1000, self.periodic_update)
