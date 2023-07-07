import serial
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import csv

# Spécifiez le port série et le débit binaire ici
port = 'COM3'  # Remplacez par votre port série '/dev/ttyACM0'
baud_rate = 9600

# Initialisez la connexion série
ser = serial.Serial(port, baud_rate)

# Fonction pour envoyer une commande par port série
def send_command(command):
    ser.write(command.encode())

# Fonction pour lire les données du port série et afficher le texte
def read_serial():
    if ser.in_waiting > 0:
        # Lire les données du port série
        data = ser.readline().decode('utf-8').rstrip()
        
        # Afficher les données dans l'interface utilisateur
        text_box.insert(tk.END, data + '\n')

    # Répéter la fonction après un délai de 100 ms
    root.after(100, read_serial)

# Fonction pour sauvegarder les données en CSV
def save_data_to_csv(data):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Fonction pour afficher le graphique 1
def plot_graph1():
    # Code pour afficher le premier graphique
    plt.figure(1)
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graphique 1')
    plt.show()

# Fonction pour afficher le graphique 2
def plot_graph2():
    # Code pour afficher le deuxième graphique
    plt.figure(2)
    plt.plot([1, 2, 3, 4], [1, 8, 27, 64])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graphique 2')
    plt.show()

# Fonction pour afficher le graphique 3
def plot_graph3():
    # Code pour afficher le troisième graphique
    plt.figure(3)
    plt.plot([1, 2, 3, 4], [1, 2, 3, 4])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graphique 3')
    plt.show()

# Création de l'interface utilisateur
root = tk.Tk()
root.title('Interface utilisateur')

# Zone de texte pour afficher les données
text_box = tk.Text(root)
text_box.pack()

# Boutons pour les commandes
start_button = ttk.Button(root, text='Start', command=lambda: send_command('start'))
start_button.pack()

pause_button = ttk.Button(root, text='Pause', command=lambda: send_command('pause'))
pause_button.pack()

continue_button = ttk.Button(root, text='Continue', command=lambda: send_command('continue'))
continue_button.pack()

# Boutons pour afficher les graphiques
graph1_button = ttk.Button(root, text='Graphique 1', command=plot_graph1)
graph1_button.pack()

graph2_button = ttk.Button(root, text='Graphique 2', command=plot_graph2)
graph2_button.pack()

graph3_button = ttk.Button(root, text='Graphique 3', command=plot_graph3)
graph3_button.pack()

# Menu déroulant pour la sélection des données à sauvegarder en CSV
data_var = tk.StringVar()
data_var.set('Données 1')

data_dropdown = ttk.OptionMenu(root, data_var, 'Données 1', 'Données 2', 'Données 3')
data_dropdown.pack()

# Bouton pour sauvegarder les données sélectionnées
save_button = ttk.Button(root, text='Sauvegarder en CSV', command=lambda: save_data_to_csv(data_var.get()))
save_button.pack()

# Lancement de la fonction de lecture du port série
read_serial()

# Démarrage de la boucle principale de l'interface utilisateur
root.mainloop()
