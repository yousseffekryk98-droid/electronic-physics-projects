#!/usr/bin/env python3
import csv
import os
import shutil
import subprocess
from pathlib import Path

REPO = Path.cwd()

# branch|instructor|title|board/platform|components (; separated)|wiring (; separated as component>signal>board)|concepts|cad
DATA = r'''
amir-01-solar-power-monitoring|Dr/Amir Elmslmany|Solar Power Monitoring and Optimization System|Arduino Uno + optional ESP32|Arduino Uno; INA219 current/voltage sensor; 6-12V solar panel; 16x2 I2C LCD; breadboard; 10k resistors; fuse; load resistor or USB load; optional ESP32|INA219 VCC>5V>5V; INA219 GND>GND>GND; INA219 SDA>SDA>A4; INA219 SCL>SCL>A5; LCD SDA>SDA>A4; LCD SCL>SCL>A5; Solar +>VIN+>INA219 VIN+; INA219 VIN->Load +>load; Solar ->GND>common GND|renewable energy, IV power measurement, efficiency, telemetry|panel
amir-02-air-quality-monitor|Dr/Amir Elmslmany|Smart Air Quality and Pollution Index Monitor|ESP32|ESP32 DevKit; MQ135; MQ7; 0.96in I2C OLED; buzzer; 10k/20k divider for 5V analog outputs; breadboard; regulated 5V supply|MQ135 AO>ADC>GPIO34 via divider; MQ7 AO>ADC>GPIO35 via divider; OLED SDA>I2C SDA>GPIO21; OLED SCL>I2C SCL>GPIO22; Buzzer +>digital out>GPIO25; all grounds>GND>GND|gas sensing, calibration, AQI-style index, IoT logging|enclosure
amir-03-eeg-controlled-assistive-device|Dr/Amir Elmslmany|Brain-Controlled LED or Wheelchair (EEG-Based Control)|Arduino Uno + EEG headset|Arduino Uno; MindWave-compatible EEG headset; Bluetooth serial module if required; LED + 220R resistor; optional motor driver and small demo motors; separate motor supply; emergency-stop switch for mobility demo|EEG TX>Arduino RX>D2 through SoftwareSerial/appropriate level; EEG GND>GND>GND; LED anode>digital out>D9 via 220R; Motor driver IN1>digital out>D5; Motor driver IN2>digital out>D6; E-stop>motor enable line>series hardware cutoff|biosignal acquisition, threshold classification, assistive control|enclosure
amir-04-traffic-density-analyzer|Dr/Amir Elmslmany|Intelligent Traffic Density Analyzer|Raspberry Pi + OpenCV|Raspberry Pi 4/5; Pi Camera or USB camera; microSD; 5V PSU; optional red/yellow/green LEDs with 330R resistors|Camera>CSI/USB>Pi camera port or USB; Red LED>GPIO17>330R to GND; Yellow LED>GPIO27>330R to GND; Green LED>GPIO22>330R to GND|computer vision, vehicle counting, adaptive signaling|camera_mount
amir-05-smart-glasses-visually-impaired|Dr/Amir Elmslmany|Smart Glasses for the Visually Impaired|Arduino Nano|Arduino Nano; HC-SR04 or VL53L0X distance sensor; coin vibration motor; NPN transistor or MOSFET; flyback diode if inductive; piezo buzzer; Li-ion battery with protected regulator; switch|HC-SR04 TRIG>digital out>D9; HC-SR04 ECHO>digital in>D10; Vibration driver gate/base>PWM>D5; Buzzer +>digital out>D6; Sensor VCC>5V>5V; grounds>GND>GND|distance sensing, haptic feedback, assistive design|glasses
amir-06-fire-detection-suppression|Dr/Amir Elmslmany|Fire Detection and Automatic Suppression System|Arduino Uno|Arduino Uno; flame sensor; temperature sensor; buzzer; SG90 servo; demo nozzle/pointer; relay only for low-voltage demo load; 5V supply|Flame DO>digital in>D2; Temp signal>sensor input>D3/A0 depending module; Buzzer +>digital out>D8; Servo signal>PWM>D9; Servo power>5V external>common GND|threshold detection, alarm logic, servo aiming, safety automation|nozzle_mount
amir-07-water-level-leakage|Dr/Amir Elmslmany|Water Level Management and Leakage Detection|Arduino Uno|Arduino Uno; HC-SR04; YF-S201 flow sensor; leak probe/module; buzzer; optional ESP32 for alerts; 16x2 I2C LCD|HC-SR04 TRIG>digital out>D9; HC-SR04 ECHO>digital in>D10; Flow pulse>interrupt>D2; Leak DO>digital in>D4; Buzzer>digital out>D8; LCD SDA/SCL>I2C>A4/A5|fluid level, flow rate, leak inference, alerts|sensor_box
amir-08-smart-waste-segregation|Dr/Amir Elmslmany|Smart Waste Segregation System|Raspberry Pi + Camera|Raspberry Pi 4/5; camera; ultrasonic sensor; 2-3 servo motors; PCA9685 servo driver recommended; bins/chutes; 5V servo supply|Camera>CSI/USB>Pi; Ultrasonic TRIG>GPIO23>Pi; Ultrasonic ECHO>GPIO24>through divider; PCA9685 SDA/SCL>I2C>GPIO2/3; Servos>PCA9685 channels>external 5V|machine vision, classification, servo sorting, sustainability|chute
amir-09-package-theft-detection|Dr/Amir Elmslmany|IoT-Based Package Theft Detection System|ESP32-CAM|ESP32-CAM; PIR sensor; optional SIM800L GSM module; status LED; 5V 2A supply; enclosure|PIR OUT>digital in>GPIO13; SIM800L TX>RX>GPIO16 via suitable serial; SIM800L RX>TX>GPIO17 with level compatibility; Camera>on-board>ESP32-CAM; grounds>GND>common|motion detection, evidence capture, remote notification|enclosure
amir-10-voice-home-automation|Dr/Amir Elmslmany|Voice-Controlled Home Automation|ESP32|ESP32; 2/4-channel opto-isolated relay module; low-voltage lamps/fans for lab demo; Wi-Fi; optional microphone/voice assistant integration|Relay IN1>digital out>GPIO26; Relay IN2>digital out>GPIO27; Relay VCC>5V>5V; Relay GND>GND>GND; demo loads>relay COM/NO>isolated low-voltage supply|speech/assistant integration, IoT switching, automation|enclosure
amir-11-face-recognition-attendance|Dr/Amir Elmslmany|Smart Attendance System using Face Recognition|Raspberry Pi + OpenCV|Raspberry Pi 4/5; Pi Camera/USB camera; microSD; display optional; network connection|Camera>CSI/USB>Pi; optional OLED SDA/SCL>I2C>GPIO2/3|computer vision, embeddings/classification, attendance logging|camera_mount
amir-12-smart-greenhouse|Dr/Amir Elmslmany|Smart Greenhouse Environment Control|Arduino Uno|Arduino Uno; DHT22; MH-Z19B or equivalent CO2 sensor; soil moisture sensor; relay/MOSFET drivers; 5V/12V fan; small water pump; LCD|DHT22 DATA>digital in>D3; CO2 TX/RX>serial>D10/D11 SoftwareSerial; Soil AO>analog>A0; Fan driver>digital>D6; Pump driver>digital>D7; LCD SDA/SCL>I2C>A4/A5|closed-loop control, environmental sensing, agriculture technology|sensor_box
amir-13-smart-refrigerator|Dr/Amir Elmslmany|Smart Refrigerator System|ESP32|ESP32; DS18B20 temperature sensor; RC522 RFID reader; door reed switch; buzzer; OLED; 4.7k resistor|DS18B20 DATA>1-Wire>GPIO4 with 4.7k pull-up; RC522 SDA/SS>SPI SS>GPIO5; RC522 SCK>SPI SCK>GPIO18; RC522 MOSI>SPI MOSI>GPIO23; RC522 MISO>SPI MISO>GPIO19; RC522 RST>RST>GPIO27; Reed switch>digital in>GPIO32 with pull-up|temperature monitoring, RFID inventory, door-state alerts|enclosure
amir-14-sound-localization-robot|Dr/Amir Elmslmany|Sound Localization Robot|Arduino Uno|Arduino Uno; 2 electret microphone amplifier modules; SG90 servo; optional 2-wheel chassis and motor driver; 5V supply|Mic L AO>analog>A0; Mic R AO>analog>A1; Servo signal>PWM>D9; optional motor driver IN1/IN2>D5/D6>Arduino|amplitude/time comparison, direction estimation, robotics|chassis
amir-15-wireless-power-transfer|Dr/Amir Elmslmany|Wireless Power Transfer Demonstration|Arduino Uno for logging|Low-voltage function generator or oscillator module; transmitter coil; receiver coil; resonant capacitors; rectifier diodes; load resistor; Arduino Uno; INA219 or divider for logging|TX coil>oscillator>low-voltage driver; RX coil>rectifier/filter>load; INA219>load path>I2C A4/A5; Arduino>USB>logging PC|electromagnetic induction, resonant coupling, efficiency|coil_jig
amir-16-wearable-health-monitor|Dr/Amir Elmslmany|Wearable Health Monitor|Arduino Nano|Arduino Nano; pulse sensor or MAX30102; temperature sensor; 0.96in OLED; LiPo + protected 5V/3.3V regulator; switch|MAX30102 SDA/SCL>I2C>A4/A5; Temp sensor>input>D3/A0 depending sensor; OLED SDA/SCL>I2C>A4/A5; battery>regulated supply>board|biomedical sensing, pulse/temperature logging, wearable IoT|wearable_case
amir-17-mini-weather-cubesat|Dr/Amir Elmslmany|Mini Weather Satellite (CubeSat Prototype)|Arduino Uno/Nano|Arduino; BMP180/BMP280; DHT11; microSD module; optional RTC; battery pack; CubeSat-style frame|BMP SDA/SCL>I2C>A4/A5; DHT DATA>digital>D3; SD CS>SPI CS>D10; SD MOSI/MISO/SCK>SPI>D11/D12/D13|atmospheric sensing, data logging, satellite simulation|cubesat
amir-18-classroom-environment-optimizer|Dr/Amir Elmslmany|Classroom Environment Optimization System|Arduino Uno|Arduino Uno; CO2 sensor; LDR; DHT22 optional; relay/MOSFET driver; low-voltage fan; LCD|CO2 TX/RX>serial>D10/D11; LDR divider>analog>A0; DHT22 DATA>digital>D3; Fan driver>digital>D6; LCD SDA/SCL>I2C>A4/A5|smart buildings, comfort optimization, feedback control|sensor_box
amir-19-smart-street-lighting|Dr/Amir Elmslmany|Energy-Efficient Smart Street Lighting|Arduino Uno|Arduino Uno; LDR; PIR sensor; solar panel; charge controller; battery; LED lamp; MOSFET; current sensor optional|LDR divider>analog>A0; PIR OUT>digital>D2; MOSFET gate>PWM>D9; LED lamp>12V via MOSFET>battery; panel>charge controller>battery|light sensing, occupancy control, energy saving|lamp_post
amir-20-em-field-detector|Dr/Amir Elmslmany|EM Field Detector and Analyzer|Arduino Uno|Arduino Uno; inductive pickup coil; low-noise op-amp such as LM358 for demo; protection diodes; RC filter; OLED; resistors/capacitors|Pickup coil>op-amp input>conditioned analog signal; Op-amp output>ADC>A0; OLED SDA/SCL>I2C>A4/A5; clamp diodes>ADC rail protection>5V/GND|electromagnetism, induction, analog amplification, signal analysis|enclosure
mostafa-01-water-level-indicator|Dr/Mostafa Elhoshy|Water Level Indicator with Alarm|Arduino Uno|Arduino Uno; 4 conductive stainless probes; 1M/100k resistors as needed; 4 LEDs + 220R; buzzer; insulated container|Probe low>digital/analog sense>A0; Probe mid>A1>Arduino; Probe high>A2>Arduino; reference probe>GND through suitable resistor>GND; LEDs>D4-D7>220R to GND; Buzzer>D8>digital out|resistive sensing, comparator-style thresholds, alarm logic|panel
mostafa-02-obstacle-avoiding-robot|Dr/Mostafa Elhoshy|Obstacle Avoiding Robot with Ultrasonic|Arduino Uno|Arduino Uno; HC-SR04; SG90 servo; L298N/TB6612 motor driver; 2 gear motors; wheels; caster; chassis; battery pack; switch|HC-SR04 TRIG>D9>Arduino; HC-SR04 ECHO>D10>Arduino; Servo signal>D3>Arduino; Motor driver IN1/IN2>D5/D6; IN3/IN4>D7/D8; ENA/ENB>PWM>D11/D12 or jumpers; battery>motor driver>motors|distance measurement, scanning, autonomous obstacle avoidance|chassis
mostafa-03-voice-robotic-arm|Dr/Mostafa Elhoshy|Voice Controlled Robotic Arm|Arduino Uno|Arduino Uno; 4x servo motors; HC-05 Bluetooth or voice recognition module; separate 5V servo PSU; arm links; gripper; emergency stop|HC-05 TX>SoftwareSerial RX>D2; HC-05 RX>SoftwareSerial TX>D3 via divider; Base servo>D5; Shoulder>D6; Elbow>D9; Gripper>D10; servo power>external 5V>common GND|voice commands, serial control, servo kinematics|arm
mostafa-04-smart-irrigation|Dr/Mostafa Elhoshy|Smart Irrigation System|Arduino Uno|Arduino Uno; capacitive soil moisture sensor; 5V relay or MOSFET; small DC water pump; 16x2 I2C LCD; manual override button; water reservoir|Moisture AO>analog>A0; Pump driver>digital>D7; Override button>digital in>D2 with INPUT_PULLUP; LCD SDA/SCL>I2C>A4/A5; pump>external supply>driver|soil moisture measurement, automatic watering, hysteresis|sensor_box
mostafa-05-home-security-alerts|Dr/Mostafa Elhoshy|Home Security System with Alerts|Arduino Uno R4 WiFi or ESP32|WiFi-capable board; PIR sensor; magnetic reed switch; buzzer; status LED; optional email/webhook service|PIR OUT>digital in>D2/ESP32 GPIO27; Door reed>digital in>D3/GPIO26 with pull-up; Buzzer>digital out>D8/GPIO25; LED>digital out>D9/GPIO2|multi-sensor intrusion detection, network alerts|enclosure
mostafa-06-voice-home-automation|Dr/Mostafa Elhoshy|Voice Controlled Home Automation|Arduino Uno|Arduino Uno; HC-05 Bluetooth or voice module; opto-isolated relay board; low-voltage demo lamps/fan; 5V supply|HC-05 TX>SoftwareSerial RX>D2; HC-05 RX>SoftwareSerial TX>D3 via divider; Relay IN1>D7; Relay IN2>D8; relay contacts>low-voltage demo load>separate supply|voice processing, relay switching, safe isolation|enclosure
mostafa-07-self-balancing-robot|Dr/Mostafa Elhoshy|Self-Balancing Robot|Arduino Uno|Arduino Uno; MPU6050; TB6612FNG motor driver; 2 encoder gear motors; wheels; rigid chassis; battery; switch|MPU6050 SDA/SCL>I2C>A4/A5; Motor driver AIN1/AIN2>D7/D8; BIN1/BIN2>D9/D10; PWMA/PWMB>PWM>D5/D6; Encoders>interrupt pins>D2/D3|IMU fusion, PID control, feedback stability|chassis
mostafa-08-solar-tracking-system|Dr/Mostafa Elhoshy|Solar Tracking System|Arduino Uno|Arduino Uno; 4 LDRs; 4x10k resistors; 2 servos or geared pan-tilt; small solar panel; frame|LDR TL/TR/BL/BR>analog>A0/A1/A2/A3 via dividers; Pan servo>PWM>D9; Tilt servo>PWM>D10; panel>mechanical mount>pan-tilt|light sensing, differential control, solar tracking|solar_mount
mostafa-09-swarm-robotics|Dr/Mostafa Elhoshy|Swarm Robotics - Basic Coordination|Arduino Uno x2|2x Arduino Uno; 2 robot chassis kits; IR transmitters and receivers; motor drivers; batteries; optional ultrasonic sensors|IR TX>digital out>D3 each robot; IR RX>digital in>D2 each robot; Motor driver inputs>D5-D8>each Arduino; grounds>common per robot>local supply|multi-agent coordination, IR communication, formation following|chassis
mostafa-10-line-following-robot|Dr/Mostafa Elhoshy|Autonomous Line Following Robot|Arduino Uno|Arduino Uno; 3-5 TCRT5000 line sensors/array; L298N or TB6612 motor driver; 2 gear motors; chassis; battery|Line sensors L/C/R>analog or digital>A0/A1/A2; Motor driver IN1-IN4>D5-D8; PWM enables>D9/D10; battery>motor driver>motors|reflectance sensing, error calculation, PID line control|chassis
mostafa-11-oxygen-level-monitor|Dr/Mostafa Elhoshy|Medical Oxygen Level Monitoring with Alert System|Arduino Uno|Arduino Uno; MAX30102; OLED; buzzer; microSD module; optional HC-05; breadboard|MAX30102 SDA/SCL>I2C>A4/A5; OLED SDA/SCL>I2C>A4/A5; Buzzer>D7; SD CS>D10; SD MOSI/MISO/SCK>D11/D12/D13|PPG, heart-rate/SpO2 estimation, data logging|enclosure
mostafa-12-multi-sensor-fire-alarm|Dr/Mostafa Elhoshy|Multi-Sensor Fire Alarm System with Emergency Protocol|ESP32 or Uno R4 WiFi|ESP32/Uno R4 WiFi; MQ-2; DHT22; flame sensor; buzzer; LED strobe; relay; LCD/OLED|MQ-2 AO>ADC>GPIO34 via divider if required; DHT22 DATA>GPIO4; Flame DO>GPIO27; Buzzer>GPIO25; Strobe>GPIO26; Relay>GPIO33; display>I2C>GPIO21/22|sensor fusion, escalating alarms, false-alarm reduction|enclosure
mostafa-13-room-light-controller|Dr/Mostafa Elhoshy|Automatic Room Light Controller|Arduino Uno|Arduino Uno; LDR; 10k resistor; 10k potentiometer; 5V relay module or MOSFET; low-voltage LED strip/lamp|LDR divider>analog>A0; Pot wiper>analog>A1; Relay/MOSFET control>digital>D7; low-voltage lamp>driver output>separate supply|light sensing, adjustable threshold, hysteresis|enclosure
mostafa-14-traffic-density-monitor|Dr/Mostafa Elhoshy|Simple Traffic Density Monitor|Arduino Uno|Arduino Uno; 2 IR break-beam sensor pairs; 16x2 LCD; RGB LED; optional buzzer; model roadway|IR sensor 1>interrupt>D2; IR sensor 2>interrupt>D3; RGB R/G/B>D9/D10/D11 via resistors; LCD SDA/SCL>I2C>A4/A5; Buzzer>D8|vehicle counting, time-of-flight speed estimate, traffic classification|road_model
mostafa-15-pedestrian-crossing|Dr/Mostafa Elhoshy|Pedestrian-Crossing Smart Lighting|Arduino Uno|Arduino Uno; push button; 2 sets red/yellow/green LEDs; pedestrian red/green LEDs; buzzer; 1-digit/4-digit 7-segment module; resistors|Button>digital in>D2 INPUT_PULLUP; Vehicle R/Y/G>D3/D4/D5; Pedestrian R/G>D6/D7; Buzzer>D8; 7-segment module>digital/I2C>remaining pins|finite-state machine, timed crossing, accessibility feedback|road_model
ahmed-01-bike-solar-charging-station|Dr/Ahmed Ayoub|Bike Charging Station from Solar Cells with QR Code and Cloud using ESP32|ESP32|ESP32; ~200W prototype PV panel; MPPT controller; optional LiFePO4 battery + BMS; USB-C PD/DC output modules; INA219/current sensor; MOSFET/relay; display/LEDs; fuse; enclosure; QR label|INA219 SDA/SCL>I2C>GPIO21/22; Port enable driver>GPIO26; Display>I2C/SPI>board; PV>MPPT>battery/DC bus; fused DC bus>USB-C PD/output module; all low-voltage grounds>common as required|photovoltaics, MPPT, battery management, QR session control, telemetry|station
ahmed-02-phone-solar-charging-station|Dr/Ahmed Ayoub|Phone Charger Station from Solar Cells with QR Code and Cloud using ESP32|ESP32|ESP32; 50-150W PV panel; MPPT/PWM charge controller; optional 7-12Ah LiFePO4 battery+BMS; USB PD multi-port module; INA219; buck converter; fuses; display; QR label; enclosure|INA219 SDA/SCL>I2C>GPIO21/22; Port enable>GPIO26; PV>charge controller>battery/DC bus; DC bus>fuse>buck/USB PD; display>I2C>GPIO21/22|solar sizing, USB charging, session logging, IoT dashboard|station
ahmed-03-car-sharing-simulation|Dr/Ahmed Ayoub|Car Sharing Simulation — Mobile App + Cloud + ESP32 Lock|ESP32 + mobile/web app|ESP32; 5/12V solenoid/electric strike; MOSFET driver + flyback diode; reed/hall door sensor; regulated PSU; backup battery optional; manual key switch; optional GPS module; phone for app|Solenoid +>supply +>5/12V; Solenoid ->MOSFET drain>driver; MOSFET gate>digital out>GPIO26; Flyback diode>across solenoid>reverse-biased; Door sensor>digital in>GPIO27 pull-up; Key switch>digital in>GPIO25; GPS TX/RX>UART>GPIO16/17|client-server booking, secure device messaging, actuator fail-safe|lock_box
ahmed-04-smart-water-tap|Dr/Ahmed Ayoub|Smart Water Tap with Proximity Sensor|ESP32 or Arduino|ESP32/Arduino; IR/ToF proximity sensor; 12V water-rated normally-closed solenoid valve; logic-level MOSFET driver; flyback diode; YF-S201 flow sensor optional; waterproof enclosure; 12V PSU; plumbing fittings|Proximity OUT>digital/ADC>GPIO27; MOSFET gate>digital out>GPIO26; Solenoid>12V through MOSFET>driver; Flyback diode>across valve>reverse-biased; Flow pulse>interrupt>GPIO25; grounds>common low-voltage ground>GND|proximity sensing, debounce/hysteresis, fluid control, flow logging|tap_mount
ahmed-05-smart-parking-detector|Dr/Ahmed Ayoub|Smart Parking Space Detector|ESP32|ESP32; HC-SR04 or waterproof ultrasonic sensor; red LED; green LED; 220R resistors; 5V supply; optional cloud dashboard|TRIG>digital out>GPIO5; ECHO>digital in>GPIO18 through divider if 5V; Green LED>GPIO25 via 220R; Red LED>GPIO26 via 220R|distance sensing, occupancy threshold, cloud status|sensor_box
ahmed-06-rfid-attendance|Dr/Ahmed Ayoub|Smart Attendance System with RFID|ESP32|ESP32; RC522 RFID reader; buzzer; green/red LEDs; 220R resistors; Wi-Fi; Google Apps Script/other HTTPS endpoint|RC522 SDA/SS>GPIO5; SCK>GPIO18; MOSI>GPIO23; MISO>GPIO19; RST>GPIO27; Buzzer>GPIO25; Green LED>GPIO32; Red LED>GPIO33|RFID authentication, timestamps, web logging|enclosure
ahmed-07-remote-power-outlet|Dr/Ahmed Ayoub|Remote-Controlled Power Outlet|ESP32|ESP32; opto-isolated relay module; fuse and certified enclosure if ever used with mains; for student demo use isolated 12V lamp/fan load; push button; status LED|Relay IN>GPIO26; Button>GPIO27 INPUT_PULLUP; LED>GPIO25 via 220R; demo supply +>relay COM; relay NO>12V demo load +; load ->demo supply -|remote switching, isolation, safe load control|outlet_box
ahmed-08-automatic-dustbin-lid|Dr/Ahmed Ayoub|Automatic Dustbin Lid|Arduino Nano|Arduino Nano; HC-SR04; SG90/MG90S servo; 5V supply; hinge/bracket|HC-SR04 TRIG>D9; HC-SR04 ECHO>D10; Servo signal>D3; Servo VCC>external 5V; grounds>common>GND|distance sensing, servo motion, automation|lid_bracket
ahmed-09-motion-alarm|Dr/Ahmed Ayoub|Motion-Activated Alarm|Arduino Uno|Arduino Uno; PIR sensor; active buzzer; LED; 220R resistor; switch|PIR OUT>D2; Buzzer>D8; LED>D9 via 220R; sensor VCC>5V; grounds>GND|PIR motion detection, alarm state machine|enclosure
ahmed-10-temperature-controlled-fan|Dr/Ahmed Ayoub|Temperature-Controlled Fan|Arduino Uno|Arduino Uno; DHT11/DHT22; 5V/12V DC fan; MOSFET driver or relay; flyback diode for brushed fan; potentiometer optional|DHT DATA>D3; Fan driver gate/input>D6; Fan>external supply>driver; Pot wiper>A0 optional; grounds>common>GND|temperature sensing, threshold/hysteresis cooling|enclosure
ahmed-11-smart-door-lock|Dr/Ahmed Ayoub|Smart Door Lock with Mobile App|ESP32|ESP32; high-torque servo or small demo latch; push button; red/green LEDs; buzzer optional; regulated supply; mechanical override for demo|Servo signal>GPIO26; Button>GPIO27 INPUT_PULLUP; Green LED>GPIO32; Red LED>GPIO33; servo power>separate regulated 5V>common GND|Wi-Fi control, authorization, remote access, manual override|lock_box
ahmed-12-medication-dispenser|Dr/Ahmed Ayoub|Smart Medication Dispenser for Elderly|ESP32|ESP32; DS3231 RTC; 2-4 servo motors or stepper; HX711 + small load cell; buzzer; OLED; buttons; enclosure; carousel|RTC SDA/SCL>I2C>GPIO21/22; OLED SDA/SCL>I2C>GPIO21/22; Servo(s)>PWM>GPIO25/26/27; HX711 DT>SDA-like data>GPIO32; HX711 SCK>clock>GPIO33; Buzzer>GPIO13|scheduling, dispensing, load verification, missed-dose notification|dispenser
ahmed-13-fall-detection|Dr/Ahmed Ayoub|Fall Detection System for Elderly|ESP32|ESP32; MPU6050; buzzer; push button cancel; optional GPS module; battery; enclosure|MPU6050 SDA/SCL>I2C>GPIO21/22; Cancel button>GPIO27 INPUT_PULLUP; Buzzer>GPIO25; GPS TX/RX>UART>GPIO16/17|accelerometer/gyro magnitude, fall-event heuristics, emergency alert|wearable_case
ahmed-14-cough-sneeze-counter|Dr/Ahmed Ayoub|Cough/Sneeze Counter for Infection Tracking|ESP32|ESP32; MAX4466 microphone amplifier; push button; OLED optional; microSD optional|MAX4466 OUT>ADC>GPIO34; Button>GPIO27 INPUT_PULLUP; OLED SDA/SCL>I2C>GPIO21/22; SD CS>SPI>GPIO5|audio envelope/features, event counting, pattern classification|enclosure
ahmed-15-mood-room-lighting|Dr/Ahmed Ayoub|Mood-Based Room Lighting System|ESP32|ESP32; addressable WS2812B LED strip; MAX4466 microphone; 2-3 touch buttons; 5V LED PSU; level shifter recommended for long strips; 1000uF capacitor; 330R data resistor|LED DIN>GPIO18 via 330R/level shifter; MAX4466 OUT>ADC>GPIO34; Touch buttons>GPIO27/32/33; LED 5V>external PSU; grounds>common>GND|sound reactivity, presets, FFT/envelope mapping, lighting control|controller_box
'''.strip()


def parse_data():
    projects = []
    for raw in DATA.splitlines():
        if not raw.strip():
            continue
        parts = raw.split('|')
        if len(parts) != 8:
            raise ValueError(f'Bad project row ({len(parts)} fields): {raw[:100]}')
        branch, instructor, title, board, comps, wiring, concepts, cad = parts
        projects.append({
            'branch': branch,
            'instructor': instructor,
            'title': title,
            'board': board,
            'components': [x.strip() for x in comps.split(';')],
            'wiring': [x.strip() for x in wiring.split(';')],
            'concepts': concepts,
            'cad': cad,
        })
    return projects


def run(*args):
    subprocess.check_call(args)


def safe_name(title):
    return ''.join(c.lower() if c.isalnum() else '_' for c in title).strip('_')[:48]


def links_for(p):
    links = [('[OpenSCAD](https://github.com/openscad/openscad)', 'Parametric CAD source used for printable/mechanical models')]
    b = p['board'].lower()
    if 'esp32' in b:
        links.append(('[Arduino core for ESP32](https://github.com/espressif/arduino-esp32)', 'Open-source ESP32 Arduino framework'))
    if 'arduino' in b:
        links.append(('[Arduino AVR core](https://github.com/arduino/ArduinoCore-avr)', 'Open-source Arduino core for Uno/Nano-class AVR boards'))
    if 'raspberry' in b:
        links.append(('[Raspberry Pi documentation/source organization](https://github.com/raspberrypi)', 'Open-source Raspberry Pi software ecosystem'))
    t = p['title'].lower()
    if 'traffic density analyzer' in t or 'face recognition' in t or 'waste segregation' in t:
        links.append(('[OpenCV](https://github.com/opencv/opencv)', 'Open-source computer-vision library'))
    if 'air quality' in t:
        links.append(('[ThingSpeak Arduino](https://github.com/mathworks/thingspeak-arduino)', 'Open-source telemetry client option'))
    if 'voice' in t or 'door lock' in t or 'parking' in t:
        links.append(('[Blynk library](https://github.com/blynkkk/blynk-library)', 'Open-source IoT client option; service terms are separate'))
    return links


def firmware_for(p):
    b = p['board'].lower()
    title = p['title']
    header = f'// {title}\n// Educational starter firmware generated for this branch.\n// Calibrate sensor thresholds before demonstration.\n\n'
    if 'raspberry' in b:
        code = '''#!/usr/bin/env python3
import time
try:
    import cv2
except ImportError:
    cv2 = None


def main():
    if cv2 is None:
        print("Install dependencies from requirements.txt")
        return
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Camera not available")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        # Replace this baseline with the branch README's project-specific detector.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.putText(frame, f"mean={gray.mean():.1f}", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow("Electronic Physics Project", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
'''
        return 'src/main.py', code, 'opencv-python\nnumpy\n'
    if 'esp32' in b:
        code = header + r'''#include <WiFi.h>

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
'''
        return 'src/main.ino', code, None
    if 'arduino' in b:
        code = header + r'''const int SENSOR_PIN = A0;
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
'''
        return 'src/main.ino', code, None
    code = '''# Project software

This project combines embedded hardware with an app/cloud component. Use `wiring.csv` for the embedded node and implement the cloud/app flow described in the branch README. Keep device credentials out of Git; use environment variables or secret storage.
'''
    return 'src/README.md', code, None


def scad_for(p):
    cad = p['cad']
    label = p['branch'][:28]
    if cad in {'chassis', 'road_model'}:
        return f'''// {p['title']} — parametric demo chassis/base
$fn=48;
L=150; W=90; T=3; axle=3.2;
difference() {{
  cube([L,W,T], center=true);
  for (x=[-55,55], y=[-32,32]) translate([x,y,0]) cylinder(h=10,d=3.4,center=true);
  for (x=[-60,60]) translate([x,0,0]) cylinder(h=10,d=axle,center=true);
}}
translate([0,0,T/2]) linear_extrude(0.8) text("{label}", size=6, halign="center");
'''
    if cad == 'cubesat':
        return f'''// {p['title']} — 1U-style educational frame (not flight hardware)
$fn=40; S=100; rail=6;
for (x=[0,S-rail], y=[0,S-rail]) translate([x,y,0]) cube([rail,rail,S]);
for (z=[0,S-rail]) {{
  translate([0,0,z]) cube([S,rail,rail]);
  translate([0,S-rail,z]) cube([S,rail,rail]);
  translate([0,0,z]) cube([rail,S,rail]);
  translate([S-rail,0,z]) cube([rail,S,rail]);
}}
'''
    if cad == 'glasses':
        return f'''// Clip-on sensor pod for glasses temple; tune dimensions to the real frame.
$fn=48;
difference() {{ cube([42,20,12],center=true); translate([0,0,2]) cube([36,14,10],center=true); }}
translate([-25,0,0]) difference() {{ cube([12,8,10],center=true); cube([14,3.2,5],center=true); }}
'''
    if cad in {'station'}:
        return f'''// Tabletop solar charging station enclosure — scale before fabrication.
$fn=48;
difference() {{
  cube([160,100,90], center=true);
  translate([0,0,3]) cube([154,94,86], center=true);
  translate([0,-51,5]) cube([90,8,28], center=true); // port/display face opening
}}
'''
    if cad == 'dispenser':
        return f'''// Medication demo carousel; educational prototype only.
$fn=96; pockets=8;
difference() {{
  cylinder(h=8,d=120);
  cylinder(h=12,d=8);
  for(i=[0:pockets-1]) rotate([0,0,i*360/pockets]) translate([40,0,-1]) cylinder(h=12,d=24);
}}
'''
    if cad in {'arm'}:
        return '''// Simple servo bracket for educational robotic arm.
$fn=48;
difference(){ cube([45,24,4],center=true); for(x=[-16,16]) translate([x,0,0]) cylinder(h=8,d=3.2,center=true); }
translate([0,0,12]) difference(){ cube([24,24,20],center=true); cube([20,14,18],center=true); }
'''
    if cad in {'tap_mount', 'lid_bracket', 'solar_mount', 'camera_mount', 'coil_jig', 'nozzle_mount', 'lamp_post'}:
        return f'''// {p['title']} — generic adjustable mounting bracket.
$fn=48;
difference() {{
  cube([60,35,4],center=true);
  for(x=[-22,22]) translate([x,0,0]) cylinder(h=8,d=4.2,center=true);
}}
translate([0,14,18]) difference() {{ cube([40,4,32],center=true); translate([0,0,4]) cylinder(h=10,d=12,center=true, $fn=48); }}
'''
    # enclosure/sensor box/wearable/lock/outlet/controller/etc.
    return f'''// {p['title']} — parametric electronics enclosure base.
$fn=48;
L=90; W=60; H=28; wall=2.4;
difference() {{
  cube([L,W,H]);
  translate([wall,wall,wall]) cube([L-2*wall,W-2*wall,H]);
  translate([L/2-14,-1,10]) cube([28,wall+2,10]);
}}
for(x=[8,L-8], y=[8,W-8]) translate([x,y,wall]) difference() {{ cylinder(h=7,d=7); cylinder(h=8,d=3); }}
'''


def README(p):
    rows = []
    for w in p['wiring']:
        bits = w.split('>')
        if len(bits) == 3:
            rows.append(f'| {bits[0]} | {bits[1]} | {bits[2]} |')
        else:
            rows.append(f'| {w} | — | — |')
    comp_lines = '\n'.join(f'- {x}' for x in p['components'])
    wiring_rows = '\n'.join(rows)
    links = '\n'.join(f'- {a} — {d}' for a,d in links_for(p))
    safety = '''- Keep all student wiring at SELV/low voltage whenever possible.
- Power motors, servos, pumps and solenoids from a suitable separate supply; connect grounds only where the circuit requires it.
- Add fuses/current limiting to battery and solar power paths.
- Do not connect exposed breadboard wiring directly to mains electricity.
- Calibrate sensors against known references before presenting measurements as quantitative results.'''
    title_lower = p['title'].lower()
    if any(k in title_lower for k in ['health', 'oxygen', 'fall', 'cough', 'eeg', 'visually impaired']):
        safety += '\n- This is an educational prototype, not a medical/clinical or life-safety device. Do not use it for diagnosis or critical decisions.'
    if 'fire' in title_lower:
        safety += '\n- Demonstrate suppression with a harmless pointer/air/water model under supervision; do not automate discharge of a real extinguisher without qualified safety review.'
    if 'power outlet' in title_lower or 'home automation' in title_lower:
        safety += '\n- For the university demo, switch an isolated low-voltage load. Any mains implementation must use a certified enclosure, protection devices, and qualified supervision.'
    return f'''# {p['title']}

**Instructor:** {p['instructor']}  
**Primary platform:** {p['board']}  
**Physics / engineering concepts:** {p['concepts']}

## Goal
Build a demonstrable educational prototype of **{p['title']}** with measurable inputs, clear outputs, reproducible wiring, and a short validation experiment.

## Components / BOM
{comp_lines}

Add jumper wires, headers/connectors, a breadboard or perfboard, appropriate resistors, an enclosure, and a correctly rated regulated supply as required by the physical build.

## Wiring
`wiring.csv` is the pin-by-pin source of truth.

| Component / node | Signal / connection | Board pin / destination |
|---|---|---|
{wiring_rows}

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
{safety}

## 3D / mechanical design
A parametric OpenSCAD model is included under `cad/`. It is a starting design sized for a classroom prototype. Measure the real PCB/sensor/servo first and adjust the parameters before printing. Export to STL from OpenSCAD only after checking clearances and cable paths.

## Open-source building blocks
{links}

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
'''


def write_project(p):
    branch = p['branch']
    run('git', 'checkout', '-B', branch, 'origin/main')
    # Remove repository-generation machinery from the project branch itself.
    if (REPO / '.github').exists():
        shutil.rmtree(REPO / '.github')
    if (REPO / 'PROJECTS.md').exists():
        (REPO / 'PROJECTS.md').unlink()

    (REPO / 'README.md').write_text(README(p), encoding='utf-8')

    with (REPO / 'wiring.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['component_or_node', 'signal_or_connection', 'board_pin_or_destination'])
        for w in p['wiring']:
            bits = w.split('>')
            bits = (bits + ['—', '—'])[:3]
            writer.writerow(bits)

    src_path, source, requirements = firmware_for(p)
    path = REPO / src_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding='utf-8')
    if requirements:
        (REPO / 'requirements.txt').write_text(requirements, encoding='utf-8')

    cad_dir = REPO / 'cad'
    cad_dir.mkdir(exist_ok=True)
    (cad_dir / 'design.scad').write_text(scad_for(p), encoding='utf-8')

    run('git', 'add', '-A')
    subprocess.run(['git', 'commit', '-m', f"Build project: {p['title']}"] , check=True)
    run('git', 'push', '--force', 'origin', branch)


def main():
    projects = parse_data()
    assert len(projects) == 50, f'Expected 50 projects, found {len(projects)}'
    run('git', 'config', 'user.name', 'github-actions[bot]')
    run('git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    run('git', 'fetch', 'origin', 'main')
    for i, p in enumerate(projects, 1):
        print(f'[{i:02d}/50] {p["branch"]}: {p["title"]}')
        write_project(p)
    run('git', 'checkout', 'main')
    print('Generated and pushed all 50 project branches.')

if __name__ == '__main__':
    main()
