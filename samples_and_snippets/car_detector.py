import tkinter as tk                    # GUI module for creating the user interface
import paho.mqtt.client as paho        # MQTT client for communication with broker

class CarDetector:
    def __init__(self):
        # Initialize MQTT client and connect to broker on localhost
        self.client = paho.Client()
        self.client.connect("localhost", 1883)

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        # --- License Plate Input ---
        tk.Label(self.root, text="License Plate:", font=('Arial', 20)).pack(padx=10, pady=2)
        self.plate_entry = tk.Entry(self.root, font=('Arial', 30))
        self.plate_entry.pack(padx=10, pady=2)

        # --- Temperature Input ---
        tk.Label(self.root, text="Temperature:", font=('Arial', 20)).pack(padx=10, pady=2)
        self.temp_entry = tk.Entry(self.root, font=('Arial', 30))
        self.temp_entry.pack(padx=10, pady=2)

        # Button to set temperature via MQTT
        self.temp_btn = tk.Button(
            self.root, text='Set Temperature', font=('Arial', 20),
            command=self.set_temperature)
        self.temp_btn.pack(padx=10, pady=2)

        # --- Incoming Car Button ---
        self.btn_incoming_car = tk.Button(
            self.root, text='Incoming Car', font=('Arial', 50), cursor='right_side',
            command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)

        # --- Outgoing Car Button ---
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car', font=('Arial', 50), cursor='bottom_left_corner',
            command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        # Start the GUI event loop
        self.root.mainloop()

    def incoming_car(self):
        # Publish license plate to MQTT when a car enters
        plate = self.plate_entry.get()
        print(f"Publishing: carpark/entry, payload: {plate}")
        self.client.publish("carpark/entry", plate)
        print(f"Car goes in: {plate}")

    def outgoing_car(self):
        # Publish license plate to MQTT when a car exits
        plate = self.plate_entry.get()
        print(f"Publishing: carpark/exit, payload: {plate}")
        self.client.publish("carpark/exit", plate)
        print(f"Car goes out: {plate}")

    def set_temperature(self):
        # Publish temperature reading to MQTT
        temp = self.temp_entry.get()
        print(f"Publishing: carpark/temp, payload: {temp}")
        self.client.publish("carpark/temp", temp)
        print(f"Temperature set: {temp}")

# Run the CarDetector app 
if __name__ == '__main__':
    CarDetector()
