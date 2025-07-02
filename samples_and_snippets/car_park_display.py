import random
import threading
import time
import tkinter as tk
import paho.mqtt.client as paho
from typing import Iterable
from car_detector import CarDetector  # This imports the earlier GUI for car detection

# GUI class for creating a window display with labeled fields
class WindowedDisplay:
    DISPLAY_INIT = '– – –'  # Initial placeholder for each field
    SEP = ':'               # Separator between field name and value

    def __init__(self, title: str, display_fields: Iterable[str]):
        # Initialize main window
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('700x300')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        # Dictionary to store label widgets
        self.gui_elements = {}

        # Create labels for each field and its corresponding value
        for i, field in enumerate(self.display_fields):
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field + self.SEP, font=('Arial', 40))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 40))
            self.gui_elements[f'lbl_field_{i}'].grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        # Start the tkinter main loop (blocking call)
        self.window.mainloop()

    def update(self, updated_values: dict):
        # Update label values based on the dictionary passed
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                label_text = self.gui_elements[field].cget('text').rstrip(self.SEP)
                self.gui_elements[field_value].configure(
                    text=updated_values[label_text])
        # Refresh the GUI
        self.window.update()

# Main class for managing the car park display logic
class CarParkDisplay:
    # Fields that will be shown in the display
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        # Initialize car park state
        self.available_bays = 130
        self.temperature = "25.0℃"
        self.last_event_time = time.strftime("%H:%M:%S")

        # Create the GUI window with fields
        self.window = WindowedDisplay('Moondalup', CarParkDisplay.fields)

        # Set up MQTT client and callbacks
        self.client = paho.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883)

        # Start MQTT listening in a separate background thread
        mqtt_thread = threading.Thread(target=self.client.loop_forever)
        mqtt_thread.daemon = True
        mqtt_thread.start()

        # Initial GUI update
        self.update_display()

        # Display the GUI
        self.window.show()

    def on_connect(self, client, userdata, flags, rc):
        # Subscribe to relevant MQTT topics
        client.subscribe("carpark/entry")
        client.subscribe("carpark/exit")
        client.subscribe("carpark/temp")

    def on_message(self, client, userdata, msg):
        # Handle incoming MQTT messages for each topic
        if msg.topic == "carpark/entry" and self.available_bays > 0:
            self.available_bays -= 1
        elif msg.topic == "carpark/exit" and self.available_bays < 130:
            self.available_bays += 1
        elif msg.topic == "carpark/temp":
            try:
                # Try to decode and parse temperature
                temp = float(msg.payload.decode())
                self.temperature = f"{temp:.1f}℃"
            except:
                # Show error if temperature is not valid
                self.temperature = "ERR"

        # Update last event time and refresh display
        self.last_event_time = time.strftime("%H:%M:%S")
        self.update_display()

    def update_display(self):
        # Prepare field values for display
        field_values = {
            'Available bays': f'{self.available_bays:03d}',  # 3-digit format
            'Temperature': self.temperature,
            'At': self.last_event_time
        }
        # Update the GUI with new values
        self.window.update(field_values)

# Run the CarParkDisplay application
if __name__ == '__main__':
    CarParkDisplay()
