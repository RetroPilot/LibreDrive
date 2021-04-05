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

Go Home Specification

1. The system should be able to detect and report user inputs

    1.1 User input torque (angle rate vs current motor voltage)

    1.2 Steering wheel angle

2. The system should be able to detect and report errors

    - 2.1 Motor failures
        - 2.1.1 jam
        - 2.1.2 disconnected
    - 2.2 Firmware check fail
    - 2.3 Bus failures
        - 2.3.1 CAN checksum
        - 2.3.2 CAN message timeout
        - 2.3.3 request exceeds limits
3. The system should not override user inputs
    - 3.1 The motor should supply a torque vector towards zero at the torque required to overcome static friction within the actuator
        - 3.1.1 this will emulate true freewheeling, allowing the vehicle's power steering system to center the wheel as normally installed
        - 3.1.2 this torque requirement can be found programmatically before installation. it should be directly proportional to a voltage value if we use SimpleFOC
        - 3.1.3 reasonable static friction should not be very high, but we can make a very low estimate here
    - 3.2 If the motor is consuming more energy than expected, the motor relays will disengage allowing the motor to freewheel
        - 3.2.1 in this fail state, reporting is still enabled and the status code is communicated to the user
        - 3.2.2 the expected energy map will be created for static friction of actuator +1Nm during the validation phase and burned into memory
    - 3.3 A  physical disconnect will be implemented to detach the motor from the driven assembly
        - 3.3.1 possibly solenoid clutches - if we use these we can add another check / error state for them

## Subcomponents / TODO

- Microcontroller selection

    - STM32F205

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
