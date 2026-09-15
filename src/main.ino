// Smart Attendance System with RFID
// Educational starter firmware generated for this branch.
// Calibrate sensor thresholds before demonstration.

#include <WiFi.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASS = "YOUR_PASSWORD";

// Conservative generic pins; use wiring.csv as the authoritative pin map.
const int SENSOR_ADC = 34;
const int OUTPUT_PIN = 26;

void setup() {
  Serial.begin(115200);
  pinMode(OUTPUT_PIN, OUTPUT);
  digitalWrite(OUTPUT_PIN, LOW);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
    delay(250);
    Serial.print('.');
  }
  Serial.println();
  Serial.println(WiFi.status() == WL_CONNECTED ? "WiFi connected" : "Offline mode");
}

void loop() {
  int raw = analogRead(SENSOR_ADC);
  Serial.printf("raw=%d\n", raw);
  // Add the project-specific conversion/control rule from README.md here.
  delay(500);
}
