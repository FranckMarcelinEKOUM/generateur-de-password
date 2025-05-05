import tkinter as tk
from tkinter import filedialog, scrolledtext
import itertools
import random

# Variable globale qui contiendra l'ensemble des mots de passe candidats
password_dictionary = []

def generate_password_candidates(personal_data, target_len=8, tol=1):
    """
    Génère une liste de candidats de mot de passe à partir d'un dictionnaire d'informations personnelles.
    On ne retient que les mots ou combinaisons dont la longueur se situe entre target_len - tol et target_len + tol.
    
    Args:
        personal_data (dict): Dictionnaire avec des informations personnelles (nom, prénom, etc.).
        target_len (int): Longueur cible pour le mot de passe (par défaut 8 caractères).
        tol (int): Tolérance sur la longueur (par défaut 1, soit entre 7 et 9 caractères).
    
    Returns:
        list: Liste triée de candidats.
    """
    candidates = set()
    min_len = target_len - tol
    max_len = target_len + tol

    # 1. Utilisation individuelle de chaque information
    for key, value in personal_data.items():
        word = value.strip().lower()
        if word and (min_len <= len(word) <= max_len):
            candidates.add(word)
        # Si l'information est trop longue, on ajoute la version tronquée
        if len(word) > target_len:
            candidates.add(word[:target_len])
            candidates.add(word[-target_len:])

    # 2. Création de combinaisons de 2 ou 3 éléments (dans tous les ordres possibles)
    fields = [v.strip().lower() for v in personal_data.values() if v.strip()]
    for r in range(2, 4):
        for combo in itertools.permutations(fields, r):
            candidate = "".join(combo)
            if min_len <= len(candidate) <= max_len:
                candidates.add(candidate)
            # On ajoute des versions tronquées quand la combinaison dépasse la longueur cible
            if len(candidate) > target_len:
                candidates.add(candidate[:target_len])
                candidates.add(candidate[-target_len:])
    return sorted(candidates)

def update_animal_field():
    """
    Active ou désactive le champ "Nom de l'animal" selon la réponse donnée via le bouton radio.
    Si "oui" est sélectionné, le champ est activé, sinon il est vidé et désactivé.
    """
    if animal_option.get() == "oui":
        animal_entry.config(state="normal")
    else:
        animal_entry.delete(0, tk.END)
        animal_entry.config(state="disabled")

def generate_dictionary():
    """
    Récupère les données saisies dans le formulaire, génère l'ensemble des candidats de mot de passe 
    et les affiche dans la zone de texte.
    """
    global password_dictionary
    # Constitution du dictionnaire à partir des infos saisies
    personal_info = {
        "nom": nom_entry.get(),
        "prenom": prenom_entry.get(),
        "date_naissance": dob_entry.get(),
        "couleur": couleur_entry.get(),
        "quartier": quartier_entry.get(),
        "metier": metier_entry.get()
    }
    if animal_option.get() == "oui":
        animal_value = animal_entry.get().strip()
        if animal_value:
            personal_info["animal"] = animal_value

    # Génération de la liste de candidats
    candidates = generate_password_candidates(personal_info, target_len=8, tol=1)
    password_dictionary = candidates  # Mise à jour de la variable globale

    # Mise à jour d'un label pour indiquer le nombre de mots de passe générés
    dictionary_label.config(text=f"{len(candidates)} mots de passe générés.")
    # Affichage des candidats dans la zone de texte
    dictionary_text.delete("1.0", tk.END)
    for pwd in candidates:
        dictionary_text.insert(tk.END, pwd + "\n")
    status_label.config(text="")  # Réinitialisation du status

def save_dictionary():
    """
    Ouvre une boîte de dialogue pour choisir le chemin et le nom du fichier dans lequel
    le dictionnaire de mots de passe généré sera sauvegardé.
    """
    if not password_dictionary:
        status_label.config(text="Aucun dictionnaire généré à sauvegarder.", fg="red")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Fichiers texte", "*.txt")],
        title="Sélectionnez l'emplacement pour sauvegarder le dictionnaire"
    )
    if file_path:
        try:
            with open(file_path, "w") as f:
                for pwd in password_dictionary:
                    f.write(pwd + "\n")
            status_label.config(text=f"Dictionnaire sauvegardé dans : {file_path}", fg="green")
        except Exception as e:
            status_label.config(text=f"Erreur lors de la sauvegarde : {e}", fg="red")
    else:
        status_label.config(text="Sauvegarde annulée.", fg="red")

# --- Création de la fenêtre principale ---
root = tk.Tk()
root.title("Générateur de dictionnaire de mots de passe")

# Création des champs du formulaire
tk.Label(root, text="Nom :").grid(row=0, column=0, sticky="e", padx=5, pady=5)
nom_entry = tk.Entry(root, width=30)
nom_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Prénom :").grid(row=1, column=0, sticky="e", padx=5, pady=5)
prenom_entry = tk.Entry(root, width=30)
prenom_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Date de naissance (JJMMAAAA) :").grid(row=2, column=0, sticky="e", padx=5, pady=5)
dob_entry = tk.Entry(root, width=30)
dob_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Couleur préférée :").grid(row=3, column=0, sticky="e", padx=5, pady=5)
couleur_entry = tk.Entry(root, width=30)
couleur_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Avez-vous un animal ?").grid(row=4, column=0, sticky="e", padx=5, pady=5)
animal_option = tk.StringVar(value="non")
tk.Radiobutton(root, text="Oui", variable=animal_option, value="oui", command=update_animal_field).grid(row=4, column=1, sticky="w", padx=5)
tk.Radiobutton(root, text="Non", variable=animal_option, value="non", command=update_animal_field).grid(row=4, column=1, padx=60)

tk.Label(root, text="Nom de l'animal :").grid(row=5, column=0, sticky="e", padx=5, pady=5)
animal_entry = tk.Entry(root, width=30, state="disabled")
animal_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Quartier :").grid(row=6, column=0, sticky="e", padx=5, pady=5)
quartier_entry = tk.Entry(root, width=30)
quartier_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Métier préféré :").grid(row=7, column=0, sticky="e", padx=5, pady=5)
metier_entry = tk.Entry(root, width=30)
metier_entry.grid(row=7, column=1, padx=5, pady=5)

# Bouton pour générer le dictionnaire
generate_button = tk.Button(root, text="Générer le dictionnaire", command=generate_dictionary)
generate_button.grid(row=8, column=0, columnspan=2, pady=10)

# Label qui affiche le nombre de mots de passe générés
dictionary_label = tk.Label(root, text="")
dictionary_label.grid(row=9, column=0, columnspan=2, pady=5)

# Zone de texte (avec défilement) pour afficher le dictionnaire de mots de passe
dictionary_text = scrolledtext.ScrolledText(root, width=50, height=10)
dictionary_text.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Bouton pour enregistrer le dictionnaire dans un fichier texte
save_button = tk.Button(root, text="Enregistrer le dictionnaire", command=save_dictionary)
save_button.grid(row=11, column=0, columnspan=2, pady=10)

# Label pour afficher les statuts ou erreurs lors de la sauvegarde
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=12, column=0, columnspan=2, pady=5)

# Boucle principale de l'interface
root.mainloop()
