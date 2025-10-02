# Demo2 OLED - OLED Display with Sensor Readings

## Description
Combines OLED display functionality with NeoPixel LEDs to show sensor readings and create interactive visual feedback.

## Features
- SSD1306 OLED display (128x64)
- Real-time ADC sensor readings
- Color cycling with Spanish names
- NeoPixel LED feedback
- Serial monitor output
- Graceful OLED failure handling

## Hardware Required
- UNIT JUN R3 Development Board
- SSD1306 OLED display (I2C, address 0x3C)
- 25 NeoPixel LEDs on pin 8
- Analog sensor connected to ADC

## Libraries Used
- `Wire.h` - I2C communication
- `Adafruit_GFX.h` - Graphics library
- `Adafruit_SSD1306.h` - OLED display
- `Adafruit_NeoPixel.h` - LED control

## Configuration
```cpp
#define SCREEN_WIDTH 128     // OLED width
#define SCREEN_HEIGHT 64     // OLED height
#define OLED_ADDRESS 0x3C    // I2C address
#define PIN        8         // NeoPixel pin
#define NUMPIXELS 25         // LED count
```

> **Note:** Make sure the OLED display is connected to the I2C pins (SDA, SCL) using the compatible JST 1.0mm 4-pin connector on the UNIT JUN R3 board.

## Functionality
- **ADC Reading**: Updates every 500ms
- **Color Cycling**: Changes every 1000ms through Red, Green, Blue
- **OLED Display**: Shows sensor values and color names in Spanish
- **LED Feedback**: Visual representation of current color
- **Error Handling**: Continues operation if OLED not detected

## Usage
1. Connect OLED display via I2C
2. Connect analog sensor to ADC input
3. Upload code and open Serial Monitor
4. Watch real-time sensor data on OLED and LEDs
