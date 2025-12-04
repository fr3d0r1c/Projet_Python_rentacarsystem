import json
from datetime import date
from enums import VehicleStatus, MaintenanceType
from maintenance import Maintenance
from vehicles import * # Importe tout vehicles
from animals import * # Importe tout animals

class StorageManager:
    def __init__(self, filename="fleet_data.json"):
        self.filename = filename

    def save_fleet(self, fleet_list):
        data = [v.to_dict() for v in fleet_list]
        try:
            with open(self.filename, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"💾 Sauvegardé dans '{self.filename}'")
        except Exception as e: print(f"❌ Erreur Save : {e}")

    def load_fleet(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f: data = json.load(f)
        except: return []

        fleet = []
        # PASSE 1 : Création
        for i in data:
            typ, tid, rate = i.get("type"), i["id"], i["daily_rate"]
            obj = None

            # TERRE
            if typ=="Car": obj=Car(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["door_count"],i["has_ac"])
            elif typ=="Truck": obj=Truck(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["cargo_volume"],i["max_weight"])
            elif typ=="Motorcycle": obj=Motorcycle(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["engine_displacement"],i["has_top_case"])
            elif typ=="Hearse": obj=Hearse(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["max_coffin_length"],i["has_refrigeration"])
            elif typ=="GoKart": obj=GoKart(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["engine_type"],i["is_indoor"])
            # MER
            elif typ=="Boat": obj=Boat(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["length_meters"],i["power_cv"])
            elif typ=="Submarine": obj=Submarine(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["max_depth"],i["is_nuclear"])
            # AIR
            elif typ=="Plane": obj=Plane(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["wingspan"],i["engines_count"])
            elif typ=="Helicopter": obj=Helicopter(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["rotor_count"],i["max_altitude"])
            # ANIMAUX
            elif typ=="Horse": obj=Horse(tid,rate,i["name"],i["breed"],i.get("age",5),i["wither_height"],i.get("shoe_size_front",0),i.get("shoe_size_rear",0))
            elif typ=="Donkey": obj=Donkey(tid,rate,i["name"],i["breed"],i.get("age",5),i["pack_capacity_kg"],i["is_stubborn"])
            elif typ=="Camel": obj=Camel(tid,rate,i["name"],i["breed"],i.get("age",5),i["hump_count"],i["water_reserve"])
            elif typ=="Whale": obj=Whale(tid,rate,i["name"],i["breed"],i.get("age",10),i["weight_tonnes"],i["can_sing"])
            elif typ=="Dolphin": obj=Dolphin(tid,rate,i["name"],i["breed"],i.get("age",5),i["swim_speed"],i["knows_tricks"])
            elif typ=="Eagle": obj=Eagle(tid,rate,i["name"],i["breed"],i.get("age",5),i["wingspan_cm"],i["max_altitude"])
            elif typ=="Dragon": obj=Dragon(tid,rate,i["name"],i["breed"],i.get("age",100),i["fire_range"],i["scale_color"])
            # ATTELAGES
            elif typ=="Carriage": obj=Carriage(tid,rate,i["seat_count"],i["has_roof"])
            elif typ=="Cart": obj=Cart(tid,rate,i["seat_count"],i["max_load_kg"])

            if obj:
                # Restauration Statut
                for s in VehicleStatus:
                    if s.value == i.get("status"): obj.status = s
                # Restauration Maintenance
                for l in i.get("maintenance_log",[]):
                    y,m,d = map(int, l["date"].split('-'))
                    mt = next((t for t in MaintenanceType if t.value==l["type"]), None)
                    if mt: obj.add_maintenance(Maintenance(l["id"], date(y,m,d), mt, l["cost"], l["description"], l.get("duration",1.0)))
                fleet.append(obj)

        # PASSE 2 : Liens Attelage
        for i in data:
            if i.get("animal_ids"):
                vehicle = next((v for v in fleet if v.id == i["id"]), None)
                if vehicle:
                    for aid in i["animal_ids"]:
                        anim = next((a for a in fleet if a.id == aid), None)
                        if anim: vehicle.animals.append(anim)

        return fleet