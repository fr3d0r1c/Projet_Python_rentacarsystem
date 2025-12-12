import json
from datetime import date
from fleet.enums import VehicleStatus, MaintenanceType
from fleet.maintenance import Maintenance
# Import de TOUS les types
from fleet.vehicles import Car, Truck, Motorcycle, Hearse, GoKart, Carriage, Cart, Boat, Plane, Helicopter, Submarine
from fleet.animals import Horse, Donkey, Camel, Whale, Eagle, Dragon, Dolphin
from clients.customer import Customer
from location.rental import Rental
from location.system import CarRentalSystem

class StorageManager:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def save_system(self, system):
        """Sauvegarde tout : Flotte, Clients, Locations"""
        data = {
            "fleet": [v.to_dict() for v in system.fleet],
            "customers": [c.to_dict() for c in system.customers],
            "rentals": [r.to_dict() for r in system.rentals]
        }
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erreur Save : {e}")

    def load_system(self):
        """Charge tout et retourne un objet CarRentalSystem prêt à l'emploi"""
        system = CarRentalSystem()

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            return system
        
        # ==========================================
        # 1. CHARGEMENT DE LA FLOTTE
        # ==========================================
        fleet_data = data.get("fleet", [])
        fleet_map = {}

        for item in fleet_data:
            typ = item.get("type")
            tid = item["id"]
            rate = item["daily_rate"]
            obj = None

            if typ=="Car": obj=Car(tid,rate,item["brand"],item["model"],item["license_plate"],item.get("year",2020),item["door_count"],item["has_ac"])
            elif typ=="Truck": obj=Truck(tid,rate,item["brand"],item["model"],item["license_plate"],item.get("year",2020),item["cargo_volume"],item["max_weight"])
            elif typ=="Motorcycle": obj=Motorcycle(tid,rate,item["brand"],item["model"],item["license_plate"],item.get("year",2020),item["engine_displacement"],item["has_top_case"])
            elif typ=="Hearse": obj=Hearse(tid,rate,item["brand"],item["model"],item["license_plate"],item.get("year",2020),item["max_coffin_length"],item["has_refrigeration"])
            elif typ=="GoKart": obj=GoKart(tid,rate,item["brand"],item["model"],item["license_plate"],item.get("year",2020),item["engine_type"],item["is_indoor"])
            elif typ=="Boat": obj=Boat(tid,rate,item["brand"],item["model"],item["license_plate"],item.get("year",2020),item["length_meters"],item["power_cv"])
            elif typ=="Submarine": obj=Submarine(tid,rate,item["brand"],item["model"],item["license_plate"],item.get("year",2020),item["max_depth"],item["is_nuclear"])
            elif typ=="Plane": obj=Plane(tid,rate,item["brand"],item["model"],item["license_plate"],item.get("year",2020),item["wingspan"],item["engines_count"])
            elif typ=="Helicopter": obj=Helicopter(tid,rate,item["brand"],item["model"],item["license_plate"],item.get("year",2020),item["rotor_count"],item["max_altitude"])

            elif typ=="Horse": obj=Horse(tid,rate,item["name"],item["breed"],item.get("age",5),item["wither_height"],item.get("shoe_size_front",0),item.get("shoe_size_rear",0))
            elif typ=="Donkey": obj=Donkey(tid,rate,item["name"],item["breed"],item.get("age",5),item["pack_capacity_kg"],item["is_stubborn"])
            elif typ=="Camel": obj=Camel(tid,rate,item["name"],item["breed"],item.get("age",5),item["hump_count"],item["water_reserve"])
            elif typ=="Whale": obj=Whale(tid,rate,item["name"],item["breed"],item.get("age",10),item["weight_tonnes"],item["can_sing"])
            elif typ=="Dolphin": obj=Dolphin(tid,rate,item["name"],item["breed"],item.get("age",5),item["swim_speed"],item["knows_tricks"])
            elif typ=="Eagle": obj=Eagle(tid,rate,item["name"],item["breed"],item.get("age",5),item["wingspan_cm"],item["max_altitude"])
            elif typ=="Dragon": obj=Dragon(tid,rate,item["name"],item["breed"],item.get("age",100),item["fire_range"],item["scale_color"])

            elif typ=="Carriage": obj=Carriage(tid,rate,item["seat_count"],item["has_roof"])
            elif typ=="Cart": obj=Cart(tid,rate,item["seat_count"],item["max_load_kg"])

            if obj:
                for s in VehicleStatus:
                    if s.value == item.get("status"): obj.status = s

                for l in item.get("maintenance_log",[]):
                    y,m,d = map(int, l["date"].split('-'))
                    mt = next((t for t in MaintenanceType if t.value==l["type"]), None)
                    if mt: obj.add_maintenance(Maintenance(l["id"], date(y,m,d), mt, l["cost"], l["description"], l.get("duration",1.0)))

                system.fleet.append(obj)
                fleet_map[obj.id] = obj
        
        for item in fleet_data:
            if item.get("animal_ids"):
                vehicle = fleet_map.get(item["id"])
                if vehicle:
                    for aid in item["animal_ids"]:
                        anim = fleet_map.get(aid)
                        if anim: vehicle.animals.append(anim)

        # ==========================================
        # 2. CHARGEMENT DES CLIENTS
        # ==========================================
        cust_data = data.get("customers", [])
        customer_map = {}

        for c in cust_data:
            user = c.get("username", f"user{c['id']}")
            pwd = c.get("password", "1234")

            new_c = Customer(c["id"], c["name"], c["driver_license"], c["email"], c["phone"], user, pwd)
            system.customers.append(new_c)
            customer_map[new_c.id] = new_c

        # ==========================================
        # 3. CHARGEMENT DES LOCATIONS
        # ==========================================
        rent_data = data.get("rentals", [])

        for r in rent_data:
            veh = fleet_map.get(r["vehicle_id"])
            cust = customer_map.get(r["customer_id"])

            if veh and cust:
                y1, m1, d1 = map(int, r["start_date"].split('-'))
                y2, m2, d2 = map(int, r["end_date"].split('-'))

                new_rental = Rental(cust, veh, r["start_date"], r["end_date"], from_history=True)

                new_rental.id = r.get("id", len(system.rentals)+1)
                new_rental.is_active = r["is_active"]
                system.rentals.append(new_rental)

        print(f"📂 Chargement complet OK")
        return system