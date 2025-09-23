# Pinout Reference

## Pin Configuration

```
              UNIT Jun R3 Development Board
                       
    D13 ○ ○ 3V3      D1  ○ ○ TX
    D12 ○ ○ REF      D0  ○ ○ RX  
    D11 ○ ○ A0       RST ○ ○ GND
    D10 ○ ○ A1       5V  ○ ○ D2
     D9 ○ ○ A2       A7  ○ ○ D3
     D8 ○ ○ A3       A6  ○ ○ D4
     D7 ○ ○ A4       D5  ○ ○ D5
     D6 ○ ○ A5       D6  ○ ○ D6
```

## Pin Descriptions

### Digital Pins (D0-D13)
- **D0-D1**: UART communication (RX/TX)
- **D2-D13**: General purpose digital I/O
- **D13**: Built-in LED pin
- **D3, D5, D6, D9-D11**: PWM capable pins

### Analog Pins (A0-A7) 
- **A0-A5**: Analog input pins (10-bit ADC)
- **A4-A5**: Also used for I2C (SDA/SCL)
- **A6-A7**: Analog input only

### Power Pins
- **3V3**: 3.3V regulated output
- **5V**: 5V from USB or external supply  
- **GND**: Ground reference
- **REF**: Analog reference voltage

### Special Pins
- **RST**: Reset pin (active low)
- **TX/RX**: Hardware UART pins

*Always check voltage levels before connecting external devices.*
