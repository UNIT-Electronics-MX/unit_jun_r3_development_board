# CPP Example 00 - Neo Blink

## Description
Basic validation sketch for UNIT JUN R3.
It blinks the onboard LED and toggles the 5x5 NeoPixel matrix.

## Features
- Onboard LED blink on pin 13
- NeoPixel matrix ON/OFF test on pin 8
- Minimal setup for first board verification

## Hardware Required
- UNIT JUN R3 Development Board
- Connection by USB-C

## Libraries Used
- `Adafruit_NeoPixel.h`

## Configuration
```cpp
#define LED_PIN 13
#define NEOPIXEL_PIN 8
#define NUM_PIXELS 25
```

## Usage
1. Open `cpp_example_00_neo_blink.ino` in Arduino IDE.
2. Select board **Arduino Uno** and the correct serial port.
3. Upload the sketch.
4. Verify the LED blinks and the NeoPixel matrix toggles white/off.
