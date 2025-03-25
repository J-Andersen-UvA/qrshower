import asyncio
import threading
import showQR  # Import from your QR code script
from listenGlossChanges import listen_to_glos_changes  # Import from your WebSocket listener script
import time

def start_qr_gui(app):
    """Starts the QR code GUI in the main thread."""
    app.create_gui()

def start_websocket_listener(app):
    """Starts the WebSocket listener."""
    asyncio.run(listen_to_glos_changes(app))

if __name__ == "__main__":
    # Create an instance of the QRCodeApp
    datap_provider = showQR.QRCodeData(glos_id="test_glos_id", time_code_modus=showQR.TimeCodeModus.TENTACLES)
    app = showQR.QRCodeApp(datap_provider)

    # No extra thread implementation
    app.create_gui()

    # # Start the QR code GUI in a separate thread
    # gui_thread = threading.Thread(target=start_qr_gui, args=(app,), daemon=True)
    # gui_thread.start()


    # # Start the WebSocket listener in the main thread's event loop
    # try:
    #     start_websocket_listener(app)
    # except KeyboardInterrupt:
    #     print("Shutting down...")
    #     app.shutdown()  # Safely shut down the GUI
