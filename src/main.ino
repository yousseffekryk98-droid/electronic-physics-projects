// Solar Tracking System
// Educational starter firmware generated for this branch.
// Calibrate sensor thresholds before demonstration.

const int SENSOR_PIN = A0;
const int OUTPUT_PIN = 8;

void setup() {
  Serial.begin(115200);
  pinMode(OUTPUT_PIN, OUTPUT);
  digitalWrite(OUTPUT_PIN, LOW);
}

void loop() {
  int raw = analogRead(SENSOR_PIN);
  Serial.print("sensor_raw=");
  Serial.println(raw);
  // Implement the project-specific state/control logic described in README.md.
  delay(250);
}
