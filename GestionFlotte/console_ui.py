from datetime import date
# On importe les classes pour vérifier les types (isinstance)
from vehicles import Car, Truck, Motorcycle, Hearse, GoKart, Carriage, Cart, TowedVehicle, MotorizedVehicle
from animals import Horse, Donkey, Camel
from transport_base import TransportAnimal, TransportMode
from maintenance import Maintenance
from enums import MaintenanceType, VehicleStatus

# --- 💰 CONFIGURATION DES PRIX ---
DEFAULT_RENTAL_PRICES = {
    '1': 50.0, '2': 35.0, '3': 250.0, '4': 90.0, '5': 300.0, 
    '6': 60.0, '7': 120.0, '8': 25.0, '9': 80.0, '10': 40.0
}

DEFAULT_MAINT_COSTS = {
    MaintenanceType.MECHANICAL_CHECK: 50.0, MaintenanceType.CLEANING: 20.0,
    MaintenanceType.HOOF_CARE: 40.0, MaintenanceType.SADDLE_MAINTENANCE: 15.0,
    MaintenanceType.TIRE_CHANGE: 120.0, MaintenanceType.OIL_CHANGE: 89.0,
    MaintenanceType.AXLE_GREASING: 30.0
}

DEFAULT_DURATIONS = {
    MaintenanceType.MECHANICAL_CHECK: 1.0, MaintenanceType.CLEANING: 0.5,
    MaintenanceType.HOOF_CARE: 0.5, MaintenanceType.SADDLE_MAINTENANCE: 2.0,
    MaintenanceType.TIRE_CHANGE: 0.5, MaintenanceType.OIL_CHANGE: 0.5,
    MaintenanceType.AXLE_GREASING: 1.0
}

# --- 🛠️ HELPER FUNCTIONS ---
def ask_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("❌ Erreur : Entier requis.")

def ask_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("❌ Erreur : Décimal requis.")

def ask_float_with_default(message, default_val):
    user_input = input(f"{message} (Entrée pour {default_val}€) : ")
    if user_input.strip() == "": return float(default_val)
    try: return float(user_input)
    except ValueError: return float(default_val)

def ask_bool(message):
    val = input(f"{message} (o/n) : ").lower()
    return val in ['o', 'oui', 'y', 'yes']

# --- 📋 MENU PRINCIPAL ---
def show_main_menu():
    print("\n" + "="*40)
    print("      GESTION DE FLOTTE v4.0")
    print("="*40)
    print("1. 📋 Voir toute la flotte")
    print("--- GESTION ---")
    print("2. 🚗 Gestion VÉHICULES (Ajout)")
    print("3. 🐎 Gestion ANIMAUX (Ajout)")
    print("4. 🚜 Gestion ATTELAGES (Ajout)")
    print("--- ATELIER & SOINS ---")
    print("5. 🔧 Maintenance MÉCANIQUE (Véhicules)")
    print("6. 🩺 Soins VÉTÉRINAIRES (Animaux)")
    print("--- ACTIONS ---")
    print("7. 🐴 Atteler un animal")
    print("8. 🗑️ Supprimer un élément")
    print("9. 💾 Sauvegarder et Quitter")

def list_fleet(fleet):
    if not fleet:
        print("\n🚫 La flotte est vide.")
    else:
        print(f"\n--- ÉTAT DE LA FLOTTE ({len(fleet)} éléments) ---")
        for v in fleet:
            print(f"[{v.id}] {v.show_details()} | Statut: {v.status.value}")

# --- 🚗 SOUS-MENU : AJOUT VÉHICULES ---
def add_motor_menu(fleet):
    print("\n--- 🚗 AJOUTER UN VÉHICULE MOTORISÉ ---")
    print("1. Voiture")
    print("2. Camion")
    print("3. Moto")
    print("4. Corbillard")
    print("5. Karting")
    print("0. Retour")
    
    choice = input("Choix : ")
    if choice == '0': return

    # Logique commune ID et Prix
    new_id = 1 if not fleet else max(v.id for v in fleet) + 1
    # Mapping des choix vers les clés de prix (1=1, 2=3(Camion), etc.)
    price_key = '1' if choice=='1' else '3' if choice=='2' else '4' if choice=='3' else '5' if choice=='4' else '6'
    rate = ask_float_with_default("Tarif journalier", DEFAULT_RENTAL_PRICES.get(price_key, 50.0))

    if choice == '1': # Voiture
        fleet.append(Car(new_id, rate, input("Marque: "), input("Modèle: "), input("Plaque: "), ask_int("Année: "), ask_int("Portes: "), ask_bool("Clim?")))
    elif choice == '2': # Camion
        fleet.append(Truck(new_id, rate, input("Marque: "), input("Modèle: "), input("Plaque: "), ask_int("Année: "), ask_float("Vol m3: "), ask_float("Poids T: ")))
    elif choice == '3': # Moto
        fleet.append(Motorcycle(new_id, rate, input("Marque: "), input("Modèle: "), input("Plaque: "), ask_int("Année: "), ask_int("CC: "), ask_bool("TopCase?")))
    elif choice == '4': # Corbillard
        fleet.append(Hearse(new_id, rate, input("Marque: "), input("Modèle: "), input("Plaque: "), ask_int("Année: "), ask_float("Long. Cercueil: "), ask_bool("Frigo?")))
    elif choice == '5': # Kart
        fleet.append(GoKart(new_id, rate, input("Marque: "), input("Modèle: "), input("Plaque: "), ask_int("Année: "), input("Moteur: "), ask_bool("Indoor?")))
    
    print("✅ Véhicule ajouté !")

# --- 🐎 SOUS-MENU : AJOUT ANIMAUX ---
def add_animal_menu(fleet):
    print("\n--- 🐎 AJOUTER UN ANIMAL ---")
    print("1. Cheval / Poney")
    print("2. Âne")
    print("3. Chameau")
    print("0. Retour")

    choice = input("Choix : ")
    if choice == '0': return

    new_id = 1 if not fleet else max(v.id for v in fleet) + 1
    price_key = '2' if choice=='1' else '8' if choice=='2' else '9'
    rate = ask_float_with_default("Tarif journalier", DEFAULT_RENTAL_PRICES.get(price_key, 35.0))

    name = input("Nom : ")
    breed = input("Race : ")
    age = ask_int("Âge : ")

    if choice == '1':
        fleet.append(Horse(new_id, rate, name, breed, age, ask_int("Taille (cm): "), ask_int("Fer Av (mm): "), ask_int("Fer Arr (mm): ")))
    elif choice == '2':
        fleet.append(Donkey(new_id, rate, name, breed, age, ask_float("Capacité (kg): "), ask_bool("Têtu?")))
    elif choice == '3':
        fleet.append(Camel(new_id, rate, name, breed, age, ask_int("Bosses: "), ask_float("Eau (L): ")))
    
    print("✅ Animal ajouté !")

# --- 🚜 SOUS-MENU : AJOUT ATTELAGES ---
def add_towed_menu(fleet):
    print("\n--- 🚜 AJOUTER UN ATTELAGE ---")
    print("1. Calèche (Chevaux)")
    print("2. Charrette (Ânes)")
    print("0. Retour")

    choice = input("Choix : ")
    if choice == '0': return

    new_id = 1 if not fleet else max(v.id for v in fleet) + 1
    price_key = '7' if choice=='1' else '10'
    rate = ask_float_with_default("Tarif journalier", DEFAULT_RENTAL_PRICES.get(price_key, 100.0))

    if choice == '1':
        fleet.append(Carriage(new_id, rate, ask_int("Places: "), ask_bool("Toit?")))
    elif choice == '2':
        fleet.append(Cart(new_id, rate, ask_int("Places: "), ask_float("Charge Max (kg): ")))
    
    print("✅ Attelage ajouté !")

# --- 🔧 & 🩺 FONCTION MAINTENANCE GÉNÉRIQUE (Filtrée) ---
def maintenance_process(fleet, category_filter):
    """
    category_filter : 'motor' ou 'animal' ou 'towed'
    """
    target_id = ask_int("ID de l'élément : ")
    obj = next((v for v in fleet if v.id == target_id), None)

    if not obj:
        print("❌ ID introuvable.")
        return

    # Vérification du type pour ne pas afficher le menu vétérinaire pour une voiture
    if category_filter == 'motor' and not isinstance(obj, MotorizedVehicle):
        print("❌ Cet ID n'est pas un véhicule motorisé.")
        return
    elif category_filter == 'animal' and not isinstance(obj, TransportAnimal):
        print("❌ Cet ID n'est pas un animal.")
        return
    
    print(f"Sélection : {obj.show_details()}")

    # Filtrage des types de maintenance disponibles
    available_types = []
    if category_filter == 'motor':
        available_types = [MaintenanceType.MECHANICAL_CHECK, MaintenanceType.OIL_CHANGE, MaintenanceType.TIRE_CHANGE, MaintenanceType.CLEANING]
    elif category_filter == 'animal':
        available_types = [MaintenanceType.HOOF_CARE, MaintenanceType.SADDLE_MAINTENANCE, MaintenanceType.CLEANING]
    else: # Towed / General
        available_types = [MaintenanceType.AXLE_GREASING, MaintenanceType.CLEANING, MaintenanceType.TIRE_CHANGE]

    print("--- Types d'interventions disponibles ---")
    for i, t in enumerate(available_types):
        print(f"{i+1}. {t.value}")
    
    idx = ask_int("Choix : ") - 1
    if not (0 <= idx < len(available_types)):
        print("❌ Choix invalide.")
        return

    selected_type = available_types[idx]
    
    # Calculs auto
    default_cost = DEFAULT_MAINT_COSTS.get(selected_type, 50.0)
    default_time = DEFAULT_DURATIONS.get(selected_type, 1.0)

    cost = ask_float_with_default("Coût", default_cost)
    print(f"Durée estimée : {default_time}j")
    
    # Création
    m_id = len(obj.maintenance_log) + 1
    new_m = Maintenance(m_id, date.today(), selected_type, cost, input("Description : "), default_time)
    obj.add_maintenance(new_m)

    if ask_bool("Mettre en indisponibilité (Maintenance) ?"):
        obj.status = VehicleStatus.UNDER_MAINTENANCE
    
    print("✅ Maintenance enregistrée !")


# --- 🐴 ATTELAGE ---
def harness_animal_menu(fleet):
    print("\n--- ATTELAGE ---")
    vid = ask_int("ID Calèche/Charrette : ")
    vehicle = next((v for v in fleet if v.id == vid), None)
    if not isinstance(vehicle, TowedVehicle):
        print("❌ Pas un véhicule tracté.")
        return
    
    aid = ask_int("ID Animal : ")
    animal = next((a for a in fleet if a.id == aid), None)
    if not isinstance(animal, TransportAnimal):
        print("❌ Pas un animal.")
        return
        
    vehicle.harness_animal(animal)

# --- 🗑️ SUPPRESSION ---
def delete_vehicle_menu(fleet):
    tid = ask_int("ID à supprimer : ")
    found = next((v for v in fleet if v.id == tid), None)
    if found and ask_bool(f"Supprimer {found.show_details()} ?"):
        fleet.remove(found)
        print("🗑️ Supprimé.")