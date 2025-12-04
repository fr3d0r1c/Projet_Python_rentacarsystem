import json
from datetime import date
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
            print(f"💾 Sauvegardé dans '{self.filename}'")
        except Exception as e:
            print(f"Erreur sauvegarde : {e}")

    def load_fleet(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data_loaded = json.load(f)
        except FileNotFoundError:
            return []

        fleet_objects = []
        default_date = date(2020, 1, 1)

        for item in data_loaded:
            obj_type = item.get("type")
            tid = item["id"]
            rate = item["daily_rate"]

            if obj_type == "Car":
                obj = Car(tid, rate, item["brand"], item["model"], item["license_plate"], item["door_count"], item["has_ac"])
            elif obj_type == "Truck":
                obj = Truck(tid, rate, item["brand"], item["model"], item["license_plate"], item["cargo_volume"], item["max_weight"])
            elif obj_type == "Horse":
                birth = date(2020, 1, 1)

                s_front = item.get("shoe_size_front", 0)
                s_rear = item.get("shoe_size_rear", 0)

                obj = Horse(tid, rate, item["name"], item["breed"], birth,
                            item["wither_height"],
                            s_front,
                            s_rear)
            elif obj_type == "Donkey":
                obj = Donkey(tid, rate, item["name"], item["breed"], default_date, item["pack_capacity_kg"], item["is_stubborn"])
            elif obj_type == "Camel":
                obj = Camel(tid, rate, item["name"], item["breed"], default_date, item["hump_count"], item["water_reserve"])
            elif obj_type == "Motorcycle":
                obj = Motorcycle(tid, rate, item["brand"], item["model"], item["license_plate"], item["engine_displacement"], item["has_top_case"])
            elif obj_type == "Hearse":
                obj = Hearse(tid, rate, item["brand"], item["model"], item["license_plate"], item["max_coffin_length"], item["has_refrigeration"])
            elif obj_type == "GoKart":
                obj = GoKart(tid, rate, item["brand"], item["model"], item["license_plate"], item["engine_type"], item["is_indoor"])
            elif obj_type == "Carriage":
                obj = Carriage(tid, rate, item["seat_count"], item["has_roof"])
            else:
                continue
            
            fleet_objects.append(obj)
        
        return fleet_objects