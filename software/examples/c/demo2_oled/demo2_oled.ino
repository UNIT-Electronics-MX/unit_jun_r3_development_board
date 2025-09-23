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

void setup() {
    Serial.begin(9600);
    while (!Serial);
    Wire.begin();
    if (display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
        oledOk = true;
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(SSD1306_WHITE);
    } else {
        Serial.println("OLED no detectada, continuo sin pantalla");
    }
    pixels.begin();
    pixels.setBrightness(64);
    pixels.clear();
    pixels.show();
    colors[0] = pixels.Color(255, 0,   0);
    colors[1] = pixels.Color(0,   255, 0);
    colors[2] = pixels.Color(0,   0,   255);
}

void loop() {
    unsigned long now = millis();

    if (now - lastADC >= ADC_INTERVAL) {
        lastADC = now;
        int valor = analogRead(A0);
        int barra = map(valor, 0, 1023, 0, SCREEN_WIDTH);
        if (oledOk) {
            display.clearDisplay();
            display.setCursor(0, 0);
            display.print("ADC A0: ");
            display.print(valor);
            display.setCursor(0, 10);
            display.print("Color: ");
            display.print(colorNames[colorStage]);
            display.fillRect(0, 20, barra, 8, SSD1306_WHITE);
            display.display();
        }
    }

    if (now - lastColor >= COLOR_INTERVAL) {
        lastColor = now;
        colorStage = (colorStage + 1) % 3;
        for (int i = 0; i < NUMPIXELS; i++) {
            pixels.setPixelColor(i, colors[colorStage]);
        }
        pixels.show();
    }
}
