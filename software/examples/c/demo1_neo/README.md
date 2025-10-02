# Demo1 Neo - Basic NeoPixel Animations

## Description
Basic NeoPixel LED demonstrations with colorful animations and effects on a 25-LED strip.

## Features
- Color wipe animation
- Theater chase effect
- Aztec-inspired color palette
- Rainbow animations
- Bouncing dot effect
- Breathing light effect

## Hardware Required
- UNIT JUN R3 Development Board
- 25 NeoPixel LEDs (WS2812B strip)
- Connection to pin 8

## Libraries Used
- `Adafruit_NeoPixel.h`

## Configuration
```cpp
#define PIN        8         // NeoPixel data pin
#define NUMPIXELS 25         // Number of LEDs
#define DELAYVAL   50        // Base animation delay (ms)
```

## Animation Effects
1. **Color Wipe** - Sequential LED lighting in solid colors
2. **Theater Chase** - Moving groups of 3 LEDs creating chase effect
3. **Aztec Colors** - Green, gold, and red color combinations
4. **Rainbow Cycle** - Smooth rainbow color transitions
5. **Bouncing Dot** - Single LED bouncing back and forth
6. **Breathing** - Smooth brightness fade in/out effect

## Usage
1. Upload code to UNIT JUN R3
2. Connect NeoPixel strip to pin 8
3. Watch various colorful animation effects cycle automatically
