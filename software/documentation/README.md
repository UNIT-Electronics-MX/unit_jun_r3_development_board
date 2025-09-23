---
title: "JUN R3 Development Board"
version: "1.0"
modified: "2025-04-30"
output: "JUN R3 Development Board"
subtitle: "Development Board based on ATmega328P with NeoPixel Matrix"
---

<!--
# README_TEMPLATE.md
This file serves as an input to generate a datasheet-style technical PDF.
Fill in each section without deleting or modifying the existing headings.
-->

# JUN R3 Development Board

![alt text](../../hardware/resources/unit_top_V_0_0_1_ue0099_Sensor_Touch.png) <!-- FILL HERE: replace image if needed -->


## KEY TECHNICAL SPECIFICATIONS

<!-- 
========================================
EDITABLE SPECIFICATIONS TEMPLATE
========================================
Edita los valores a continuación según necesites.
El formato se mantendrá automáticamente en el PDF generado.
-->
- **Microcontroller:** ATmega328P (8-bit AVR)
- **Clock Speed:** 16 MHz
- **Flash Memory:** 32KB
- QWIIC Connector
- NeoPixel 5x5 Matrix
- USB-C Power Input (5V)


### 🔌 CONNECTIVITY (Conectividad)
<!-- Edita las interfaces y conectores disponibles -->
| Interface | Details |
|-----------|---------|
| **Primary Interface** | GPIO (Interrupt) |
| **Logic Levels** | VCC (2V – 5.5V tolerant) |
| **Matrix 5x5** | GPIO-8 |





## Electrical Characteristics & Signal Overview

<!-- FILL HERE -->
- **Wide supply range**: 2.0 V to 5.5 V, compatible with 3.3 V and 5 V systems.  
- **Low power**: < 1 μA in standby mode.

<!-- <!-- ## Applications



## Features -->

<!-- FILL HERE -->
## Features

- **ATMEGA328P** microcontroller (8-bit AVR)
- **NeoPixel 5x5 Matrix** for visual feedback
- **QWIIC Connector** for I2C peripherals
- **USB-C Power Input** (5V)
- **Breadboard Friendly**: Standard 0.1" pin spacing
- **Compact Size**: 40mm x 40mm
- **Wide Supply Range**: 2.0 V to 5.5 V,


## Block Diagram

![Function diagram](../../hardware/resources/unit_pinout_v_0_0_1_ue0099_sensor_touch_en.png) <!-- FILL HERE: replace image if needed -->

## Dimensions

![Dimensions](../../hardware/resources/unit_dimension_V_0_0_1_ue0099_Sensor_Touch.png) <!-- FILL HERE: replace image if needed -->

## Usage

<!-- FILL HERE -->
Mention supported development platforms and toolchains 

- (e.g., Arduino IDE, ESP-IDF, PlatformIO, etc.)

## Downloads

<!-- FILL HERE -->
- [Schematic PDF](docs/schematic.pdf)
- [Board Dimensions DXF](docs/dimensions.dxf)
- [Pinout Diagram PNG](docs/pinout.png)

## Purchase

<!-- FILL HERE -->
- [Buy from vendor](https://example.com)
- [Product page](https://example.com/product/template-board)
