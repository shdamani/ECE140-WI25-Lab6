import paho.mqtt.client as mqtt
import json
from datetime import datetime
from collections import deque
import numpy as np
import requests 
import time

# MQTT Broker settings
BROKER = "broker.hivemq.com"
PORT = 1883
BASE_TOPIC = "shlok/ece140/sensors"
TOPIC = BASE_TOPIC + "/#"

if BASE_TOPIC == "/ece140/sensors":
    print("Please enter a unique topic for your server")
    exit()

# Global variable to throttle POST requests (only one every 5 seconds)
last_post_time = 0

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker."""
    if rc == 0:
        print("Successfully connected to MQTT broker")
        client.subscribe(TOPIC)
        print(f"Subscribed to {TOPIC}")
    else:
        print(f"Failed to connect with result code {rc}")

def on_message(client, userdata, msg):
    """Callback for when a message is received."""
    global last_post_time
    try:
        # Parse JSON message
        payload = json.loads(msg.payload.decode())
        current_time = datetime.now()
        print(f"Received message on topic {msg.topic} at {current_time}: {payload}")
        
        # Process only temperature messages
        if msg.topic == BASE_TOPIC + "/readings/temperature":
            print(f"Temperature: {payload['temperature']} at {current_time}")
            # Throttle POST requests: ensure at least 5 seconds between requests
            if time.time() - last_post_time >= 5:
                last_post_time = time.time()
                post_data = {
                    "value": payload['temperature'],
                    "unit": payload.get("unit", "C"),  # Default to Celsius if not provided
                    "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                # POST request to your web server running on port 6543
                url = "http://0.0.0.0:8000//api/temperature"
                try:
                    response = requests.post(url, json=post_data)
                    print("POST response:", response.json())
                except Exception as e:
                    print("Error sending POST request:", e)
            else:
                print("Throttling POST request; waiting 5 seconds before sending the next one.")
                
    except json.JSONDecodeError:
        print(f"\nReceived non-JSON message on {msg.topic}:")
        print(f"Payload: {msg.payload.decode()}")

def main():
    # Create MQTT client
    print("Creating MQTT client...")
    client = mqtt.Client()

    # Set the callback functions on_connect and on_message
    print("Setting callback functions...")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        # Connect to broker
        print("Connecting to broker...")
        client.connect(BROKER, PORT)
        
        # Start the MQTT loop
        print("Starting MQTT loop...")
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\nDisconnecting from broker...")
        client.loop_stop()
        print("Exited successfully")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
