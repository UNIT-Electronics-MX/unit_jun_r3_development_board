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
  // 33: !
  {0x00, 0x17, 0x00},
  // 34: "
  {0x03, 0x00, 0x03},
  // 35: #
  {0x0A, 0x1F, 0x0A},
  // 36: $
  {0x12, 0x1F, 0x09},
  // 37: %
  {0x13, 0x08, 0x19},
  // 38: &
  {0x0A, 0x15, 0x08},
  // 39: '
  {0x00, 0x03, 0x00},
  // 40: (
  {0x00, 0x0E, 0x11},
  // 41: )
  {0x11, 0x0E, 0x00},
  // 42: *
  {0x0A, 0x04, 0x0A},
  // 43: +
  {0x04, 0x0E, 0x04},
  // 44: ,
  {0x00, 0x18, 0x00},
  // 45: -
  {0x04, 0x04, 0x04},
  // 46: .
  {0x00, 0x10, 0x00},
  // 47: /
  {0x18, 0x04, 0x03},
  // 48: 0
  {0x0E, 0x11, 0x0E},
  // 49: 1
  {0x00, 0x1F, 0x00},
  // 50: 2
  {0x19, 0x15, 0x12},
  // 51: 3
  {0x11, 0x15, 0x0A},
  // 52: 4
  {0x07, 0x04, 0x1F},
  // 53: 5
  {0x17, 0x15, 0x09},
  // 54: 6
  {0x0E, 0x15, 0x08},
  // 55: 7
  {0x01, 0x01, 0x1F},
  // 56: 8
  {0x0A, 0x15, 0x0A},
  // 57: 9
  {0x02, 0x15, 0x0E},
  // 58: :
  {0x00, 0x0A, 0x00},
  // 59: ;
  {0x00, 0x1A, 0x00},
  // 60: <
  {0x04, 0x0A, 0x11},
  // 61: =
  {0x0A, 0x0A, 0x0A},
  // 62: >
  {0x11, 0x0A, 0x04},
  // 63: ?
  {0x01, 0x15, 0x02},
  // 64: @
  {0x0E, 0x15, 0x16},
  // 65: A
  {0x1E, 0x05, 0x1E},
  // 66: B
  {0x1F, 0x15, 0x0A},
  // 67: C
  {0x0E, 0x11, 0x11},
  // 68: D
  {0x1F, 0x11, 0x0E},
  // 69: E
  {0x1F, 0x15, 0x11},
  // 70: F
  {0x1F, 0x05, 0x01},
  // 71: G
  {0x0E, 0x15, 0x1D},
  // 72: H
  {0x1F, 0x04, 0x1F},
  // 73: I
  {0x11, 0x1F, 0x11},
  // 74: J
  {0x08, 0x10, 0x0F},
  // 75: K
  {0x1F, 0x04, 0x1B},
  // 76: L
  {0x1F, 0x10, 0x10},
  // 77: M
  {0x1F, 0x02, 0x1F},
  // 78: N
  {0x1F, 0x02, 0x1C},
  // 79: O
  {0x0E, 0x11, 0x0E},
  // 80: P
  {0x1F, 0x05, 0x02},
  // 81: Q
  {0x0E, 0x19, 0x1E},
  // 82: R
  {0x1F, 0x05, 0x1A},
  // 83: S
  {0x12, 0x15, 0x09},
  // 84: T
  {0x01, 0x1F, 0x01},
  // 85: U
  {0x0F, 0x10, 0x0F},
  // 86: V
  {0x07, 0x18, 0x07},
  // 87: W
  {0x1F, 0x08, 0x1F},
  // 88: X
  {0x1B, 0x04, 0x1B},
  // 89: Y
  {0x03, 0x1C, 0x03},
  // 90: Z
  {0x19, 0x15, 0x13}
};

// Mapeo de caracteres ASCII a índices en el array font3x5
int getCharIndex(char c) {
  // Mapeo directo ASCII: caracteres del 32 al 90 (espacio a Z)
  if (c >= 32 && c <= 90) {
    return c - 32; // Índice directo basado en código ASCII
  }
  // Convertir minúsculas a mayúsculas
  else if (c >= 97 && c <= 122) { // a-z
    return (c - 97) + (65 - 32); // Mapear a A-Z
  }
  else {
    return 0; // Espacio por defecto para caracteres no soportados
  }
}

void displayChar(char c, int offsetX, int offsetY, uint32_t color) {
  int charIndex = getCharIndex(c);
  
  // Orientación optimizada para matriz 5x5
  for (int col = 0; col < 3; col++) {
    uint8_t columnData = font3x5[charIndex][2 - col]; // Invertir el orden de las columnas
    
    for (int row = 0; row < 5; row++) {
      if (columnData & (1 << row)) {
        // Mapeo directo para orientación correcta
        int newX = offsetX + row;        // row se convierte en X (horizontal)
        int newY = offsetY + col;        // col se convierte en Y (vertical)
        
        int pixelIndex = getPixelIndex(newX, newY);
        if (pixelIndex >= 0 && pixelIndex < NUM_LEDS) {
          strip.setPixelColor(pixelIndex, color);
        }
      }
    }
  }
}

void displayText(String text, int offsetX, int offsetY, uint32_t color) {
  strip.clear();
  
  for (int i = 0; i < text.length(); i++) {
    // Cada carácter se coloca verticalmente uno debajo del otro
    int charY = offsetY + (i * 4); // 4 píxeles de separación vertical entre caracteres
    if (offsetX >= -5 && offsetX < MATRIX_WIDTH && charY >= -3 && charY + 2 < MATRIX_HEIGHT + 3) {
      displayChar(text[i], offsetX, charY, color);
    }
  }
  
  strip.show();
}

void scrollText(String text, uint32_t color, int delayTime) {
  // Barrido en el eje vertical (de arriba hacia abajo)
  // El texto entra desde arriba (posición negativa) y sale por abajo
  int textLength = text.length() * 4; // Longitud total del texto en píxeles
  
  for (int offset = -textLength; offset < MATRIX_HEIGHT + 3; offset++) {
    displayText(text, 0, offset, color); // Posición X fija, Y variable
    delay(delayTime);
  }
}

// Función para invertir cadenas de texto automáticamente
String reverseString(String text) {
  String reversed = "";
  for (int i = text.length() - 1; i >= 0; i--) {
    reversed += text[i];
  }
  return reversed;
}

// Efecto bandera mexicana horizontal para 5x5
void banderaMexicana(int duration) {
  for (int cycle = 0; cycle < duration; cycle++) {
    strip.clear();
    
    // Dividir la matriz en 3 secciones horizontales
    for (int y = 0; y < MATRIX_HEIGHT; y++) {
      for (int x = 0; x < MATRIX_WIDTH; x++) {
        int pixelIndex = getPixelIndex(x, y);
        if (pixelIndex >= 0) {
          // Simular el águila: área central apagada (1 LED en el centro)
          bool isEagleArea = (x == 2 && y == 2);
          
          if (isEagleArea) {
            // Área del águila apagada
            strip.setPixelColor(pixelIndex, strip.Color(0, 0, 0));
          } else if (y < 2) {
            // Rojo (parte superior)
            strip.setPixelColor(pixelIndex, strip.Color(255, 0, 0));
          } else if (y < 4) {
            // Blanco (centro)
            strip.setPixelColor(pixelIndex, strip.Color(255, 255, 255));
          } else {
            // Verde (parte inferior)
            strip.setPixelColor(pixelIndex, strip.Color(0, 255, 0));
          }
        }
      }
    }
    
    strip.show();
    delay(50);
  }
}

// Efecto bandera ondeando para 5x5
void banderaOndeando(int cycles) {
  for (int cycle = 0; cycle < cycles; cycle++) {
    for (int wave = 0; wave < 8; wave++) {
      strip.clear();
      
      for (int y = 0; y < MATRIX_HEIGHT; y++) {
        for (int x = 0; x < MATRIX_WIDTH; x++) {
          int pixelIndex = getPixelIndex(x, y);
          if (pixelIndex >= 0) {
            // Crear efecto de ondeo
            int waveOffset = (x + wave) % 3;
            int adjustedY = y;
            
            // Ajustar posición Y basada en la onda
            if (waveOffset == 1) adjustedY = (y > 0) ? y - 1 : y;
            else if (waveOffset == 2) adjustedY = (y < MATRIX_HEIGHT - 1) ? y + 1 : y;
            
            // Simular el águila
            bool isEagleArea = (x == 2 && adjustedY == 2);
            
            if (isEagleArea) {
              strip.setPixelColor(pixelIndex, strip.Color(0, 0, 0));
            } else if (adjustedY < 2) {
              strip.setPixelColor(pixelIndex, strip.Color(255, 0, 0)); // Rojo
            } else if (adjustedY < 4) {
              strip.setPixelColor(pixelIndex, strip.Color(255, 255, 255)); // Blanco
            } else {
              strip.setPixelColor(pixelIndex, strip.Color(0, 255, 0)); // Verde
            }
          }
        }
      }
      
      strip.show();
      delay(100);
    }
  }
}

// Fuego artificial individual para 5x5
void fuegoIndividual(uint32_t color) {
  // Posición aleatoria de lanzamiento
  int launchX = random(1, MATRIX_WIDTH - 1);
  
  // FASE 1: Trayectoria ascendente desde abajo
  for (int y = MATRIX_HEIGHT - 1; y >= 1; y--) {
    strip.clear();
    
    // Dibujar la trayectoria
    for (int trail = 0; trail < 2 && (y + trail) < MATRIX_HEIGHT; trail++) {
      int pixelIndex = getPixelIndex(launchX, y + trail);
      if (pixelIndex >= 0) {
        if (trail == 0) {
          strip.setPixelColor(pixelIndex, color); // Punto principal
        } else {
          // Estela
          strip.setPixelColor(pixelIndex, strip.Color(100, 100, 0));
        }
      }
    }
    
    strip.show();
    delay(150);
  }
  
  // FASE 2: Explosión compacta
  int explodeX = launchX;
  int explodeY = 1;
  
  for (int radius = 0; radius <= 2; radius++) {
    strip.clear();
    
    for (int dx = -radius; dx <= radius; dx++) {
      for (int dy = -radius; dy <= radius; dy++) {
        if (abs(dx) + abs(dy) <= radius) {
          int explodePixelX = explodeX + dx;
          int explodePixelY = explodeY + dy;
          
          int pixelIndex = getPixelIndex(explodePixelX, explodePixelY);
          if (pixelIndex >= 0) {
            if (radius == 0) {
              strip.setPixelColor(pixelIndex, strip.Color(255, 255, 255)); // Centro blanco
            } else if (radius == 1) {
              strip.setPixelColor(pixelIndex, color); // Color principal
            } else {
              strip.setPixelColor(pixelIndex, strip.Color(255, 50, 0)); // Naranja
            }
          }
        }
      }
    }
    
    strip.show();
    delay(200);
  }
  
  // FASE 3: Partículas cayendo
  for (int fall = 0; fall < 3; fall++) {
    strip.clear();
    
    for (int particle = 0; particle < 3; particle++) {
      int particleX = explodeX + random(-1, 2);
      int particleY = explodeY + fall + random(0, 2);
      
      int pixelIndex = getPixelIndex(particleX, particleY);
      if (pixelIndex >= 0 && particleY < MATRIX_HEIGHT) {
        int intensity = 255 - (fall * 80);
        if (intensity > 0) {
          strip.setPixelColor(pixelIndex, strip.Color(intensity/3, intensity/6, 0));
        }
      }
    }
    
    strip.show();
    delay(120);
  }
}

// Fuegos artificiales múltiples simultáneos para 5x5
void fuegosSimultaneos(int numFuegos) {
  // Arrays para manejar múltiples fuegos
  int launchX[numFuegos];
  int currentY[numFuegos];
  uint32_t colors[numFuegos];
  bool exploded[numFuegos];
  int explodeRadius[numFuegos];
  int fallFrame[numFuegos];
  bool finished[numFuegos];
  
  // Inicializar cada fuego
  for (int i = 0; i < numFuegos; i++) {
    launchX[i] = random(1, MATRIX_WIDTH - 1);
    currentY[i] = MATRIX_HEIGHT - 1;
    exploded[i] = false;
    explodeRadius[i] = 0;
    fallFrame[i] = 0;
    finished[i] = false;
    
    // Colores aleatorios festivos
    int colorChoice = random(0, 5);
    switch(colorChoice) {
      case 0: colors[i] = strip.Color(255, 0, 0); break;    // Rojo
      case 1: colors[i] = strip.Color(0, 255, 0); break;    // Verde
      case 2: colors[i] = strip.Color(255, 200, 0); break;  // Dorado
      case 3: colors[i] = strip.Color(255, 255, 255); break; // Blanco
      case 4: colors[i] = strip.Color(255, 100, 0); break;  // Naranja
    }
  }
  
  // Animar todos los fuegos simultáneamente
  bool allFinished = false;
  while (!allFinished) {
    strip.clear();
    allFinished = true;
    
    for (int i = 0; i < numFuegos; i++) {
      if (!finished[i]) {
        allFinished = false;
        
        if (!exploded[i]) {
          // FASE 1: Trayectoria ascendente
          if (currentY[i] >= 1) {
            // Dibujar la trayectoria
            for (int trail = 0; trail < 2 && (currentY[i] + trail) < MATRIX_HEIGHT; trail++) {
              int pixelIndex = getPixelIndex(launchX[i], currentY[i] + trail);
              if (pixelIndex >= 0) {
                if (trail == 0) {
                  strip.setPixelColor(pixelIndex, colors[i]); // Punto principal
                } else {
                  strip.setPixelColor(pixelIndex, strip.Color(100, 100, 0));
                }
              }
            }
            currentY[i]--; // Mover hacia arriba
          } else {
            exploded[i] = true; // Comenzar explosión
          }
        } else {
          // FASE 2: Explosión
          if (explodeRadius[i] <= 2) {
            int explodeX = launchX[i];
            int explodeY = 1;
            
            // Dibujar la explosión
            for (int dx = -explodeRadius[i]; dx <= explodeRadius[i]; dx++) {
              for (int dy = -explodeRadius[i]; dy <= explodeRadius[i]; dy++) {
                if (abs(dx) + abs(dy) <= explodeRadius[i]) {
                  int explodePixelX = explodeX + dx;
                  int explodePixelY = explodeY + dy;
                  
                  int pixelIndex = getPixelIndex(explodePixelX, explodePixelY);
                  if (pixelIndex >= 0) {
                    if (explodeRadius[i] == 0) {
                      strip.setPixelColor(pixelIndex, strip.Color(255, 255, 255)); // Centro blanco
                    } else if (explodeRadius[i] == 1) {
                      strip.setPixelColor(pixelIndex, colors[i]); // Color principal
                    } else {
                      strip.setPixelColor(pixelIndex, strip.Color(255, 50, 0)); // Naranja
                    }
                  }
                }
              }
            }
            explodeRadius[i]++;
          } else {
            // FASE 3: Partículas cayendo
            if (fallFrame[i] < 3) {
              int explodeX = launchX[i];
              int explodeY = 1;
              
              for (int particle = 0; particle < 2; particle++) {
                int particleX = explodeX + random(-1, 2);
                int particleY = explodeY + fallFrame[i] + random(0, 2);
                
                int pixelIndex = getPixelIndex(particleX, particleY);
                if (pixelIndex >= 0 && particleY < MATRIX_HEIGHT) {
                  int intensity = 255 - (fallFrame[i] * 80);
                  if (intensity > 0) {
                    strip.setPixelColor(pixelIndex, strip.Color(intensity/3, intensity/6, 0));
                  }
                }
              }
              fallFrame[i]++;
            } else {
              finished[i] = true; // Este fuego ha terminado
            }
          }
        }
      }
    }
    
    strip.show();
    delay(150);
  }
}

// Espectáculo de fuegos artificiales para 5x5
void espectaculoFuegos() {
  // Espectáculo con 2 fuegos simultáneos
  fuegosSimultaneos(2);
  delay(300);
  
  // Segundo round con 1 fuego
  fuegosSimultaneos(1);
  delay(300);
  
  // Gran final con 2 fuegos
  fuegosSimultaneos(2);
}

void setup() {
  strip.begin();
  strip.setBrightness(64);
  strip.clear();
  strip.show();
  
  Serial.begin(9600);
  Serial.println("=== UNIT ELECTRONICS ===");

}

void loop() {
  // === FIESTAS PATRIAS OPTIMIZADO PARA MATRIZ 5x5 ===

  git branch 
  // 2. Efecto bandera mexicana horizontal estática
  banderaMexicana(30); // Bandera más corta
  delay(300);
  
  // 3. Scroll "UNIT" en blanco (texto corto)
  scrollText(reverseString("  UNIT"), strip.Color(255, 255, 255), 100);
  fuegoIndividual(strip.Color(255, 255, 255)); // Fuego blanco
  delay(300);
  
  // 4. Efecto bandera ondeando
  banderaOndeando(2);
  delay(300);
  
  // 5. Scroll fecha corta
  scrollText(reverseString("  2025"), strip.Color(0, 255, 0), 110);
  fuegoIndividual(strip.Color(0, 255, 0)); // Fuego verde
  delay(300);
  

  
  // 10. Gran final con bandera estática
  banderaMexicana(25);
  delay(300);
  
  // 11. ¡GRAN FINAL CON FUEGOS ARTIFICIALES!
  espectaculoFuegos();
  delay(500);
}
