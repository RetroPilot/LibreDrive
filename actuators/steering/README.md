# Steering Acutator
General documentation for development surrounding the steering actuator

## Requirements
Note: ** double asterisks mark soft requirements that can be changed. This allows us
to determine other requirements in order to move on with a design

General
- ** Under $150 for complete BOM
  
Mechanical
- Peak Torque: ~5 Nm (needs verification)
- Peak Rate: 400 deg/s
- ** 300mm OD Driven Ring
- ** 18mm OD Drive Gear

Electrical
- ** Estimated Power: ~25W
- ** Input Voltage: 12V
- ** Estimated Current: 2.9A

Human Centric
- Does not interfere with drivers hands
- Able to be over-powered and software shutdown after sustained input force

## Subcomponents / TODO

- Microcontroller selection
    - Teensy or STM32?

- PCB design

    - Physical dimensions / layout
    - Power supply

- Motor selection

    - Type, specifications

- Angle sensor / position feedback
    - Theory of operation

- User override detection
    - Theory of operation

- Firmware

    - CAN I/O specification
    - Motor control algorithm
    - Go home mode specification
    - Self-testing and error reporting
    - Safety

- Mechanical Design

    - Mechanical specifications
    - Gearing for motor / actuation
    - Gearing for angle sensor
    - Column mount
    - Wheel mount system

## Models

### Full Stupid

![Full Stupid Honda](https://media.discordapp.net/attachments/697072551792345099/814937633885126697/honda-entirety.jpg?width=1625&height=1219)

- Contributors: smurf
- Status: WIP
- [Link to Files](https://github.com/RetroPilot/full-stupid/tree/master)

### retropilot-drivetronik

- Contributors: wocsor
- Status: WIP, tested actuaton on 2003 Toyota Celica
    - [Video](https://youtu.be/OpUxE-Uwttc)
- [Link to Files](https://github.com/wocsor/retropilot-drivetronik)

### Second model 

- Contributors: amzoo
- Status: WIP
- Link: 
