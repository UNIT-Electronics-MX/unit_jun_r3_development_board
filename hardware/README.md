# Hardware

<div align="center">
    <a href="./unit_sch_v_0_0_1_ue0081_Jun-R3.pdf"><img src="./resources/schematics_icon.jpg" width="500px"><br/>Schematics</a>
    <br/>
</div>

---

## Pinout

<div align="center">
    <a href="./resources/unit_pinout_v_0_0_1_ue0081_unit_jun_r3_en.jpg"><img src="./resources/unit_pinout_v_0_0_1_ue0081_unit_jun_r3_en.png" width="500px"><br/>Pinout</a>
    <br/><br/>

</div>


<div align="center">

### **Pinout Details**

| Pin Label | Function / Notes                |
| --------- | ------------------------------- |
| D0        | RX – Serial Receive             |
| D1        | TX – Serial Transmit            |
| D2        | Digital I/O – Interrupt capable |
| D3        | PWM – Pulse Width Modulation    |
| D4        | Digital I/O                     |
| D5        | PWM – Pulse Width Modulation    |
| D6        | PWM – Pulse Width Modulation    |
| D7        | Digital I/O                     |
| D8        | Digital I/O                     |
| D9        | PWM – Pulse Width Modulation    |
| D10       | SPI CS – Chip Select            |
| D11       | SPI MOSI – Master Out Slave In  |
| D12       | SPI MISO – Master In Slave Out  |
| D13       | SPI SCK – Serial Clock          |
| A0        | Analog Input – 10-bit ADC       |
| A1        | Analog Input – 10-bit ADC       |
| A2        | Analog Input – 10-bit ADC       |
| A3        | Analog Input – 10-bit ADC       |
| A4        | I2C SDA – Serial Data Line      |
| A5        | I2C SCL – Serial Clock Line     |
| VCC       | Power Supply – 5V/3.3V (design) |
| GND       | Ground – Common reference       |


</div>

## Board Dimensions
<div align="center">
    <a href="./resources/unit_dimension_v_0_0_1_ue0081_jun_r3.png"><img src="./resources/unit_dimension_v_0_0_1_ue0081_jun_r3.png" width="500px"><br/>Dimensions</a>
</div>

## Board Topology
<div align="center">
    <a href="./resources/unit_topology_v_0_0_1_ue0081_jun_r3.png"><img src="./resources/unit_topology_v_0_0_1_ue0081_jun_r3.png" width="500px"><br/>Topology</a>

| Ref.  | Description                                                                 |
|-------|-----------------------------------------------------------------------------|
| IC1   | ATMEGA 328P Microcontroller                                                 |
| IC2   | CH340 USB to Serial Controller                                              |
| U1    | MP1482 5V Step-Down Regulator                                               |
| U2    | AP2112K 3.3V Regulator                                                      |
| SW1   | Reset Push Button                                                           |
| L1    | Built-In LED                                                                |
| L2    | Tx LED                                                                      |
| L3    | Rx LED                                                                      |
| L4    | Power On LED                                                                |
| L5    | Neopixel Matrix                                                             |
| J1    | USB Type-C Connector                                                        |
| J2    | 5mm DC Barrel Power Jack                                                    |
| J3    | QWIIC Connector (JST 1mm)                                                   |
| JP1   | Header for GPIOs                                                            |
| JP2   | Header for GPIOs                                                            |
| JP3   | Header for Power Supply and System Functions                                |
| JP4   | Header for GPIOs (Analog)                                                   |
| JP5   | Header for GPIOs (SPI)                                                      |
</div>