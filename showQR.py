import tkinter as tk
from tkinter import messagebox
import threading
import time
import qrcode
from tentacles import TentacleSync
from PIL import Image, ImageTk
import json

class TimeCodeModus:
    NONE = None
    CLOCK_TIME = "clock_time"
    TENTACLES = "tentacles"
    TENTACLES_AND_CLOCK_TIME = "tentacles_and_clock_time"

class QRCodeData:
    def __init__(self, glos_id="testGlosId", time_code_modus=TimeCodeModus.NONE):
        self.glos_id = glos_id
        self.selected_type = "example"
        self.time_code_modus = time_code_modus

    def set_time_code_modus(self, time_code_modus):
        self.time_code_modus = time_code_modus
        print(f"Set time code modus: {time_code_modus}")

    def update_glos(self, glos_id, selected_type):
        self.glos_id = glos_id
        self.selected_type = selected_type
        print(f"Updated gloss: glos_id={glos_id}, selected_type={selected_type}")

    def get_qr_data(self):
        current_time = None
        if self.time_code_modus == TimeCodeModus.CLOCK_TIME:
            current_time = time.strftime("%H:%M:%S")
        elif self.time_code_modus == TimeCodeModus.TENTACLES:
            tentacle_sync = TentacleSync()
            tentacle_sync.start()
            current_time = tentacle_sync.get_current_timecode()
        return json.dumps([self.glos_id, self.selected_type, current_time])

    def stop_getting_timecode(self):
        if self.time_code_modus == TimeCodeModus.TENTACLES:
            tentacle_sync = TentacleSync()
            tentacle_sync.stop()

class QRCodeApp:
    def __init__(self, data_provider):
        self.data_provider = data_provider
        self.qr_code_interval = None
        self.qrcode_image = None
        self.window = None
        self.qr_code_label = None

    def shutdown(self):
        if self.window:
            self.window.quit()
            self.window.destroy()

    def handle_start(self):
        print("Handling 'start' status")
        self.display_qr_code(True)
        if self.qr_code_interval:
            self.qr_code_interval.cancel()
        self.qr_code_interval = threading.Timer(1, self.regenerate_qr_code)
        self.qr_code_interval.start()

    def regenerate_qr_code(self):
        qr_data = self.data_provider.get_qr_data()
        print("Regenerating QR Code with data:", qr_data)
        self.generate_qr_code(qr_data)

        if self.qr_code_interval:
            self.qr_code_interval.cancel()

        self.qr_code_interval = threading.Timer(1, self.regenerate_qr_code)
        self.qr_code_interval.start()

    def handle_stop(self):
        print("Handling 'stop' status")
        self.display_qr_code(False)
        self.data_provider.stop_getting_timecode()
        if self.qr_code_interval:
            self.qr_code_interval.cancel()
            self.qr_code_interval = None

    def generate_qr_code(self, data):
        print(f"Generating QR Code with data: {data}")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=30,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        self.qrcode_image = ImageTk.PhotoImage(img)
        if self.qr_code_label:
            self.qr_code_label.config(image=self.qrcode_image)
            self.qr_code_label.image = self.qrcode_image

    def display_qr_code(self, show):
        if show:
            print("Displaying QR Code")
            self.qr_code_label.pack()
        else:
            print("Hiding QR Code")
            self.qr_code_label.pack_forget()

    def start_simulation(self):
        self.handle_start()

    def stop_simulation(self):
        self.handle_stop()

    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("Local QR Code App")
        self.window.geometry("1200x1200")

        self.qr_code_label = tk.Label(self.window)
        self.qr_code_label.pack()

        start_button = tk.Button(self.window, text="Start", command=self.start_simulation)
        start_button.pack(pady=5)

        stop_button = tk.Button(self.window, text="Stop", command=self.stop_simulation)
        stop_button.pack(pady=5)

        exit_button = tk.Button(self.window, text="Exit", command=self.window.quit)
        exit_button.pack(pady=5)

        self.window.resizable(True, True)
        self.window.mainloop()

# Example usage
if __name__ == "__main__":
    data_provider = QRCodeData()
    app = QRCodeApp(data_provider)
    app.create_gui()
