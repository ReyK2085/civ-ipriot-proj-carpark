import random
import threading
import time
import tkinter as tk
import paho.mqtt.client as paho
from typing import Iterable
from car_detector import CarDetector  

class WindowedDisplay:
    DISPLAY_INIT = '– – –'
    SEP = ':'

    def __init__(self, title: str, display_fields: Iterable[str]):
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('700x300')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field + self.SEP, font=('Arial', 40))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 40))
            self.gui_elements[f'lbl_field_{i}'].grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        self.window.mainloop()

    def update(self, updated_values: dict):
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()

class CarParkDisplay:
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.available_bays = 130
        self.temperature = "25.0℃"
        self.last_event_time = time.strftime("%H:%M:%S")

        self.window = WindowedDisplay('Moondalup', CarParkDisplay.fields)

        self.client = paho.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883)

        mqtt_thread = threading.Thread(target=self.client.loop_forever)
        mqtt_thread.daemon = True
        mqtt_thread.start()

        self.update_display()
        self.window.show()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe("carpark/entry")
        client.subscribe("carpark/exit")
        client.subscribe("carpark/temp")

    def on_message(self, client, userdata, msg):
        if msg.topic == "carpark/entry" and self.available_bays > 0:
            self.available_bays -= 1
        elif msg.topic == "carpark/exit" and self.available_bays < 130:
            self.available_bays += 1
        elif msg.topic == "carpark/temp":
            try:
                temp = float(msg.payload.decode())
                self.temperature = f"{temp:.1f}℃"
            except:
                self.temperature = "ERR"
        self.last_event_time = time.strftime("%H:%M:%S")
        self.update_display()

    def update_display(self):
        field_values = {
            'Available bays': f'{self.available_bays:03d}',
            'Temperature': self.temperature,
            'At': self.last_event_time
        }
        self.window.update(field_values)

if __name__ == '__main__':
    CarParkDisplay()
