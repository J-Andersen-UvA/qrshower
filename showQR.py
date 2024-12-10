import tkinter as tk
from tkinter import messagebox
import threading
import time
import qrcode
from PIL import Image, ImageTk
import json

class QRCodeApp:
    def __init__(self, glos_id="testGlosId"):
        # Initialize class attributes
        self.glos_id = glos_id
        self.selected_type = "example"  # Default selected type
        self.qr_code_interval = None  # Timer for periodic updates
        self.qrcode_image = None
        self.window = None
        self.qr_code_label = None

    def update_glos(self, glos_id, selected_type):
        """Update the gloss ID and selected type."""
        self.glos_id = glos_id
        self.selected_type = selected_type
        print(f"Updated gloss: glos_id={glos_id}, selected_type={selected_type}")

    def shutdown(self):
        """Safely close the Tkinter window."""
        if self.window:
            self.window.quit()
            self.window.destroy()

    def handle_start(self):
        """Start generating and displaying QR codes."""
        print("Handling 'start' status")
        self.display_qr_code(True)
        if self.qr_code_interval:
            self.qr_code_interval.cancel()
        self.qr_code_interval = threading.Timer(1, self.regenerate_qr_code)
        self.qr_code_interval.start()

    def regenerate_qr_code(self):
        """Regenerate the QR code periodically."""
        current_time = time.strftime("%H:%M:%S")
        qr_data = [self.glos_id, self.selected_type, current_time]
        print("Regenerating QR Code with data:", qr_data)
        self.generate_qr_code(json.dumps(qr_data))

        if self.qr_code_interval:
            self.qr_code_interval.cancel()

        # Restart the interval
        self.qr_code_interval = threading.Timer(1, self.regenerate_qr_code)
        self.qr_code_interval.start()

    def handle_stop(self):
        """Stop generating and displaying QR codes."""
        print("Handling 'stop' status")
        self.display_qr_code(False)
        if self.qr_code_interval:
            self.qr_code_interval.cancel()
            self.qr_code_interval = None

    def generate_qr_code(self, data):
        """Generate a QR code image from the given data."""
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
        """Show or hide the QR code."""
        if show:
            print("Displaying QR Code")
            self.qr_code_label.pack()
        else:
            print("Hiding QR Code")
            self.qr_code_label.pack_forget()

    def start_simulation(self):
        """Simulate starting QR code generation."""
        self.handle_start()

    def stop_simulation(self):
        """Simulate stopping QR code generation."""
        self.handle_stop()

    def create_gui(self):
        """Create the Tkinter GUI."""
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
    app = QRCodeApp()
    app.create_gui()
