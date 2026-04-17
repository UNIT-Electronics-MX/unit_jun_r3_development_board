#include <Adafruit_NeoPixel.h>

#define LED_PIN 13
#define NEOPIXEL_PIN 8
#define NUM_PIXELS 25

Adafruit_NeoPixel matrix(NUM_PIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
 pinMode(LED_PIN, OUTPUT);
 matrix.begin();
 matrix.show();
}

void loop() {
 // Toggle onboard LED
 digitalWrite(LED_PIN, HIGH);

 // Turn NeoPixels ON (white)
 for (int i = 0; i < NUM_PIXELS; i++) {
   matrix.setPixelColor(i, matrix.Color(50, 50, 50));
 }
 matrix.show();
 delay(500);

 digitalWrite(LED_PIN, LOW);

 // Turn NeoPixels OFF
 matrix.clear();
 matrix.show();
 delay(500);
}
