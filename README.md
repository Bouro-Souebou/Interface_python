# Interface_python
Le code que vous avez fourni est une application Python qui implémente une interface utilisateur graphique (GUI) à l'aide de la bibliothèque Tkinter. L'application communique avec un périphérique externe via un port série pour lire et afficher les données reçues, effectuer des calculs et afficher des graphiques en temps réel.

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
