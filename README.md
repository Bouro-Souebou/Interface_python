# Interface_python
Ce code est une application Python qui utilise la bibliothèque Tkinter pour créer une interface utilisateur graphique (GUI). L'application est conçue pour lire des données à partir d'un port série et les afficher dans une zone de texte et sur des graphiques en temps réel.

Voici une explication des différentes parties du code :
1. Les importations : Le code commence par importer les bibliothèques nécessaires, telles que:
- `serial` : Permet la communication avec le port série.
- `time` pour la gestion du temps.
- `tkinter` : Fournit les fonctionnalités pour créer une interface utilisateur.
- `ttk` : Offre des widgets améliorés pour Tkinter.
- `matplotlib` pour la création des graphiques.
- `csv` pour la sauvegarde des données en format CSV.
  
2. Définition des variables : Les variables telles que le port série, le débit binaire, la pleine échelle, l'accélération gravitationnelle, la tension de référence, dA et dB sont définies avec leurs valeurs respectives.
```python
port = '/dev/ttyACM0'  # Remplacez par votre port série
baud_rate = 9600 # Vous devez spécifier le port série sur lequel votre Arduino est connecté et le débit binaire correspondant.
```
3. Initialisation de la connexion série : La connexion série est établie en utilisant la bibliothèque `serial` et les valeurs du port et du débit binaire définis précédemment.

4. Création des graphiques : Une figure et trois axes de graphiques sont créés en utilisant `matplotlib`.

5. Définition des lignes des graphiques : Des lignes vides sont créées pour les graphiques à l'aide des axes précédemment définis.

6. Ajout des étiquettes d'axe : Des étiquettes d'axe sont définies pour les graphiques en utilisant les axes correspondants.

7. Définition des listes pour stocker les données des graphiques : Des listes vides sont créées pour stocker les valeurs de temps, de tension, de force sur la palette et de réaction sur la lame de la palette.

8. Fonction pour mettre à jour les graphiques : Cette fonction est utilisée pour ajouter de nouvelles valeurs aux listes de données des graphiques, mettre à jour les lignes des graphiques avec les nouvelles données et redessiner les graphiques.

9. Fonction pour lire les données du port série : Cette fonction est appelée périodiquement pour lire les données du port série. Si des données sont disponibles, elles sont traitées et affichées dans l'interface utilisateur. Si les données correspondent à des valeurs de temps et d'ADC, la fonction `compute` est appelée pour effectuer des calculs et mettre à jour les graphiques.

10. Fonction pour effectuer des calculs : Cette fonction prend le temps et la valeur ADC en tant que paramètres, effectue des calculs sur ces valeurs pour obtenir la tension, la force sur la palette et la réaction sur la lame de la palette, puis appelle la fonction `update_graphs` pour mettre à jour les graphiques.

11. Fonction pour sauvegarder les données en CSV : Cette fonction est utilisée pour demander à l'utilisateur de spécifier un nom de fichier et enregistrer les données actuelles des graphiques dans un fichier CSV.

12. Fonctions pour activer/désactiver les boutons : Ces fonctions sont utilisées pour activer ou désactiver les boutons en fonction des valeurs sélectionnées dans l'interface utilisateur.

13. Fonction pour envoyer les valeurs : Cette fonction est appelée lorsque le bouton "Envoyer les valeurs" est cliqué. Elle récupère les valeurs sélectionnées dans l'interface utilisateur et les envoie au périphérique connecté via le port série.

14. Fonction pour convertir les millisecondes en format de temps : Cette fonction est utilisée pour convertir les millisecondes en heures, minutes, secondes et millisecondes, puis formater le temps sous forme d'une chaîne de caractères.

15. Fonction pour vérifier si une chaîne de caractères peut être convertie en nombre flottant : Cette fonction est utilisée pour vérifier si une chaîne de caractères peut être convertie en nombre flottant. Elle renvoie `True` si la conversion est possible, sinon elle renvoie `False`.

16. Création de l'interface utilisateur : Une fenêtre principale est créée en utilisant `tkinter`. Elle contient une zone de texte pour afficher les données, des champs de saisie et des boutons pour sélectionner et envoyer des valeurs, des graphiques pour afficher les données en temps réel, des boutons pour contrôler la réception de données, un bouton pour sauvegarder les données en CSV.

17. Lancement de la lecture du port série et de la boucle principale de l'interface utilisateur : La fonction `read_serial` est appelée pour commencer la lecture des données du port série, puis la boucle principale de l'interface utilisateur (`root.mainloop()`) est démarrée pour afficher l'interface et attendre les interactions de l'utilisateur.

Pour installer les dépendances nécessaires et créer un environnement virtuel Python, vous pouvez suivre les étapes suivantes :

1. Assurez-vous que Python est installé sur votre système.

2. Ouvrez un terminal ou une invite de commande.

3. Créez un nouvel environnement virtuel en utilisant la commande suivante :
   ```
   python -m venv mon_environnement
   ```
   Remplacez "mon_environnement" par le nom que vous souhaitez donner à votre environnement.

4. Activez l'environnement virtuel en utilisant la commande appropriée selon votre système d'exploitation :
   - Sur Windows :
     ```
     mon_environnement\Scripts\activate
     ```
   - Sur macOS et Linux :
     ```
     source mon_environnement/bin/activate
     ```

5. Installez les dépendances nécessaires en utilisant la commande suivante :
   ```
   pip install pyserial matplotlib
   ```
   Cela installera les bibliothèques `pyserial` et `matplotlib` requises par le code.

# serial_bluetooth.ino

Dans ce code Arduino, nous utilisons la bibliothèque SoftwareSerial pour établir une communication série avec le module Bluetooth. Assurez-vous de connecter correctement les broches RX et TX du module Bluetooth à des broches numériques appropriées de votre Arduino et de spécifier les broches correctes dans le code (SoftwareSerial bluetoothSerial(10, 11)).

Le code lit les données du port série (Serial) provenant de l'interface utilisateur Python. Il envoie ensuite ces données à l'autre carte via Bluetooth en utilisant bluetoothSerial.println(command).

Ensuite, le code Arduino reçoit les données de l'autre carte via Bluetooth en utilisant bluetoothSerial.available() et bluetoothSerial.readString(). Ces données peuvent être traitées selon vos besoins.

Finalement, le code envoie les données reçues de l'autre carte au port série (Serial.println(data)) pour les renvoyer à l'interface utilisateur Python.
Assurez-vous de configurer correctement le module Bluetooth sur l'autre carte (vérifier le nom du module, le débit binaire, etc.) et d'adapter le code Arduino en conséquence.
