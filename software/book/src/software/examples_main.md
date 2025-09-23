# Code Examples

This section contains practical examples to help you get started with the UNIT Jun R3 Development Board.

## Available Examples

### 🔤 [Demo Text](./examples/demo_text.md)
Basic text display and serial communication example.

### 🌈 [Demo Neo](./examples/demo_neo.md)  
NeoPixel LED strip control and effects.

### 📺 [Demo OLED](./examples/demo_oled.md)
OLED display graphics and text rendering.

## Example Structure

Each example includes:

- **Purpose**: What the example demonstrates
- **Hardware**: Required components and connections  
- **Code**: Complete, commented source code
- **Explanation**: How the code works
- **Variations**: Suggested modifications

## Getting Started with Examples

1. **Choose an example** from the list above
2. **Review hardware requirements** and make connections
3. **Copy the code** to your development environment  
4. **Upload and test** on your board
5. **Experiment** with modifications

## Example Template

```cpp
/*
 * Example Title
 * Description of what this example does
 * 
 * Hardware:
 * - List required components
 * - Pin connections
 * 
 * Author: UNIT Electronics MX
 * Date: 2025
 */

// Libraries (if needed)
#include <SomeLibrary.h>

// Pin definitions
#define LED_PIN 13

// Global variables
int counter = 0;

void setup() {
  // Initialization code
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // Main program logic
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}
```

*All examples are tested and ready to use with the UNIT Jun R3 Development Board.*
