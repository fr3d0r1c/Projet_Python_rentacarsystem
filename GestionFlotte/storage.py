# Fichier: storage.py
import json
from datetime import date
from enums import VehicleStatus, MaintenanceType # ✅ On a besoin des types d'entretien
from maintenance import Maintenance # ✅ On a besoin de la classe Maintenance
from vehicles import Car, Truck, Motorcycle, Hearse, GoKart, Carriage
from animals import Horse, Donkey, Camel

class StorageManager:
    def __init__(self, filename="fleet_data.json"):
        self.filename = filename

    def save_fleet(self, fleet_list):
        data_to_save = [v.to_dict() for v in fleet_list]
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
            print(f"💾 Flotte sauvegardée dans '{self.filename}'")
        except Exception as e:
            print(f"❌ Erreur sauvegarde : {e}")

    def load_fleet(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data_loaded = json.load(f)
        except FileNotFoundError:
            return []

        fleet_objects = []
        
        for item in data_loaded:
            obj_type = item.get("type")
            tid = item["id"]
            rate = item["daily_rate"]
            obj = None

            # --- CRÉATION VÉHICULE (Code identique à avant) ---
            if obj_type == "Car":
                obj = Car(tid, rate, item["brand"], item["model"], item["license_plate"], item.get("year", 2020), item["door_count"], item["has_ac"])
            elif obj_type == "Truck":
                obj = Truck(tid, rate, item["brand"], item["model"], item["license_plate"], item.get("year", 2020), item["cargo_volume"], item["max_weight"])
            elif obj_type == "Motorcycle":
                obj = Motorcycle(tid, rate, item["brand"], item["model"], item["license_plate"], item.get("year", 2020), item["engine_displacement"], item["has_top_case"])
            elif obj_type == "Hearse":
                obj = Hearse(tid, rate, item["brand"], item["model"], item["license_plate"], item.get("year", 2020), item["max_coffin_length"], item["has_refrigeration"])
            elif obj_type == "GoKart":
                obj = GoKart(tid, rate, item["brand"], item["model"], item["license_plate"], item.get("year", 2020), item["engine_type"], item["is_indoor"])
            elif obj_type == "Carriage":
                obj = Carriage(tid, rate, item["seat_count"], item["has_roof"])
            elif obj_type == "Horse":
                obj = Horse(tid, rate, item["name"], item["breed"], item.get("age", 5), item["wither_height"], item.get("shoe_size_front", 0), item.get("shoe_size_rear", 0))
            elif obj_type == "Donkey":
                obj = Donkey(tid, rate, item["name"], item["breed"], item.get("age", 5), item["pack_capacity_kg"], item["is_stubborn"])
            elif obj_type == "Camel":
                obj = Camel(tid, rate, item["name"], item["breed"], item.get("age", 5), item["hump_count"], item["water_reserve"])

            # --- SI L'OBJET EST CRÉÉ, ON GÈRE LE RESTE ---
            if obj:
                # 1. RESTAURATION DU STATUT
                saved_status = item.get("status")
                for s in VehicleStatus:
                    if s.value == saved_status:
                        obj.status = s
                        break
                
                # 2. ✅ RESTAURATION DES ENTRETIENS (MAINTENANCE)
                saved_logs = item.get("maintenance_log", []) # Liste vide si pas d'entretien
                
                for log in saved_logs:
                    # Conversion de la date texte "2023-12-25" -> Objet date
                    y, m, d = map(int, log["date"].split('-'))
                    m_date = date(y, m, d)
                    
                    # Retrouver le bon type Enum depuis le texte
                    m_type_enum = None
                    for t in MaintenanceType:
                        if t.value == log["type"]:
                            m_type_enum = t
                            break
                    if not m_type_enum: continue # Sécurité
                    
                    # Création de l'entretien
                    new_maint = Maintenance(log["id"], m_date, m_type_enum, log["cost"], log["description"])
                    
                    # Ajout au véhicule
                    obj.add_maintenance(new_maint)

                fleet_objects.append(obj)
        
        return fleet_objects