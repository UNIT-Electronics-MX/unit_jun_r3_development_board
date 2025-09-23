# Code Examples

> 📋 **Auto-generated**: 2025-09-23 09:30:46

## Available Examples

### ⚡ demo_text: demo_text.ino
```cpp
#include <Adafruit_NeoPixel.h>

#define PIN        8
#define NUM_LEDS   25
#define MATRIX_WIDTH  5
#define MATRIX_HEIGHT 5
#define DELAYVAL   100

Adafruit_NeoPixel strip(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

// Función para convertir coordenadas x,y a índice LED
int getPixelIndex(int x, int y) {
  if (x < 0 || x >= MATRIX_WIDTH || y < 0 || y >= MATRIX_HEIGHT) {
    return -1; // Fuera de los límites
  }
  
  // Para matriz 5x5 con conexión lineal (cada fila consecutiva)
  // Asumiendo que los LEDs van de izquierda a derecha en cada fila
  return y * MATRIX_WIDTH + x;
}

// Definición de caracteres 3x5 optimizados para matriz 5x5
const uint8_t font3x5[][3] = {
  // 32: Espacio
  {0x00, 0x00, 0x00},
```
[📄 Ver código completo](software/examples/c/demo_text/demo_text.ino)

### ⚡ demo1_neo: demo1_neo.ino
```cpp
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
```
[📄 Ver código completo](software/examples/c/demo1_neo/demo1_neo.ino)

### ⚡ demo3_neo: demo3_neo.ino
```cpp
#include <Adafruit_NeoPixel.h>

#define PIN 8
#define NUMPIXELS 25
#define DELAYVAL 50

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

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
```
[📄 Ver código completo](software/examples/c/demo3_neo/demo3_neo.ino)

### ⚡ demo2_oled: demo2_oled.ino
```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET   -1
#define OLED_ADDRESS 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
bool oledOk = false;

#define PIN        8
#define NUMPIXELS 25
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

const unsigned long ADC_INTERVAL   = 500;
const unsigned long COLOR_INTERVAL = 1000;

unsigned long lastADC   = 0;
unsigned long lastColor = 0;

int colorStage = 0;
uint32_t colors[3];
const char* colorNames[3] = {"Rojo", "Verde", "Azul"};
```
[📄 Ver código completo](software/examples/c/demo2_oled/demo2_oled.ino)

