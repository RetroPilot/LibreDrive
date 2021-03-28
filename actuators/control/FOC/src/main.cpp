#include <Arduino.h>
#include <SimpleFOC.h>

#define	TLE012_CS PA4

// MagneticSensorSPI(MagneticSensorSPIConfig_s config, int cs)
//  config  - SPI config
//  cs      - SPI chip select pin 
// magnetic sensor instance - SPI
MagneticSensorSPI sensor = MagneticSensorSPI(MA730_SPI, TLE012_CS);
// alternative constructor (chipselsect, bit_resolution, angle_read_register, )
// MagneticSensorSPI sensor = MagneticSensorSPI(10, 14, 0x3FFF);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  // monitoring port
  Serial.begin(115200);

  // initialise magnetic sensor hardware
  sensor.init();

  Serial.println("Sensor ready");
  _delay(1000);
}

void loop() {
  float angle = sensor.getAngle();
  float velo = sensor.getVelocity();
  // display the angle and the angular velocity to the terminal
  Serial.print(sensor.getAngle());
  Serial.print("\t");
  Serial.println(sensor.getVelocity());

  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);              // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);              // wait for a second

}
