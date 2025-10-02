# Demo3 Neo - Advanced NeoPixel Effects

## Description
Advanced NeoPixel animations featuring complex lighting effects including bouncing dots, confetti, and smooth color transitions.

## Features
- Color wipe animation
- Theater chase effect  
- Rainbow color wheel algorithm
- Bouncing dot animation
- Confetti particle effect with fade
- Smooth color transitions
- Random color generation

## Hardware Required
- UNIT JUN R3 Development Board
- 25 NeoPixel LEDs (WS2812B strip)
- Connection to pin 8

## Libraries Used
- `Adafruit_NeoPixel.h`

## Configuration
```cpp
#define PIN 8            // NeoPixel data pin
#define NUMPIXELS 25     // Number of LEDs
#define DELAYVAL 50      // Base animation delay (ms)
```

## Animation Effects
1. **Color Wipe** - Sequential LED coloring
2. **Theater Chase** - Moving LED groups
3. **Bouncing Dot** - Single LED bouncing with trail
4. **Confetti** - Random sparkle effect with fade-out
5. **Rainbow Wheel** - Smooth color transitions using HSV color space

## Key Functions
- `Wheel(byte)` - Converts 0-255 to rainbow colors
- `confetti(wait)` - Creates random sparkle effects with decay
- `bouncing(color, wait)` - Bounces single LED back and forth

## Usage
1. Upload code to UNIT JUN R3
2. Connect 25-LED NeoPixel strip to pin 8
3. Enjoy advanced lighting effects cycling automatically
4. Modify timing and colors for custom effects
