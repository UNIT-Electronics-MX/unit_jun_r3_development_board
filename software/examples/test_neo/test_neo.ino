#include <Adafruit_NeoPixel.h>

#define PIN        8
#define NUMPIXELS 25
#define DELAYVAL   50

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
    pixels.begin();
    pixels.setBrightness(64);
    pixels.clear();
    pixels.show();
}

void colorWipe(uint32_t color, int wait) {
    for (int i = 0; i < NUMPIXELS; i++) {
        pixels.setPixelColor(i, color);
        pixels.show();
        delay(wait);
    }
}

void theaterChase(uint32_t color, int wait) {
    for (int a = 0; a < 10; a++) {
        for (int b = 0; b < 3; b++) {
            pixels.clear();
            for (int i = b; i < NUMPIXELS; i += 3) {
                pixels.setPixelColor(i, color);
            }
            pixels.show();
            delay(wait);
        }
    }
}

uint32_t aztecPalette[] = {
    pixels.Color(34, 139, 34),
    pixels.Color(218, 165, 32),
    pixels.Color(178, 34, 34),
    pixels.Color(255, 215, 0),
    pixels.Color(0, 100, 0)
};
const int SNAKE_LEN = 7;

void quetzalcoatlEffect(int wait) {
    int head = 0;
    int paletteSize = sizeof(aztecPalette) / sizeof(aztecPalette[0]);

    for (int step = 0; step < NUMPIXELS + SNAKE_LEN; step++) {
        pixels.clear();

        for (int i = 0; i < SNAKE_LEN; i++) {
            int idx = (head - i + NUMPIXELS) % NUMPIXELS;
            uint32_t color = aztecPalette[i % paletteSize];
            pixels.setPixelColor(idx, color);
        }

        pixels.show();
        delay(wait);
        head = (head + 1) % NUMPIXELS;
    }
}

uint32_t Wheel(byte WheelPos) {
    WheelPos = 255 - WheelPos;
    if (WheelPos < 85) {
        return pixels.Color(255 - WheelPos * 3, 0, WheelPos * 3);
    } else if (WheelPos < 170) {
        WheelPos -= 85;
        return pixels.Color(0, WheelPos * 3, 255 - WheelPos * 3);
    } else {
        WheelPos -= 170;
        return pixels.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
    }
}

void rainbowCycle(int wait) {
    for (int j = 0; j < 256; j++) {
        for (int i = 0; i < NUMPIXELS; i++) {
            pixels.setPixelColor(i, Wheel((i * 256 / NUMPIXELS + j) & 255));
        }
        pixels.show();
        delay(wait);
    }
}

void scanner(uint32_t color, int wait) {
    for (int i = 0; i < NUMPIXELS; i++) {
        pixels.clear();
        pixels.setPixelColor(i, color);
        pixels.show();
        delay(wait);
    }
    for (int i = NUMPIXELS - 2; i > 0; i--) {
        pixels.clear();
        pixels.setPixelColor(i, color);
        pixels.show();
        delay(wait);
    }
}

void confetti(int wait) {
    for (int i = 0; i < NUMPIXELS; i++) {
        uint32_t c = pixels.getPixelColor(i);
        uint8_t r = (c >> 16) & 0xFF;
        uint8_t g = (c >> 8) & 0xFF;
        uint8_t b = c & 0xFF;
        pixels.setPixelColor(i, pixels.Color(r * 0.94, g * 0.94, b * 0.94));
    }
    int pos = random(NUMPIXELS);
    pixels.setPixelColor(pos, Wheel(random(0, 255)));
    pixels.show();
    delay(wait);
}

void fadeInOut(uint32_t color) {
    uint8_t r = (color >> 16) & 0xFF;
    uint8_t g = (color >> 8) & 0xFF;
    uint8_t b = color & 0xFF;
    for (int bri = 0; bri <= 64; bri++) {
        pixels.setBrightness(bri);
        colorWipe(pixels.Color(r, g, b), 5);
    }
    for (int bri = 64; bri >= 0; bri--) {
        pixels.setBrightness(bri);
        colorWipe(pixels.Color(r, g, b), 5);
    }
}

void loop() {
    colorWipe(pixels.Color(255, 0, 0), DELAYVAL);
    colorWipe(pixels.Color(0, 255, 0), DELAYVAL);
    colorWipe(pixels.Color(0, 0, 255), DELAYVAL);
    delay(500);

    theaterChase(pixels.Color(127, 127, 127), DELAYVAL);
    delay(500);

    quetzalcoatlEffect(60);
    delay(500);
    unsigned long start = millis();
    while (millis() - start < 3000) {
        confetti(30);
    }
    delay(500);

    pixels.clear();
    pixels.show();
    delay(1000);
}
