import json
from datetime import date
from enums import VehicleStatus, MaintenanceType
from maintenance import Maintenance
# Import de TOUS les types de véhicules et animaux
from vehicles import Car, Truck, Motorcycle, Hearse, GoKart, Carriage, Cart
from animals import Horse, Donkey, Camel

class StorageManager:
    def __init__(self, filename="fleet_data.json"):
        self.filename = filename

    def save_fleet(self, fleet_list):
        """Sauvegarde la liste d'objets en fichier JSON."""
        # On convertit chaque objet en dictionnaire
        data_to_save = [v.to_dict() for v in fleet_list]
        
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
            print(f"💾 Flotte sauvegardée avec succès dans '{self.filename}'")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde : {e}")

    # 👇 C'EST CETTE FONCTION QUI MANQUAIT OU ÉTAIT MAL PLACÉE 👇
    def load_fleet(self):
        """Charge le JSON, recrée les objets, restaure les statuts, entretiens et attelages."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data_loaded = json.load(f)
        except FileNotFoundError:
            return [] # Fichier inexistant = liste vide

        fleet_objects = []
        
        # --- PASSE 1 : CRÉATION DES OBJETS ---
        for item in data_loaded:
            obj_type = item.get("type")
            tid = item["id"]
            rate = item["daily_rate"]
            
            obj = None

            # 1. Véhicules Motorisés (Gestion de l'année)
            if obj_type == "Car":
                obj = Car(tid, rate, item["brand"], item["model"], item["license_plate"], 
                          item.get("year", 2020), item["door_count"], item["has_ac"])

            elif obj_type == "Truck":
                obj = Truck(tid, rate, item["brand"], item["model"], item["license_plate"], 
                            item.get("year", 2020), item["cargo_volume"], item["max_weight"])

            elif obj_type == "Motorcycle":
                obj = Motorcycle(tid, rate, item["brand"], item["model"], item["license_plate"], 
                                 item.get("year", 2020), item["engine_displacement"], item["has_top_case"])

            elif obj_type == "Hearse":
                obj = Hearse(tid, rate, item["brand"], item["model"], item["license_plate"], 
                             item.get("year", 2020), item["max_coffin_length"], item["has_refrigeration"])

            elif obj_type == "GoKart":
                obj = GoKart(tid, rate, item["brand"], item["model"], item["license_plate"], 
                             item.get("year", 2020), item["engine_type"], item["is_indoor"])

            # 2. Animaux (Gestion de l'âge)
            elif obj_type == "Horse":
                # Récupération des deux fers
                s_front = item.get("shoe_size_front", 0)
                s_rear = item.get("shoe_size_rear", 0)
                obj = Horse(tid, rate, item["name"], item["breed"], item.get("age", 5), 
                            item["wither_height"], s_front, s_rear)

            elif obj_type == "Donkey":
                obj = Donkey(tid, rate, item["name"], item["breed"], item.get("age", 5), 
                             item["pack_capacity_kg"], item["is_stubborn"])

            elif obj_type == "Camel":
                obj = Camel(tid, rate, item["name"], item["breed"], item.get("age", 5), 
                            item["hump_count"], item["water_reserve"])

            # 3. Véhicules Tractés (Calèche et Charrette)
            elif obj_type == "Carriage":
                obj = Carriage(tid, rate, item["seat_count"], item["has_roof"])
            
            elif obj_type == "Cart":
                obj = Cart(tid, rate, item["seat_count"], item["max_load_kg"])

            else:
                print(f"⚠️ Type inconnu ignoré : {obj_type}")
                continue
            
            # --- GESTION COMMUNE (Une fois l'objet créé) ---
            if obj:
                # A. Restauration du Statut
                saved_status = item.get("status")
                for s in VehicleStatus:
                    if s.value == saved_status:
                        obj.status = s
                        break
                
                # B. Restauration des Entretiens (Maintenance)
                saved_logs = item.get("maintenance_log", [])
                for log in saved_logs:
                    # Conversion Date (Str -> Date)
                    y, m, d = map(int, log["date"].split('-'))
                    m_date = date(y, m, d)
                    
                    # Retrouver l'Enum MaintenanceType
                    m_type_enum = None
                    for t in MaintenanceType:
                        if t.value == log["type"]:
                            m_type_enum = t
                            break
                    
                    if m_type_enum:
                        duration = log.get("duration", 1.0) # Récup durée
                        new_m = Maintenance(log["id"], m_date, m_type_enum, log["cost"], log["description"], duration)
                        obj.add_maintenance(new_m)

                # Ajout à la liste temporaire
                fleet_objects.append(obj)

        # --- PASSE 2 : RECONSTITUTION DES ATTELAGES ---
        for item in data_loaded:
            if item.get("animal_ids"):
                target_vehicle = next((v for v in fleet_objects if v.id == item["id"]), None)
                
                if target_vehicle:
                    for a_id in item["animal_ids"]:
                        animal_obj = next((a for a in fleet_objects if a.id == a_id), None)
                        if animal_obj:
                            target_vehicle.animals.append(animal_obj)

        print(f"📂 Chargement terminé : {len(fleet_objects)} objets récupérés.")
        return fleet_objects