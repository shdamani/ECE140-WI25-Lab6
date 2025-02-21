#include "ECE140_WIFI.h"
#include "ECE140_MQTT.h"
#include "Adafruit_BMP085.h"
// MQTT client - using descriptive client ID and topic
const char* clientid =CLIENT_ID;
const char* topicprefix =TOPIC_PREFIX;
Adafruit_BMP085 bmp;
ECE140_MQTT mqtt(clientid, topicprefix);
ECE140_WIFI wifi;
// WiFi credentials
const char* ucsdUsername = UCSD_USERNAME;
const char* ucsdPassword = "Riajayshree#11";
const char* wifiSsid = WIFI_SSID;
const char* nonEnterpriseWifiPassword = NON_ENTERPRISE_WIFI_PASSWORD;

void setup() {
    Serial.begin(115200);
    Serial.println("Connecting to Wifi...");
    wifi.connectToWPAEnterprise(wifiSsid,ucsdUsername,ucsdPassword);
    //Not UCSD wifi wifi.connectTowifi
    Serial.println("Connecting to MQtt...");
    if(!mqtt.connectToBroker(1883))
    Serial.println("Connection unsucessful...");
    if (!bmp.begin()) {
        Serial.println("Could not find a valid BMP085 sensor, check wiring!");
        while (1) {}
      }
 }

void loop() {
    // Reading in sensor data
    mqtt.loop();
    float pressure_value=bmp.readPressure();
    float  temp_value=bmp.readTemperature();
    Serial.print("Temperature = ");
    Serial.print(temp_value);
    Serial.println(" *C");
    Serial.print("Pressure = ");
    Serial.print(pressure_value);
    Serial.println(" Pa");
    //sending data
    String payload = "{\"temperature\": " + String(temp_value) +
    ", \"pressure\": " + String(pressure_value) + "}";
    Serial.print("Publishing Sensor Data...");
    Serial.print(payload);
    mqtt.publishMessage("readings", payload);
    delay(2000);
}