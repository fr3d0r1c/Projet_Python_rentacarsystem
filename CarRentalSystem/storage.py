import json
from datetime import date
# Imports Flotte
from GestionFlotte.enums import VehicleStatus, MaintenanceType
from GestionFlotte.maintenance import Maintenance
from GestionFlotte.vehicles import * 
from GestionFlotte.animals import *
# Imports Business
from clients.customer import Customer
from location.rental import Rental
from location.system import CarRentalSystem

class StorageManager:
    def __init__(self, filename="data_complete.json"): # Nouveau nom de fichier
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
            # print(f"💾 Système complet sauvegardé !") # Optionnel en console
        except Exception as e:
            print(f"❌ Erreur Save : {e}")

    def load_system(self):
        """Charge tout et retourne un objet CarRentalSystem prêt à l'emploi"""
        system = CarRentalSystem() # On crée un système vide
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            return system # Retourne système vide si pas de fichier

        # ==========================================
        # 1. CHARGEMENT DE LA FLOTTE
        # ==========================================
        fleet_data = data.get("fleet", [])
        # Dictionnaire temporaire pour retrouver les objets par ID (optimisation)
        fleet_map = {} 

        for i in fleet_data:
            typ, tid, rate = i.get("type"), i["id"], i["daily_rate"]
            obj = None

            # --- MOTEURS ---
            if typ=="Car": obj=Car(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["door_count"],i["has_ac"])
            elif typ=="Truck": obj=Truck(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["cargo_volume"],i["max_weight"])
            elif typ=="Motorcycle": obj=Motorcycle(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["engine_displacement"],i["has_top_case"])
            elif typ=="Hearse": obj=Hearse(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["max_coffin_length"],i["has_refrigeration"])
            elif typ=="GoKart": obj=GoKart(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["engine_type"],i["is_indoor"])
            elif typ=="Boat": obj=Boat(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["length_meters"],i["power_cv"])
            elif typ=="Submarine": obj=Submarine(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["max_depth"],i["is_nuclear"])
            elif typ=="Plane": obj=Plane(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["wingspan"],i["engines_count"])
            elif typ=="Helicopter": obj=Helicopter(tid,rate,i["brand"],i["model"],i["license_plate"],i.get("year",2020),i["rotor_count"],i["max_altitude"])
            
            # --- ANIMAUX ---
            elif typ=="Horse": obj=Horse(tid,rate,i["name"],i["breed"],i.get("age",5),i["wither_height"],i.get("shoe_size_front",0),i.get("shoe_size_rear",0))
            elif typ=="Donkey": obj=Donkey(tid,rate,i["name"],i["breed"],i.get("age",5),i["pack_capacity_kg"],i["is_stubborn"])
            elif typ=="Camel": obj=Camel(tid,rate,i["name"],i["breed"],i.get("age",5),i["hump_count"],i["water_reserve"])
            elif typ=="Whale": obj=Whale(tid,rate,i["name"],i["breed"],i.get("age",10),i["weight_tonnes"],i["can_sing"])
            elif typ=="Dolphin": obj=Dolphin(tid,rate,i["name"],i["breed"],i.get("age",5),i["swim_speed"],i["knows_tricks"])
            elif typ=="Eagle": obj=Eagle(tid,rate,i["name"],i["breed"],i.get("age",5),i["wingspan_cm"],i["max_altitude"])
            elif typ=="Dragon": obj=Dragon(tid,rate,i["name"],i["breed"],i.get("age",100),i["fire_range"],i["scale_color"])
            
            # --- ATTELAGES ---
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
                
                system.fleet.append(obj)
                fleet_map[obj.id] = obj # Pour accès rapide

        # Reconstitution Attelages
        for i in fleet_data:
            if i.get("animal_ids"):
                vehicle = fleet_map.get(i["id"])
                if vehicle:
                    for aid in i["animal_ids"]:
                        anim = fleet_map.get(aid)
                        if anim: vehicle.animals.append(anim)

        # ==========================================
        # 2. CHARGEMENT DES CLIENTS
        # ==========================================
        cust_data = data.get("customers", [])
        customer_map = {}

        for c in cust_data:
            new_c = Customer(c["id"], c["name"], c["driver_license"], c["email"], c["phone"])
            system.customers.append(new_c)
            customer_map[new_c.id] = new_c

        # ==========================================
        # 3. CHARGEMENT DES LOCATIONS
        # ==========================================
        rent_data = data.get("rentals", [])
        
        for r in rent_data:
            # On retrouve les objets grâce aux IDs
            veh = fleet_map.get(r["vehicle_id"])
            cust = customer_map.get(r["customer_id"])
            
            if veh and cust:
                # Dates
                y1, m1, d1 = map(int, r["start_date"].split('-'))
                y2, m2, d2 = map(int, r["end_date"].split('-'))
                
                # Création
                new_rental = Rental(r["id"], veh, cust, date(y1,m1,d1), date(y2,m2,d2))
                new_rental.is_active = r["is_active"]
                # Le prix est recalculé par le constructeur Rental, mais on pourrait le forcer si besoin
                
                system.rentals.append(new_rental)

        print(f"📂 Chargement : {len(system.fleet)} véhicules, {len(system.customers)} clients, {len(system.rentals)} locations.")
        return system