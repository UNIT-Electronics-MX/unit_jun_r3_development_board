# Getting Started

## Prerequisites

Before you begin, make sure you have:

- UNIT Jun R3 Development Board
- USB-C cable
- Computer with Windows, macOS, or Linux
- Arduino IDE or PlatformIO installed

## Quick Setup

### 1. Install Development Environment

**Option A: Arduino IDE**
1. Download and install [Arduino IDE](https://www.arduino.cc/en/software)
2. Install required board definitions
3. Add UNIT Electronics board package URL

**Option B: PlatformIO**
1. Install [VS Code](https://code.visualstudio.com/)
2. Install PlatformIO extension
3. Configure for UNIT Jun R3 board

### 2. Connect Your Board

1. Connect the USB-C cable to your development board
2. Connect the other end to your computer
3. The power LED should illuminate
4. Your system should recognize the device

### 3. Test Connection

1. Open your development environment
2. Select the correct board and port
3. Upload a simple blink example
4. Verify the onboard LED blinks

## First Program

Let's start with the classic "Hello World" of embedded systems:

```cpp
// Blink LED example
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW); 
  delay(1000);
}
```

## Next Steps

Once you have the basic setup working:

1. 📚 Explore the [Examples](../software/examples.md) section
2. 🔧 Learn about [Development](../development/setup.md) tools
3. 📋 Review [Hardware](../hardware/overview.md) details
4. 🆘 Check [Troubleshooting](../development/troubleshooting.md) if needed

*Need help? Check our support resources in the sidebar.*
