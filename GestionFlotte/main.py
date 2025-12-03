import sys
from datetime import date
from storage import StorageManager
from vehicles import Car, Truck, Motorcycle, Hearse, GoKart, Carriage
from animals import Horse, Donkey, Camel

# --- 🛠️ FONCTIONS UTILITAIRES (Pour ne pas faire planter le programme) ---
def ask_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("❌ Erreur : Veuillez entrer un nombre entier.")

def ask_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("❌ Erreur : Veuillez entrer un nombre décimal (ex: 10.5).")

def ask_bool(message):
    val = input(f"{message} (o/n) : ").lower()
    return val == 'o' or val == 'oui'

def add_vehicle_menu(fleet):
    print("\n--- AJOUTER UN NOUVEAU VÉHICULE ---")
    print("1. Voiture")
    print("2. Poney")
    print("3. Camion")
    print("4. Calèche")
    print("5. Chameau")
    print("6. Moto")
    print("7. Corbillard")
    print("8. Ane")
    print("9. Kart")
    print("0. Annuler")
    
    choice = input("Votre choix : ")
    
    new_id = 1
    if fleet:
        new_id = max(v.id for v in fleet) + 1
    
    if choice in ['1', '2', '3']:
        rate = ask_float("Tarif journalier (€) : ")

    if choice == '1':
        brand = input("Marque : ")
        model = input("Modèle : ")
        plate = input("Plaque : ")
        doors = ask_int("Nombre de portes : ")
        ac = ask_bool("A la climatisation ?")
        
        new_obj = Car(new_id, rate, brand, model, plate, doors, ac)
        fleet.append(new_obj)
        print("✅ Voiture ajoutée avec succès !")

    elif choice == '2':
        name = input("Nom du poney : ")
        breed = input("Race : ")
        height = ask_int("Hauteur au garrot (cm) : ")
        shoe = ask_int("Taille du fer : ")
        birth = date(2020, 1, 1)
        
        new_obj = Horse(new_id, rate, name, breed, birth, height, shoe)
        fleet.append(new_obj)
        print("✅ Poney ajouté avec succès !")

    elif choice == '3':
        brand = input("Marque : ")
        model = input("Modèle : ")
        plate = input("Plaque : ")
        vol = ask_float("Volume (m3) : ")
        weight = ask_float("Poids Max (T) : ")
        
        new_obj = Truck(new_id, rate, brand, model, plate, vol, weight)
        fleet.append(new_obj)
        print("✅ Camion ajouté avec succès !")

    elif choice == '0':
        print("Annulation.")
    else:
        print("❌ Choix invalide.")

# --- 🗑️ FONCTION SUPPRIMER UN VÉHICULE ---
def delete_vehicle_menu(fleet):
    print("\n--- SUPPRIMER UN VÉHICULE ---")
    target_id = ask_int("Entrez l'ID du véhicule à supprimer : ")
    
    # On cherche le véhicule dans la liste
    found = None
    for v in fleet:
        if v.id == target_id:
            found = v
            break
    
    if found:
        print(f"❓ Êtes-vous sûr de vouloir supprimer : {found.show_details()} ?")
        confirm = ask_bool("Confirmer la suppression")
        if confirm:
            fleet.remove(found)
            print("🗑️ Véhicule supprimé.")
        else:
            print("Annulation.")
    else:
        print("❌ Aucun véhicule trouvé avec cet ID.")

# --- 📋 FONCTION LISTER ---
def list_fleet(fleet):
    if not fleet:
        print("\nLa flotte est vide.")
    else:
        print(f"\n--- ÉTAT DE LA FLOTTE ({len(fleet)} véhicules) ---")
        for v in fleet:
            print(f"[{v.id}] {v.show_details()} | Statut: {v.status.value}")

# --- 🚀 MENU PRINCIPAL ---
def main():
    storage = StorageManager("ma_flotte.json")
    my_fleet = storage.load_fleet()
    
    while True:
        print("\n" + "="*30)
        print("   GESTION DE FLOTTE v1.0")
        print("="*30)
        print("1. 📋 Voir la flotte")
        print("2. ➕ Ajouter un véhicule")
        print("3. 🗑️ Supprimer un véhicule")
        print("4. 💾 Sauvegarder et Quitter")
        
        choix = input("\nVotre choix : ")

        if choix == '1':
            list_fleet(my_fleet)
        
        elif choix == '2':
            add_vehicle_menu(my_fleet)
            
        elif choix == '3':
            delete_vehicle_menu(my_fleet)
            
        elif choix == '4':
            storage.save_fleet(my_fleet)
            print("Au revoir !")
            break
        
        else:
            print("Je n'ai pas compris votre choix.")

if __name__ == "__main__":
    main()