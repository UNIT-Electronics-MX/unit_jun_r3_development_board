# Demo Text - Text Display on LED Matrix

## Description
Displays scrolling text and characters on a 5x5 NeoPixel LED matrix using custom 3x5 pixel font.

## Features
- Custom 3x5 pixel font for ASCII characters (32-122)
- Scrolling text animation
- Optimized for 5x5 LED matrix layout
- Supports numbers, letters, and special characters

## Hardware Required
- UNIT JUN R3 Development Board
- 5x5 NeoPixel LED matrix (25 LEDs total)
- Connection to pin 8

## Libraries Used
- `Adafruit_NeoPixel.h`

## Configuration
```cpp
#define PIN        8         // NeoPixel data pin
#define NUM_LEDS   25        // Total LEDs in matrix
#define MATRIX_WIDTH  5      // Matrix width
#define MATRIX_HEIGHT 5      // Matrix height  
#define DELAYVAL   100       // Animation delay (ms)
```

## Usage
1. Upload the code to your UNIT JUN R3
2. Connect 5x5 NeoPixel matrix to pin 8
3. Watch scrolling text display on the LED matrix
4. Modify the text string in code to display custom messages

## Functions
- `getPixelIndex(x,y)` - Converts x,y coordinates to LED index
- `drawChar(char, x, y, color)` - Draws character at position with color
- `scrollText(text, color, delay)` - Scrolls text across matrix
