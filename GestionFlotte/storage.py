import json
from datetime import date
# Import de TOUTES les classes nécessaires
from vehicles import Car, Truck, Motorcycle, Hearse, GoKart, Carriage
from animals import Horse, Donkey, Camel

class StorageManager:
    def __init__(self, filename="fleet_data.json"):
        self.filename = filename

    def save_fleet(self, fleet_list):
        """Sauvegarde la liste d'objets en fichier JSON"""
        data_to_save = [v.to_dict() for v in fleet_list]
        
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
            print(f"💾 Flotte sauvegardée avec succès dans '{self.filename}'")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def load_fleet(self):
        """Charge le JSON et recrée les objets Python correspondants"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data_loaded = json.load(f)
        except FileNotFoundError:
            return [] # Fichier inexistant = liste vide

        fleet_objects = []
        
        for item in data_loaded:
            obj_type = item.get("type")
            
            # On convertit l'ID et le tarif qui sont communs
            t_id = item["id"]
            rate = item["daily_rate"]

            # --- RECONSTRUCTION SELON LE TYPE ---
            if obj_type == "Car":
                obj = Car(t_id, rate, item["brand"], item["model"], item["license_plate"], 
                          item["door_count"], item["has_ac"])

            elif obj_type == "Truck":
                obj = Truck(t_id, rate, item["brand"], item["model"], item["license_plate"], 
                            item["cargo_volume"], item["max_weight"])

            elif obj_type == "Motorcycle":
                obj = Motorcycle(t_id, rate, item["brand"], item["model"], item["license_plate"], 
                                 item["engine_displacement"], item["has_top_case"])

            elif obj_type == "Hearse":
                obj = Hearse(t_id, rate, item["brand"], item["model"], item["license_plate"], 
                             item["max_coffin_length"], item["has_refrigeration"])

            elif obj_type == "GoKart":
                obj = GoKart(t_id, rate, item["brand"], item["model"], item["license_plate"], 
                             item["engine_type"], item["is_indoor"])

            elif obj_type == "Horse":
                # Note: JSON ne stocke pas les dates, on met une date par défaut pour simplifier l'exemple
                # Pour faire pro, il faudrait convertir la string "2018-05-12" en objet date()
                birth = date(2020, 1, 1) 
                obj = Horse(t_id, rate, item["name"], item["breed"], birth, 
                           item["wither_height"], item["shoe_size"])

            elif obj_type == "Donkey":
                birth = date(2020, 1, 1)
                obj = Donkey(t_id, rate, item["name"], item["breed"], birth, 
                             item["pack_capacity_kg"], item["is_stubborn"])

            elif obj_type == "Camel":
                birth = date(2020, 1, 1)
                obj = Camel(t_id, rate, item["name"], item["breed"], birth, 
                            item["hump_count"], item["water_reserve"])

            elif obj_type == "Carriage":
                obj = Carriage(t_id, rate, item["seat_count"], item["has_roof"])
                # (Optionnel) Ici on pourrait recharger les animaux attelés si besoin

            else:
                print(f"Type inconnu ignoré : {obj_type}")
                continue
            
            # On remet le statut correct (ex: si le véhicule était Loué)
            # obj.status = VehicleStatus(item["status"]) 
            
            fleet_objects.append(obj)

        print(f"📂 Chargement terminé : {len(fleet_objects)} véhicules récupérés.")
        return fleet_objects