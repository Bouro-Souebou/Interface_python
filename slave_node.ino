#include <Adafruit_NAU7802.h>
#include <Arduino.h>
#include <Wire.h>

Adafruit_NAU7802 nau;

template< typename T, size_t N > size_t ArraySize (T (&) [N]){ return N; } // to get string length

bool isRunning = false; // Flag to indicate if the data acquisition is running

bool isStarted = true;
bool isSendingData = false;
int freq = 320;  // Fréquence initiale en Hz
int gain = 32;  // Gain initial
float vref = 0.122;  // Tension de référence initiale
float LDO = 2.4 ;
unsigned long timer;

void setup() {
  Serial.begin(115200); // Serial communication with the intermediate PC
  
  //   while (! nau.begin()) {
  //     delay(2000);
  //     if (! nau.begin()) {
  //       Serial.println("Failed to find NAU7802");
  //     }
  //   }

  //   //ADC configuration
  //   ADCconfig(LDO, gain, freq);
    
  // // Take 10 readings to flush out readings
  //   for (uint8_t i=0; i<10; i++) {
  //     while (! nau.available()) delay(1);
  //     nau.read();
  //   } 
  //   // ADC calibration
  //   setCalibration(true, false, false); // INTERNAL, GAIN, OFFSET

  Serial1.begin(38400); // Bluetooth communication
  delay(1000);
  Serial1.flush(); // vider le buffer
  // Wait for Bluetooth connection
  Serial.print("waitting connection");
  while (!Serial1.available()) {
    Serial.print(".");
    //Serial1.flush(); // vider le buffer
    Serial1.print("yes\n"); // Send "Ready" message to indicate Arduino is ready
    delay(1000);
  }
  Serial.println("");
  delay(1000);
  //Serial1.flush(); // vider le buffer
  Serial.println("connected");
  delay(500);

  timer = millis();
}

void loop() {

  if (Serial1.available()) {
    String command = Serial1.readStringUntil('\n'); // Read command from the first Arduino
     
    // Process the received command
    if (command.startsWith("F") && command.indexOf("G") > 0 && command.indexOf("V") > 0) {

      // Modifier les paramètres de fréquence, gain et tension de référence
      int freqIndex = command.indexOf("F") + 1;
      int gainIndex = command.indexOf("G") + 1;
      int vrefIndex = command.indexOf("V") + 1;
      
      // Extraire les nouvelles valeurs de fréquence, gain et tension de référence
      freq = command.substring(freqIndex, gainIndex - 1).toInt();
      gain = command.substring(gainIndex, vrefIndex - 1).toInt();
      vref = command.substring(vrefIndex).toFloat();
      
      // Mettre à jour la configuration de l'ADC
      //ADCconfig(LDO, gain, freq);

      // Envoyer un accusé de réception au code Python
      Serial1.print("ACK " + command );
      Serial.println("ACK " + command );
      

    } else if (command == "start") {
      // Start data acquisition
      isRunning = true;
      //Serial.println("start command");
    } else if (command == "stop") {
      // Stop data acquisition
      isRunning = false;
    } else if (command == "pause") {
      // Pause data acquisition
      isRunning = false;
      //Serial1.write("command start received from master node \n");
    } else if (command == "continue") {
      // Continue data acquisition
       isRunning = true;
    } else if (command == "Ready?") {
      // Continue data acquisition
      Serial1.print("yes\n");
      isRunning = false;
      //Serial1.flush(); // vider le buffer
      delay(200);
    }else if (command == "ok from master") {
      // Continue data acquisition
      Serial1.print("connected from slave\n");
      isRunning = false;
      //Serial1.flush(); // vider le buffer
      delay(200);
    } else {
      // Continue data acquisition
      Serial.print("Error received ");
      //Serial1.print("Error");
      //isRunning = true;
    }
    //Serial.println(command);
    delay(200);
  }

  if (isRunning) {
    readADC(freq);  // Read ADC value
    delay(100); 
  }
  
}

int ADCconfig(int LDO, int gain, int rate) {
  
  switch (LDO) {
    case 45:   nau.setLDO(NAU7802_4V5); break; //Serial.println("4.5V");
    case 42:   nau.setLDO(NAU7802_4V2); break; // Serial.println("4.2V");
    case 39:   nau.setLDO(NAU7802_3V9); break; // Serial.println("3.9V");
    case 36:   nau.setLDO(NAU7802_3V6); break; // Serial.println("3.6V");
    case 33:   nau.setLDO(NAU7802_3V3); break; // Serial.println("3.3V");
    case 30:   nau.setLDO(NAU7802_3V0); break; // Serial.println("3.0V");
    case 27:   nau.setLDO(NAU7802_2V7); break; // Serial.println("2.7V");
    case 24:   nau.setLDO(NAU7802_2V4); break; // Serial.println("2.4V");
    //case NAU7802_EXTERNAL:  Serial.println("External"); ;break; //  5.06 mV
  }
 
  switch (gain) {
    case 1:   nau.setGain(NAU7802_GAIN_1); break; // Serial.println("1x");
    case 2:   nau.setGain(NAU7802_GAIN_2); break; // Serial.println("2x");
    case 4:   nau.setGain(NAU7802_GAIN_4); break; // Serial.println("4x");
    case 8:   nau.setGain(NAU7802_GAIN_8); break; // Serial.println("8x");
    case 16:   nau.setGain(NAU7802_GAIN_16); break; // Serial.println("16x");
    case 32:   nau.setGain(NAU7802_GAIN_32); break; // Serial.println("32x");
    case 64:   nau.setGain(NAU7802_GAIN_64); break; // Serial.println("64x");
    case 128:  nau.setGain(NAU7802_GAIN_128); break; // Serial.println("128x");
  }

  switch (rate) {
    case 10:    nau.setRate(NAU7802_RATE_10SPS); break; // Serial.println("10 SPS");
    case 20:    nau.setRate(NAU7802_RATE_20SPS); break; // Serial.println("20 SPS");
    case 40:    nau.setRate(NAU7802_RATE_40SPS); break; // Serial.println("40 SPS");
    case 80:    nau.setRate(NAU7802_RATE_80SPS); break; // Serial.println("80 SPS");
    case 320:   nau.setRate(NAU7802_RATE_320SPS); break; // Serial.println("320 SPS");
  }

}

void setCalibration(bool internal, bool gain, bool offset) {
  //  The calibration mode to perform: NAU7802_CALMOD_INTERNAL, NAU7802_CALMOD_OFFSET or NAU7802_CALMOD_GAIN
  if (internal){
    
    while (! nau.calibrate(NAU7802_CALMOD_INTERNAL)) {
      delay(1000);
      if (! nau.calibrate(NAU7802_CALMOD_INTERNAL)){
          Serial.println("Failed to calibrate internal offset, retrying!");
      }
    }  
  }
  if (gain){
    while (! nau.calibrate(NAU7802_CALMOD_GAIN)) {
      delay(1000);
      if (! nau.calibrate(NAU7802_CALMOD_INTERNAL)){
          Serial.println("Failed to calibrate internal offset, retrying!");
      }
    }
  }
  if (offset){
    while (! nau.calibrate(NAU7802_CALMOD_OFFSET)) {
      delay(1000);
      if (! nau.calibrate(NAU7802_CALMOD_INTERNAL)){
          Serial.println("Failed to calibrate internal offset, retrying!");
      }
    } 
  }
}

long readADC(int freq) {
   for (int i= 0; i < freq; i++){ 
      while (! nau.begin() && i < freq) { // while (! nau.available()) {
          String data = (String) i + ";" + (String) millis() + ";"  + (String) (random(2000, 8600300))  + "\n"; // remplacer random par "nau.read()"
          Serial.println(data); 
          Serial1.print(data);
          i++;
        } 
    // delay(1000);   
   }  
}

long readADC_tab(long read_time[], long ADC_val[], int freq) {
   for (int i= 0; i < freq; i++){
      while (! nau.available()) delay(1);
      read_time[i] = millis();
      ADC_val[i] = nau.read();
   }
   
}

void convertirTemps(unsigned long timer, char* resultat) {
  unsigned long ms = timer % 1000;
  unsigned long s = (timer /= 1000) % 60;
  unsigned long m = (timer /= 60) % 60;
  unsigned long h = (timer /= 60) % 24;

  sprintf(resultat, "%02lu:%02lu:%02lu:%03lu", h, m, s, ms);
}
