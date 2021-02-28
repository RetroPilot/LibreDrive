<h1>DISCLAIMER<h1>
<h1>!!!!!USE AT YOUR OWN RISK!!!!!</h1>
<h2>**THIS HARDWARE AND SOFTWARE HAS NO SAFETY ENGINEERING DONE WHAT SO EVER. THIS MAY KILL YOU, THIS MAY KILL ME. FUCK, THAT'S HALF THE FUN!**</h2>
<h3>The creator of the hardware and software contained herein takes no responsibility for the actions taken by those using it.</h3>
<h4>MISUSE OF THIS HARDWARE AND SOFTWARE **WILL** CAUSE DEATH OR GREVIOUS BODILY HARM. PLAY FULL STUPID AT YOUR OWN RISK.</h4>

# Project Full Stupid

A fully open source steering wheel actuator for the Honda Fit. It's stupid, dangerous, and I fucking love it.

# What?

This is a physical steering actuator for a 2019 Honda Fit.

# Why?

Honda limits the amount of steering torque that the lane keep assist system can apply to the wheel. This limits the usefulness of third party LKAS systems such as OpenPilot.

While some models of Honda have [EPS firmware modifications](https://docs.google.com/spreadsheets/d/1WCDRSo2-_SB-W0uBIjPNsxdIqDE7Edwu80YUjy6XZQ8/edit#gid=599567437) to allow for more torque it is not an option for every model. Several of the Honda models, including the Fit, erase the EPS system when it is [put into boot mode](https://github.com/gregjhogan/renesas-bootmode).

# How?

A modified version of Open Pilot to read the `controlsState` [cereal](https://github.com/commaai/cereal) messages to be sent to a RPi that is controlling an ODrive.

```
import cereal.messaging as messaging
 sm = messaging.SubMaster(['controlsState'])
 while 1:
    sm.update()
    print(sm['controlsState'].enabled) #Enabled
    print(sm['controlsState'].angleSteers) #Current wheel angle
    print(sm['controlsState'].angleSteersDes) #Desired angle
```

The Brains will take this data and feed it to its own odrive control loop.

The wheel actuator consists of 4 main parts:

1. Wheel Ring
    - Composed of Wheel Quadrants
    - A variety of sizes
2. Wheel Clamps
    - Carriers
    - Carrier Screws
    - Heads
    - Head Adjustment Screw
3. Power Unit
    - BLDC Motor
    - ODrive w/encoder
    - Sits **Somewhere** (TBD)
    - Adjustable feet for leveling and tension
4. Brain
    - RPi for prototypes
    - Possibly running on Comma2+ hardware using CAN to odrive in the future
# Files

### CAD Source
The CAD files for the interceptor ring are in the `CAD` folder. 

### To Slice for 3d Prints

In the `3d-prints` folder there is a `160mm-rad` folder which contains the **Wheel Ring** and a `power-unit` folder which contains the **Power Unit**.

# Current Status?

### Wheel Ring

This is just a draft and does not have a groove or teeth for any kind of actual interception.

### Wheel Clamps

These are practically final and fit with very little gap.

### Power Unit/OpenTorque-6368 Actuator

This is currently being printed and test fit. The drive unit is based off of the OpenTorque actuator modified for a 6368 BLDC motor.
