import serial
import time
import tkinter as tk
from tkinter import ttk, filedialog
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Spécifiez le port série et le débit binaire ici
port = 'COM4'  # Remplacez par votre port série
baud_rate = 115200

fullScale = 8388608
g = 9.80665
Vref = 0.122
dA = 1
dB = 1

# Initialisez la connexion série
ser = serial.Serial(port, baud_rate)

# Création de la figure et des axes pour les graphiques
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))

# Initialisation des lignes des graphiques
line1, = ax1.plot([], [])
line2, = ax2.plot([], [])
line3, = ax3.plot([], [])

# Ajout des étiquettes d'axe pour les graphiques
ax1.set_xlabel('Temps')
ax1.set_ylabel('Tension')
ax2.set_xlabel('Temps')
ax2.set_ylabel('Force(N)')
ax3.set_xlabel('Temps')
ax3.set_ylabel('Reaction(N)')

# Variables pour stocker les données des graphiques
x = []
y1 = []
y2 = []
y3 = []

# Fonction pour mettre à jour les graphiques
def update_graphs(time, voltage, paddle_force, blade_reaction):
    # Ajouter les nouvelles valeurs aux listes existantes
    x.append(time)
    y1.append(voltage)
    y2.append(paddle_force)
    y3.append(blade_reaction)

    # Mettre à jour les données des graphiques
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    line3.set_data(x, y3)

    # Redessiner les graphiques
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    ax3.relim()
    ax3.autoscale_view()
    fig.canvas.draw()

# Fonction pour lire les données du port série et appeler la mise à jour des graphiques
def read_serial():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        py_time = time.time()
        data_tab = data.split(';')
        
        if len(data_tab) > 1 and data_tab[1][:3] == 'ACK':
            # Activation du bouton start
            start_button.config(state=tk.NORMAL)
            # Afficher les données dans l'interface utilisateur
            text_box.insert(tk.END, data_tab[0] + " - " + data_tab[1] + '\n')
            text_box.see(tk.END)  # Défiler vers le bas
            
        elif len(data_tab) > 2:
            if is_float(data_tab[2]) :
                read_time = float(data_tab[2])
                recep_time = float(data_tab[0])
                read_time_formatted = convert_milliseconds(read_time)
                recep_time_formated = convert_milliseconds(recep_time)
                ADC_value = float(data_tab[3])
                # Afficher les données dans l'interface utilisateur
                data_new = data_tab[1] + " - " + read_time_formatted + " - " + recep_time_formated + " - " + data_tab[2] + " - " + data_tab[0] + " - " + data_tab[3]
                text_box.insert(tk.END, data_new + '\n')
                text_box.see(tk.END)  # Défiler vers le bas
                compute(read_time, ADC_value)           
        else:
            # Afficher les données dans l'interface utilisateur
            text_box.insert(tk.END, data + '\n')
            text_box.see(tk.END)  # Défiler vers le bas
            
    # Répéter la fonction après un délai de 2ms
    root.after(2, read_serial)

def compute(time, ADC_value):
    dA = float(dA_entry.get())
    dB = float(dB_entry.get())
    #dA = 2
    #dB = 1.4
    

    fsdv = float(ref_voltage_entry.get()) / float(gain_var.get()) / 2
    #fsdv = 0.22 / 32 / 2
    # Calculer la tension
    voltage = ADC_value * fsdv / fullScale
    # Calculer le poids    y = 0,0125x - 9,1068
    weightCal = 0.0125 * voltage
    # Calculer la force sur l'arbre de la pale
    paddle_force = weightCal * g
    # Calculer la force de réaction sur la lame de la pale
    blade_reaction = paddle_force * (dA / (dA + dB))

    # Mettre à jour les graphiques
    update_graphs(time, voltage, paddle_force, blade_reaction)

# Fonction pour sauvegarder les données en CSV
def save_to_csv():
    # Demande à l'utilisateur de saisir le nom du fichier de sauvegarde
    filename = filedialog.asksaveasfilename(defaultextension=".csv")

    # Vérifie si un nom de fichier a été saisi
    if filename:
        # Crée le fichier CSV et écrit les données
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Temps', 'Tension', 'Force'])  # Écrit les en-têtes des colonnes
            writer.writerows(zip(x, y1, y2))  # Écrit les données des graphiques

# Fonction pour activer/désactiver le bouton d'envoi des valeurs de fréquence, gain et vref
def toggle_send_button():
    selected_freq = freq_var.get()
    selected_gain = gain_var.get()
    selected_ref_voltage = ref_voltage_entry.get()
    dA = dA_entry.get()
    dB = dB_entry.get()

    if selected_freq and selected_gain and selected_ref_voltage and dA and dB:
        send_button.config(state=tk.NORMAL)
    else:
        send_button.config(state=tk.DISABLED)

# Fonction pour activer/désactiver le bouton "Pause"/"Continue"
def toggle_pause_continue_button():
    if command_button_state.get() == 'Stop':
        if pause_continue_button_state.get() == 'Pause':
            pause_continue_button_state.set('Continue')
            command = 'pause\n'
        else:
            pause_continue_button_state.set('Pause')
            command = 'continue\n'
        ser.write(command.encode())

# Fonction pour changer l'état du bouton de commande démarrer/arrêter
def toggle_command_button():
    if command_button_state.get() == 'Start':
        command_button_state.set('Stop')
        command = 'start\n'
        pause_continue_button.config(state=tk.NORMAL)
    else:
        command_button_state.set('Start')
        command = 'stop\n'
        pause_continue_button.config(state=tk.DISABLED)
    ser.write(command.encode())

# Fonction pour envoyer les valeurs par port série
def send_values():
    freq = freq_var.get()
    gain = gain_var.get()
    ref_voltage = ref_voltage_entry.get()
    dA = dA_entry.get()
    dB = dB_entry.get()

    if freq and gain and ref_voltage and dA and dB:
        command = f"F{freq} G{gain} V{ref_voltage}"  # Format de la commande pour Arduino
        # Envoie des valeurs par port série
        ser.write(command.encode())
        
def convert_milliseconds(milliseconds):
    # Calcul des heures, minutes, secondes et millisecondes
    hours = int(milliseconds // (1000 * 60 * 60))
    milliseconds %= (1000 * 60 * 60)
    minutes = int(milliseconds // (1000 * 60))
    milliseconds %= (1000 * 60)
    seconds = int(milliseconds // 1000)
    milliseconds %= 1000

    # Formatage du temps
    time_string = "{:02d}:{:02d}:{:02d}:{:03.0f}".format(hours, minutes, seconds, milliseconds)

    return time_string
def is_float(string):
    try:
        float_value = float(string)
        return True
    except ValueError:
        return False

   
    
# Création de l'interface utilisateur
root = tk.Tk()
root.title('MUSSAKA')

# Zone de texte pour afficher les données
#text_box = tk.Text(root, width=40, height=10)
text_box = tk.Text(root)
text_box.pack(side=tk.LEFT)

# Frame pour la saisie de les distances
input_frame  = tk.Frame(root)
# Label pour la distance dA
dA_label = ttk.Label(input_frame  , text="dA :") 
dA_label.pack(side=tk.LEFT, padx=10)
# Zone de texte pour la saisie de la distance dA
dA_entry = ttk.Entry(input_frame  ) 
dA_entry.pack(side=tk.LEFT)
# Label pour la distance dB
dB_label = ttk.Label(input_frame  , text="dB : ") 
dB_label.pack(side=tk.LEFT, padx=10)
# Zone de texte pour la saisie de la distance dB
dB_entry = ttk.Entry(input_frame  ) 
dB_entry.pack(side=tk.LEFT)
# Label pour la tension de référence
ref_voltage_label = ttk.Label(input_frame , text="Vref:")
ref_voltage_label.pack(side=tk.LEFT, padx=10)
# Zone de texte pour la saisie de la tension de référence
ref_voltage_entry = ttk.Entry(input_frame )
ref_voltage_entry.pack(side=tk.LEFT)
input_frame  .pack()

# Frame pour les boutons de fréquence
freq_frame = tk.Frame(root)
freq_var = tk.StringVar() # Variable pour stocker la fréquence sélectionnée
freq_var.set("80") # Valeur initiale
freq_label = ttk.Label(freq_frame, text="Fréquence (Hz):") # Label pour le choix de la fréquence
freq_label.pack(side=tk.LEFT, padx=10)
# Boutons pour choisir la fréquence
freq_button_10 = ttk.Radiobutton(freq_frame, text="10", value="10", variable=freq_var, command=toggle_send_button)
freq_button_10.pack(side=tk.LEFT)
freq_button_20 = ttk.Radiobutton(freq_frame, text="20", value="20", variable=freq_var, command=toggle_send_button)
freq_button_20.pack(side=tk.LEFT)
freq_button_40 = ttk.Radiobutton(freq_frame, text="40", value="40", variable=freq_var, command=toggle_send_button)
freq_button_40.pack(side=tk.LEFT)
freq_button_80 = ttk.Radiobutton(freq_frame, text="80", value="80", variable=freq_var, command=toggle_send_button)
freq_button_80.pack(side=tk.LEFT)
freq_button_320 = ttk.Radiobutton(freq_frame, text="320", value="320", variable=freq_var, command=toggle_send_button)
freq_button_320.pack(side=tk.LEFT)
freq_frame.pack()

# Frame pour les boutons de gain
gain_frame = tk.Frame(root)
# Variable pour stocker le gain sélectionné
gain_var = tk.StringVar()
gain_var.set("32")  # Valeur initiale
# Label pour le choix du gain
gain_label = ttk.Label(gain_frame, text="Gain:")
gain_label.pack(side=tk.LEFT, padx=10)
# Boutons pour choisir le gain
gain_button_4 = ttk.Radiobutton(gain_frame, text="4", value="4", variable=gain_var, command=toggle_send_button)
gain_button_4.pack(side=tk.LEFT)
gain_button_8 = ttk.Radiobutton(gain_frame, text="8", value="8", variable=gain_var, command=toggle_send_button)
gain_button_8.pack(side=tk.LEFT)
gain_button_16 = ttk.Radiobutton(gain_frame, text="16", value="16", variable=gain_var, command=toggle_send_button)
gain_button_16.pack(side=tk.LEFT)
gain_button_32 = ttk.Radiobutton(gain_frame, text="32", value="32", variable=gain_var, command=toggle_send_button)
gain_button_32.pack(side=tk.LEFT)
gain_button_64 = ttk.Radiobutton(gain_frame, text="64", value="64", variable=gain_var, command=toggle_send_button)
gain_button_64.pack(side=tk.LEFT)
gain_button_128 = ttk.Radiobutton(gain_frame, text="128", value="128", variable=gain_var, command=toggle_send_button)
gain_button_128.pack(side=tk.LEFT)
gain_frame.pack()



# Bouton pour envoyer les valeurs
send_button = ttk.Button(root, text="Envoyer les valeurs", command=send_values, state=tk.DISABLED)
send_button.pack()

# Affichage des graphiques
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Frame pour les boutons de commande
command_frame = tk.Frame(root)

# Variable de contrôle pour le bouton de démarrer/arrêter
command_button_state = tk.StringVar()
command_button_state.set('Start')
# Bouton pour démarrer/arrêter la réception de données
start_button = ttk.Button(command_frame, textvariable=command_button_state, command=toggle_command_button, state=tk.DISABLED)
start_button.pack(side=tk.LEFT, padx=10)

# Variable de contrôle pour le bouton "Pause"/"Continue"
pause_continue_button_state = tk.StringVar()
pause_continue_button_state.set('Pause')
# Bouton pour les commandes "Pause"/"Continue"
pause_continue_button = ttk.Button(command_frame , textvariable=pause_continue_button_state, command=toggle_pause_continue_button, state=tk.DISABLED)
pause_continue_button.pack(side=tk.LEFT, padx=10)

command_frame .pack()


# Bouton pour sauvegarder les données en CSV
save_button = ttk.Button(root, text="Sauvegarder en CSV", command=save_to_csv)
save_button.pack()


# Pour stocker les commandes à envoyer
command = ''


# Lancement de la fonction de lecture du port série
read_serial()

# Démarrage de la boucle principale de l'interface utilisateur
root.mainloop()
