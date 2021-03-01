# Actuators
Development around automating driver input


## FAQ

### Why use stepper motors?

[@dzid_ Stepper Motor Selection](https://docs.google.com/spreadsheets/d/1i-fc_-HzTeXHEhWJxIY2qmCmWLXJygV-4YG03bAaAyE/edit#gid=0)

Pros
- Low speed high torque
- Standard NEMA frame mounting
- Wide range of geared/non-geared options
- Wide range of libraries/controllers to use

Cons
- Gearing needed to get higher speed requirements
- Stepping control isn't necessary as external encoders are used

### Why use BLDC (Brushless DC) motors?

Pros
- High speed low torque
- Smooth operation
- Many options from the hobby RC drone/airplane world
- Custom motors are available without breaking the bank

Cons
- Gearing needed to get higher torque requirements
- Back driving through larger gear ratios becomes more difficult