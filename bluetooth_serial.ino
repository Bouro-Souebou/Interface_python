#include <SoftwareSerial.h>

SoftwareSerial bluetoothSerial(10, 11);  // RX, TX

bool isWriting = false;

void setup() {
  Serial.begin(9600);
  bluetoothSerial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readString();

    if (command == "start") {
      isWriting = true;
    } else if (command == "pause") {
      isWriting = false;
    } else if (command == "continue") {
      isWriting = true;
    }
  }

  if (bluetoothSerial.available()) {
    String data = bluetoothSerial.readString();

    if (isWriting) {
      // Écrire les données dans un fichier ou effectuer l'action souhaitée
      // ...
    }
  }
}
