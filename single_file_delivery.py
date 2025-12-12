import json
import sys
import os
import time
from datetime import date, timedelta, datetime
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Optional

# =========================================================
# 1. UTILITAIRES (AFFICHAGE & SAISIE SANS DÉPENDANCES)
# =========================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "=" * 60)
    print(f"   {title.upper()}")
    print("=" * 60)

def ask_int(msg):
    while True:
        try:
            return int(input(f"{msg} : ").strip())
        except ValueError:
            print("❌ Erreur : Entier requis.")

def ask_float(msg):
    while True:
        try:
            return float(input(f"{msg} : ").replace(',', '.').strip())
        except ValueError:
            print("❌ Erreur : Nombre décimal requis.")

def ask_float_def(msg, default):
    while True:
        val = input(f"{msg} [Défaut: {default}] : ").replace(',', '.').strip()
        if not val: return default
        try: return float(val)
        except ValueError: print("❌ Erreur.")

def ask_text(msg, default=None):
    prompt = f"{msg} [Défaut: {default}] : " if default else f"{msg} : "
    val = input(prompt).strip()
    return default if not val and default else val

def ask_bool(msg):
    while True:
        val = input(f"{msg} (O/N) : ").lower().strip()
        if val in ['o', 'oui', 'y']: return True
        if val in ['n', 'non']: return False

def ask_date(msg):
    while True:
        val = input(f"{msg} (YYYY-MM-DD) : ").strip()
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print("❌ Format invalide (ex: 2024-05-20).")

# =========================================================
# 2. ENUMS
# =========================================================

class VehicleStatus(Enum):
    AVAILABLE = "Disponible"
    RENTED = "Loué"
    UNDER_MAINTENANCE = "En Maintenance"
    OUT_OF_SERVICE = "Hors Service"

class MaintenanceType(Enum):
    MECHANICAL_CHECK = "Contrôle Mécanique"
    CLEANING = "Nettoyage"
    HOOF_CARE = "Soin Sabots"
    SADDLE_MAINTENANCE = "Sellerie"
    TIRE_CHANGE = "Pneus"
    OIL_CHANGE = "Vidange"
    AXLE_GREASING = "Essieux"
    HULL_CLEANING = "Carénage"
    SONAR_CHECK = "Sonar"
    NUCLEAR_SERVICE = "Réacteur"
    AVIONICS_CHECK = "Avionique"
    ROTOR_INSPECTION = "Rotor"
    WING_CARE = "Ailes"
    SCALE_POLISHING = "Écailles"

# =========================================================
# 3. CLASSES MÉTIER
# =========================================================

class Maintenance:
    def __init__(self, m_id, date_m, m_type, cost, description, duration):
        self.id = m_id; self.date = date_m; self.type = m_type
        self.cost = cost; self.description = description; self.duration = duration
    def to_dict(self):
        return {"id": self.id, "date": str(self.date), "type": self.type.value, "cost": self.cost, "description": self.description, "duration": self.duration}

class TransportMode(ABC):
    def __init__(self, t_id: int, daily_rate: float):
        self.id = t_id
        self.daily_rate = daily_rate
        self.status = VehicleStatus.AVAILABLE
        self.maintenance_log: List[Maintenance] = []

    # Propriété pour robustesse des tests et validations
    @property
    def is_available(self):
        return self.status == VehicleStatus.AVAILABLE

    def add_maintenance(self, maintenance):
        self.maintenance_log.append(maintenance)

    def to_dict(self):
        return {
            "type": self.__class__.__name__, "id": self.id,
            "daily_rate": self.daily_rate, "status": self.status.value,
            "maintenance_log": [m.to_dict() for m in self.maintenance_log]
        }
    @abstractmethod
    def show_details(self): pass

# --- VÉHICULES ---
class MotorizedVehicle(TransportMode):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year):
        super().__init__(t_id, daily_rate)
        self.brand = brand; self.model = model; self.license_plate = license_plate; self.year = year
    def to_dict(self):
        d = super().to_dict()
        d.update({"brand": self.brand, "model": self.model, "license_plate": self.license_plate, "year": self.year})
        return d

class Car(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, door_count, has_ac):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.door_count = door_count; self.has_ac = has_ac
    def show_details(self): return f"[Voiture] {self.brand} {self.model}"
    def to_dict(self): d=super().to_dict(); d.update({"door_count": self.door_count, "has_ac": self.has_ac}); return d

class Truck(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, cargo_volume, max_weight):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.cargo_volume = cargo_volume; self.max_weight = max_weight
    def show_details(self): return f"[Camion] {self.brand} {self.model}"
    def to_dict(self): d=super().to_dict(); d.update({"cargo_volume": self.cargo_volume, "max_weight": self.max_weight}); return d

# --- ANIMAUX ---
class TransportAnimal(TransportMode):
    def __init__(self, t_id, daily_rate, name, breed, age):
        super().__init__(t_id, daily_rate)
        self.name = name; self.breed = breed; self.age = age
    def to_dict(self): d = super().to_dict(); d.update({"name": self.name, "breed": self.breed, "age": self.age}); return d

class Dragon(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, fire_range, scale_color):
        super().__init__(t_id, daily_rate, name, breed, age)
        self.fire_range = fire_range; self.scale_color = scale_color
    def show_details(self): return f"[Dragon] {self.name} ({self.scale_color})"
    def to_dict(self): d=super().to_dict(); d.update({"fire_range": self.fire_range, "scale_color": self.scale_color}); return d

class Horse(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, wither_height):
        super().__init__(t_id, daily_rate, name, breed, age); self.wither_height = wither_height
    def show_details(self): return f"[Cheval] {self.name}"
    def to_dict(self): d=super().to_dict(); d.update({"wither_height": self.wither_height}); return d

# --- CLIENTS & LOCATIONS ---
class Customer:
    def __init__(self, c_id, name, driver_license, email, phone, username, password):
        self.id = c_id; self.name = name; self.driver_license = driver_license
        self.email = email; self.phone = phone; self.username = username; self.password = password
    def to_dict(self):
        return {"id": self.id, "name": self.name, "driver_license": self.driver_license, "email": self.email, "phone": self.phone, "username": self.username, "password": self.password}

# === CLASSE RENTAL MISE À JOUR (CORRECTION CRITIQUE) ===
class Rental:
    def __init__(self, customer, vehicle, start_date_str, end_date_str, from_history=False):
        self.customer = customer; self.vehicle = vehicle
        self.from_history = from_history # Indicateur pour le chargement

        try:
            self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            self.end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError: raise ValueError("Date invalide.")
        
        self.actual_return_date = None; self.total_cost = 0.0; self.penalty = 0.0; self.is_active = False
        
        # Validation sécurisée
        self._validate_rental()
        
        # Activation
        self.is_active = True
        self.vehicle.status = VehicleStatus.RENTED # Mise à jour du statut

    def _validate_rental(self):
        if self.start_date > self.end_date: raise ValueError("Fin avant Début.")
        
        # Si on charge depuis l'historique (JSON), on ignore la vérification de disponibilité
        # car le véhicule est DEJA marqué comme loué dans le système.
        if not self.from_history and not self.vehicle.is_available: 
            # Gestion du nom pour l'erreur
            nom = getattr(self.vehicle, 'brand', getattr(self.vehicle, 'name', 'Véhicule'))
            raise ValueError(f"{nom} indisponible.")

    def calculate_cost(self):
        days = max(1, (self.end_date - self.start_date).days)
        return days * self.vehicle.daily_rate

    def close_rental(self, return_date_str):
        self.actual_return_date = datetime.strptime(return_date_str, "%Y-%m-%d")
        base = max(1, (self.actual_return_date - self.start_date).days) * self.vehicle.daily_rate
        
        if self.actual_return_date > self.end_date:
            days_late = (self.actual_return_date - self.end_date).days
            self.penalty = (days_late * self.vehicle.daily_rate) * 0.10
            print(f"⚠️ Retard: {days_late}j. Pénalité: {self.penalty}€")
        
        self.total_cost = base + self.penalty
        self.is_active = False
        self.vehicle.status = VehicleStatus.AVAILABLE # Libération du véhicule
        return self.total_cost

    def to_dict(self):
        return {
            "customer_id": self.customer.id, "vehicle_id": self.vehicle.id,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "is_active": self.is_active, "total_cost": self.total_cost
        }

# =========================================================
# 4. SYSTEME & STOCKAGE
# =========================================================

class CarRentalSystem:
    def __init__(self):
        self.fleet = []; self.customers = []; self.rentals = []
    def add_vehicle(self, v): self.fleet.append(v)
    def add_customer(self, c): self.customers.append(c)

class StorageManager:
    def __init__(self, filename="data.json"): self.filename = filename
    def save_system(self, system):
        data = {"fleet": [v.to_dict() for v in system.fleet], "customers": [c.to_dict() for c in system.customers], "rentals": [r.to_dict() for r in system.rentals]}
        with open(self.filename, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)

    def load_system(self):
        system = CarRentalSystem()
        if not os.path.exists(self.filename): return system
        try:
            with open(self.filename, 'r', encoding='utf-8') as f: data = json.load(f)
        except: return system

        fleet_map = {}
        for item in data.get("fleet", []):
            typ = item.get("type"); tid = item["id"]; rate = item["daily_rate"]
            obj = None
            if typ == "Car": obj = Car(tid, rate, item["brand"], item["model"], item["license_plate"], item["year"], item["door_count"], item["has_ac"])
            elif typ == "Truck": obj = Truck(tid, rate, item["brand"], item["model"], item["license_plate"], item["year"], item["cargo_volume"], item["max_weight"])
            elif typ == "Dragon": obj = Dragon(tid, rate, item["name"], item["breed"], item["age"], item["fire_range"], item["scale_color"])
            elif typ == "Horse": obj = Horse(tid, rate, item["name"], item["breed"], item["age"], item["wither_height"])
            
            if obj:
                for s in VehicleStatus:
                    if s.value == item.get("status"): obj.status = s
                system.fleet.append(obj); fleet_map[obj.id] = obj

        cust_map = {}
        for c in data.get("customers", []):
            new_c = Customer(c["id"], c["name"], c["driver_license"], c["email"], c["phone"], c["username"], c["password"])
            system.customers.append(new_c); cust_map[new_c.id] = new_c

        # === CORRECTION CHARGEMENT ===
        for r in data.get("rentals", []):
            veh = fleet_map.get(r["vehicle_id"]); cust = cust_map.get(r["customer_id"])
            if veh and cust:
                # On passe from_history=True pour bypasser la vérif de dispo
                new_r = Rental(cust, veh, r["start_date"], r["end_date"], from_history=True)
                
                new_r.is_active = r["is_active"]
                new_r.total_cost = r.get("total_cost", 0.0)
                system.rentals.append(new_r)
        
        return system

# =========================================================
# 5. UI CONSOLE (MENU PRINCIPAL)
# =========================================================

def fleet_menu(system, storage):
    while True:
        clear_screen(); print_header("GESTION FLOTTE")
        print("1. Voir la liste\n2. Ajouter un véhicule\n3. Maintenance\n8. Sauvegarder\n0. Retour")
        c = input("Choix: ").strip()
        if c == '0': break
        elif c == '1':
            print_header("LISTE")
            for v in system.fleet: print(f"{v.id}. {v.show_details()} - {v.status.value} ({v.daily_rate}€/j)")
            input("Entrée...")
        elif c == '2':
            print("1.Car 2.Truck 3.Dragon 4.Horse"); t = input("Type: ")
            nid = len(system.fleet)+1; r = ask_float("Prix/j")
            if t=='1': system.add_vehicle(Car(nid, r, ask_text("Marque"), ask_text("Modèle"), "XX-000", 2024, 5, True))
            elif t=='3': system.add_vehicle(Dragon(nid, r, ask_text("Nom"), "Dragon", 100, 50, "Rouge"))
            elif t=='4': system.add_vehicle(Horse(nid, r, ask_text("Nom"), "Cheval", 5, 160))
            print("✅ Ajouté!"); time.sleep(1)
        elif c == '8': storage.save_system(system); print("✅ Sauvegardé!"); time.sleep(1)

def rental_menu(system):
    while True:
        clear_screen(); print_header("LOCATIONS")
        print("1. Nouvelle Location\n2. Retour Véhicule\n3. Liste Actives\n0. Retour")
        c = input("Choix: ").strip()
        if c == '0': break
        elif c == '1':
            cid = ask_int("ID Client"); vid = ask_int("ID Véhicule")
            cust = next((x for x in system.customers if x.id == cid), None)
            veh = next((x for x in system.fleet if x.id == vid), None)
            if cust and veh:
                try:
                    # from_history=False par défaut ici
                    r = Rental(cust, veh, ask_date("Début"), ask_date("Fin"))
                    system.rentals.append(r)
                    print(f"✅ Location OK. Coût: {r.calculate_cost()}€")
                except ValueError as e: print(f"❌ Erreur: {e}")
            else: print("❌ Introuvable.")
            input("Entrée...")
        elif c == '2':
            actives = [r for r in system.rentals if r.is_active]
            for i, r in enumerate(actives): print(f"{i}. {r.vehicle.show_details()} par {r.customer.name}")
            idx = ask_int("Index")
            if 0 <= idx < len(actives):
                r = actives[idx]
                cost = r.close_rental(ask_date("Date Retour Réel"))
                print(f"✅ Retourné. Total: {cost}€")
            input("Entrée...")

def client_menu(system):
    while True:
        clear_screen(); print_header("CLIENTS")
        print("1. Liste\n2. Ajout\n0. Retour")
        c = input("Choix: ").strip()
        if c=='0': break
        elif c=='1':
            for cu in system.customers: print(f"{cu.id}. {cu.name} ({cu.email})")
            input("Entrée...")
        elif c=='2':
            nid = len(system.customers)+1
            system.add_customer(Customer(nid, ask_text("Nom"), "B", "email", "06", ask_text("User"), "123"))
            print("✅ Ajouté!"); time.sleep(1)

def main():
    storage = StorageManager("data.json")
    system = storage.load_system()
    
    while True:
        clear_screen(); print_header("RENT-A-DREAM")
        print("1. Flotte\n2. Clients\n3. Locations\n4. Sauvegarder\n0. Quitter")
        c = input("Choix: ").strip()
        if c=='1': fleet_menu(system, storage)
        elif c=='2': client_menu(system)
        elif c=='3': rental_menu(system)
        elif c=='4': storage.save_system(system); print("Sauvegarde OK"); time.sleep(1)
        elif c=='0': sys.exit()

if __name__ == "__main__":
    main()