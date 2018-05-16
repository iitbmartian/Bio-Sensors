/********************************************************************/
// First we include the libraries
#include <OneWire.h> 
#include <DallasTemperature.h>
/********************************************************************/
// Data wire is plugged into pin 2 on the Arduino 
#define ONE_WIRE_BUS 2 
/********************************************************************/
// Setup a oneWire instance to communicate with any OneWire devices  
// (not just Maxim/Dallas temperature ICs) 
OneWire oneWire(ONE_WIRE_BUS); 
/********************************************************************/
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);
/********************************************************************/ 
//MQ-4 Params
int gas_sensor = A0; //Sensor pin
float m = -0.318; //Slope
float b = 1.133; //Y-Intercept
float R0 = 18.3; //Sensor Resistance in fresh air from previous code
void setup(void) 
{ 
 // start serial port 
 Serial.begin(9600); 
 //Serial.println("Dallas Temperature IC Control Library Demo"); 
 // Start up the library 
 pinMode(gas_sensor, INPUT); //Set gas sensor as input
 sensors.begin(); 
} 
void loop(void) 
{ 
  float sensor_val[2];
 // call sensors.requestTemperatures() to issue a global temperature 
 // request to all devices on the bus 
/********************************************************************/
 
 sensors.requestTemperatures(); // Send the command to get temperature readings 
 
/********************************************************************/
 
 //Serial.print("Temperature is: "); 
 //Serial.print(sensors.getTempCByIndex(0)); // Why "byIndex"?  
   // You can have more than one DS18B20 on the same bus.  
   // 0 refers to the first IC on the wire 
 sensor_val[0]=sensors.getTempCByIndex(0);
 float sensor_volt; //Define variable for sensor voltage
  float RS_gas; //Define variable for sensor resistance
  float ratio; //Define variable for ratio
  float sensorValue = analogRead(gas_sensor); //Read analog values of sensor
  sensor_volt = sensorValue * (5.0 / 1023.0); //Convert analog values to voltage
  
  RS_gas = ((5.0 * 10.0) / sensor_volt) - 10.0; //Get value of RS in a gas
  ratio = RS_gas / R0;   // Get ratio RS_gas/RS_air
  //Serial.println(ratio);
  double ppm_log = (log10(ratio) - b) / m; //Get ppm value in linear scale according to the the ratio value
  double ppm = pow(10, ppm_log); //Convert ppm value to log scale
  sensor_val[1]=ppm_log;
  Serial.print("[");
  Serial.print(sensor_val[0]);
  Serial.print(",");
  Serial.print(sensor_val[1]); 
  Serial.println("]");
   delay(1000); 
} 