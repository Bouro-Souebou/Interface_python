# Fonctionnement ensemble :
Trois codes : le code Python exécuté sur un PC, le code "Master Node" exécuté sur un Arduino et le code "Slave Node" exécuté sur un autre Arduino. Ces trois codes fonctionnent ensemble pour établir une communication bidirectionnelle entre le PC et les Arduinos via Bluetooth. Voici une explication détaillée de leur fonctionnement ensemble :

1. Code Python (Exécuté sur un PC) :
   - Le code Python est responsable de l'établissement de la communication Bluetooth avec les Arduinos et de l'envoi/reception des commandes et des données.
   - Il utilise une bibliothèque Python telle que `pyserial` pour communiquer avec le port série Bluetooth du PC.
   - La communication entre le PC et les Arduinos est réalisée via des commandes et des réponses sous forme de chaînes de caractères.
   - Le code Python peut envoyer des commandes de contrôle (par exemple, "start", "stop", "pause", "continue") au "Master Node" pour démarrer, arrêter ou mettre en pause l'acquisition de données.
   - Le code Python peut également envoyer des commandes de configuration (par exemple, "F200 G32 V0.5") pour modifier les paramètres du "Master Node" tels que la fréquence, le gain et la tension de référence.
   - Le "Slave Node" envoie des données acquises au "Master Node" sous forme de chaînes de caractères (par exemple, "0;12345;67890\n" où "0" est l'index de l'échantillon, "12345" est le temps de l'échantillon, et "67890" est la valeur de l'échantillon).

2. Code "Master Node" (Exécuté sur un Arduino) :
   - Le "Master Node" est le code exécuté sur un Arduino qui agit comme le nœud principal de l'ensemble du système.
   - Il est responsable de la communication Bluetooth avec le PC et la communication série avec le "Slave Node".
   - Le "Master Node" utilise la communication série (`Serial`) pour envoyer des commandes au "Slave Node" et recevoir des données acquises de celui-ci.
   - Il utilise la communication Bluetooth (`Serial1`) pour recevoir des commandes du PC et envoyer les réponses correspondantes.
   - Le "Master Node" analyse les commandes reçues du PC et effectue les actions appropriées :
     - Si une commande de configuration (par exemple, "F200 G32 V0.5") est reçue, le "Master Node" extrait les nouvelles valeurs de fréquence, gain et tension de référence, puis les envoie au "Slave Node" via la communication série.
     - Si une commande de contrôle (par exemple, "start", "stop", "pause", "continue") est reçue, le "Master Node" effectue l'action correspondante en démarrant, arrêtant ou mettant en pause l'acquisition de données.
   - Le "Master Node" reçoit les données acquises du "Slave Node" via la communication série et les envoie au PC via la communication Bluetooth.

3. Code "Slave Node" (Exécuté sur un autre Arduino) :
   - Le "Slave Node" est le code exécuté sur un autre Arduino qui agit comme un nœud esclave du système.
   - Il est responsable de la communication série avec le "Master Node" et l'acquisition de données à partir du convertisseur analogique-numérique (CAN) NAU7802.
   - Le "Slave Node" utilise la communication série (`Serial`) pour recevoir des commandes du "Master Node" et envoyer des données acquises à celui-ci.
   - Il utilise également le CAN NAU7802 pour effectuer l'acquisition de données à une fréquence spécifiée.
   - Le "Slave Node" lit les commandes reçues du "Master Node" et effectue les actions correspondantes :
     - Si une commande de configuration (par exemple, "F200 G32 V0.5") est reçue, le "Slave Node" extrait les nouvelles valeurs de fréquence, gain et tension de référence, puis met à jour la configuration du CAN NAU7802.
     - Si une commande de contrôle (par exemple, "start", "stop", "pause", "continue") est reçue, le "Slave Node" démarre, arrête ou met en pause l'acquisition de données en fonction de la commande.
   - Le "Slave Node" effectue l'acquisition de données à la fréquence spécifiée à l'aide du CAN NAU7802, puis envoie les données acquises au "Master Node" via la communication série.

En résumé, le code Python sert d'interface utilisateur et envoie des commandes de contrôle et de configuration au "Master Node". Le "Master Node" agit comme l'intermédiaire entre le PC et le "Slave Node", en recevant les commandes du PC et en les transmettant au "Slave Node" pour effectuer les actions correspondantes. Le "Slave Node" effectue l'acquisition de données à partir du CAN NAU7802 et envoie les données acquises au "Master Node", qui les renvoie ensuite au PC via Bluetooth. Ainsi, les trois codes fonctionnent ensemble pour établir une communication bidirectionnelle et effectuer l'acquisition de données à partir du "Slave Node" vers le PC.

## interface.py
Ce code est une application Python qui utilise la bibliothèque Tkinter pour créer une interface utilisateur graphique (GUI). L'application est conçue pour lire des données à partir d'un port série et les afficher dans une zone de texte et sur des graphiques. L'interface graphique affiche les données reçues en temps réel dans une zone de texte, et les graphiques se mettent à jour en fonction des nouvelles données reçues. Les boutons permettent de configurer certains paramètres et d'interagir avec l'appareil connecté via le port série.

Voici une explication détaillée du code :

1. Importation des bibliothèques :
   - La bibliothèque `serial` est utilisée pour la communication avec le port série.
   - La bibliothèque `time` est utilisée pour le suivi du temps.
   - La bibliothèque `tkinter` est utilisée pour la création de l'interface utilisateur.
   - `ttk` est une sous-bibliothèque de `tkinter` qui fournit des widgets avec un aspect amélioré.
   - `csv` est utilisé pour sauvegarder les données dans un fichier CSV.
   - `matplotlib.pyplot` est utilisé pour tracer les graphiques.
   - `FigureCanvasTkAgg` est utilisé pour afficher les graphiques dans l'interface utilisateur.

2. Définition des paramètres de communication :
   - `port` : spécifie le port série à utiliser pour la communication.
   - `baud_rate` : spécifie le débit binaire pour la communication série.

3. Initialisation de la connexion série :
   - La variable `ser` est créée en utilisant `serial.Serial(port, baud_rate)`. Elle est utilisée pour la communication avec le périphérique externe.

4. Création des graphiques :
   - La fonction `plt.subplots(3, 1, figsize=(8, 6))` crée une figure avec trois graphiques disposés en colonnes.
   - Les objets `ax1`, `ax2` et `ax3` représentent les axes des graphiques.
   - Les objets `line1`, `line2` et `line3` représentent les lignes des graphiques.
   - Les étiquettes d'axe sont définies pour chaque graphique.

5. Variables pour stocker les données des graphiques :
   - Les listes `x`, `y1`, `y2` et `y3` sont utilisées pour stocker les données des graphiques.

6. Fonction `update_graphs(time, voltage, paddle_force, blade_reaction)` :
   - Cette fonction est appelée pour mettre à jour les graphiques avec de nouvelles données.
   - Les nouvelles valeurs sont ajoutées aux listes existantes.
   - Les données des graphiques sont mises à jour en utilisant les nouvelles valeurs.
   - Les graphiques sont redessinés.

7. Fonction `read_serial()` :
   - Cette fonction est appelée périodiquement pour lire les données du port série.
   - Si des données sont disponibles dans le buffer d'entrée (`ser.in_waiting > 0`), elles sont lues et décryptées.
   - Selon le contenu des données, différentes actions sont effectuées :
     - Si les données contiennent une réponse ACK, un bouton "start" est activé et les données sont affichées dans l'interface utilisateur.
     - Si les données contiennent des valeurs de temps et de tension, elles sont affichées dans l'interface utilisateur et la fonction `compute()` est appelée pour effectuer des calculs.
     - Sinon, les données sont simplement affichées dans l'interface utilisateur.
   - La fonction se répète après un délai de 2 ms en utilisant `root.after(2, read_serial)`.

8. Fonction `compute(time, ADC_value)` :
   - Cette fonction est appelée pour effectuer des calculs à partir des données lues du port série.
   - Les valeurs de `dA` et `dB` sont récupérées à partir des zones de texte de l'interface utilisateur.
   - Différents calculs sont effectués pour obtenir la tension, le poids, la force sur l'arbre de la pale et la force de réaction sur la lame de la pale.
   - Les graphiques sont mis à jour en utilisant la fonction `update_graphs()`.

9. Fonction `save_to_csv()` :
   - Cette fonction est appelée lorsque l'utilisateur souhaite sauvegarder les données des graphiques dans un fichier CSV.
   - Une boîte de dialogue de sauvegarde de fichier s'affiche, permettant à l'utilisateur de choisir l'emplacement et le nom du fichier CSV.
   - Si un nom de fichier est sélectionné, les données des graphiques sont écrites dans le fichier CSV.

10. Fonctions `toggle_send_button()`, `toggle_pause_continue_button()` et `toggle_command_button()` :
    - Ces fonctions sont appelées lorsque les valeurs des boutons de l'interface utilisateur sont modifiées.
    - Elles permettent de mettre à jour l'état des boutons en fonction des valeurs saisies.

11. Fonction `send_values()` :
    - Cette fonction est appelée lorsque l'utilisateur clique sur le bouton "Envoyer les valeurs".
    - Elle récupère les valeurs sélectionnées dans les boutons radio et les zones de texte de l'interface utilisateur.
    - Les valeurs sont formatées et envoyées au périphérique externe via le port série.

12. Fonction `convert_milliseconds(milliseconds)` :
    - Cette fonction est utilisée pour convertir une durée en millisecondes en une chaîne de caractères au format "HH:MM:SS:SSS".

13. Fonction `is_float(string)` :
    - Cette fonction vérifie si une chaîne de caractères peut être convertie en nombre flottant.

14. Création de l'interface utilisateur :
    - Une fenêtre principale est créée en utilisant `tk.Tk()`.
    - Différents widgets (texte, boutons, graphiques) sont ajoutés à la fenêtre en utilisant des dispositions de mise en page.
    - Les fonctions de rappel sont liées aux événements des widgets.
    - La boucle principale de l'interface utilisateur est démarrée en utilisant `root.mainloop()`.

N'oubliez pas d'installer les bibliothèques nécessaires dans votre environnement virtuel Python avec conda, telles que `serial`, `tkinter`, `csv` et `matplotlib`. Vous pouvez les installer en exécutant les commandes suivantes dans votre environnement virtuel :
```
conda install pyserial
conda install tk
conda install matplotlib
```

## master_node.ino

Le code est destiné à un nœud maître (master node) qui communique avec un nœud esclave (slave node) à l'aide de la communication série et du Bluetooth. Le nœud maître reçoit des commandes de l'ordinateur intermédiaire via la communication série et les envoie au nœud esclave via le Bluetooth. Il reçoit également des données du nœud esclave et les transmet à l'ordinateur intermédiaire.

Voici une explication détaillée du code :

1. Déclaration et initialisation des variables :
   - `start` : un booléen indiquant si le nœud maître est prêt à démarrer.
   - `isRunning` : un booléen indiquant si le nœud maître est en cours d'exécution.
   - `counter` : un compteur utilisé pour déterminer si le nœud maître doit démarrer l'acquisition de données.
   - `command` : une chaîne de caractères utilisée pour stocker les commandes reçues.
   - `timer` : une variable qui enregistre le temps écoulé depuis le début du traitement d'une commande.

2. Fonction `setup()` :
   - Cette fonction est exécutée une seule fois au démarrage du programme.
   - Elle initialise les communications série avec le nœud esclave (`Serial1.begin(38400)`) et le Bluetooth (`Serial.begin(115200)`).
   - Le buffer de communication série du Bluetooth est vidé (`Serial1.flush()`).
   - La fonction attend une connexion Bluetooth en envoyant périodiquement un message "Ready?" au nœud esclave avec `Serial1.print("Ready?\n")`.
   - Une fois la connexion établie (`Serial1.available()`), la fonction affiche "connected" et attend une seconde avant de passer à la boucle principale.

3. Boucle principale `loop()` :
   - Cette boucle s'exécute en boucle indéfiniment après l'exécution de la fonction `setup()`.
   - Elle vérifie si des données sont disponibles sur le port série (`Serial.available()`).
   - Si des données sont disponibles, elles sont lues avec `Serial.readStringUntil('\n')` et stockées dans la variable `command`.
   - En fonction de la commande reçue, différentes actions sont effectuées :
     - Si la commande commence par "F" et contient les sous-chaînes "G" et "V", elle est traitée comme une commande de modification des paramètres de fréquence, de gain et de tension de référence.
       - Les nouvelles valeurs sont extraites de la commande.
       - Les valeurs sont ensuite envoyées au nœud esclave via le Bluetooth avec `Serial1.print()`.
     - Si la commande est "start", "stop", "pause" ou "continue", elle est envoyée au nœud esclave via le Bluetooth avec `Serial1.print()` pour contrôler l'acquisition de données.
   - Si des données sont disponibles sur le port série du Bluetooth (`Serial1.available()`), elles sont lues avec `Serial1.readStringUntil('\n')` et stockées dans la variable `data_rec`.
     - Si la valeur de `data_rec` est "yes", cela signifie que le nœud esclave est prêt à démarrer l'acquisition de données.
       - Le compteur `counter` est incrémenté et si sa valeur atteint 8, la variable `isRunning` est définie sur `true`.
     - Si la commande commence par "A" et contient les sous-chaînes "G" et "V", cela signifie que des données ont été reçues du nœud esclave et elles sont affichées.
     - Sinon, la commande et les données reçues sont envoyées à l'ordinateur intermédiaire via la communication série pour un traitement ultérieur.
   - Si `isRunning` est `true`, cela signifie que le nœud maître est en cours d'exécution et il envoie le message "ok from master\n" au nœud esclave pour le notifier.
   - La variable `isRunning` est ensuite définie sur `false` et il y a un délai de 200 ms avant la prochaine itération de la boucle.

Cela résume l'explication du code. Le nœud maître reçoit des commandes de l'ordinateur intermédiaire via la communication série, les transmet au nœud esclave via le Bluetooth et renvoie les données du nœud esclave à l'ordinateur intermédiaire.

## slave_node.ino

Le code est le code du "Slave Node" dans un système de communication à deux nœuds (Master-Slave) utilisant Bluetooth pour interagir avec un autre Arduino (le "Master Node"). Voici une explication détaillée du code :

1. Bibliothèques incluses :
   - `Adafruit_NAU7802.h` : Bibliothèque pour communiquer avec le convertisseur analogique-numérique (CAN) NAU7802.
   - `Arduino.h` : Bibliothèque principale d'Arduino.
   - `Wire.h` : Bibliothèque pour la communication I2C (utilisée par `Adafruit_NAU7802`).

2. Variables globales :
   - `bool isRunning = false;` : Un indicateur booléen pour indiquer si le processus d'acquisition de données est en cours.
   - `bool isStarted = true;` : Un indicateur booléen pour indiquer si le processus d'acquisition de données a démarré.
   - `bool isSendingData = false;` : Un indicateur booléen pour indiquer si les données sont en cours d'envoi.
   - `int freq = 320;` : La fréquence initiale en Hz pour l'acquisition de données.
   - `int gain = 32;` : Le gain initial pour le convertisseur NAU7802.
   - `float vref = 0.122;` : La tension de référence initiale pour le convertisseur NAU7802.
   - `float LDO = 2.4;` : La tension de l'alimentation du convertisseur NAU7802.

3. Fonction `setup()` :
   - La communication série avec le PC intermédiaire est initialisée.
   - La communication série avec le convertisseur NAU7802 est établie.
   - Le convertisseur NAU7802 est configuré avec les valeurs de tension de l'alimentation, du gain et de la fréquence définies par défaut.
   - Les valeurs lues du convertisseur NAU7802 sont lues et éliminées pour vider le tampon.
   - Le calibrage du convertisseur NAU7802 est effectué en fonction des indicateurs `internal`, `gain` et `offset`. S'il échoue, il tente de nouveau le calibrage.

4. 
  

5. Fonction `loop()` : Lecture des commandes du "Master Node" :
   - Si des données sont disponibles sur le port série Bluetooth (`Serial1.available()`), la fonction lit la commande envoyée par le "Master Node".
   - En fonction de la commande reçue, différentes actions sont effectuées :
     - Si la commande commence par "F" et contient les sous-chaînes "G" et "V", cela signifie qu'elle contient de nouvelles valeurs pour la fréquence, le gain et la tension de référence. Ces valeurs sont extraites de la commande et utilisées pour mettre à jour les paramètres du convertisseur NAU7802.
     - Si la commande est "start", l'indicateur `isRunning` est défini sur true pour indiquer que le processus d'acquisition de données peut démarrer.
     - Si la commande est "stop" ou "pause", l'indicateur `isRunning` est défini sur false pour arrêter le processus d'acquisition de données.
     - Si la commande est "continue", l'indicateur `isRunning` est défini sur true pour reprendre le processus d'acquisition de données.
     - Si la commande est "Ready?" ou "ok from master", un message de confirmation est envoyé au "Master Node" via la communication Bluetooth.

6. Fonction `ADCconfig()` :
   - Cette fonction configure le convertisseur NAU7802 en fonction des valeurs de tension de l'alimentation, du gain et de la fréquence spécifiées.
   - Les valeurs de tension de l'alimentation, du gain et de la fréquence sont sélectionnées à partir des paramètres de la fonction pour configurer le convertisseur NAU7802.

7. Fonction `setCalibration()` :
   - Cette fonction effectue le calibrage du convertisseur NAU7802 en fonction des indicateurs `internal`, `gain` et `offset`.
   - S'il est nécessaire de calibrer l'offset, le gain ou les valeurs internes, la fonction tente de calibrer le convertisseur NAU7802 et réessaie s'il échoue.

8. Fonction `readADC()` :
   - Cette fonction effectue l'acquisition de données à partir du convertisseur NAU7802.
   - Le nombre d'acquisitions à effectuer est déterminé par la fréquence spécifiée.
   - Pour chaque acquisition, les données sont lues du convertisseur NAU7802 et envoyées au "Master Node" via la communication Bluetooth.
