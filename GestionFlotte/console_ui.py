from datetime import date
from vehicles import Car, Truck, Motorcycle, Hearse, GoKart, Carriage
from animals import Horse, Donkey, Camel
from enums import MaintenanceType, VehicleStatus
from maintenance import Maintenance

# --- 🛠️ HELPER FUNCTIONS (Validations) ---
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
    return val in ['o', 'oui', 'y', 'yes']

# --- 📋 FONCTIONS D'AFFICHAGE ---
def show_main_menu():
    print("\n" + "="*30)
    print("   GESTION DE FLOTTE v3.0")
    print("="*30)
    print("1. 📋 Voir la flotte")
    print("2. ➕ Ajouter un véhicule")
    print("3. 🔧 Modifier un véhicule")
    print("4. 🛠️ Ajouter un entretien")
    print("5. 🗑️ Supprimer un véhicule")
    print("6. 💾 Sauvegarder et Quitter")

def add_maintenance_menu(fleet):
    print("\n--- AJOUTER UN ENTRETIEN ---")
    target_id = ask_int("ID du véhicule : ")

    vehicle = next((v for v in fleet if v.id == target_id), None)
    if not vehicle:
        print("❌ Véhicule introuvable.")
        return
    
    print(f"Véhicule : {vehicle.show_details()}")

    print("Types :")
    types_list = list(MaintenanceType)
    for i, t in enumerate(types_list):
        print(f"{i+1}. {t.value}")

    type_index = ask_int("Choix du type : ") - 1
    if 0 <= type_index < len(types_list):
        selected_type = types_list[type_index]
    else:
        print("❌ Type invalide.")
        return
    
    cost = ask_float("Coût (€) : ")
    desc = input("Description : ")

    m_id = len(vehicle.maintenance_log) + 1
    today = date.today()

    new_m = Maintenance(m_id, today, selected_type, cost, desc)
    vehicle.add_maintenance(new_m)

    if ask_bool("Passer le véhicule en statut 'En Maintenance' ?"):
        vehicle.status = VehicleStatus.UNDER_MAINTENANCE

    print("✅ Entretien enregistré !")

def list_fleet(fleet):
    if not fleet:
        print("\n🚫 La flotte est vide.")
    else:
        print(f"\n--- ÉTAT DE LA FLOTTE ({len(fleet)} véhicules) ---")
        for v in fleet:
            print(f"[{v.id}] {v.show_details()} | Statut: {v.status.value}")

# --- ➕ FONCTION DE CRÉATION COMPLÈTE ---
def add_vehicle_menu(fleet):
    print("\n--- AJOUTER UN NOUVEAU VÉHICULE ---")
    print("--- Moteurs ---")
    print("1. Voiture      | 3. Camion")
    print("4. Moto         | 5. Corbillard")
    print("6. Karting")
    print("--- Animaux ---")
    print("2. Cheval/Poney | 8. Âne")
    print("9. Chameau")
    print("--- Autre ---")
    print("7. Calèche")
    print("0. Annuler")
    
    choice = input("\nVotre choix : ")
    
    if choice == '0':
        return

    # Calcul ID automatique
    new_id = 1
    if fleet:
        new_id = max(v.id for v in fleet) + 1
    
    # Tarif (commun à tous)
    rate = ask_float("Tarif journalier (€) : ")

    # --- LOGIQUE DE CRÉATION PAR TYPE ---
    
    if choice == '1': # VOITURE
        brand = input("Marque : ")
        model = input("Modèle : ")
        year = ask_int("Année : ")
        plate = input("Plaque : ")
        doors = ask_int("Portes : ")
        ac = ask_bool("Climatisation ?")
        fleet.append(Car(new_id, rate, brand, model, plate, year, doors, ac))
        print("✅ Voiture ajoutée !")

    elif choice == '2': # CHEVAL / PONEY
        name = input("Nom : ")
        breed = input("Race : ")
        age = ask_int("Âge (ans) : ")
        height = ask_int("Taille au garrot (cm) : ")
        shoe_front = ask_int("Fer Antérieur (mm) : ")
        shoe_rear = ask_int("Fer Postérieur (mm) : ")
        
        # Le programme détectera tout seul si c'est un Poney ou un Cheval
        new_horse = Horse(new_id, rate, name, breed, age, height, shoe_front, shoe_rear)
        fleet.append(new_horse)
        print(f"✅ {new_horse.category} ajouté !")

    elif choice == '3': # CAMION
        brand = input("Marque : ")
        model = input("Modèle : ")
        year = ask_int("Année : ")
        plate = input("Plaque : ")
        vol = ask_float("Volume (m3) : ")
        weight = ask_float("Poids Max (T) : ")
        fleet.append(Truck(new_id, rate, brand, model, plate, year, vol, weight))
        print("✅ Camion ajouté !")

    elif choice == '4': # MOTO
        brand = input("Marque : ")
        model = input("Modèle : ")
        year = ask_int("Année : ")
        plate = input("Plaque : ")
        cc = ask_int("Cylindrée (cc) : ")
        top_case = ask_bool("TopCase ?")
        fleet.append(Motorcycle(new_id, rate, brand, model, plate, year, cc, top_case))
        print("✅ Moto ajoutée !")

    elif choice == '5': # CORBILLARD
        brand = input("Marque : ")
        model = input("Modèle : ")
        year = ask_int("Année : ")
        plate = input("Plaque : ")
        length = ask_float("Longueur max cercueil (m) : ")
        frigo = ask_bool("Réfrigération active ?")
        fleet.append(Hearse(new_id, rate, brand, model, plate, year, length, frigo))
        print("✅ Corbillard ajouté !")

    elif choice == '6': # KART
        brand = input("Marque : ")
        model = input("Modèle : ")
        year = ask_int("Année : ")
        plate = input("Numéro de Kart (ex: K-01) : ")
        engine = input("Type moteur (ex: 4T Honda) : ")
        indoor = ask_bool("Est-ce un kart Indoor ?")
        fleet.append(GoKart(new_id, rate, brand, model, plate, year, engine, indoor))
        print("✅ Kart ajouté !")

    elif choice == '7': # CALÈCHE
        seats = ask_int("Nombre de places : ")
        roof = ask_bool("A un toit ?")
        fleet.append(Carriage(new_id, rate, seats, roof))
        print("✅ Calèche ajoutée !")

    elif choice == '8': # ÂNE
        name = input("Nom : ")
        breed = input("Race : ")
        age = ask_int("Âge (ans) : ")
        capacity = ask_float("Capacité de portage (kg) : ")
        stubborn = ask_bool("Est-il têtu ?")
        fleet.append(Donkey(new_id, rate, name, breed, age, capacity, stubborn))
        print("✅ Âne ajouté !")

    elif choice == '9': # CHAMEAU
        name = input("Nom : ")
        breed = input("Race : ")
        age = ask_int("Âge (ans) : ")
        humps = ask_int("Nombre de bosses (1 ou 2) : ")
        water = ask_float("Réserve d'eau (L) : ")
        fleet.append(Camel(new_id, rate, name, breed, age, humps, water))
        print("✅ Chameau/Dromadaire ajouté !")

    else:
        print("❌ Choix invalide.")

# --- 🔧 FONCTION DE MODIFICATION ---
def modify_vehicle_menu(fleet):
    print("\n--- MODIFIER UN VÉHICULE ---")
    target_id = ask_int("ID du véhicule à modifier : ")
    
    found = None
    for v in fleet:
        if v.id == target_id:
            found = v
            break
            
    if not found:
        print("❌ Véhicule introuvable.")
        return

    print(f"\nSélection : {found.show_details()}")
    print(f"Tarif actuel : {found.daily_rate}€ | Statut : {found.status.value}")
    print("1. Modifier Tarif | 2. Modifier Statut | 0. Annuler")
    
    choix = input("Choix : ")

    if choix == '1':
        found.daily_rate = ask_float("Nouveau tarif : ")
        print("✅ Tarif mis à jour.")

    elif choix == '2':
        print("1. Disponible | 2. Loué | 3. Maintenance | 4. Hors Service")
        s = input("Nouveau statut : ")
        if s == '1': found.status = VehicleStatus.AVAILABLE
        elif s == '2': found.status = VehicleStatus.RENTED
        elif s == '3': found.status = VehicleStatus.UNDER_MAINTENANCE
        elif s == '4': found.status = VehicleStatus.OUT_OF_SERVICE
        print(f"✅ Statut mis à jour : {found.status.value}")

# --- 🗑️ FONCTION DE SUPPRESSION ---
def delete_vehicle_menu(fleet):
    print("\n--- SUPPRIMER ---")
    target_id = ask_int("ID à supprimer : ")
    
    found = next((v for v in fleet if v.id == target_id), None)
    
    if found:
        print(f"❓ Supprimer : {found.show_details()}")
        if ask_bool("Confirmer ?"):
            fleet.remove(found)
            print("🗑️ Supprimé.")
        else:
            print("Annulé.")
    else:
        print("❌ Introuvable.")