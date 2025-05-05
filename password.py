"""
Dans ce script utilise Tkinter pour présenter un formulaire interactif. Dans ce formulaire, 
l'utilisateur peut sélectionner s'il possède un animal (via des boutons radio);
dans le cas où il répond "Oui", le champ pour entrer le nom de l'animal devient actif.
Ensuite, une fois que toutes les informations sont remplies,
le script génère un mot de passe de manière aléatoire lorsqu'on clique sur le bouton générer un mot de passe
et sauvegarde ce mot de passe dans un fichier texte choisi à l'aide d'une boîte de dialogue
"""
import tkinter as tk
from tkinter import filedialog
import itertools
import random

# Variable globale pour stocker le dernier mot de passe généré
current_password = ""

def generate_password_candidates(personal_data, target_len=8, tol=1):
    """
    Génère une liste de candidats de mot de passe à partir d'un dictionnaire d'informations personnelles.
    
    Seules les combinaisons dont la longueur se situe entre target_len - tol et target_len + tol sont retenues.
    
    Args:
        personal_data (dict): Dictionnaire avec des informations personnelles (ex: "nom", "prénom", etc.).
        target_len (int): Longueur cible pour le mot de passe (par défaut, 8 caractères).
        tol (int): Tolérance sur la longueur (par défaut, 1, donc entre 7 et 9 caractères).
        
    Returns:
        list: Liste triée des candidats de mot de passe.
    """
    candidates = set()  # On utilise un ensemble pour éviter les doublons.
    min_len = target_len - tol
    max_len = target_len + tol

    # Étape 1 : Examiner chaque information individuellement.
    for key, value in personal_data.items():
        word = value.strip().lower()  # On nettoie (enlève les espaces inutiles) et on met en minuscule.
        if word and (min_len <= len(word) <= max_len):
            candidates.add(word)  # Ajoute le mot si sa longueur est dans la plage désirée.
        # S'il est trop long, on ajoute une version tronquée (les premiers ou les derniers target_len caractères).
        if len(word) > target_len:
            candidates.add(word[:target_len])
            candidates.add(word[-target_len:])

    # Étape 2 : Combiner 2 ou 3 informations en différentes permutations.
    # On filtre les valeurs vides pour éviter des combinaisons non désirées.
    fields = [v.strip().lower() for v in personal_data.values() if v.strip()]
    for r in range(2, 4):  # r = 2 et r = 3 pour combiner 2 ou 3 éléments.
        for combo in itertools.permutations(fields, r):
            candidate = "".join(combo)  # On concatène les éléments de la permutation.
            if min_len <= len(candidate) <= max_len:
                candidates.add(candidate)  # Ajoute la combinaison si elle a une longueur correcte.
            # Si la combinaison est trop longue, ajouter des versions tronquées.
            if len(candidate) > target_len:
                candidates.add(candidate[:target_len])
                candidates.add(candidate[-target_len:])
                
    return sorted(candidates)

def update_animal_field():
    """
    Active ou désactive le champ "Nom de l'animal" selon la sélection de l'utilisateur.
    Si l'utilisateur choisit "Oui", le champ devient éditable. Sinon, il est effacé et désactivé.
    """
    if animal_option.get() == "oui":
        animal_entry.config(state="normal")
    else:
        animal_entry.delete(0, tk.END)
        animal_entry.config(state="disabled")

def generate_password():
    """
    Récupère les informations du formulaire, génère une liste de candidats de mot de passe,
    choisit aléatoirement un mot de passe dans cette liste et met à jour l'affichage dans l'interface.
    """
    global current_password
    # Constitution du dictionnaire avec les données saisies par l'utilisateur
    personal_info = {
        "nom": nom_entry.get(),
        "prenom": prenom_entry.get(),
        "date_naissance": dob_entry.get(),
        "couleur": couleur_entry.get(),
        "quartier": quartier_entry.get(),
        "metier": metier_entry.get()
    }
    # Si l'utilisateur possède un animal, on ajoute son nom au dictionnaire
    if animal_option.get() == "oui":
        animal_value = animal_entry.get().strip()
        if animal_value:
            personal_info["animal"] = animal_value

    # Génère la liste des candidats de mot de passe en se basant sur les données personnelles
    candidates = generate_password_candidates(personal_info, target_len=8, tol=1)
    if candidates:
        # Sélectionner aléatoirement l'un des candidats pour avoir une génération différente à chaque clic.
        current_password = random.choice(candidates)
    else:
        current_password = "Aucun"

    # Met à jour l'affichage du mot de passe généré dans le label dédié
    password_label.config(text=f"Mot de passe généré : {current_password}")
    status_label.config(text="")  # Réinitialise le message de statut

def save_password():
    """
    Ouvre une boîte de dialogue pour que l'utilisateur choisisse l'emplacement et le nom du fichier texte
    dans lequel le mot de passe généré sera sauvegardé.
    Un message de statut informe ensuite l'utilisateur du succès ou d'une éventuelle erreur.
    """
    if not current_password:
        status_label.config(text="Aucun mot de passe à sauvegarder.", fg="red")
        return

    # Ouvre la boîte de dialogue de sauvegarde de fichier
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",  # Définit l'extension par défaut
        filetypes=[("Fichiers texte", "*.txt")],
        title="Choisissez l'emplacement pour sauvegarder le mot de passe"
    )
    if file_path:
        try:
            # Écriture du mot de passe dans le fichier choisi
            with open(file_path, "w") as f:
                f.write(current_password)
            status_label.config(text=f"Mot de passe sauvegardé dans : {file_path}", fg="green")
        except Exception as e:
            status_label.config(text=f"Erreur lors de la sauvegarde : {e}", fg="red")
    else:
        status_label.config(text="Sauvegarde annulée.", fg="red")

# --- Création de la fenêtre principale avec Tkinter ---
root = tk.Tk()
root.title("Générateur de mot de passe personnalisé")

# Création du formulaire pour saisir les informations personnelles

# Champ Nom
tk.Label(root, text="Nom :").grid(row=0, column=0, sticky="e", padx=5, pady=5)
nom_entry = tk.Entry(root, width=30)
nom_entry.grid(row=0, column=1, padx=5, pady=5)

# Champ Prénom
tk.Label(root, text="Prénom :").grid(row=1, column=0, sticky="e", padx=5, pady=5)
prenom_entry = tk.Entry(root, width=30)
prenom_entry.grid(row=1, column=1, padx=5, pady=5)

# Champ Date de naissance (format JJMMAAAA)
tk.Label(root, text="Date de naissance (JJMMAAAA) :").grid(row=2, column=0, sticky="e", padx=5, pady=5)
dob_entry = tk.Entry(root, width=30)
dob_entry.grid(row=2, column=1, padx=5, pady=5)

# Champ Couleur préférée
tk.Label(root, text="Couleur préférée :").grid(row=3, column=0, sticky="e", padx=5, pady=5)
couleur_entry = tk.Entry(root, width=30)
couleur_entry.grid(row=3, column=1, padx=5, pady=5)

# Boutons radio pour indiquer si l'utilisateur a un animal
tk.Label(root, text="Avez-vous un animal ?").grid(row=4, column=0, sticky="e", padx=5, pady=5)
animal_option = tk.StringVar(value="non")  # La valeur par défaut est "non"
tk.Radiobutton(root, text="Oui", variable=animal_option, value="oui", command=update_animal_field).grid(row=4, column=1, sticky="w", padx=5)
tk.Radiobutton(root, text="Non", variable=animal_option, value="non", command=update_animal_field).grid(row=4, column=1, padx=60)

# Champ pour le Nom de l'animal (désactivé par défaut)
tk.Label(root, text="Nom de l'animal :").grid(row=5, column=0, sticky="e", padx=5, pady=5)
animal_entry = tk.Entry(root, width=30, state="disabled")
animal_entry.grid(row=5, column=1, padx=5, pady=5)

# Champ Quartier
tk.Label(root, text="Quartier :").grid(row=6, column=0, sticky="e", padx=5, pady=5)
quartier_entry = tk.Entry(root, width=30)
quartier_entry.grid(row=6, column=1, padx=5, pady=5)

# Champ Métier préféré
tk.Label(root, text="Métier préféré :").grid(row=7, column=0, sticky="e", padx=5, pady=5)
metier_entry = tk.Entry(root, width=30)
metier_entry.grid(row=7, column=1, padx=5, pady=5)

# Bouton pour générer le mot de passe à partir des données saisies
generate_button = tk.Button(root, text="Générer le mot de passe", command=generate_password)
generate_button.grid(row=8, column=0, columnspan=2, pady=10)

# Label pour afficher le mot de passe généré
password_label = tk.Label(root, text="Mot de passe généré : ", fg="blue")
password_label.grid(row=9, column=0, columnspan=2, pady=5)

# Bouton pour enregistrer le mot de passe dans un fichier texte
save_button = tk.Button(root, text="Enregistrer dans un fichier", command=save_password)
save_button.grid(row=10, column=0, columnspan=2, pady=10)

# Label pour afficher le statut (succès ou erreur) lorsque le mot de passe est sauvegardé
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=11, column=0, columnspan=2, pady=5)

# Lancement de la boucle principale pour afficher la fenêtre
root.mainloop()
