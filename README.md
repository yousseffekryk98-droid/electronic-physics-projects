# Smart Attendance System using Face Recognition

**Instructor:** Dr/Amir Elmslmany  
**Primary platform:** Raspberry Pi + OpenCV  
**Physics / engineering concepts:** computer vision, embeddings/classification, attendance logging

## Goal
Build a demonstrable educational prototype of **Smart Attendance System using Face Recognition** with measurable inputs, clear outputs, reproducible wiring, and a short validation experiment.

## Components / BOM
- Raspberry Pi 4/5
- Pi Camera/USB camera
- microSD
- display optional
- network connection

Add jumper wires, headers/connectors, a breadboard or perfboard, appropriate resistors, an enclosure, and a correctly rated regulated supply as required by the physical build.

## Wiring
`wiring.csv` is the pin-by-pin source of truth.

| Component / node | Signal / connection | Board pin / destination |
|---|---|---|
| Camera | CSI/USB | Pi |
| optional OLED SDA/SCL | I2C | GPIO2/3 |

## Build sequence
1. Assemble and power-test only the controller and one sensor first.
2. Verify raw sensor readings in Serial Monitor / terminal.
3. Add displays, indicators and actuators one at a time.
4. Power high-current loads (motors, pumps, servos, solenoids, LED strips) from their own properly rated supply.
5. Implement the control rule and add hysteresis/debounce so outputs do not chatter near a threshold.
6. Calibrate the sensor(s), record at least three test conditions, and compare measured vs expected behavior.
7. Mount the electronics in the supplied CAD design where present; adjust dimensions to your exact modules before printing.
8. Perform the acceptance tests below before the final demo.

## Software
The `src/` folder contains a starter implementation for the specified platform. It is intentionally credential-free. Use `wiring.csv` as the authoritative mapping, then replace the baseline sensor conversion/control section with the equations or logic for this project.

For IoT projects, never commit Wi-Fi passwords, API tokens or webhook secrets. Put them in a local secrets header ignored by Git or inject them at build/runtime.

## Validation / experiment
- Confirm the system starts safely with actuators OFF.
- Record raw and converted sensor readings for at least 3 known conditions.
- Trigger each alert/output deliberately and verify it resets correctly.
- Disconnect/reconnect a sensor and confirm the software fails safely rather than driving an actuator unpredictably.
- Measure supply voltage/current under idle and active load.
- Document calibration constants, threshold values and uncertainty/limitations in your report.

## Safety
- Keep all student wiring at SELV/low voltage whenever possible.
- Power motors, servos, pumps and solenoids from a suitable separate supply; connect grounds only where the circuit requires it.
- Add fuses/current limiting to battery and solar power paths.
- Do not connect exposed breadboard wiring directly to mains electricity.
- Calibrate sensors against known references before presenting measurements as quantitative results.

## 3D / mechanical design
A parametric OpenSCAD model is included under `cad/`. It is a starting design sized for a classroom prototype. Measure the real PCB/sensor/servo first and adjust the parameters before printing. Export to STL from OpenSCAD only after checking clearances and cable paths.

## Open-source building blocks
- [OpenSCAD](https://github.com/openscad/openscad) — Parametric CAD source used for printable/mechanical models
- [Raspberry Pi documentation/source organization](https://github.com/raspberrypi) — Open-source Raspberry Pi software ecosystem
- [OpenCV](https://github.com/opencv/opencv) — Open-source computer-vision library

The branch does **not** claim that an upstream repository is the complete project. The links above are the open-source libraries/tooling used as building blocks or useful references.

## Suggested report structure
1. Objective and physics principle
2. Block diagram
3. Circuit/wiring diagram
4. Hardware design and CAD
5. Software/control algorithm
6. Calibration method
7. Measurements and plots
8. Errors/limitations
9. Safety considerations
10. Conclusion and future improvements
