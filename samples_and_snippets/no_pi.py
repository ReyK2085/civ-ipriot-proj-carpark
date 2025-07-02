"""The following code is used to provide an alternative to students who do not have a Raspberry Pi.
If you have a Raspberry Pi, or a SenseHAT emulator under Debian, you do not need to use this code.

You need to split the classes here into two files, one for the CarParkDisplay and one for the CarDetector.
Attend to the TODOs in each class to complete the implementation."""
import random
import threading
import time
import tkinter as tk
from typing import Iterable

# ------------------------------------------------------------------------------------#
# You don't need to understand how to implement this class, just how to use it.       #
# ------------------------------------------------------------------------------------#
# TODO: got to the main section of this script **first** and run the CarParkDisplay.  #


class WindowedDisplay:
    """Displays values for a given set of fields as a simple GUI window. Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, title: str, display_fields: Iterable[str]):
        """Creates a Windowed (tkinter) display to replace sense_hat display. To show the display (blocking) call .show() on the returned object.

        Parameters
        ----------
        title : str
            The title of the window (usually the name of your carpark from the config)
        display_fields : Iterable
            An iterable (usually a list) of field names for the UI. Updates to values must be presented in a dictionary with these values as keys.
        """
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):

            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field+self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""
        self.window.mainloop()

    def update(self, updated_values: dict):
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to the constructor."""
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()

# -----------------------------------------#
# TODO: STUDENT IMPLEMENTATION STARTS HERE #
# -----------------------------------------#


class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.window = WindowedDisplay('Moondalup', CarParkDisplay.fields)
        # Initial state
        self.available_bays = 150
        self.temperature = '25℃'
        self.last_event_time = time.strftime("%H:%M:%S")
        self.update_display()
        # No timer/thread: display updates only on event
        self.window.show()

    def car_in(self, license_plate: str):
        if self.available_bays > 0:
            self.available_bays -= 1
        self.last_event_time = time.strftime("%H:%M:%S")
        self.update_display()

    def car_out(self, license_plate: str):
        if self.available_bays < 150:
            self.available_bays += 1
        self.last_event_time = time.strftime("%H:%M:%S")
        self.update_display()

    def temperature_changed(self, temp_value: str):
        # Validate temperature (should be an integer or float, e.g. 23 or 23.5)
        try:
            temp = float(temp_value)
            if temp < -30 or temp > 60:
                raise ValueError
            self.temperature = f"{temp:.1f}℃"
        except Exception:
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


class CarDetector:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self, display=None):
        self.display = display
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
            self.root, text='Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car',  font=('Arial', 50), cursor='bottom_left_corner', command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.root.mainloop()

    def incoming_car(self):
        plate = self.plate_entry.get()
        if self.display:
            self.display.car_in(plate)
        print(f"Car goes in: {plate}")

    def outgoing_car(self):
        plate = self.plate_entry.get()
        if self.display:
            self.display.car_out(plate)
        print(f"Car goes out: {plate}")

    def set_temperature(self):
        temp = self.temp_entry.get()
        if self.display:
            self.display.temperature_changed(temp)
        print(f"Temperature set: {temp}")


if __name__ == '__main__':
    # For demo: run both in one process, display in a thread, detector in main
    display = CarParkDisplay()
    # Start display in a thread so detector can run in mainloop
    import threading
    display_thread = threading.Thread(target=lambda: display.window.show())
    display_thread.daemon = True
    display_thread.start()
    CarDetector(display=display)
