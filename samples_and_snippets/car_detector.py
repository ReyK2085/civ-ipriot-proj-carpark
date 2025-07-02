import tkinter as tk
import paho.mqtt.client as paho

class CarDetector:
    def __init__(self):
        self.client = paho.Client()
        self.client.connect("localhost", 1883)

        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        # License plate entry
        tk.Label(self.root, text="License Plate:", font=('Arial', 20)).pack(padx=10, pady=2)
        self.plate_entry = tk.Entry(self.root, font=('Arial', 30))
        self.plate_entry.pack(padx=10, pady=2)

         # Temperature entry
        tk.Label(self.root, text="Temperature:", font=('Arial', 20)).pack(padx=10, pady=2)
        self.temp_entry = tk.Entry(self.root, font=('Arial', 30))
        self.temp_entry.pack(padx=10, pady=2)
        self.temp_btn = tk.Button(self.root, text='Set Temperature', font=('Arial', 20), command=self.set_temperature)
        self.temp_btn.pack(padx=10, pady=2)

        self.btn_incoming_car = tk.Button(
        self.root, text='Incoming Car', font=('Arial', 50), cursor='right_side',
        command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)

        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car', font=('Arial', 50), cursor='bottom_left_corner',
            command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.root.mainloop()

    def incoming_car(self):
        plate = self.plate_entry.get()
        print(f"Publishing: carpark/entry, payload: {plate}")
        self.client.publish("carpark/entry", plate)
        print(f"Car goes in: {plate}")

    def outgoing_car(self):
        plate = self.plate_entry.get()
        print(f"Publishing: carpark/exit, payload: {plate}")
        self.client.publish("carpark/exit", plate)
        print(f"Car goes out: {plate}")

    def set_temperature(self):
        temp = self.temp_entry.get()
        print(f"Publishing: carpark/temp, payload: {temp}")
        self.client.publish("carpark/temp", temp)
        print(f"Temperature set: {temp}")

if __name__ == '__main__':
    CarDetector()
