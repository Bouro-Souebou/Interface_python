#include <SoftwareSerial.h>

SoftwareSerial bluetoothSerial(10, 11);  // RX, TX

void setup() {
  Serial.begin(9600);
  bluetoothSerial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readString();
    
    // Envoyer la commande à l'autre carte via Bluetooth
    bluetoothSerial.println(command);
    
    // Exécuter les actions en fonction de la commande reçue
    if (command == "start") {
      // Action pour la commande "start"
    } else if (command == "pause") {
      // Action pour la commande "pause"
    } else if (command == "continue") {
      // Action pour la commande "continue"
    }
  }
  
  if (bluetoothSerial.available()) {
    String data = bluetoothSerial.readString();
    
    // Traiter les données reçues depuis l'autre carte via Bluetooth
    // ...
    
    // Envoyer les données au port série (vers l'interface utilisateur Python)
    Serial.println(data);
  }
}
