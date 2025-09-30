# Getting Started

## Quick Start Guide

### 1. Hardware Setup

1. **Connect to Computer**: Use the USB-C cable to connect your UNIT JUN R3 to your computer
2. **Install Drivers**: Most operating systems will automatically recognize the board
3. **Verify Connection**: Check that the power LED is on

### 2. Development Environment

#### Arduino IDE
1. Install [Arduino IDE](https://www.arduino.cc/en/software) 
2. Add the ATmega328P board support if needed
3. Select **Arduino Uno** as the board type
4. Install required libraries:
   - Adafruit NeoPixel Library

### 3. First Program

Try the basic NeoPixel example to verify everything works:

```cpp
#include <Adafruit_NeoPixel.h>

#define PIN        8
#define NUMPIXELS 25

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin();
  pixels.setBrightness(50);
}

void loop() {
  pixels.clear();
  pixels.setPixelColor(0, pixels.Color(255, 0, 0)); // Red
  pixels.show();
  delay(1000);
}
```

### 4. Next Steps

- Explore the [Examples](./examples/) section
- Check out QWIIC sensor integration
- Try different NeoPixel patterns
