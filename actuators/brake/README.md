# Brake Acutator
General documentation for development surrounding the brake actuator

## Requirements
Note: ** double asterisks mark soft requirements that can be changed. This allows us
to determine other requirements in order to move on with a design

General
- ** Under $150 for complete BOM

Mechanical
- Can exert 700N a distance of 50mm (resolution 2mm) to end of brake pedal
- Emergency mechanical release decouples actuator from pedal
- Can withstand human input of 2500N
- Does not restrict pedal's full range of motion

Electrical

Option 1: 700N, 0.3s actuation time, 50mm travel
- Estimated Power: ~120W
- ** Input Voltage: 12V
- ** Estimated Current: 10A

Option 2: 700N, 0.6s actuation time, 50mm travel
- Estimated Power: ~60W
- ** Input Voltage: 12V
- ** Estimated Current: 5A

Option 3: 350N, 0.3s actuation time, 50mm travel
- Estimated Power: ~42W
- ** Input Voltage: 12V
- ** Estimated Current: 3.5A

Option 3: 350N, 0.6s actuation time, 50mm travel
- Estimated Power: ~21W
- ** Input Voltage: 12V
- ** Estimated Current: 1.75A

## Subcomponents / TODO

- Microcontroller selection
    - STM32

- PCB design

    - Physical dimensions / layout
    - Power supply

- Motor selection

    - Type, specifications

- Pedal throw sensor

    - angle sensor at fulcrum of pedal lever + magnet

- User override detection

    - strain gauge / pressure sensor on pedal surface
    - emergency release state detection

- Firmware

    - CAN I/O specification
    - Motor control algorithm
    - Go home mode specification
    - Self-testing and error reporting
    - Safety

- Mechanical Design

    - Mechanical specifications
    - Gearing for motor / actuator unit
    - Sensor package mount on pedal surface
    - Actuator unit mount
    - Emergency physical release mechanism


## Models

### Clippy on the Brakey

- Contributors: amzoo
- Status: WIP
- Link: 

### Second model 

- Contributors: amzoo
- Status: WIP
- Link: 
