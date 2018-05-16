/*
Arduino MQ4 gas sensor - Geekstips.com
 This example is for calculating R0 which is
 the resistance of the sensor at a known concentration 
 without the presence of other gases, or in fresh air
*/
void setup() {
  Serial.begin(9600); //Baud rate
}

void loop() {
  float sensor_volt; //Define variable for sensor voltage
  float RS_air; //Define variable for sensor resistance
  float R0; //Define variable for R0
  float sensorValue=0; //Define variable for analog readings
  for (int x = 0 ; x < 500 ; x++){
    sensorValue = sensorValue + analogRead(A0); //Add analog values of sensor 500 times
  }
  sensorValue = sensorValue / 500.0; //Take average of readings
  sensor_volt = sensorValue * (5.0 / 1023.0); //Convert average to voltage
 
  RS_air = ((5.0 * 10.0) / sensor_volt) - 10.0; //Calculate RS in fresh air
  R0 = RS_air / 4.4; //Calculate R0

  Serial.print("R0 = ");
  Serial.println(R0); //Display value of R0
  delay(1000);
}