# ECE140-WI25-Lab6

In this lab, you will integrate an ESP32 device with an MQTT broker to publish sensor data and create a Python application to subscribe to and process those messages. The ESP32 will read data from its built-in hall effect sensor and temperature sensor, format the readings as a JSON message, and publish them to a unique MQTT topic. On the server side, you will use Python with the Paho MQTT client to receive and display these sensor readings.

## Setting up the ESP32 and PlatformIO

Let's follow Tutorial 1 of Tech Assignment 6: [https://docs.google.com/document/d/1kJXkjd9mZuU9rxEta7ioY88oTqeasn2Xset-PqUs36I/edit?usp=sharing](https://docs.google.com/document/d/1kJXkjd9mZuU9rxEta7ioY88oTqeasn2Xset-PqUs36I/edit?usp=sharing)

### If you're on Mac or Linux

Plug in the ESP32 board to your computer via the provided cable, and you're good to go!

Install PlatformIO following the tutorial linked above.

### If you're on Windows

In addition to installing PlatformIO, you'll need to install the drivers for the ESP32 board. Follow the tutorial linked above for instructions on how to do this.

## Instructions

Here is the project structure:


* `IOT/` – Contains the ESP32 firmware code:
  * `src/main.cpp`: Your main ESP32 program.
  * `include/`: Header files for WiFi and MQTT handling. The `src` folder contains the source code for these header files.
  * `platformio.ini`: PlatformIO configuration file.
  * `.env` (to be created): Environment variables (e.g., WiFi credentials).
* `Server/` – Contains the Python MQTT client:
  * `main.py`: Your Python script that subscribes to the MQTT broker and processes sensor data.
  * `requirements.txt`: Python dependencies.

### Part 1: ESP32 Firmware (C++ with PlatformIO)

**Tasks**

1. Setup Your Environment:
   * Copy `env.example` to a new file called `.env` in the IOT folder.
   * Update `.env` with your WiFi credentials and any other required variables.

2. Complete the Firmware Code:
   * Open the `src/main.cpp` file.
   * Implement the sensor reading logic by calling the ESP32 functions (e.g., `hallRead()` for the hall sensor and an equivalent for the temperature sensor).
   * Format the sensor values into a JSON string that includes a timestamp.
   * Publish the JSON message to an MQTT topic (ensure that you update the `TOPIC_PREFIX` with a unique value).

3. Use PlatformIO to build the project. If you are using VSCode, click on the PlatformIO build button. Upload the firmware to your ESP32. Open the serial monitor to observe debug messages and verify that sensor readings are being published.

### Part 2: Python MQTT Client

1. Install the required Python libraries. You can use the `requirements.txt` file from the `Server/` folder.
2. Complete the Python Script:
   * Open the `Server/main.py` file.
   * In the `on_message` callback, write code to:
     * Parse the JSON message received from the ESP32.
     * Check that the topic matches the sensor reading topic (e.g., /readings appended to your base topic).
     * Print the sensor data (hall value and temperature) along with a timestamp.
   * Ensure that your MQTT client subscribes to the correct topic (update the `BASE_TOPIC` to match the one used in your ESP32 code).
   * Run the Python cient and verify that it receives and processes sensor data!

## Helpful Resources

Paho MQTT Python Client Documentation: https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html

Tip: Use the callback functions provided by Paho to troubleshoot connection issues or data parsing errors.
