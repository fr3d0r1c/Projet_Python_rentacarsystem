from datetime import date
from vehicles import Car, Truck, Motorcycle, Hearse, GoKart, Carriage, Cart, TowedVehicle
from animals import Horse, Donkey, Camel
from transport_base import TransportAnimal
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

def ask_float_with_default(message, default_val):
    user_input = input(f"{message} (Entrée pour {default_val}€) : ")

    if user_input.strip() == "":
        return float(default_val)
    
    try:
        return float(user_input)
    except ValueError:
        print(f"⚠️ Saisie invalide. Utilisation de la valeur par défaut : {default_val}")
        return float(default_val)

DEFAULT_DURATIONS = {
    MaintenanceType.MECHANICAL_CHECK: 1.0,
    MaintenanceType.CLEANING: 0.5,
    MaintenanceType.HOOF_CARE: 0.5,
    MaintenanceType.SADDLE_MAINTENANCE: 2.0,
    MaintenanceType.TIRE_CHANGE: 0.5,
    MaintenanceType.OIL_CHANGE: 0.5,
    MaintenanceType.AXLE_GREASING: 1.0
}

DEFAULT_RENTAL_PRICES = {
    '1': 50.0,  # Voiture
    '2': 35.0,  # Cheval/Poney
    '3': 250.0, # Camion
    '4': 90.0,  # Moto
    '5': 300.0, # Corbillard
    '6': 60.0,  # Kart
    '7': 120.0, # Calèche
    '8': 25.0,  # Âne
    '9': 80.0   # Chameau
}

DEFAULT_MAINT_COSTS = {
    MaintenanceType.MECHANICAL_CHECK: 50.0,
    MaintenanceType.CLEANING: 20.0,
    MaintenanceType.HOOF_CARE: 40.0,        # Maréchal-ferrant
    MaintenanceType.SADDLE_MAINTENANCE: 15.0,
    MaintenanceType.TIRE_CHANGE: 120.0,
    MaintenanceType.OIL_CHANGE: 89.0,
    MaintenanceType.AXLE_GREASING: 30.0
}


# --- 📋 FONCTIONS D'AFFICHAGE ---
def show_main_menu():
    print("\n" + "="*30)
    print("   GESTION DE FLOTTE v3.1")
    print("="*30)
    print("1. 📋 Voir la flotte")
    print("2. ➕ Ajouter un véhicule")
    print("3. 🔧 Modifier un véhicule")
    print("4. 🛠️ Ajouter un entretien")
    print("5. 🐴 Atteler un animal")
    print("6. 🗑️ Supprimer un véhicule")
    print("7. 💾 Sauvegarder et Quitter")

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
    
    default_time = DEFAULT_DURATIONS.get(selected_type, 1.0)

    standard_cost = DEFAULT_MAINT_COSTS.get(selected_type, 50.0)

    print(f"Durée standard estimée : {default_time} jour(s).")
    user_duration_str = input(f"Appuyez sur Entrée pour valider ou tapez une autre durée : ")

    if user_duration_str.strip() == "":
        final_duration = default_time
    else:
        try:
            final_duration = float(user_duration_str)
        except ValueError:
            print("Erreur de saisie, utilisation de la durée par défaut.")
            final_duration = default_time
    
    cost = ask_float_with_default("Coût de l'intervention", standard_cost)
    desc = input("Description : ")

    m_id = len(vehicle.maintenance_log) + 1
    today = date.today()

    new_m = Maintenance(m_id, today, selected_type, cost, desc, final_duration)
    vehicle.add_maintenance(new_m)

    print(f"⚠️ Le véhicule sera indisponible jusqu'au {new_m.end_date}")

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
    print("--- Attelages ---")
    print("7. Calèche (Chevaux)")
    print("10. Charrette (Ânes)")
    print("0. Annuler")
    
    choice = input("\nVotre choix : ")
    
    if choice == '0':
        return

    # Calcul ID automatique
    new_id = 1
    if fleet:
        new_id = max(v.id for v in fleet) + 1
    
    standard_price = DEFAULT_RENTAL_PRICES.get(choice, 50.0)

    rate = ask_float_with_default("Tarif journalier", standard_price)

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

    elif choice == '10':
        seats = ask_int("Nombre de places assises (conducteur) : ")
        load = ask_float("Charge maximale (kg) : ")
        fleet.append(Cart(new_id, rate, seats, load))
        print("✅ Charrette ajoutée !")

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

def harness_animal_menu(fleet):
    print("\n--- ATTELER UN ANIMAL ---")

    target_id = ask_int("ID de la Calèche ou Charrette : ")
    vehicle = next((v for v in fleet if v.id == target_id), None)

    if not isinstance(vehicle, TowedVehicle):
        print("❌ Ce véhicule ne peut pas être attelé (ou n'existe pas).")
        return
    
    print(f"Véhicule sélectionné : {vehicle.show_details()}")

    animal_id = ask_int("ID de l'animal à atteler : ")
    animal = next((a for a in fleet if a.id == animal_id), None)

    if not isinstance(animal, TransportAnimal):
        print("❌ Cet ID ne correspond pas à un animal.")
        return
    
    print(f"Tentative d'attelage de {animal.name}...")
    vehicle.harness_animal(animal)