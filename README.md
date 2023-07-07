# Interface_python
Bien sûr ! Voici une explication du code fourni :

1. Importation des bibliothèques nécessaires :
```python
import serial
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import csv
```
Les bibliothèques importées sont les suivantes :
- `serial` : Permet la communication avec le port série.
- `tkinter` : Fournit les fonctionnalités pour créer une interface utilisateur.
- `ttk` : Offre des widgets améliorés pour Tkinter.
- `matplotlib.pyplot` : Utilisée pour afficher les graphiques.
- `csv` : Permet de travailler avec les fichiers CSV.

2. Définition des variables pour le port série :
```python
port = '/dev/ttyACM0'  # Remplacez par votre port série
baud_rate = 9600
```
Vous devez spécifier le port série sur lequel votre Arduino est connecté et le débit binaire correspondant.

3. Initialisation de la connexion série :
```python
ser = serial.Serial(port, baud_rate)
```
Cette ligne crée un objet `Serial` en utilisant le port série et le débit binaire spécifiés.

4. Définition de la fonction pour envoyer une commande par port série :
```python
def send_command(command):
    ser.write(command.encode())
```
Cette fonction prend une commande en tant que paramètre, encode la commande en bytes et l'envoie via le port série.

5. Définition de la fonction pour lire les données du port série et afficher le texte :
```python
def read_serial():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        text_box.insert(tk.END, data + '\n')
    root.after(100, read_serial)
```
Cette fonction est appelée de manière récurrente pour lire les données disponibles sur le port série. Si des données sont disponibles, elles sont lues à l'aide de `ser.readline()`, décodées en utilisant UTF-8 et affichées dans la zone de texte de l'interface utilisateur.

6. Définition de la fonction pour sauvegarder les données en CSV :
```python
def save_data_to_csv(data):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
```
Cette fonction prend des données en tant que paramètre et les ajoute en tant que ligne dans un fichier CSV nommé "data.csv".

7. Définition des fonctions pour afficher les graphiques :
```python
def plot_graph1():
    # Code pour afficher le premier graphique
    pass

def plot_graph2():
    # Code pour afficher le deuxième graphique
    pass

def plot_graph3():
    # Code pour afficher le troisième graphique
    pass
```
Ces fonctions sont appelées lorsque les boutons correspondants sont cliqués. Vous pouvez remplacer les commentaires par votre propre code pour afficher les graphiques souhaités.

8. Création de l'interface utilisateur :
```python
root = tk.Tk()
root.title('Interface utilisateur')

text_box = tk.Text(root)
text_box.pack()

# ... Autres widgets (boutons, menus déroulants) ...

root.mainloop()
```
Cette partie du code crée une fenêtre principale pour l'interface utilisateur en utilisant Tkinter et définit son titre. La zone de texte est créée pour afficher les données reçues.

9. Démarrage de la boucle principale de l'interface utilisateur et appel de la fonction de lecture du port série :
```python
read_serial()
root.mainloop()
```
La fonction `read_serial()` est appelée de manière récurrente pour lire les données du port série et mettre à jour l'interface utilisateur. La boucle principale de l'interface utilisateur (`root.mainloop()`) est lancée pour afficher la fenêtre et répondre aux interactions de l'utilisateur.

N'oubliez pas d'adapter le port série (`port`) à votre configuration et de remplir les fonctions vides pour afficher les graphiques et gérer la sauvegarde en CSV en fonction de vos besoins spécifiques.

# serial_bluetooth.ino

Dans ce code Arduino, nous utilisons la bibliothèque SoftwareSerial pour établir une communication série avec le module Bluetooth. Assurez-vous de connecter correctement les broches RX et TX du module Bluetooth à des broches numériques appropriées de votre Arduino et de spécifier les broches correctes dans le code (SoftwareSerial bluetoothSerial(10, 11)).

Le code lit les données du port série (Serial) provenant de l'interface utilisateur Python. Il envoie ensuite ces données à l'autre carte via Bluetooth en utilisant bluetoothSerial.println(command).

Ensuite, le code Arduino reçoit les données de l'autre carte via Bluetooth en utilisant bluetoothSerial.available() et bluetoothSerial.readString(). Ces données peuvent être traitées selon vos besoins.

Finalement, le code envoie les données reçues de l'autre carte au port série (Serial.println(data)) pour les renvoyer à l'interface utilisateur Python.
Assurez-vous de configurer correctement le module Bluetooth sur l'autre carte (vérifier le nom du module, le débit binaire, etc.) et d'adapter le code Arduino en conséquence.
