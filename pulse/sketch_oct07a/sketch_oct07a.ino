//arduino setup
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

//loop through and send temperature data via serial
void loop() {
  //read from grove port a
  int a = analogRead(0);

  //voltage to fahrenheight 
  const int B = 4275;               // B value of the thermistor
  const int R0 = 100000;            // R0 = 100k
  float R = 1023.0/a-1.0;
  R = R0*R;
  float temperature = 1.8 * (1.0/(log(R/R0)/B+1/298.15)-273.15) + 32; // convert to temperature via datasheet
  
  //send every 1/5 second
  Serial.println(temperature);
  delay(250);
}
