bool start = true;
bool isRunning = false;
int counter = 0;
String command;
unsigned long timer;

void setup() {
  Serial.begin(115200); // Serial communication with the slave node
  Serial1.begin(38400); // Bluetooth communication

  delay(1000);
  Serial1.flush(); // vider le buffer
  // Wait for Bluetooth connection
  Serial.print("Wait connection");
  while (!Serial1.available()) {
    Serial.print(".");
    //Serial1.flush(); // vider le buffer
    Serial1.print("Ready?\n"); // Send "Ready" message to indicate Arduino is ready
    //Serial1.flush(); // vider le buffer 
    delay(1000); 
  }
  Serial.println("");
  delay(1000); 
  //Serial.println(Serial1.readString());
  Serial.println("connected");
  delay(5000);  
}

void loop() {

  if (Serial.available()) {
    timer = millis();
    command = Serial.readStringUntil('\n'); // Read command from the intermediate PC

    // Process the received command
    if (command.startsWith("F") && command.indexOf("G") > 0 && command.indexOf("V") > 0) {

      // Modifier les paramètres de fréquence, gain et tension de référence
      int freqIndex = command.indexOf("F") + 1;
      int gainIndex = command.indexOf("G") + 1;
      int vrefIndex = command.indexOf("V") + 1;
      
      // Extraire les nouvelles valeurs de fréquence, gain et tension de référence
      int freq = command.substring(freqIndex, gainIndex - 1).toInt();
      int gain = command.substring(gainIndex, vrefIndex - 1).toInt();
      float vref = command.substring(vrefIndex).toFloat();

      // Evoi les données au noeud dacquisition
      Serial1.print("F" + (String) freq + " G" + (String) gain + " V" + (String) vref + "\n" );

    } else if (command == "start") {
      // Send the start command to the slave node
      Serial1.print("start\n");
    } else if (command == "stop") {
      // Send the stop command to the slave node
      Serial1.print("stop\n");
    } else if (command == "pause") {
      // Send the pause command to the slave node
      Serial1.print("pause\n");
    } else if (command == "continue") {
      // Send the continue command to the first Arduino
      Serial1.print("continue\n");
     } 
     //else if (command == "") {
    //   // Send the continue command to the first Arduino
    //   delay(1);
    // }
    // else {
    //   // Send the continue command to the first Arduino
    //   Serial.print("Error serial rec: ");
     
    // }
  }

  if (Serial1.available()) {
    String recep_time = (String) (millis() - timer); // temps depuis la reception des commandes
    String data_rec = Serial1.readStringUntil('\n');
    if (data_rec == "yes") {
      // Start data acquisition
      counter++;
      if (counter >= 8){
        isRunning = true;
        counter = 0;
      }    
    }else if (command.startsWith("A") && command.indexOf("G") > 0 && command.indexOf("V") > 0) {
           Serial.println(data_rec);
    }else{ 
        //Serial.print("from slave");
        Serial.println(recep_time + ";" + data_rec);
    }
  }

  if (isRunning) {
    Serial1.print("ok from master\n");
    isRunning = false; 
    delay(200);  
  }

}
