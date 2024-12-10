import asyncio
import websockets
import json
import ssl

async def listen_to_glos_changes(app):
    """
    Listen for WebSocket messages and update the QR code app.
    Args:
        app: Instance of the QRCodeApp class for updating the QR code.
    """
    uri = "wss://leffe.science.uva.nl:8043/unrealServer/"
    ssl_context = ssl.SSLContext()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        print("Connected to WebSocket server")
        while True:
            try:
                message = await websocket.recv()
                print("Received message:", message)
                
                # Parse the JSON message
                parsed_message = json.loads(message)

                # Extract the required fields from the message
                if parsed_message.get("set", "") == "broadcastGlos":
                    glos_id = parsed_message.get("handler", "")
                    selected_type = parsed_message.get("selectedType", "").lower()

                    print("RECEIVED GLOS ID:", glos_id)

                    if glos_id == "" or glos_id == None:  # Skip empty gloss ID
                        continue
                    
                    if selected_type == "" or selected_type == None:
                        selected_type = "default"  # Set default type if not provided

                    app.update_glos(glos_id, selected_type)  # Update gloss ID and type in app
                    # app.simulate_message(json.dumps({
                    #     "glosId": glos_id,
                    #     "selectedType": selected_type,
                    #     "status": "start"
                    # }))
            except websockets.ConnectionClosed:
                print("WebSocket connection closed")
                break
            except Exception as e:
                print("Error in WebSocket listener:", e)
