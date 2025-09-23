# Demo Text Example

This example demonstrates basic serial communication and text display functionality.

## Purpose
- Send text messages via serial communication
- Display text on connected displays
- Learn basic string manipulation

## Hardware Required
- UNIT Jun R3 Development Board
- USB-C cable for serial communication
- Optional: External display module

## Code

```cpp
/*
 * Demo Text - Serial Communication Example
 * Demonstrates text output and basic string operations
 */

String messages[] = {
  "Hello from UNIT Jun R3!",
  "Text display example",
  "Serial communication active",
  "Ready for development"
};

int currentMessage = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("=== UNIT Jun R3 Demo Text ===");
  Serial.println("Starting serial communication...");
  delay(2000);
}

void loop() {
  // Display current message
  Serial.print("Message ");
  Serial.print(currentMessage + 1);
  Serial.print(": ");
  Serial.println(messages[currentMessage]);
  
  // Move to next message
  currentMessage = (currentMessage + 1) % 4;
  
  delay(3000);
}
```

## How it Works

1. **Setup**: Initializes serial communication at 9600 baud
2. **Message Array**: Stores multiple text messages
3. **Loop**: Cycles through messages every 3 seconds
4. **Serial Output**: Displays formatted text to serial monitor

## Try This

- Modify messages in the array
- Change display timing
- Add user input handling
- Connect external display module
